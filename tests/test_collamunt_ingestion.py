from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from apps.api.collamunt import (
    COLLAMUNT_SOURCE_URI,
    build_collamunt_chunks,
    collamunt_business_id_for_page,
)
from apps.api.config import RagLocalSettings
from apps.api.drafting import RagGroundedDraftService
from apps.api.models import GuidedBrief
from apps.api.rag import LocalChromaIndex, extract_pdf_pages, sha256_file


class FakeCollection:
    def __init__(self) -> None:
        self.records: dict[str, dict[str, object]] = {}
        self.upsert_calls = 0

    def upsert(self, **kwargs: object) -> None:
        self.upsert_calls += 1
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
            "distances": [[0.1 for _ in records]],
        }


class FakeClient:
    def __init__(self) -> None:
        self.collection = FakeCollection()

    def get_or_create_collection(self, **_: object) -> FakeCollection:
        return self.collection


def make_index(client: FakeClient) -> LocalChromaIndex:
    return LocalChromaIndex(
        RagLocalSettings(),
        embedding_function=lambda texts: [[float(len(text))] for text in texts],
        chroma_client=client,
    )


class CollAmuntIngestionTests(unittest.TestCase):
    def test_local_pdf_parser_preserves_pages_and_is_deterministic(self) -> None:
        fixture = Path(__file__).parent / "fixtures" / "scoped-business-context-rag" / "synthetic-business-context.pdf"
        first = extract_pdf_pages(fixture)
        second = extract_pdf_pages(fixture)
        self.assertEqual(first, second)
        self.assertEqual([page["page_number"] for page in first], [1, 2])
        self.assertTrue(first[0]["text"])

    def test_collamunt_source_uses_association_and_stable_business_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.pdf"
            source.write_bytes(b"official-source")
            pages = [
                {"page_number": 1, "text": "Coll Amunt associacio"},
                {"page_number": 3, "text": "Pelu Sonia. La Sonia treballa al Coll."},
            ]
            ingestion = build_collamunt_chunks(source, pages)
            expected_sha256 = sha256_file(source)

        self.assertEqual(ingestion.source_sha256, expected_sha256)
        self.assertEqual(collamunt_business_id_for_page(1), "coll-amunt")
        self.assertEqual(collamunt_business_id_for_page(3), "coll-amunt-pelu-sonia")
        self.assertEqual({chunk.business_id for chunk in ingestion.chunks}, {"coll-amunt", "coll-amunt-pelu-sonia"})
        self.assertTrue(all(chunk.source_uri == COLLAMUNT_SOURCE_URI for chunk in ingestion.chunks))
        self.assertTrue(all(chunk.source_version == "2025" for chunk in ingestion.chunks))

    def test_ingestion_is_idempotent_and_retrieval_is_business_scoped(self) -> None:
        client = FakeClient()
        index = make_index(client)
        chunks = build_collamunt_chunks(
            Path(__file__),
            [
                {"page_number": 3, "text": "Pelu Sonia, perruqueria del barri."},
                {"page_number": 4, "text": "Centre d'Estetica Alma, cura personal."},
            ],
        ).chunks
        first = index.ingest(chunks)
        second = index.ingest(chunks)
        self.assertEqual(first, second)
        self.assertEqual(len(client.collection.records), len(chunks))
        results = index.query("perruqueria", "coll-amunt-pelu-sonia", top_k=5)
        self.assertTrue(results)
        self.assertTrue(all(result.business_id == "coll-amunt-pelu-sonia" for result in results))
        self.assertEqual(results[0].source_type, "pdf")
        self.assertEqual(results[0].source_uri, COLLAMUNT_SOURCE_URI)
        self.assertEqual(results[0].page_number, 3)

    def test_grounded_generation_supports_and_rejects_claims_with_pdf_provenance(self) -> None:
        client = FakeClient()
        index = make_index(client)
        chunks = build_collamunt_chunks(
            Path(__file__),
            [{"page_number": 3, "text": "Pelu Sonia, perruqueria del barri."}],
        ).chunks
        index.ingest(chunks)
        generator = Mock()
        generator.generate.return_value = "Pelu Sonia és una perruqueria del barri."
        brief = GuidedBrief(
            topic_or_offer="Pelu Sonia",
            objective="Donar a conèixer el comerç",
            audience_context="Persones del barri",
            platforms=["instagram"],
            format="single_image",
            brand_and_constraints="Clar i proper",
            facts=[
                {
                    "statement": "Pelu Sonia és una perruqueria del barri.",
                    "status": "CONFIRMED",
                    "source": "Coll Amunt! PDF",
                    "reason": "claim from official source",
                    "scope": "business",
                    "validation_needed": False,
                },
                {
                    "statement": "Pelu Sonia ofereix servei 24 hores.",
                    "status": "CONFIRMED",
                    "source": "test negative claim",
                    "reason": "must be rejected",
                    "scope": "business",
                    "validation_needed": True,
                },
            ],
        )
        draft = RagGroundedDraftService(index, generator).draft(
            brief, business_id="coll-amunt-pelu-sonia", top_k=1
        )[0]
        self.assertEqual(draft.evidence_provenance[0]["source_type"], "pdf")
        self.assertEqual(draft.evidence_provenance[0]["source_uri"], COLLAMUNT_SOURCE_URI)
        self.assertEqual(draft.evidence_provenance[0]["page_number"], 3)
        self.assertEqual(draft.evidence_provenance[0]["source_version"], "2025")
        self.assertEqual(draft.evidence_provenance[0]["business_id"], "coll-amunt-pelu-sonia")
        self.assertIn("Pelu Sonia ofereix servei 24 hores.", draft.unsupported_claims)
        self.assertIn("SUPPORTED: Pelu Sonia és una perruqueria del barri.", generator.generate.call_args.args[0])
        self.assertIn("UNSUPPORTED: Pelu Sonia ofereix servei 24 hores.", generator.generate.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
