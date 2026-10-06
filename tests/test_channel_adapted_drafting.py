from __future__ import annotations

import unittest
from unittest.mock import Mock

from apps.api.drafting import ChannelAdaptedDraftService
from apps.api.models import GuidedBrief


def make_brief(*platforms: str) -> GuidedBrief:
    return GuidedBrief(
        topic_or_offer="Free 15-minute diagnosis",
        objective="prompt a request",
        audience_context="Local residents deciding whether repair is worthwhile",
        platforms=list(platforms),  # type: ignore[arg-type]
        format="single_image",
        brand_and_constraints="clear and practical; no unsupported claims",
        facts=[
            {
                "statement": "The diagnosis lasts 15 minutes and is free",
                "status": "CONFIRMED",
                "source": "synthetic F-01 brief",
                "reason": "Explicitly supplied",
                "scope": "offer",
                "validation_needed": False,
            },
            {
                "statement": "A repair will save money",
                "status": "UNKNOWN",
                "source": "none",
                "reason": "Not supplied",
                "scope": "offer",
                "validation_needed": True,
            },
        ],
    )


class ChannelAdaptedDraftServiceTests(unittest.TestCase):
    def test_selects_versioned_templates_and_adapts_both_channels(self) -> None:
        generator = Mock()
        generator.generate.side_effect = [
            "Instagram editable draft",
            "Facebook editable draft",
        ]

        drafts = ChannelAdaptedDraftService(generator).draft(
            make_brief("instagram", "facebook")
        )

        self.assertEqual([draft.channel for draft in drafts], ["instagram", "facebook"])
        self.assertEqual(
            [draft.template_id for draft in drafts],
            ["social.instagram.text-draft", "social.facebook.text-draft"],
        )
        self.assertEqual([draft.template_version for draft in drafts], ["1.0.0", "1.0.0"])
        self.assertNotEqual(drafts[0].caption, drafts[1].caption)
        self.assertEqual(generator.generate.call_count, 2)
        self.assertNotEqual(
            generator.generate.call_args_list[0].args[0],
            generator.generate.call_args_list[1].args[0],
        )

    def test_prompt_preserves_grounding_statuses_and_excludes_publication(self) -> None:
        generator = Mock()
        generator.generate.return_value = "Bounded editable draft"

        draft = ChannelAdaptedDraftService(generator).draft(make_brief("instagram"))[0]
        prompt = generator.generate.call_args.args[0]

        self.assertIn("[CONFIRMED] The diagnosis lasts 15 minutes and is free", prompt)
        self.assertIn("[UNKNOWN] A repair will save money", prompt)
        self.assertIn(
            "Audience context: Local residents deciding whether repair is worthwhile",
            prompt,
        )
        self.assertIn(
            "Brand and constraints: clear and practical; no unsupported claims",
            prompt,
        )
        self.assertIn("Never invent business facts", prompt)
        self.assertIn("Do not render media, publish, schedule", prompt)
        self.assertEqual(draft.evidence_refs, ["The diagnosis lasts 15 minutes and is free"])
        self.assertEqual(draft.assumptions, ["A repair will save money"])
        self.assertIn("not a publication request", draft.review_notes[1])

    def test_editable_output_can_be_revised_without_changing_grounding_metadata(self) -> None:
        generator = Mock()
        generator.generate.return_value = "Initial editable draft"

        draft = ChannelAdaptedDraftService(generator).draft(make_brief("instagram"))[0]
        original_evidence = draft.evidence_refs.copy()
        draft.caption = "Revised editable draft"

        self.assertEqual(draft.caption, "Revised editable draft")
        self.assertEqual(draft.evidence_refs, original_evidence)
        self.assertTrue(draft.assumptions)
        self.assertTrue(draft.review_notes)

    def test_empty_provider_output_is_rejected(self) -> None:
        generator = Mock()
        generator.generate.return_value = "   "

        with self.assertRaises(ValueError):
            ChannelAdaptedDraftService(generator).draft(make_brief("facebook"))


if __name__ == "__main__":
    unittest.main()
