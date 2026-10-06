from __future__ import annotations

import re
import unittest
from pathlib import Path
from unittest.mock import Mock

from apps.api.drafting import ChannelAdaptedDraftService
from apps.api.models import GuidedBrief


FIXTURES = Path(__file__).parents[1] / "openspec" / "changes" / "expert-content-generation" / "examples" / "brief-fixtures.md"


def fixture_sections() -> dict[str, str]:
    content = FIXTURES.read_text(encoding="utf-8")
    sections = re.split(r"(?=## F-0[123] )", content)
    return {
        match.group(1): section
        for section in sections
        if (match := re.match(r"## (F-0[123]) ", section))
    }


def brief_from_fixture(fixture_id: str, section: str) -> GuidedBrief:
    values = {
        key: re.search(pattern, section, re.MULTILINE).group(1).strip()
        for key, pattern in {
            "topic": r"^- \*\*Topic/offer:\*\* (.+)$",
            "objective": r"^- \*\*Objective:\*\* (.+)$",
            "audience": r"^- \*\*Audience:\*\* (.+)$",
            "format": r"^- \*\*Format:\*\* (.+)$",
        }.items()
    }
    platforms = {"F-01": ["instagram"], "F-02": ["facebook"], "F-03": ["instagram", "facebook"]}[fixture_id]
    formats = {"single-image feed post": "single_image", "carousel": "carousel", "Reel": "reel"}
    objective = None if "`UNKNOWN`" in values["objective"] else values["objective"]
    audience = None if "`UNKNOWN`" in values["audience"] else values["audience"]
    status = "CONFIRMED" if fixture_id == "F-01" else "UNKNOWN"

    return GuidedBrief(
        topic_or_offer=values["topic"],
        objective=objective,
        audience_context=audience,
        platforms=platforms,  # type: ignore[arg-type]
        format=formats[values["format"].rstrip(".")],
        facts=[
            {
                "statement": f"{fixture_id} documented brief facts",
                "status": status,
                "source": f"synthetic {fixture_id} fixture",
                "reason": "State documented by the approved fixture",
                "scope": "post",
                "validation_needed": status != "CONFIRMED",
            }
        ],
    )


class ChannelAdaptedFixtureTests(unittest.TestCase):
    def test_f01_f02_f03_cover_template_channel_state_and_editable_contract(self) -> None:
        sections = fixture_sections()
        self.assertEqual(set(sections), {"F-01", "F-02", "F-03"})

        generator = Mock()
        generator.generate.side_effect = [
            "F-01 Instagram draft",
            "F-02 Facebook draft",
            "F-03 Instagram draft",
            "F-03 Facebook draft",
        ]

        service = ChannelAdaptedDraftService(generator)
        drafts_by_fixture = {
            fixture_id: service.draft(brief_from_fixture(fixture_id, section))
            for fixture_id, section in sections.items()
        }

        self.assertEqual(drafts_by_fixture["F-01"][0].template_id, "social.instagram.text-draft")
        self.assertEqual(drafts_by_fixture["F-02"][0].template_id, "social.facebook.text-draft")
        self.assertEqual(
            [draft.channel for draft in drafts_by_fixture["F-03"]],
            ["instagram", "facebook"],
        )
        self.assertTrue(all(draft.template_version == "1.0.0" for drafts in drafts_by_fixture.values() for draft in drafts))
        self.assertEqual(drafts_by_fixture["F-01"][0].evidence_refs, ["F-01 documented brief facts"])
        self.assertEqual(drafts_by_fixture["F-02"][0].assumptions, ["F-02 documented brief facts"])
        self.assertEqual(drafts_by_fixture["F-03"][0].assumptions, ["F-03 documented brief facts"])
        self.assertTrue(all(draft.caption for drafts in drafts_by_fixture.values() for draft in drafts))
        self.assertTrue(all(draft.review_notes for drafts in drafts_by_fixture.values() for draft in drafts))


if __name__ == "__main__":
    unittest.main()
