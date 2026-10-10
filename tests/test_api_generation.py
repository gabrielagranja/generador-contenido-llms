from unittest.mock import patch

from fastapi.testclient import TestClient

from apps.api.llm import LlmConfigurationError
from apps.api.main import app


class FakeGenerator:
    def generate(self, prompt: str) -> str:
        assert "Channel: instagram" in prompt
        return "Un borrador generado para revisión humana."


client = TestClient(app)


def brief_payload() -> dict[str, object]:
    return {
        "topic_or_offer": "Pan de temporada",
        "objective": "Dar a conocer el producto",
        "audience_context": "Personas del barrio",
        "business_context_refs": ["panaderialaplaza"],
        "platforms": ["instagram"],
        "format": "single_image",
        "brand_and_constraints": "Cercano y claro",
        "notes": "Fixture sintético",
        "facts": [],
    }


def test_create_drafts_returns_reviewable_content_without_exposing_secrets() -> None:
    with patch("apps.api.main.build_text_generator", return_value=FakeGenerator()):
        response = client.post("/drafts", json={"brief": brief_payload()})

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "mock"
    assert body["model"] == "deterministic-mock"
    assert body["review_state"] == "pending_human_review"
    assert body["drafts"][0]["caption"] == "Un borrador generado para revisión humana."
    assert "api_key" not in response.text.lower()


def test_create_drafts_rejects_invalid_brief() -> None:
    response = client.post("/drafts", json={"brief": {"platforms": []}})

    assert response.status_code == 422


def test_create_drafts_surfaces_missing_provider_configuration() -> None:
    with patch(
        "apps.api.main.build_text_generator",
        side_effect=LlmConfigurationError("provider configuration missing"),
    ):
        response = client.post("/drafts", json={"brief": brief_payload()})

    assert response.status_code == 503
    assert response.json()["detail"] == "provider configuration missing"
