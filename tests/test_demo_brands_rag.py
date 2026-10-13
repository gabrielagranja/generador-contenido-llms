from __future__ import annotations

from unittest.mock import Mock

from apps.api.config import RagLocalSettings
from apps.api.demo_brands import build_talent_hive_chunks, build_wayddh_chunks
from apps.api.drafting import DraftOutputError, RagGroundedDraftService
from apps.api.models import GuidedBrief
from apps.api.rag import LocalChromaIndex


class DemoCollection:
    def __init__(self) -> None:
        self.records: dict[str, dict[str, object]] = {}
        self.last_where: object = None

    def upsert(self, **kwargs: object) -> None:
        for position, record_id in enumerate(kwargs["ids"]):
            self.records[record_id] = {
                "id": record_id,
                "document": kwargs["documents"][position],
                "metadata": kwargs["metadatas"][position],
            }

    def query(self, **kwargs: object) -> dict[str, list[list[object]]]:
        self.last_where = kwargs["where"]
        where = kwargs["where"]
        if "$and" in where:
            filters = {next(iter(item)): next(iter(item.values())) for item in where["$and"]}
        else:
            filters = where
        records = [
            record
            for record in self.records.values()
            if all(record["metadata"].get(key) == value for key, value in filters.items())
        ][: kwargs["n_results"]]
        return {
            "ids": [[record["id"] for record in records]],
            "documents": [[record["document"] for record in records]],
            "metadatas": [[record["metadata"] for record in records]],
            "distances": [[0.1 for _ in records]],
        }


class DemoClient:
    def __init__(self) -> None:
        self.collection = DemoCollection()

    def get_or_create_collection(self, **_: object) -> DemoCollection:
        return self.collection


def make_index(client: DemoClient) -> LocalChromaIndex:
    return LocalChromaIndex(
        RagLocalSettings(),
        embedding_function=lambda texts: [[float(len(text))] for text in texts],
        chroma_client=client,
    )


def brief(topic: str) -> GuidedBrief:
    return GuidedBrief(
        topic_or_offer=topic,
        objective="explicar la experiencia con datos respaldados",
        audience_context="equipos de empresa",
        platforms=["instagram"],
        format="single_image",
        brand_and_constraints="No inventar servicios, clientes, cifras ni resultados garantizados.",
        facts=[],
    )


def test_brand_filter_prevents_talent_hive_and_wayddh_context_mixing() -> None:
    client = DemoClient()
    index = make_index(client)
    wayddh = build_wayddh_chunks(
        "corporate.pdf",
        pages=[{"page_number": 32, "text": "WAYDDH marketing digital y presencia digital."}],
    )
    index.ingest([*build_talent_hive_chunks(), *wayddh])

    talent_results = index.query("team building gamificación", "talent-hive", 5, brand_id="talent-hive")
    assert talent_results
    assert {result.brand_id for result in talent_results} == {"talent-hive"}
    assert {result.business_id for result in talent_results} == {"talent-hive"}
    assert client.collection.last_where == {
        "$and": [{"brand_id": "talent-hive"}, {"business_id": "talent-hive"}]
    }

    wayddh_results = index.query("marketing digital", "wayddh", 5, brand_id="wayddh")
    assert wayddh_results
    assert {result.brand_id for result in wayddh_results} == {"wayddh"}
    assert {result.business_id for result in wayddh_results} == {"wayddh"}


def test_talent_hive_generation_uses_team_building_and_gamification_evidence() -> None:
    index = make_index(DemoClient())
    index.ingest(build_talent_hive_chunks())
    generator = Mock()
    generator.generate.return_value = "Una experiencia de team building para aprender jugando."

    draft = RagGroundedDraftService(index, generator).draft(
        brief("team building y gamificación"),
        business_id="talent-hive",
        brand_id="talent-hive",
        top_k=2,
    )[0]

    assert "team building" in generator.generate.call_args.args[0]
    assert "gamificadas" in generator.generate.call_args.args[0]
    assert draft.evidence_provenance[0]["brand_id"] == "talent-hive"
    assert draft.evidence_provenance[0]["source_url"].startswith("https://thehive.barcelona/")


def test_wayddh_generation_is_grounded_in_the_corporate_pdf() -> None:
    index = make_index(DemoClient())
    index.ingest(
        build_wayddh_chunks(
            "corporate.pdf",
            pages=[{"page_number": 32, "text": "WAYDDH marketing digital y presencia digital."}],
        )
    )
    generator = Mock()
    generator.generate.return_value = "WAYDDH: presencia digital basada en la fuente corporativa."

    draft = RagGroundedDraftService(index, generator).draft(
        brief("WAYDDH marketing digital"),
        business_id="wayddh",
        brand_id="wayddh",
        top_k=1,
    )[0]

    assert draft.caption.startswith("WAYDDH")
    assert draft.evidence_provenance[0]["source_type"] == "pdf"
    assert draft.evidence_provenance[0]["source_file"] == "2025-Coll-Amunt-Llibre-_compressed.pdf"
    assert draft.evidence_provenance[0]["page_number"] == 32


def test_internal_scaffold_is_not_publishable() -> None:
    index = make_index(DemoClient())
    index.ingest(build_talent_hive_chunks())
    generator = Mock()
    generator.generate.return_value = "Scaffold: Copy approach PAS"

    try:
        RagGroundedDraftService(index, generator).draft(
            brief("team building"),
            business_id="talent-hive",
            brand_id="talent-hive",
            top_k=1,
        )
    except DraftOutputError as error:
        assert "instrucciones internas" in str(error)
    else:
        raise AssertionError("internal provider instructions were accepted")
