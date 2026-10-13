"""Minimal provider-independent API foundation."""

from datetime import date
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Path, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from apps.api.auth import (
    AuthSettings,
    issue_token,
    login_attempt_key,
    login_attempt_limiter,
    require_secure_transport,
    require_session,
    resolve_username,
)
from apps.api.copy_formulas import approach_for_formula, select_copy_approach
from apps.api.drafting import ChannelAdaptedDraftService, DraftOutputError, EditableTextDraft
from apps.api.editorial_review import (
    EditorialContent,
    EditorialReviewService,
    EditorialTransitionError,
    HumanReview,
    RegenerationRequest,
)
from apps.api.editorial_store import CreativeStore, EditorialContentStore, EditorialPlanStore
from apps.api.llm import LlmConfigurationError, build_text_generator
from apps.api.models import GuidedBrief
from apps.api.config import CreativeStorageSettings, EditorialPersistenceSettings, OpenAiImageSettings, RagLocalSettings
from apps.api.creative_formats import get_meta_creative_format
from apps.api.creatives import CreativeGenerationError, CreativeRecord, CreativeService, OpenAiImageGenerator
from apps.api.drafting import RagGroundedDraftService
from apps.api.editorial_planning import EditorialPlan, reschedule_item
from apps.api.rag import LocalChromaIndex


class ReadinessResponse(BaseModel):
    """Stable response returned by the local readiness endpoint."""

    status: Literal["ready"] = "ready"
    service: Literal["api"] = "api"


class DraftRequest(BaseModel):
    """Validated request for one or more channel-adapted text drafts."""

    brief: GuidedBrief
    rag_enabled: bool = False
    brand_id: str | None = None
    business_id: str | None = None
    top_k: int = 3
    formula: Literal["AIDA", "PAS", "4CS", "BAB", "4PS", "OPEN_LOOP"] | None = None


class DraftResponse(BaseModel):
    """Reviewable drafts returned before any approval or publication action."""

    drafts: list[EditableTextDraft]
    content_ids: list[str]
    content_id: str | None = None
    provider: str
    model: str
    review_state: Literal["pending_human_review"] = "pending_human_review"


class CreativeRequest(BaseModel):
    """Inputs for one non-published visual asset."""

    brand_id: Literal["coll-amunt", "talent-hive", "wayddh"]
    brief: str = Field(min_length=1)
    platform: Literal["instagram", "facebook"]
    placement: str = Field(min_length=1)
    format: Literal["single_image", "carousel", "reel"]
    copy_text: str = Field(min_length=1, alias="copy")
    style: str = Field(min_length=1)


class CreativeResponse(BaseModel):
    id: str
    image_url: str
    prompt: str
    brand_id: str
    platform: str
    placement: str
    format: str
    width: int
    height: int
    aspect_ratio: str
    model: str
    generated_at: str
    review_state: Literal["pending-review", "approved-prototype", "discarded"]
    provenance: list[dict[str, object]]
    source_creative_id: str | None = None


class ReviewRequest(BaseModel):
    decision: Literal["approve", "request_regeneration"]
    reviewer_ref: str = Field(min_length=1)
    feedback: str | None = Field(default=None, min_length=1)


class RegenerateRequest(BaseModel):
    """Inputs needed to regenerate one draft after human feedback was recorded."""

    brief: GuidedBrief
    feedback: str = Field(min_length=1)
    formula: Literal["AIDA", "PAS", "4CS", "BAB", "4PS", "OPEN_LOOP"] | None = None
    rag_enabled: bool = False
    top_k: int = 3


class ManualEditRequest(BaseModel):
    caption: str = Field(min_length=1)
    cta: str | None = None


class ReviewStatusResponse(BaseModel):
    content_id: str
    state: Literal["generated_draft", "pending_human_review", "approved_final"]
    review: HumanReview | None = None


app = FastAPI(
    title="Generador de contenido API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3004",
        "http://127.0.0.1:3004",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

persistence_settings = EditorialPersistenceSettings.from_environment()
editorial_store = EditorialContentStore(persistence_settings.database_path)
editorial_plan_store = EditorialPlanStore(persistence_settings.database_path)
creative_store = CreativeStore(persistence_settings.database_path)


@app.get("/readiness", response_model=ReadinessResponse)
def readiness() -> ReadinessResponse:
    """Report local API readiness without contacting external providers."""

    return ReadinessResponse()


def build_creative_service() -> CreativeService:
    """Construct the image provider only when a creative is requested."""
    return CreativeService(
        OpenAiImageGenerator(OpenAiImageSettings.from_environment()),
        CreativeStorageSettings.from_environment(),
    )


def _creative_response(creative: CreativeRecord) -> CreativeResponse:
    return CreativeResponse(
        id=creative.id,
        image_url=f"/creatives/{creative.id}/image",
        prompt=creative.prompt,
        brand_id=creative.brand_id,
        platform=creative.platform,
        placement=creative.placement,
        format=creative.format,
        width=creative.width,
        height=creative.height,
        aspect_ratio=creative.aspect_ratio,
        model=creative.model,
        generated_at=creative.generated_at.isoformat(),
        review_state=creative.review_state,
        provenance=[item.model_dump() for item in creative.provenance],
        source_creative_id=creative.source_creative_id,
    )


def _get_creative(creative_id: str, username: str) -> CreativeRecord:
    creative = creative_store.get(creative_id, owner_username=username)
    if creative is None:
        raise HTTPException(status_code=404, detail="creative_id not found")
    return creative


def _creative_contexts(request: CreativeRequest):
    """Retrieve only selected-brand context; missing evidence is explicit in the prompt."""
    try:
        index = LocalChromaIndex(RagLocalSettings())
        return index.query(
            f"{request.brief} {request.copy_text}",
            business_id=request.brand_id,
            brand_id=request.brand_id,
            top_k=3,
        )
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=503, detail=f"No se pudo recuperar el contexto RAG: {error}") from error


def _create_creative(
    request: CreativeRequest,
    username: str,
    *,
    source_creative_id: str | None = None,
) -> CreativeResponse:
    try:
        target = get_meta_creative_format(request.platform, request.placement, request.format)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    contexts = _creative_contexts(request)
    try:
        service = build_creative_service()
        creative = service.generate(
            creative_id=creative_store.create_id(),
            brand_id=request.brand_id,
            brief=request.brief,
            copy=request.copy_text,
            style=request.style,
            target=target,
            contexts=contexts,
            owner_username=username,
            source_creative_id=source_creative_id,
        )
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except CreativeGenerationError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    creative_store.create(creative)
    return _creative_response(creative)


@app.post("/creatives", response_model=CreativeResponse)
def create_creative(request: CreativeRequest, username: str = Depends(require_session)) -> CreativeResponse:
    """Generate one review-only image from an isolated brand RAG scope."""
    return _create_creative(request, username)


@app.get("/creatives/{creative_id}", response_model=CreativeResponse)
def get_creative(creative_id: str, username: str = Depends(require_session)) -> CreativeResponse:
    return _creative_response(_get_creative(creative_id, username))


@app.get("/creatives/{creative_id}/image")
def get_creative_image(creative_id: str, username: str = Depends(require_session)) -> FileResponse:
    creative = _get_creative(creative_id, username)
    path = CreativeStorageSettings.from_environment().directory / creative.image_filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="creative image file not found")
    return FileResponse(path, media_type="image/png")


@app.post("/creatives/{creative_id}/regenerate", response_model=CreativeResponse)
def regenerate_creative(creative_id: str, request: CreativeRequest, username: str = Depends(require_session)) -> CreativeResponse:
    source = _get_creative(creative_id, username)
    if source.review_state == "discarded":
        raise HTTPException(status_code=409, detail="discarded creatives cannot be regenerated")
    if source.brand_id != request.brand_id:
        raise HTTPException(status_code=422, detail="brand_id must match the creative being regenerated")
    return _create_creative(request, username, source_creative_id=source.id)


@app.post("/creatives/{creative_id}/discard", response_model=CreativeResponse)
def discard_creative(creative_id: str, username: str = Depends(require_session)) -> CreativeResponse:
    creative = _get_creative(creative_id, username)
    if creative.review_state == "approved-prototype":
        raise HTTPException(status_code=409, detail="approved creatives cannot be discarded")
    return _creative_response(creative_store.save(creative.model_copy(update={"review_state": "discarded"})))


@app.post("/creatives/{creative_id}/approve", response_model=CreativeResponse)
def approve_creative(creative_id: str, username: str = Depends(require_session)) -> CreativeResponse:
    creative = _get_creative(creative_id, username)
    if creative.review_state == "discarded":
        raise HTTPException(status_code=409, detail="discarded creatives cannot be approved")
    return _creative_response(creative_store.save(creative.model_copy(update={"review_state": "approved-prototype"})))


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    username: str
    expires_at: int


@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, http_request: Request) -> LoginResponse:
    """Exchange the local credentials for a signed, expiring session token."""

    settings = AuthSettings.from_environment()
    if settings is None:
        raise HTTPException(status_code=503, detail="authentication is not configured")
    require_secure_transport(http_request, settings)
    attempt_key = login_attempt_key(http_request, request.username)
    if not login_attempt_limiter.allow(
        attempt_key,
        max_attempts=settings.login_max_attempts,
        window_seconds=settings.login_window_seconds,
    ):
        raise HTTPException(
            status_code=429,
            detail="too many login attempts; try again later",
            headers={"Retry-After": str(settings.login_window_seconds)},
        )
    username = resolve_username(settings, request.username, request.password)
    if username is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    login_attempt_limiter.reset(attempt_key)
    token, expires_at = issue_token(settings, username=username)
    return LoginResponse(access_token=token, username=username, expires_at=expires_at)


@app.get("/auth/me")
def current_user(username: str = Depends(require_session)) -> dict[str, str]:
    return {"username": username}


@app.post("/drafts", response_model=DraftResponse)
def create_drafts(
    request: DraftRequest,
    username: str = Depends(require_session),
) -> DraftResponse:
    """Generate editable drafts through the configured provider.

    The API owns provider credentials. The browser receives only reviewable
    draft data and never receives the configured API key.
    """

    try:
        generator = build_text_generator()
    except LlmConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    try:
        approach_override = (
            approach_for_formula(request.formula, request.brief)
            if request.formula
            else None
        )
        if request.rag_enabled:
            if not request.business_id:
                raise HTTPException(
                    status_code=422,
                    detail="business_id is required when rag_enabled=true",
                )
            rag_brand_id = request.brand_id or request.business_id
            if request.top_k <= 0:
                raise HTTPException(status_code=422, detail="top_k must be positive")
            try:
                index = LocalChromaIndex(RagLocalSettings())
                drafts = RagGroundedDraftService(index, generator).draft(
                    request.brief,
                    business_id=request.business_id,
                    brand_id=rag_brand_id,
                    top_k=request.top_k,
                    approach_override=approach_override,
                )
            except DraftOutputError:
                raise
            except (ValueError, RuntimeError) as error:
                raise HTTPException(status_code=503, detail=str(error)) from error
        else:
            drafts = ChannelAdaptedDraftService(generator).draft(
                request.brief, approach_override=approach_override
            )
    except LlmConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except DraftOutputError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    from apps.api.config import LlmSettings

    llm_settings = LlmSettings.from_environment()
    provider = llm_settings.provider
    model = ("deterministic-mock" if provider == "mock" else llm_settings.ollama_model if provider == "ollama" else llm_settings.groq_model)
    content_ids: list[str] = []
    for draft in drafts:
        content_id = editorial_store.create_id()
        content = EditorialReviewService.from_generated_draft(
            draft,
            content_id=content_id,
            owner_username=username,
            brand_id=request.brand_id,
            business_id=request.business_id,
        )
        editorial_store.create(EditorialReviewService.submit_for_review(content))
        content_ids.append(content_id)
    return DraftResponse(
        drafts=drafts,
        content_ids=content_ids,
        content_id=content_ids[0] if len(content_ids) == 1 else None,
        provider=provider,
        model=model,
    )


def _get_editorial_content(content_id: str, username: str) -> EditorialContent:
    """Resolve content owned by the authenticated user.

    Records created before ownership was introduced remain readable as legacy
    local data. New records always receive the authenticated owner.
    """
    content = editorial_store.get(content_id, owner_username=username)
    if content is None:
        raise HTTPException(status_code=404, detail="content_id not found")
    return content


@app.get("/drafts/{content_id}", response_model=EditorialContent)
def get_draft(content_id: str, username: str = Depends(require_session)) -> EditorialContent:
    return _get_editorial_content(content_id, username)


@app.get("/drafts/{content_id}/review", response_model=ReviewStatusResponse)
def get_review_status(
    content_id: str, username: str = Depends(require_session)
) -> ReviewStatusResponse:
    content = _get_editorial_content(content_id, username)
    return ReviewStatusResponse(
        content_id=content.content_id,
        state=content.state,
        review=content.review,
    )


@app.post("/drafts/{content_id}/review", response_model=EditorialContent)
def record_review(
    content_id: str,
    request: ReviewRequest,
    username: str = Depends(require_session),
) -> EditorialContent:
    content = _get_editorial_content(content_id, username)
    if not request.reviewer_ref.strip():
        raise HTTPException(status_code=422, detail="reviewer_ref must contain text")
    try:
        if request.decision == "approve":
            updated = EditorialReviewService.approve(
                content, reviewer_ref=request.reviewer_ref
            )
        else:
            if request.feedback is None or not request.feedback.strip():
                raise HTTPException(
                    status_code=422,
                    detail="feedback must contain text when requesting regeneration",
                )
            updated = EditorialReviewService.record_feedback(
                content,
                feedback=request.feedback,
                reviewer_ref=request.reviewer_ref,
            )
    except EditorialTransitionError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return editorial_store.save(updated)


@app.post(
    "/drafts/{content_id}/regenerate",
    response_model=EditorialContent,
)
def regenerate_draft(
    content_id: str,
    request: RegenerateRequest,
    username: str = Depends(require_session),
) -> EditorialContent:
    """Regenerate from the exact recorded feedback without approving the result."""

    content = _get_editorial_content(content_id, username)
    if not request.feedback.strip():
        raise HTTPException(status_code=422, detail="feedback must contain text")
    if request.top_k <= 0:
        raise HTTPException(status_code=422, detail="top_k must be positive")
    brief = request.brief.model_copy(update={"platforms": [content.draft.channel]})
    approach = (
        approach_for_formula(request.formula, brief)
        if request.formula
        else select_copy_approach(brief)
    )

    try:
        generator = build_text_generator()
    except LlmConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    def draft_factory(
        source: EditorialContent, _regeneration: RegenerationRequest
    ) -> EditableTextDraft:
        if request.rag_enabled:
            if not source.business_id:
                raise ValueError("business_id is required when rag_enabled=true")
            index = LocalChromaIndex(RagLocalSettings())
            return RagGroundedDraftService(index, generator).draft(
                brief,
                business_id=source.business_id,
                brand_id=source.brand_id or source.business_id,
                top_k=request.top_k,
                approach_override=approach,
                reviewer_feedback=request.feedback,
            )[0]
        return ChannelAdaptedDraftService(generator).draft(
            brief,
            approach_override=approach,
            reviewer_feedback=request.feedback,
        )[0]

    try:
        regenerated = EditorialReviewService.regenerate(
            content,
            RegenerationRequest(trigger="human_feedback", feedback=request.feedback),
            draft_factory=draft_factory,
        )
    except EditorialTransitionError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except DraftOutputError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except (LlmConfigurationError, RuntimeError, ValueError) as error:
        raise HTTPException(
            status_code=503,
            detail=f"No se pudo completar la generación: {error}",
        ) from error
    return editorial_store.create(regenerated)


@app.patch("/drafts/{content_id}", response_model=EditorialContent)
def edit_draft(
    content_id: str,
    request: ManualEditRequest,
    username: str = Depends(require_session),
) -> EditorialContent:
    content = _get_editorial_content(content_id, username)
    try:
        updated = EditorialReviewService.manual_edit(
            content, caption=request.caption, cta=request.cta
        )
    except EditorialTransitionError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return editorial_store.save(updated)


class StoredEditorialPlan(BaseModel):
    """Validated plan plus its stable local identifier."""

    plan_id: str
    plan: EditorialPlan


class PlanItemDayRequest(BaseModel):
    day: date


@app.post("/plans", response_model=StoredEditorialPlan)
def save_plan(
    plan: EditorialPlan,
    username: str = Depends(require_session),
) -> StoredEditorialPlan:
    """Persist an already validated plan for later calendar rendering."""

    owned_plan = plan.model_copy(update={"owner_username": username})
    plan_id = editorial_plan_store.create_id()
    editorial_plan_store.save(plan_id, owned_plan)
    return StoredEditorialPlan(plan_id=plan_id, plan=owned_plan)


@app.get("/plans/{plan_id}", response_model=StoredEditorialPlan)
def get_plan(plan_id: str, username: str = Depends(require_session)) -> StoredEditorialPlan:
    plan = editorial_plan_store.get(plan_id, owner_username=username)
    if plan is None:
        raise HTTPException(status_code=404, detail="plan_id not found")
    return StoredEditorialPlan(plan_id=plan_id, plan=plan)


@app.get("/plans", response_model=list[StoredEditorialPlan])
def list_plans(username: str = Depends(require_session)) -> list[StoredEditorialPlan]:
    return [
        StoredEditorialPlan(plan_id=plan_id, plan=plan)
        for plan_id, plan in editorial_plan_store.list(owner_username=username)
    ]


@app.patch(
    "/plans/{plan_id}/items/{item_index}/day",
    response_model=StoredEditorialPlan,
)
def update_plan_item_day(
    plan_id: str,
    request: PlanItemDayRequest,
    item_index: int = Path(ge=0),
    username: str = Depends(require_session),
) -> StoredEditorialPlan:
    plan = editorial_plan_store.get(plan_id, owner_username=username)
    if plan is None:
        raise HTTPException(status_code=404, detail="plan_id not found")
    try:
        updated = reschedule_item(plan, item_index, request.day)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    editorial_plan_store.save(plan_id, updated)
    return StoredEditorialPlan(plan_id=plan_id, plan=updated)
