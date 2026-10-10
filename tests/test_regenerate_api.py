import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from apps.api.copy_formulas import approach_for_formula, formula_from_feedback
from apps.api.main import app, editorial_store
from apps.api.models import GuidedBrief


class RecordingGenerator:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return f"Borrador {len(self.prompts)}"


client = TestClient(app)


def brief_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "topic_or_offer": "Aprender jugando",
        "objective": "Que conozcan la gamificación",
        "audience_context": "Responsables de equipos",
        "business_context_refs": ["talenthive"],
        "platforms": ["instagram"],
        "format": "single_image",
        "brand_and_constraints": "Cercano y profesional",
        "facts": [],
    }
    payload.update(overrides)
    return payload


@pytest.fixture(autouse=True)
def clear_editorial_store() -> None:
    editorial_store.clear()
    yield
    editorial_store.clear()


def create_and_request_changes(generator: RecordingGenerator, feedback: str) -> str:
    with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}, clear=False), patch(
        "apps.api.main.build_text_generator", return_value=generator
    ):
        content_id = client.post("/drafts", json={"brief": brief_payload()}).json()["content_id"]
    recorded = client.post(
        f"/drafts/{content_id}/review",
        json={"decision": "request_regeneration", "reviewer_ref": "reviewer-local", "feedback": feedback},
    )
    assert recorded.status_code == 200
    return content_id


def regenerate(generator: RecordingGenerator, content_id: str, **body: object):
    with patch("apps.api.main.build_text_generator", return_value=generator):
        return client.post(f"/drafts/{content_id}/regenerate", json={"brief": brief_payload(), **body})


def test_feedback_naming_pas_regenerates_with_that_formula_and_returns_to_review() -> None:
    generator = RecordingGenerator()
    feedback = "Prueba en modo PAS"
    content_id = create_and_request_changes(generator, feedback)

    response = regenerate(generator, content_id, feedback=feedback)

    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "pending_human_review"
    assert body["content_id"] != content_id
    assert body["lineage"]["source_draft_id"] == content_id
    assert body["draft"]["copy_formula"] == "PAS"
    assert "solicitud de cambios" in body["draft"]["approach_rationale"]
    assert "optional scaffold: PAS" in generator.prompts[-1]
    assert "Reviewer feedback to apply" in generator.prompts[-1]
    assert client.get(f"/drafts/{body['content_id']}").status_code == 200


def test_explicit_formula_overrides_feedback_text() -> None:
    generator = RecordingGenerator()
    content_id = create_and_request_changes(generator, "Más cercano, por favor")

    response = regenerate(generator, content_id, feedback="Más cercano, por favor", formula="AIDA")

    assert response.status_code == 200
    assert response.json()["draft"]["copy_formula"] == "AIDA"


def test_regeneration_needs_recorded_matching_feedback() -> None:
    generator = RecordingGenerator()
    content_id = create_and_request_changes(generator, "Prueba en modo PAS")

    mismatch = regenerate(generator, content_id, feedback="Otra cosa distinta")
    assert mismatch.status_code == 409

    with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}, clear=False), patch(
        "apps.api.main.build_text_generator", return_value=generator
    ):
        fresh = client.post("/drafts", json={"brief": brief_payload()}).json()["content_id"]
    unrecorded = regenerate(generator, fresh, feedback="Prueba en modo PAS")
    assert unrecorded.status_code == 409


def test_unknown_content_and_unknown_formula_are_rejected() -> None:
    generator = RecordingGenerator()
    assert regenerate(generator, "missing", feedback="PAS").status_code == 404
    content_id = create_and_request_changes(generator, "PAS")
    assert regenerate(generator, content_id, feedback="PAS", formula="XYZ").status_code == 422


def test_reviewer_choice_is_not_blocked_but_warns_without_confirmed_facts() -> None:
    brief = GuidedBrief(**brief_payload())  # type: ignore[arg-type]
    approach, reason = approach_for_formula("PAS", brief)
    assert approach.formula == "PAS"
    assert "sin datos ni pruebas concretas" in reason
    _, aida_reason = approach_for_formula("AIDA", brief)
    assert "sin datos" not in aida_reason


def test_formula_is_read_from_feedback_only_when_named() -> None:
    assert formula_from_feedback("Prueba en modo PAS") == "PAS"
    assert formula_from_feedback("usa AIDA") == "AIDA"
    assert formula_from_feedback("Más cercano") is None
    assert formula_from_feedback("Pasto verde") is None
