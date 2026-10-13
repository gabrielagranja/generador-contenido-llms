from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from apps.api.config import CreativeStorageSettings, OpenAiImageSettings
from apps.api.creatives import CreativeGenerationError, CreativeService
from apps.api.editorial_store import CreativeStore
from apps.api.main import app, creative_store
from apps.api.rag import RetrievedBusinessContext


class FakeIndex:
    calls: list[dict[str, object]] = []

    def __init__(self, *_args, **_kwargs) -> None:
        pass

    def query(self, query: str, business_id: str, top_k: int, brand_id: str | None = None):
        self.calls.append({"query": query, "business_id": business_id, "brand_id": brand_id, "top_k": top_k})
        text = "Escape Boxes portátiles para equipos" if brand_id == "talent-hive" else "Servicios documentados en el PDF corporativo WAYDDH"
        return [RetrievedBusinessContext(
            query=query, business_id=business_id, brand_id=brand_id, chunk_id="chunk-1", text=text,
            score=0.1, source_id="source-1", source_version="2026", consent_ref="approved",
            embedding_model="fake", source_type="pdf" if brand_id == "wayddh" else "api",
            source_name="WAYDDH corporate PDF" if brand_id == "wayddh" else "Talent Hive official pages",
            source_url="https://example.test/source", language="es", retrieved_at="2026-10-13T00:00:00Z",
        )]


class FakeImageGenerator:
    model = "gpt-image-2.5-flare"

    def __init__(self) -> None:
        self.prompts: list[str] = []

    def generate(self, *, prompt: str, size: str) -> bytes:
        self.prompts.append(prompt)
        image = Image.new("RGB", (1536, 1024), color=(36, 83, 212))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()


@pytest.fixture(autouse=True)
def isolate_creatives(monkeypatch: pytest.MonkeyPatch, tmp_path):
    import apps.api.main as main

    creative_store.clear()
    FakeIndex.calls.clear()
    generator = FakeImageGenerator()
    monkeypatch.setattr(main, "LocalChromaIndex", FakeIndex)
    monkeypatch.setattr(
        main,
        "build_creative_service",
        lambda: CreativeService(generator, CreativeStorageSettings(tmp_path / "creatives")),
    )
    monkeypatch.setenv("CREATIVE_STORAGE_DIRECTORY", str(tmp_path / "creatives"))
    yield generator
    creative_store.clear()


client = TestClient(app)


def payload(brand_id: str = "talent-hive") -> dict[str, str]:
    return {
        "brand_id": brand_id,
        "brief": "Presentar una experiencia para equipos",
        "platform": "instagram",
        "placement": "feed",
        "format": "carousel",
        "copy": "Una experiencia para activar al equipo.",
        "style": "editorial",
    }


def test_openai_image_configuration_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        OpenAiImageSettings.from_environment()


def test_openai_image_model_is_configurable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-only")
    monkeypatch.setenv("OPENAI_IMAGE_MODEL", "gpt-image-2.5-flare")
    assert OpenAiImageSettings.from_environment().model == "gpt-image-2.5-flare"


def test_creative_uses_talent_hive_context_and_meta_size(isolate_creatives: FakeImageGenerator) -> None:
    response = client.post("/creatives", json=payload())
    assert response.status_code == 200
    body = response.json()
    assert body["review_state"] == "pending-review"
    assert (body["width"], body["height"], body["aspect_ratio"]) == (1080, 1350, "1080:1350")
    assert body["provenance"][0]["brand_id"] == "talent-hive"
    assert "Escape Boxes" in body["prompt"]
    assert FakeIndex.calls[0]["business_id"] == "talent-hive"
    assert FakeIndex.calls[0]["brand_id"] == "talent-hive"
    image = client.get(body["image_url"])
    assert image.status_code == 200
    with Image.open(BytesIO(image.content)) as rendered:
        assert rendered.size == (1080, 1350)


def test_wayddh_isolated_and_pdf_grounded(isolate_creatives: FakeImageGenerator) -> None:
    response = client.post("/creatives", json=payload("wayddh"))
    assert response.status_code == 200
    body = response.json()
    assert body["brand_id"] == "wayddh"
    assert body["provenance"][0]["source_name"] == "WAYDDH corporate PDF"
    assert "PDF corporativo" in body["prompt"]
    assert "Talent Hive" not in body["prompt"]


def test_regeneration_discard_and_prototype_approval(isolate_creatives: FakeImageGenerator) -> None:
    created = client.post("/creatives", json=payload()).json()
    regenerated = client.post(f"/creatives/{created['id']}/regenerate", json=payload())
    assert regenerated.status_code == 200
    assert regenerated.json()["source_creative_id"] == created["id"]
    discarded = client.post(f"/creatives/{created['id']}/discard")
    assert discarded.json()["review_state"] == "discarded"
    approved = client.post(f"/creatives/{regenerated.json()['id']}/approve")
    assert approved.json()["review_state"] == "approved-prototype"


def test_openai_error_is_specific_and_never_exposes_key(monkeypatch: pytest.MonkeyPatch) -> None:
    import apps.api.main as main

    class FailingGenerator(FakeImageGenerator):
        def generate(self, *, prompt: str, size: str) -> bytes:
            raise CreativeGenerationError("OpenAI image generation timed out or is unavailable")

    monkeypatch.setattr(main, "build_creative_service", lambda: CreativeService(FailingGenerator(), CreativeStorageSettings(Path(".local/test-creatives"))))
    response = client.post("/creatives", json=payload())
    assert response.status_code == 502
    assert "OpenAI image generation timed out" in response.json()["detail"]
    assert "test-only" not in response.text
