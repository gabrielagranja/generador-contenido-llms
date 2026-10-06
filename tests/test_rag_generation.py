from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import Mock

from apps.api.config import RagLocalSettings
from apps.api.drafting import ChannelAdaptedDraftService, RagGroundedDraftService
from apps.api.models import GuidedBrief
from apps.api.rag import JsonPlaceholderApiConnector, LocalChromaIndex, parse_pdf_to_canonical_chunks


ROOT = Path(__file__).resolve().parents[1]
PDF_FIXTURE = ROOT / "tests" / "fixtures" / "scoped-business-context-rag" / "synthetic-business-context.pdf"


class FakeCollection:
    def __init__(self) -> None:
        self.records: dict[str, dict[str, object]] = {}

    def upsert(self, **kwargs: object) -> None:
        for position, record_id in enumerate(kwargs["ids"]):
            self.records[record_id] = {
                "id": record_id,
                "document": kwargs["documents"][position],
                "metadata": kwargs["metadatas"][position],
            }

    def query(self, **kwargs: object) -> dict[str, list[list[object]]]:
        records = [
            record
            for record in self.records.values()
            if record["metadata"]["business_id"] == kwargs["where"]["business_id"]
        ][: kwargs["n_results"]]
        return {
            "ids": [[record["id"] for record in records]],
            "documents": [[record["document"] for record in records]],
            "metadatas": [[record["metadata"] for record in records]],
            "distances": [[0.2 for _ in records]],
        }


class FakeClient:
    def __init__(self) -> None:
        self.collection = FakeCollection()

    def get_or_create_collection(self, **_: object) -> FakeCollection:
        return self.collection


def make_brief(claim: str, platforms: list[str] | None = None) -> GuidedBrief:
    return GuidedBrief(
        topic_or_offer="weekday breakfast box",
        objective="explain the offer accurately",
        audience_context="local residents",
        platforms=platforms or ["instagram"],
        format="single_image",
        brand_and_constraints="clear and factual",
        facts=[
            {
                "statement": claim,
                "status": "CONFIRMED",
                "source": "synthetic test brief",
                "reason": "test input",
                "scope": "offer",
                "validation_needed": False,
            }
        ],
    )


def make_index(client: FakeClient) -> LocalChromaIndex:
    return LocalChromaIndex(
        RagLocalSettings(),
        embedding_function=lambda texts: [[float(len(text))] for text in texts],
        chroma_client=client,
    )


class RagGenerationEndToEndTests(unittest.TestCase):
    def test_pdf_evidence_flows_to_instagram_and_facebook_drafts(self) -> None:
        client = FakeClient()
        chunks = parse_pdf_to_canonical_chunks(
            PDF_FIXTURE,
            business_id="synthetic-bakery-a",
            source_id="business-guide",
            source_version="v1",
            consent_ref="synthetic-fixture",
        )
        index = make_index(client)
        index.ingest(chunks)
        generator = Mock()
        generator.generate.side_effect = [
            "Instagram breakfast box draft.",
            "Facebook breakfast box draft.",
        ]

        drafts = RagGroundedDraftService(index, generator).draft(
            make_brief(
                "Weekday breakfast box includes bread and fruit.",
                platforms=["instagram", "facebook"],
            ),
            business_id="synthetic-bakery-a",
            top_k=1,
        )

        self.assertEqual([draft.channel for draft in drafts], ["instagram", "facebook"])
        self.assertEqual(len(drafts[0].evidence_provenance), 1)
        self.assertEqual(drafts[0].evidence_provenance, drafts[1].evidence_provenance)
        self.assertIn("Channel: instagram", generator.generate.call_args_list[0].args[0])
        self.assertIn("Channel: facebook", generator.generate.call_args_list[1].args[0])

    def test_pdf_brief_retrieval_generation_and_evidence(self) -> None:
        client = FakeClient()
        chunks = parse_pdf_to_canonical_chunks(
            PDF_FIXTURE,
            business_id="synthetic-bakery-a",
            source_id="business-guide",
            source_version="v1",
            consent_ref="synthetic-fixture",
        )
        index = make_index(client)
        index.ingest(chunks)
        generator = Mock()
        generator.generate.return_value = "Weekday breakfast box includes bread and fruit."

        drafts = RagGroundedDraftService(index, generator).draft(
            make_brief("Weekday breakfast box includes bread and fruit."),
            business_id="synthetic-bakery-a",
            top_k=1,
        )

        draft = drafts[0]
        prompt = generator.generate.call_args.args[0]
        self.assertIn("source_id: business-guide", prompt)
        self.assertIn("page_number: 1", prompt)
        self.assertIn("SUPPORTED", prompt)
        self.assertEqual(draft.evidence_provenance[0]["source_type"], "pdf")
        self.assertEqual(draft.evidence_provenance[0]["page_number"], 1)
        self.assertEqual(draft.evidence_provenance[0]["business_id"], "synthetic-bakery-a")

    def test_api_brief_retrieval_generation_and_evidence(self) -> None:
        response = Mock()
        response.json.return_value = {
            "id": 7,
            "title": "weekday breakfast box",
            "body": "Bread and fruit are included.",
        }
        http_client = Mock()
        http_client.get.return_value = response
        chunks = JsonPlaceholderApiConnector(
            RagLocalSettings(api_base_url="https://api.example.test"),
            http_client=http_client,
        ).fetch_post(
            post_id=7,
            business_id="business-a",
            source_version="post-v1",
            consent_ref="authorized-demo",
            retrieved_at="2026-10-06T10:00:00+00:00",
        )
        index = make_index(FakeClient())
        index.ingest(chunks)
        generator = Mock()
        generator.generate.return_value = "Bread and fruit are included."

        draft = RagGroundedDraftService(index, generator).draft(
            make_brief("Bread and fruit are included."),
            business_id="business-a",
            top_k=1,
        )[0]

        self.assertEqual(draft.evidence_provenance[0]["source_type"], "api")
        self.assertEqual(draft.evidence_provenance[0]["source_uri"], "https://api.example.test/posts/7")
        self.assertEqual(draft.evidence_provenance[0]["business_id"], "business-a")
        self.assertIn("source_uri: https://api.example.test/posts/7", generator.generate.call_args.args[0])

    def test_business_isolation_and_unsupported_claim_are_explicit(self) -> None:
        client = FakeClient()
        chunks = parse_pdf_to_canonical_chunks(
            PDF_FIXTURE,
            business_id="synthetic-bakery-a",
            source_id="business-guide",
            source_version="v1",
            consent_ref="synthetic-fixture",
        )
        index = make_index(client)
        index.ingest(chunks)
        generator = Mock()
        generator.generate.return_value = "No unsupported price claim included."

        draft = RagGroundedDraftService(index, generator).draft(
            make_brief("The box costs five euros."),
            business_id="synthetic-bakery-a",
            top_k=1,
        )[0]

        self.assertEqual(draft.unsupported_claims, ["The box costs five euros."])
        self.assertIn("UNSUPPORTED: The box costs five euros.", generator.generate.call_args.args[0])
        self.assertNotIn("The box costs five euros.", draft.caption)

        isolated_draft = RagGroundedDraftService(index, generator).draft(
            make_brief("Weekday breakfast box includes bread and fruit."),
            business_id="synthetic-bakery-b",
            top_k=1,
        )[0]
        self.assertEqual(isolated_draft.evidence_provenance, [])
        self.assertNotIn("synthetic-bakery-a", generator.generate.call_args.args[0])

        with self.assertRaisesRegex(ValueError, "business_id"):
            ChannelAdaptedDraftService(generator).draft(
                make_brief("Weekday breakfast box includes bread and fruit."),
                retrieved_contexts=index.query("breakfast", "synthetic-bakery-a", 1),
                business_id="synthetic-bakery-b",
                grounding_enabled=True,
            )


if __name__ == "__main__":
    unittest.main()
