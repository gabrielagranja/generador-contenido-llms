from __future__ import annotations

import unittest

from apps.api.drafting import EditableTextDraft
from apps.api.editorial_review import (
    EditorialContent,
    EditorialReviewService,
    EditorialTransitionError,
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


if __name__ == "__main__":
    unittest.main()
