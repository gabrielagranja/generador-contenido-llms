from __future__ import annotations

import unittest

from pydantic import ValidationError

from apps.api.models import GuidedBrief


class GuidedBriefModelTests(unittest.TestCase):
    def test_accepts_approved_partial_brief_and_fact_statuses(self) -> None:
        brief = GuidedBrief(
            topic_or_offer="Breakfast menu",
            objective="inform",
            platforms=["instagram", "facebook"],
            format="single_image",
            facts=[
                {
                    "statement": "The menu is available on weekdays",
                    "status": "CONFIRMED",
                    "source": "user brief",
                    "reason": "Explicitly supplied by the user",
                    "scope": "offer",
                    "validation_needed": False,
                },
                {
                    "statement": "Nearby workers are the audience",
                    "status": "INFERRED",
                    "source": "user brief",
                    "reason": "Derived from the described morning context",
                    "scope": "audience",
                    "validation_needed": True,
                },
                {
                    "statement": "A discount is available",
                    "status": "UNKNOWN",
                    "source": "none",
                    "reason": "No discount was provided",
                    "scope": "offer",
                    "validation_needed": True,
                },
            ],
        )

        self.assertEqual(brief.format, "single_image")
        self.assertEqual([fact.status for fact in brief.facts], ["CONFIRMED", "INFERRED", "UNKNOWN"])

    def test_requires_at_least_one_approved_platform(self) -> None:
        with self.assertRaises(ValidationError):
            GuidedBrief(platforms=[], format="reel")

    def test_rejects_unsupported_platform_and_format(self) -> None:
        with self.assertRaises(ValidationError):
            GuidedBrief(platforms=["tiktok"], format="story")  # type: ignore[list-item]

    def test_rejects_duplicate_platforms(self) -> None:
        with self.assertRaises(ValidationError):
            GuidedBrief(platforms=["instagram", "instagram"], format="carousel")

    def test_rejects_empty_material_fact_fields(self) -> None:
        with self.assertRaises(ValidationError):
            GuidedBrief(
                platforms=["instagram"],
                format="reel",
                facts=[
                    {
                        "statement": "",
                        "status": "CONFIRMED",
                        "source": "brief",
                        "reason": "provided",
                        "scope": "business",
                        "validation_needed": False,
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
