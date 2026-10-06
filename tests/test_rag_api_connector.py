from __future__ import annotations

import unittest
from unittest.mock import Mock

from apps.api.config import RagLocalSettings
from apps.api.rag import (
    CanonicalDocumentChunk,
    GroundingProvenance,
    JsonPlaceholderApiConnector,
    LocalChromaIndex,
    ground_claim,
)


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
            "distances": [[0.15 for _ in records]],
        }


class FakeClient:
    def __init__(self) -> None:
        self.collection = FakeCollection()

    def get_or_create_collection(self, **_: object) -> FakeCollection:
        return self.collection


class ApiRagConnectorTests(unittest.TestCase):
    def test_connector_builds_get_request_and_normalizes_document(self) -> None:
        response = Mock()
        response.json.return_value = {
            "id": 7,
            "userId": 2,
            "title": "weekday breakfast box",
            "body": "Bread and fruit are included.",
        }
        http_client = Mock()
        http_client.get.return_value = response
        connector = JsonPlaceholderApiConnector(
            RagLocalSettings(api_base_url="https://api.example.test"),
            http_client=http_client,
        )

        chunks = connector.fetch_post(
            post_id=7,
            business_id="business-a",
            source_version="post-v1",
            consent_ref="authorized-demo",
            retrieved_at="2026-10-06T10:00:00+00:00",
        )

        http_client.get.assert_called_once_with("/posts/7")
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(len(chunks), 1)
        chunk = chunks[0]
        self.assertIsInstance(chunk, CanonicalDocumentChunk)
        self.assertEqual(chunk.business_id, "business-a")
        self.assertEqual(chunk.source_type, "api")
        self.assertEqual(chunk.source_id, "jsonplaceholder-post-7")
        self.assertEqual(chunk.source_version, "post-v1")
        self.assertEqual(chunk.consent_ref, "authorized-demo")
        self.assertEqual(chunk.source_uri, "https://api.example.test/posts/7")
        self.assertEqual(chunk.retrieved_at, "2026-10-06T10:00:00+00:00")
        self.assertEqual(chunk.chunk_id, "jsonplaceholder-post-7-post-v1-0001")
        self.assertIn("Bread and fruit", chunk.text)

    def test_api_chunks_use_shared_index_retrieval_and_grounding(self) -> None:
        response = Mock()
        response.json.side_effect = [
            {
                "id": 7,
                "title": "weekday breakfast box",
                "body": "Bread and fruit are included.",
            },
            {
                "id": 8,
                "title": "weekday breakfast box",
                "body": "Bread and fruit are included.",
            },
        ]
        http_client = Mock()
        http_client.get.return_value = response
        connector = JsonPlaceholderApiConnector(
            RagLocalSettings(api_base_url="https://api.example.test"),
            http_client=http_client,
        )
        chunks_a = connector.fetch_post(
            post_id=7,
            business_id="business-a",
            source_version="post-v1",
            consent_ref="authorized-demo",
            retrieved_at="2026-10-06T10:00:00+00:00",
        )
        chunks_b = connector.fetch_post(
            post_id=8,
            business_id="business-b",
            source_version="post-v1",
            consent_ref="authorized-demo",
            retrieved_at="2026-10-06T10:00:00+00:00",
        )
        client = FakeClient()
        index = LocalChromaIndex(
            RagLocalSettings(),
            embedding_function=lambda texts: [[float(len(text))] for text in texts],
            chroma_client=client,
        )
        index.ingest([*chunks_a, *chunks_b])

        result = index.query("bread fruit", "business-a", top_k=1)[0]
        self.assertEqual(result.business_id, "business-a")
        self.assertEqual(result.source_type, "api")
        self.assertEqual(result.source_uri, "https://api.example.test/posts/7")
        self.assertEqual(result.retrieved_at, "2026-10-06T10:00:00+00:00")
        self.assertEqual(result.score, 0.15)

        grounded = ground_claim("Bread and fruit are included.", [result])
        self.assertTrue(grounded.supported)
        self.assertEqual(
            grounded.provenance,
            GroundingProvenance(
                business_id="business-a",
                source_id="jsonplaceholder-post-7",
                source_version="post-v1",
                chunk_id="jsonplaceholder-post-7-post-v1-0001",
                consent_ref="authorized-demo",
                source_type="api",
                source_uri="https://api.example.test/posts/7",
                retrieved_at="2026-10-06T10:00:00+00:00",
            ),
        )
        self.assertFalse(ground_claim("The box costs five euros.", [result]).supported)
        self.assertEqual(
            index.query("bread fruit", "business-b", top_k=1)[0].business_id,
            "business-b",
        )


if __name__ == "__main__":
    unittest.main()
