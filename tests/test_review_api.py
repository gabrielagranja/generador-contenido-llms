import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from apps.api.drafting import EditableTextDraft
from apps.api.editorial_review import EditorialReviewService
from apps.api.main import app, editorial_store


class FakeGenerator:
    def generate(self, prompt: str) -> str:
        return "Borrador realista pendiente de revisiÃ³n."


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
        "notes": "Prueba de contrato",
        "facts": [],
    }


@pytest.fixture(autouse=True)
def clear_editorial_store() -> None:
    editorial_store.clear()
    yield
    editorial_store.clear()


def create_draft(*, brand_id: str = "brand-demo", business_id: str = "business-a") -> dict:
    with patch.dict(os.environ, {"LLM_PROVIDER": "mock"}, clear=False), patch(
        "apps.api.main.build_text_generator", return_value=FakeGenerator()
    ):
        response = client.post(
            "/drafts",
            json={
                "brief": brief_payload(),
                "brand_id": brand_id,
                "business_id": business_id,
            },
        )
    assert response.status_code == 200
    return response.json()


def test_post_assigns_stable_id_and_get_preserves_scope() -> None:
    body = create_draft()
    content_id = body["content_id"]

    retrieved = client.get(f"/drafts/{content_id}")
    assert retrieved.status_code == 200
    item = retrieved.json()
    assert item["content_id"] == content_id
    assert item["state"] == "pending_human_review"
    assert item["brand_id"] == "brand-demo"
    assert item["business_id"] == "business-a"
    assert client.get(f"/drafts/{content_id}").json()["content_id"] == content_id


def test_approval_requires_reviewer_and_invalid_transition_is_rejected() -> None:
    content_id = create_draft()["content_id"]

    missing_reviewer = client.post(
        f"/drafts/{content_id}/review",
        json={"decision": "approve", "reviewer_ref": ""},
    )
    assert missing_reviewer.status_code == 422

    approved = client.post(
        f"/drafts/{content_id}/review",
        json={"decision": "approve", "reviewer_ref": "reviewer-local"},
    )
    assert approved.status_code == 200
    assert approved.json()["state"] == "approved_final"
    assert approved.json()["review"]["reviewer_ref"] == "reviewer-local"

    second_approval = client.post(
        f"/drafts/{content_id}/review",
        json={"decision": "approve", "reviewer_ref": "reviewer-local"},
    )
    assert second_approval.status_code == 409


@pytest.mark.parametrize("feedback", ["", "   "])
def test_feedback_rejects_empty_or_whitespace_text(feedback: str) -> None:
    content_id = create_draft()["content_id"]
    response = client.post(
        f"/drafts/{content_id}/review",
        json={
            "decision": "request_regeneration",
            "reviewer_ref": "reviewer-local",
            "feedback": feedback,
        },
    )
    assert response.status_code == 422


def test_feedback_requires_text_and_keeps_draft_pending() -> None:
    content_id = create_draft()["content_id"]
    response = client.post(
        f"/drafts/{content_id}/review",
        json={
            "decision": "request_regeneration",
            "reviewer_ref": "reviewer-local",
            "feedback": "Aclarar el beneficio principal.",
        },
    )
    assert response.status_code == 200
    assert response.json()["state"] == "pending_human_review"
    assert response.json()["review"]["decision"] == "request_regeneration"

    missing_feedback = client.post(
        f"/drafts/{content_id}/review",
        json={"decision": "request_regeneration", "reviewer_ref": "reviewer-local"},
    )
    assert missing_feedback.status_code == 422


def test_whitespace_reviewer_reference_is_rejected_as_client_input() -> None:
    content_id = create_draft()["content_id"]
    response = client.post(
        f"/drafts/{content_id}/review",
        json={"decision": "approve", "reviewer_ref": "   "},
    )
    assert response.status_code == 422


def test_manual_edit_keeps_pending_state() -> None:
    content_id = create_draft()["content_id"]
    response = client.patch(
        f"/drafts/{content_id}",
        json={"caption": "Texto editado por una persona."},
    )
    assert response.status_code == 200
    assert response.json()["state"] == "pending_human_review"
    assert response.json()["review"] is None
    assert response.json()["draft"]["caption"] == "Texto editado por una persona."


def test_unknown_id_does_not_cross_business_boundary() -> None:
    first = create_draft(business_id="business-a")["content_id"]
    second = create_draft(business_id="business-b")["content_id"]
    assert first != second
    assert client.get("/drafts/not-a-real-content-id").status_code == 404
    assert client.get(f"/drafts/{first}").json()["business_id"] == "business-a"
    assert client.get(f"/drafts/{second}").json()["business_id"] == "business-b"


def test_review_status_and_rag_metadata_are_preserved() -> None:
    draft = EditableTextDraft(
        template_id="social.instagram.text-draft",
        template_version="1.0.0",
        channel="instagram",
        format="single_image",
        caption="Texto respaldado.",
        evidence_provenance=[
            {
                "business_id": "coll-amunt-pelu-sonia",
                "source_type": "pdf",
                "source_uri": "https://example.test/coll-amunt.pdf",
                "page_number": 7,
                "source_version": "2025",
            }
        ],
        supported_claims=["Texto respaldado."],
        unsupported_claims=["AfirmaciÃ³n no respaldada."],
    )
    content = EditorialReviewService.from_generated_draft(
        draft,
        content_id="rag-content",
        brand_id="coll-amunt",
        business_id="coll-amunt-pelu-sonia",
    )
    editorial_store.create(EditorialReviewService.submit_for_review(content))

    response = client.get("/drafts/rag-content")
    assert response.status_code == 200
    item = response.json()
    assert item["business_id"] == "coll-amunt-pelu-sonia"
    assert item["draft"]["evidence_provenance"][0]["source_type"] == "pdf"
    assert item["draft"]["evidence_provenance"][0]["page_number"] == 7
    assert item["draft"]["supported_claims"] == ["Texto respaldado."]
    assert item["draft"]["unsupported_claims"] == ["AfirmaciÃ³n no respaldada."]


def test_review_status_endpoint_returns_current_state() -> None:
    content_id = create_draft()["content_id"]
    response = client.get(f"/drafts/{content_id}/review")
    assert response.status_code == 200
    assert response.json()["state"] == "pending_human_review"
    assert response.json()["content_id"] == content_id

