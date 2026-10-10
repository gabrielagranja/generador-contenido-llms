"""Minimal provider-independent API foundation."""

from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from apps.api.drafting import ChannelAdaptedDraftService, EditableTextDraft
from apps.api.llm import LlmConfigurationError, build_text_generator
from apps.api.models import GuidedBrief


class ReadinessResponse(BaseModel):
    """Stable response returned by the local readiness endpoint."""

    status: Literal["ready"] = "ready"
    service: Literal["api"] = "api"


class DraftRequest(BaseModel):
    """Validated request for one or more channel-adapted text drafts."""

    brief: GuidedBrief


class DraftResponse(BaseModel):
    """Reviewable drafts returned before any approval or publication action."""

    drafts: list[EditableTextDraft]
    provider: str
    model: str
    review_state: Literal["pending_human_review"] = "pending_human_review"


app = FastAPI(
    title="Generador de contenido API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/readiness", response_model=ReadinessResponse)
def readiness() -> ReadinessResponse:
    """Report local API readiness without contacting external providers."""

    return ReadinessResponse()


@app.post("/drafts", response_model=DraftResponse)
def create_drafts(request: DraftRequest) -> DraftResponse:
    """Generate editable drafts through the configured provider.

    The API owns provider credentials. The browser receives only reviewable
    draft data and never receives the configured API key.
    """

    try:
        generator = build_text_generator()
    except LlmConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    drafts = ChannelAdaptedDraftService(generator).draft(request.brief)
    from apps.api.config import LlmSettings

    llm_settings = LlmSettings.from_environment()
    provider = llm_settings.provider
    model = "deterministic-mock" if provider == "mock" else llm_settings.groq_model
    return DraftResponse(drafts=drafts, provider=provider, model=model)
