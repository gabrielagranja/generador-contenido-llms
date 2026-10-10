from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from apps.api.collamunt import (
    COLLAMUNT_SOURCE_URI,
    COLLAMUNT_SHEET_CHUNK_SIZE,
    build_collamunt_chunks,
    collamunt_business_id_for_page,
    split_business_sheet,
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


class BusinessSheetChunkingTests(unittest.TestCase):
    def test_short_sheet_stays_in_one_chunk(self) -> None:
        text = "Pelu Sonia treballa al Coll.\n\nObre amb cita prèvia."
        self.assertEqual(split_business_sheet(text), ["Pelu Sonia treballa al Coll. Obre amb cita prèvia."])

    def test_long_sheet_splits_on_sentences_never_mid_sentence(self) -> None:
        sentences = [f"Frase número {i} sobre el comerç del barri." for i in range(40)]
        chunks = split_business_sheet(" ".join(sentences), max_size=200)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 200 for chunk in chunks))
        self.assertTrue(all(chunk.endswith(".") for chunk in chunks))
        self.assertEqual(" ".join(chunks), " ".join(sentences))

    def test_oversized_sentence_falls_back_to_word_boundaries(self) -> None:
        sentence = " ".join(["paraula"] * 100)
        chunks = split_business_sheet(sentence, max_size=120)
        self.assertTrue(all(len(chunk) <= 120 for chunk in chunks))
        self.assertEqual(" ".join(chunks), sentence)

    def test_empty_text_and_invalid_size(self) -> None:
        self.assertEqual(split_business_sheet("  \n\n "), [])
        with self.assertRaises(ValueError):
            split_business_sheet("text", max_size=0)

    def test_business_chunks_carry_name_and_stay_in_their_business(self) -> None:
        sheet = " ".join(f"Frase {i} de la fitxa." for i in range(120))
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.pdf"
            source.write_bytes(b"official-source")
            expected_sha256 = sha256_file(source)
            ingestion = build_collamunt_chunks(
                source,
                [
                    {"page_number": 3, "text": sheet},
                    {"page_number": 4, "text": "Centre d'Estètica Alma. Cura personal."},
                ],
            )
        sonia = [c for c in ingestion.chunks if c.business_id == "coll-amunt-pelu-sonia"]
        self.assertGreater(len(sonia), 1)
        self.assertTrue(all(c.text.startswith("Pelu Sonia. ") for c in sonia))
        self.assertTrue(all(len(c.text) <= COLLAMUNT_SHEET_CHUNK_SIZE for c in sonia))
        self.assertTrue(all(c.page_number == 3 for c in sonia))
        self.assertTrue(all(c.source_id == "collamunt-llibre" for c in sonia))
        self.assertTrue(all(c.source_version == "2025" for c in sonia))
        self.assertTrue(all(c.source_sha256 == expected_sha256 for c in sonia))
        self.assertEqual(
            [c.chunk_id.rsplit("-c", 1)[-1] for c in sonia],
            [f"{position:04d}" for position in range(1, len(sonia) + 1)],
        )
        self.assertEqual(len({c.chunk_id for c in ingestion.chunks}), len(ingestion.chunks))

    def test_association_pages_keep_generic_chunking(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.pdf"
            source.write_bytes(b"official-source")
            ingestion = build_collamunt_chunks(source, [{"page_number": 1, "text": "Coll Amunt associacio"}])
        self.assertEqual([c.text for c in ingestion.chunks], ["Coll Amunt associacio"])
