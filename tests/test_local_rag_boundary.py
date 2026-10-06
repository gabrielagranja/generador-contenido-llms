from __future__ import annotations

import os
import json
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from apps.api.config import (
    DEFAULT_RAG_CHROMA_COLLECTION,
    DEFAULT_RAG_CHROMA_PERSIST_DIRECTORY,
    DEFAULT_RAG_EMBEDDING_MODEL,
    DEFAULT_RAG_EMBEDDING_REVISION,
    RagLocalSettings,
)
from apps.api.rag import (
    CanonicalBusinessRecord,
    CanonicalDocumentChunk,
    DEFAULT_PDF_CHUNK_OVERLAP,
    DEFAULT_PDF_CHUNK_SIZE,
    GroundingProvenance,
    LocalChromaIndex,
    RetrievedBusinessContext,
    build_local_embedding,
    api_response_to_canonical_chunks,
    chunk_id_for,
    ground_claim,
    parse_pdf_to_canonical_chunks,
    pdf_to_canonical_chunks,
)


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_FIXTURE = (
    ROOT
    / "tests"
    / "fixtures"
    / "scoped-business-context-rag"
    / "synthetic-business-context.json"
)
PDF_FIXTURE = ROOT / "tests" / "fixtures" / "scoped-business-context-rag" / "synthetic-business-context.pdf"


class FakeEmbeddingModel:
    def encode(self, texts: list[str], **_: object) -> list[list[float]]:
        return [[float(len(text))] for text in texts]


class FakeChromaCollection:
    def __init__(self) -> None:
        self.upserts: list[dict[str, object]] = []
        self.records: dict[str, dict[str, object]] = {}

    def upsert(self, **kwargs: object) -> None:
        self.upserts.append(kwargs)
        for index, record_id in enumerate(kwargs["ids"]):
            self.records[record_id] = {
                "id": record_id,
                "document": kwargs["documents"][index],
                "metadata": kwargs["metadatas"][index],
            }

    def query(self, **kwargs: object) -> dict[str, list[list[object]]]:
        self.query_calls = getattr(self, "query_calls", [])
        self.query_calls.append(kwargs)
        business_id = kwargs["where"]["business_id"]
        records = [
            record
            for record in self.records.values()
            if record["metadata"]["business_id"] == business_id
        ][: kwargs["n_results"]]
        return {
            "ids": [[record["id"] for record in records]],
            "documents": [[record["document"] for record in records]],
            "metadatas": [[record["metadata"] for record in records]],
            "distances": [[float(index) + 0.25 for index, _ in enumerate(records)]],
        }


class FakeChromaClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []
        self.collection = FakeChromaCollection()

    def get_or_create_collection(self, **kwargs: object) -> FakeChromaCollection:
        self.calls.append((str(kwargs["name"]), kwargs["embedding_function"]))
        return self.collection


class LocalRagBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = RagLocalSettings()
        self.client = FakeChromaClient()
        self.embedding_calls: list[list[str]] = []

        def embedding(texts: list[str]) -> list[list[float]]:
            self.embedding_calls.append(texts)
            return [[float(len(text))] for text in texts]

        self.embedding = embedding

    def test_defaults_are_explicit_and_provider_free(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            settings = RagLocalSettings.from_environment()

        self.assertEqual(settings.embedding_model, DEFAULT_RAG_EMBEDDING_MODEL)
        self.assertEqual(settings.embedding_revision, DEFAULT_RAG_EMBEDDING_REVISION)
        self.assertEqual(settings.chroma_collection, DEFAULT_RAG_CHROMA_COLLECTION)
        self.assertEqual(
            settings.chroma_persist_directory,
            DEFAULT_RAG_CHROMA_PERSIST_DIRECTORY,
        )

    def test_settings_can_use_a_temporary_persistence_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(
                os.environ,
                {"RAG_CHROMA_PERSIST_DIRECTORY": directory},
                clear=True,
            ):
                settings = RagLocalSettings.from_environment()

        self.assertEqual(settings.chroma_persist_directory, Path(directory))

    def test_embedding_can_be_injected_without_loading_a_model(self) -> None:
        settings = RagLocalSettings()
        factory_calls: list[tuple[str, str]] = []

        def factory(model_name: str, *, revision: str) -> FakeEmbeddingModel:
            factory_calls.append((model_name, revision))
            return FakeEmbeddingModel()

        embedding = build_local_embedding(settings, model_factory=factory)

        self.assertEqual(embedding(["offline text"]), [[12.0]])
        self.assertEqual(
            factory_calls,
            [(settings.embedding_model, settings.embedding_revision)],
        )

    def test_index_uses_injected_embedding_and_local_client_only(self) -> None:
        embedding = object()

        with patch.object(
            socket,
            "socket",
            side_effect=AssertionError("local index must not use the network"),
        ):
            index = LocalChromaIndex(
                self.settings,
                embedding_function=embedding,
                chroma_client=self.client,
            )

        self.assertIs(index.collection, self.client.collection)
        self.assertEqual(
            self.client.calls,
            [(self.settings.chroma_collection, embedding)],
        )

    def test_chunk_id_is_deterministic_and_positioned(self) -> None:
        self.assertEqual(chunk_id_for("menu-a", "v1"), "menu-a-v1-0001")
        self.assertEqual(chunk_id_for("menu-a", "v1", 2), "menu-a-v1-0002")
        self.assertEqual(chunk_id_for("menu-a", "v1"), chunk_id_for("menu-a", "v1"))

    def test_canonical_record_requires_all_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "consent_ref"):
            CanonicalBusinessRecord(
                business_id="business",
                source_id="source",
                source_version="v1",
                consent_ref="",
                    text="approved text",
            )

    def test_pdf_and_api_sources_produce_the_same_canonical_structure(self) -> None:
        pdf_chunks = pdf_to_canonical_chunks(
            business_id="business",
            source_id="guide",
            source_version="v2",
            consent_ref="consent-1",
            source_file="guide.pdf",
            pages=[{"page_number": 3, "text": "PDF content"}],
        )
        api_chunks = api_response_to_canonical_chunks(
            business_id="business",
            source_id="guide-api",
            source_version="2026-10",
            consent_ref="consent-1",
            source_uri="https://authorized.example/guide",
            response=[{"text": "API content"}],
            retrieved_at="2026-10-06T10:00:00Z",
        )

        self.assertIsInstance(pdf_chunks[0], CanonicalDocumentChunk)
        self.assertIsInstance(api_chunks[0], CanonicalDocumentChunk)
        self.assertEqual(pdf_chunks[0].source_type, "pdf")
        self.assertEqual(api_chunks[0].source_type, "api")
        for chunk in [*pdf_chunks, *api_chunks]:
            self.assertTrue(chunk.business_id)
            self.assertTrue(chunk.chunk_id)
            self.assertTrue(chunk.text)
            self.assertTrue(chunk.source_id)
            self.assertTrue(chunk.source_version)
            self.assertTrue(chunk.consent_ref)
        self.assertEqual((pdf_chunks[0].source_file, pdf_chunks[0].page_number), ("guide.pdf", 3))
        self.assertEqual(
            (api_chunks[0].source_uri, api_chunks[0].retrieved_at),
            ("https://authorized.example/guide", "2026-10-06T10:00:00Z"),
        )

    def test_canonical_chunk_requires_business_id_and_origin_metadata(self) -> None:
        with self.assertRaisesRegex(ValueError, "business_id"):
            CanonicalDocumentChunk(
                business_id="",
                source_type="api",
                source_id="source",
                source_version="v1",
                consent_ref="consent",
                text="text",
                chunk_id="chunk",
                    source_uri="https://authorized.example/source",
            )

    def test_real_pdf_extraction_preserves_pages_and_ignores_empty_pages(self) -> None:
        chunks = parse_pdf_to_canonical_chunks(
            PDF_FIXTURE,
            business_id="synthetic-bakery-a",
            source_id="business-guide",
            source_version="v1",
            consent_ref="synthetic-fixture",
            max_chunk_size=500,
            overlap=50,
        )

        self.assertTrue(chunks)
        self.assertTrue(all(isinstance(chunk, CanonicalDocumentChunk) for chunk in chunks))
        self.assertEqual({chunk.page_number for chunk in chunks}, {1, 2})
        self.assertTrue(all(chunk.source_type == "pdf" for chunk in chunks))
        self.assertTrue(all(chunk.source_file == str(PDF_FIXTURE) for chunk in chunks))
        self.assertIn("bread", " ".join(chunk.text for chunk in chunks))
        self.assertIn("Opening hours", " ".join(chunk.text for chunk in chunks))

    def test_pdf_chunking_is_deterministic_and_uses_page_position_ids(self) -> None:
        kwargs = {
            "business_id": "synthetic-bakery-a",
            "source_id": "business-guide",
            "source_version": "v1",
            "consent_ref": "synthetic-fixture",
            "max_chunk_size": 32,
            "overlap": 8,
        }
        first = parse_pdf_to_canonical_chunks(PDF_FIXTURE, **kwargs)
        second = parse_pdf_to_canonical_chunks(PDF_FIXTURE, **kwargs)

        self.assertEqual(first, second)
        self.assertGreater(len(first), 2)
        self.assertEqual(first[0].chunk_id, "business-guide-v1-p0001-c0001")
        self.assertTrue(all(len(chunk.text) <= 32 for chunk in first))
        page_one = [chunk for chunk in first if chunk.page_number == 1]
        self.assertGreater(len(page_one), 1)
        self.assertTrue(set(page_one[0].text.split()) & set(page_one[1].text.split()))
        self.assertEqual(DEFAULT_PDF_CHUNK_SIZE, 500)
        self.assertEqual(DEFAULT_PDF_CHUNK_OVERLAP, 50)

    def test_pdf_chunks_are_indexable_and_provenance_is_retrievable(self) -> None:
        chunks = parse_pdf_to_canonical_chunks(
            PDF_FIXTURE,
            business_id="synthetic-bakery-a",
            source_id="business-guide",
            source_version="v1",
            consent_ref="synthetic-fixture",
            max_chunk_size=500,
            overlap=50,
        )
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )

        ids = index.ingest(chunks)
        results = index.query("bread fruit", "synthetic-bakery-a", top_k=1)

        self.assertEqual(ids, [chunk.chunk_id for chunk in chunks])
        self.assertEqual(results[0].source_type, "pdf")
        self.assertEqual(results[0].source_file, str(PDF_FIXTURE))
        self.assertEqual(results[0].page_number, 1)
        self.assertEqual(results[0].chunk_id, chunks[0].chunk_id)

    def test_grounding_supported_pdf_claim_keeps_page_provenance(self) -> None:
        pdf_context = RetrievedBusinessContext(
            query="bread fruit",
            business_id="synthetic-bakery-a",
            chunk_id="business-guide-v1-p0001-c0001",
            text="Business A weekday breakfast box includes bread and fruit.",
            score=0.12,
            source_id="business-guide",
            source_version="v1",
            consent_ref="synthetic-fixture",
            embedding_model="local-model@revision",
            source_type="pdf",
            source_file=str(PDF_FIXTURE),
            page_number=1,
        )

        result = ground_claim("The weekday breakfast box includes bread and fruit.", [pdf_context])

        self.assertTrue(result.supported)
        self.assertEqual(result.evidence, pdf_context.text)
        self.assertEqual(result.provenance.source_type, "pdf")
        self.assertEqual(result.provenance.source_file, str(PDF_FIXTURE))
        self.assertEqual(result.provenance.page_number, 1)

    def test_ingestion_stores_metadata_for_both_synthetic_businesses(self) -> None:
        fixture = json.loads(SYNTHETIC_FIXTURE.read_text(encoding="utf-8"))
        records = [CanonicalBusinessRecord.from_mapping(item) for item in fixture["records"]]
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )

        ids = index.ingest(records)

        self.assertEqual(ids, ["menu-a-v1-0001", "menu-b-v1-0001"])
        upsert = self.client.collection.upserts[-1]
        self.assertEqual(upsert["ids"], ids)
        self.assertEqual(
            {metadata["business_id"] for metadata in upsert["metadatas"]},
            {"synthetic-bakery-a", "synthetic-bakery-b"},
        )
        self.assertEqual(
            set(upsert["metadatas"][0]),
            {
                "business_id",
                "source_id",
                "source_version",
                "consent_ref",
                "chunk_id",
                "embedding_model",
                "source_type",
                "source_uri",
                "retrieved_at",
            },
        )
        self.assertEqual(self.embedding_calls, [[record.text for record in records]])
        self.assertNotIn(fixture["negative_claims"][0]["claim"], upsert["documents"])

    def test_reingestion_uses_same_ids_and_chroma_upsert(self) -> None:
        record = CanonicalBusinessRecord(
            business_id="synthetic-bakery-a",
            source_id="menu-a",
            source_version="v1",
            consent_ref="synthetic-fixture",
            text="Weekday breakfast box includes bread and fruit.",
        )
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )

        first_ids = index.ingest([record])
        second_ids = index.ingest([record])

        self.assertEqual(first_ids, second_ids)
        self.assertEqual(
            [upsert["ids"] for upsert in self.client.collection.upserts],
            [["menu-a-v1-0001"], ["menu-a-v1-0001"]],
        )

    def test_query_is_scoped_by_business_id_and_preserves_provenance(self) -> None:
        fixture = json.loads(SYNTHETIC_FIXTURE.read_text(encoding="utf-8"))
        records = [CanonicalBusinessRecord.from_mapping(item) for item in fixture["records"]]
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )
        index.ingest(records)

        results_a = index.query("breakfast box", "synthetic-bakery-a", top_k=5)
        results_b = index.query("breakfast box", "synthetic-bakery-b", top_k=5)

        self.assertEqual([result.business_id for result in results_a], ["synthetic-bakery-a"])
        self.assertEqual([result.business_id for result in results_b], ["synthetic-bakery-b"])
        self.assertEqual(results_a[0].source_id, "menu-a")
        self.assertEqual(results_a[0].source_version, "v1")
        self.assertEqual(results_a[0].consent_ref, "synthetic-fixture")
        self.assertEqual(results_a[0].chunk_id, "menu-a-v1-0001")
        self.assertEqual(
            results_a[0].embedding_model,
            f"{self.settings.embedding_model}@{self.settings.embedding_revision}",
        )
        self.assertEqual(results_a[0].query, "breakfast box")
        self.assertEqual(results_a[0].score, 0.25)
        self.assertEqual(results_a[0].source_type, "api")
        self.assertEqual(results_a[0].source_uri, "synthetic://menu-a")
        self.assertEqual(
            self.client.collection.query_calls[0]["where"],
            {"business_id": "synthetic-bakery-a"},
        )
        self.assertEqual(
            self.client.collection.query_calls[1]["where"],
            {"business_id": "synthetic-bakery-b"},
        )

    def test_indexing_preserves_pdf_and_api_provenance(self) -> None:
        documents = [
            *pdf_to_canonical_chunks(
                business_id="business",
                source_id="manual",
                source_version="v1",
                consent_ref="consent-pdf",
                source_file="manual.pdf",
                pages=[{"page_number": 4, "text": "PDF policy"}],
            ),
            *api_response_to_canonical_chunks(
                business_id="business",
                source_id="catalog",
                source_version="v7",
                consent_ref="consent-api",
                source_uri="https://authorized.example/catalog",
                retrieved_at="2026-10-06T10:00:00Z",
                response=[{"text": "API catalog"}],
            ),
        ]
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )
        index.ingest(documents)
        results = index.query("policy", "business", top_k=2)

        self.assertEqual(results[0].source_type, "pdf")
        self.assertEqual(results[0].source_file, "manual.pdf")
        self.assertEqual(results[0].page_number, 4)
        self.assertEqual(results[1].source_type, "api")
        self.assertEqual(results[1].source_uri, "https://authorized.example/catalog")
        self.assertEqual(results[1].retrieved_at, "2026-10-06T10:00:00Z")

    def test_query_uses_top_k_and_query_embedding(self) -> None:
        fixture = json.loads(SYNTHETIC_FIXTURE.read_text(encoding="utf-8"))
        records = [CanonicalBusinessRecord.from_mapping(item) for item in fixture["records"]]
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )
        index.ingest(records)

        results = index.query("breakfast box", "synthetic-bakery-a", top_k=1)

        self.assertLessEqual(len(results), 1)
        self.assertEqual(self.embedding_calls[-1], ["breakfast box"])
        self.assertEqual(self.client.collection.query_calls[-1]["n_results"], 1)

    def test_query_rejects_invalid_inputs(self) -> None:
        index = LocalChromaIndex(
            self.settings,
            embedding_function=self.embedding,
            chroma_client=self.client,
        )
        for query, business_id, top_k, message in (
            ("", "business", 1, "query"),
            ("query", "", 1, "business_id"),
            ("query", "business", 0, "top_k"),
            ("query", "business", -1, "top_k"),
        ):
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    index.query(query, business_id, top_k)

    def test_grounding_supports_claim_from_business_a_evidence(self) -> None:
        context = RetrievedBusinessContext(
            query="breakfast box",
            business_id="synthetic-bakery-a",
            chunk_id="menu-a-v1-0001",
            text="Weekday breakfast box includes bread and fruit.",
            score=0.25,
            source_id="menu-a",
            source_version="v1",
            consent_ref="synthetic-fixture",
            embedding_model="local-model@revision",
        )

        result = ground_claim(
            "The weekday box includes bread and fruit.",
            [context],
        )

        self.assertTrue(result.supported)
        self.assertEqual(result.evidence, context.text)
        self.assertEqual(
            result.provenance,
            GroundingProvenance(
                business_id="synthetic-bakery-a",
                source_id="menu-a",
                source_version="v1",
                chunk_id="menu-a-v1-0001",
                consent_ref="synthetic-fixture",
            ),
        )

    def test_grounding_rejects_unsupported_price_claim(self) -> None:
        context = RetrievedBusinessContext(
            query="breakfast box",
            business_id="synthetic-bakery-a",
            chunk_id="menu-a-v1-0001",
            text="Weekday breakfast box includes bread and fruit.",
            score=0.25,
            source_id="menu-a",
            source_version="v1",
            consent_ref="synthetic-fixture",
            embedding_model="local-model@revision",
        )

        result = ground_claim("The box costs five euros.", [context])

        self.assertFalse(result.supported)
        self.assertIsNone(result.evidence)
        self.assertIsNone(result.provenance)
        self.assertTrue(result.reason)

    def test_grounding_rejects_empty_context_and_other_business(self) -> None:
        other_business = RetrievedBusinessContext(
            query="breakfast box",
            business_id="synthetic-bakery-b",
            chunk_id="menu-b-v1-0001",
            text="Weekend breakfast box includes bread and fruit.",
            score=0.25,
            source_id="menu-b",
            source_version="v1",
            consent_ref="synthetic-fixture",
            embedding_model="local-model@revision",
        )

        unsupported_from_empty = ground_claim("The weekday box includes bread and fruit.", [])
        unsupported_from_other = ground_claim(
            "The weekday box includes bread and fruit.",
            [other_business],
        )

        self.assertFalse(unsupported_from_empty.supported)
        self.assertFalse(unsupported_from_other.supported)

    def test_grounding_is_deterministic(self) -> None:
        context = RetrievedBusinessContext(
            query="breakfast box",
            business_id="synthetic-bakery-a",
            chunk_id="menu-a-v1-0001",
            text="Weekday breakfast box includes bread and fruit.",
            score=0.25,
            source_id="menu-a",
            source_version="v1",
            consent_ref="synthetic-fixture",
            embedding_model="local-model@revision",
        )

        first = ground_claim("The weekday box includes bread and fruit.", [context])
        second = ground_claim("The weekday box includes bread and fruit.", [context])

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
