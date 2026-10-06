from __future__ import annotations

import unittest

from apps.api.drafting import EditableTextDraft
from apps.api.editorial_review import (
    EditorialContent,
    EditorialReviewService,
    EditorialTransitionError,
    RegenerationRequest,
)


def make_content() -> EditorialContent:
    draft = EditableTextDraft(
        template_id="social.instagram.text-draft",
        template_version="1.0.0",
        channel="instagram",
        format="single_image",
        caption="A grounded editable caption.",
        cta="Ask for details",
        evidence_refs=["confirmed offer"],
        assumptions=["Review unknown audience detail"],
        review_notes=["Review before approval."],
        evidence_provenance=[{"source_id": "source-1"}],
        unsupported_claims=["An unsupported claim"],
    )
    return EditorialReviewService.from_generated_draft(draft, content_id="content-1")


class EditorialReviewServiceTests(unittest.TestCase):
    def test_generated_draft_enters_pending_human_review_explicitly(self) -> None:
        generated = make_content()

        self.assertEqual(generated.state, "generated_draft")
        pending = EditorialReviewService.submit_for_review(generated)

        self.assertEqual(pending.state, "pending_human_review")
        self.assertIsNone(pending.review)
        self.assertEqual(pending.draft.caption, generated.draft.caption)

    def test_approval_requires_explicit_reviewer_and_current_text_fingerprint(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())

        approved = EditorialReviewService.approve(pending, reviewer_ref="reviewer-1")

        self.assertEqual(approved.state, "approved_final")
        self.assertIsNotNone(approved.review)
        self.assertEqual(approved.review.decision, "approve")
        self.assertEqual(
            approved.review.reviewed_text_fingerprint,
            EditorialReviewService.text_fingerprint(pending),
        )

        with self.assertRaisesRegex(EditorialTransitionError, "reviewer_ref"):
            EditorialReviewService.approve(pending, reviewer_ref=" ")

    def test_feedback_is_recorded_without_regeneration_or_approval(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())

        with_feedback = EditorialReviewService.record_feedback(
            pending,
            feedback="Make the opening more direct.",
            reviewer_ref="reviewer-1",
        )

        self.assertEqual(with_feedback.state, "pending_human_review")
        self.assertEqual(with_feedback.review.decision, "request_regeneration")
        self.assertEqual(with_feedback.review.feedback, "Make the opening more direct.")
        self.assertEqual(with_feedback.draft.caption, pending.draft.caption)

        with self.assertRaisesRegex(EditorialTransitionError, "meaningful text"):
            EditorialReviewService.record_feedback(pending, feedback=" ")

    def test_invalid_transitions_are_rejected(self) -> None:
        generated = make_content()
        pending = EditorialReviewService.submit_for_review(generated)
        approved = EditorialReviewService.approve(pending, reviewer_ref="reviewer-1")

        with self.assertRaises(EditorialTransitionError):
            EditorialReviewService.submit_for_review(pending)
        with self.assertRaises(EditorialTransitionError):
            EditorialReviewService.approve(generated, reviewer_ref="reviewer-1")
        with self.assertRaises(EditorialTransitionError):
            EditorialReviewService.record_feedback(generated, feedback="Change hook")
        with self.assertRaises(EditorialTransitionError):
            EditorialReviewService.manual_edit(approved, caption="Edited after approval")

    def test_manual_edit_keeps_content_pending_and_preserves_grounding_metadata(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())
        edited = EditorialReviewService.manual_edit(
            pending,
            caption="Human-edited caption.",
            cta="Use the revised CTA",
        )

        self.assertEqual(edited.state, "pending_human_review")
        self.assertIsNone(edited.review)
        self.assertEqual(edited.draft.caption, "Human-edited caption.")
        self.assertEqual(edited.draft.cta, "Use the revised CTA")
        self.assertEqual(edited.draft.evidence_refs, pending.draft.evidence_refs)
        self.assertEqual(edited.draft.assumptions, pending.draft.assumptions)

    def test_feedback_regeneration_creates_pending_lineage_and_preserves_source(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())
        with_feedback = EditorialReviewService.record_feedback(
            pending,
            feedback="Make the opening more direct.",
            reviewer_ref="reviewer-1",
        )
        request = RegenerationRequest(
            trigger="human_feedback",
            feedback="Make the opening more direct.",
        )

        regenerated = EditorialReviewService.regenerate(
            with_feedback,
            request,
            draft_factory=lambda _content, _request: with_feedback.draft.model_copy(
                update={"caption": "Regenerated caption."}
            ),
        )

        self.assertNotEqual(regenerated.content_id, with_feedback.content_id)
        self.assertEqual(regenerated.state, "pending_human_review")
        self.assertEqual(regenerated.draft.caption, "Regenerated caption.")
        self.assertEqual(regenerated.lineage.source_draft_id, with_feedback.content_id)
        self.assertEqual(regenerated.lineage.trigger, "human_feedback")
        self.assertEqual(regenerated.lineage.feedback, request.feedback)
        self.assertEqual(
            regenerated.lineage.source_text_fingerprint,
            EditorialReviewService.text_fingerprint(with_feedback),
        )
        self.assertEqual(regenerated.draft.evidence_refs, with_feedback.draft.evidence_refs)
        self.assertEqual(
            regenerated.draft.evidence_provenance,
            with_feedback.draft.evidence_provenance,
        )
        self.assertEqual(with_feedback.draft.caption, "A grounded editable caption.")

    def test_changed_input_regeneration_records_only_allowed_inputs(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())
        request = RegenerationRequest(
            trigger="changed_inputs",
            changed_inputs={"objective": "invite a consultation", "format": "carousel"},
        )

        regenerated = EditorialReviewService.regenerate(
            pending,
            request,
            draft_factory=lambda _content, _request: pending.draft.model_copy(
                update={"caption": "Changed-input draft."}
            ),
        )

        self.assertEqual(regenerated.state, "pending_human_review")
        self.assertEqual(regenerated.lineage.trigger, "changed_inputs")
        self.assertEqual(regenerated.lineage.changed_inputs, request.changed_inputs)
        self.assertIsNone(regenerated.review)

        with self.assertRaises(ValueError):
            RegenerationRequest(
                trigger="changed_inputs",
                changed_inputs={"invented_business_fact": "unsupported"},
            )

    def test_regeneration_requires_recorded_feedback_and_preserves_state_on_failure(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())
        request = RegenerationRequest(trigger="human_feedback", feedback="Change the hook")

        with self.assertRaisesRegex(EditorialTransitionError, "recorded human feedback"):
            EditorialReviewService.regenerate(
                pending,
                request,
                draft_factory=lambda _content, _request: pending.draft,
            )

        with_feedback = EditorialReviewService.record_feedback(
            pending, feedback="Change the hook"
        )
        with self.assertRaisesRegex(EditorialTransitionError, "provider failed"):
            EditorialReviewService.regenerate(
                with_feedback,
                request,
                draft_factory=lambda _content, _request: (_ for _ in ()).throw(
                    RuntimeError("provider unavailable")
                ),
            )
        self.assertEqual(with_feedback.state, "pending_human_review")
        self.assertIsNone(with_feedback.lineage)

    def test_copy_and_export_return_exact_approved_text_and_metadata(self) -> None:
        pending = EditorialReviewService.submit_for_review(make_content())
        approved = EditorialReviewService.approve(pending, reviewer_ref="reviewer-1")

        copied = EditorialReviewService.copy_final(approved)
        exported = EditorialReviewService.export_final(approved)

        for artifact in (copied, exported):
            self.assertEqual(artifact.content_id, approved.content_id)
            self.assertEqual(artifact.text, approved.draft.caption)
            self.assertEqual(artifact.channel, approved.draft.channel)
            self.assertEqual(artifact.format, approved.draft.format)
            self.assertEqual(
                set(artifact.model_dump()), {"content_id", "text", "channel", "format"}
            )
        self.assertEqual(approved.state, "approved_final")

    def test_copy_and_export_reject_unapproved_content_without_mutating_state(self) -> None:
        generated = make_content()
        pending = EditorialReviewService.submit_for_review(generated)

        for content in (generated, pending):
            for operation in (
                EditorialReviewService.copy_final,
                EditorialReviewService.export_final,
            ):
                with self.assertRaisesRegex(EditorialTransitionError, "approved_final"):
                    operation(content)
            self.assertIn(content.state, {"generated_draft", "pending_human_review"})


if __name__ == "__main__":
    unittest.main()
