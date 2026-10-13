"""Review-only visual creative generation behind the OpenAI Images API."""

from __future__ import annotations

import base64
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Protocol

import httpx
from PIL import Image, ImageOps
from pydantic import BaseModel, Field

from apps.api.config import CreativeStorageSettings, OpenAiImageSettings
from apps.api.creative_formats import MetaCreativeFormat
from apps.api.rag import RetrievedBusinessContext


class CreativeGenerationError(RuntimeError):
    """A controlled failure that is safe to return to the API client."""


class ImageGenerator(Protocol):
    model: str

    def generate(self, *, prompt: str, size: str) -> bytes: ...


class OpenAiImageGenerator:
    """Minimal HTTP adapter; its credential never leaves this backend object."""

    def __init__(self, settings: OpenAiImageSettings, client: Any | None = None) -> None:
        settings.validate()
        self._settings = settings
        self.model = settings.model
        self._client = client or httpx.Client(timeout=settings.timeout_seconds)

    def generate(self, *, prompt: str, size: str) -> bytes:
        try:
            response = self._client.post(
                "https://api.openai.com/v1/images/generations",
                headers={
                    "Authorization": f"Bearer {self._settings.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "size": size,
                    "n": 1,
                    "response_format": "b64_json",
                    "output_format": "png",
                },
            )
            response.raise_for_status()
            payload = response.json()
            encoded = payload.get("data", [{}])[0].get("b64_json")
            if not isinstance(encoded, str) or not encoded:
                raise ValueError("OpenAI did not return image data")
            return base64.b64decode(encoded, validate=True)
        except (httpx.TimeoutException, httpx.NetworkError) as error:
            raise CreativeGenerationError("OpenAI image generation timed out or is unavailable") from error
        except httpx.HTTPStatusError as error:
            raise CreativeGenerationError(
                f"OpenAI image generation failed with HTTP {error.response.status_code}"
            ) from error
        except (ValueError, KeyError, TypeError) as error:
            raise CreativeGenerationError("OpenAI returned an invalid image response") from error


class CreativeProvenance(BaseModel):
    business_id: str
    brand_id: str | None = None
    source_name: str | None = None
    source_url: str | None = None
    source_type: str | None = None
    language: str | None = None
    retrieved_at: str | None = None


class CreativeRecord(BaseModel):
    id: str
    brand_id: str
    brief: str
    copy_text: str = Field(serialization_alias="copy")
    style: str
    platform: str
    placement: str
    format: str
    width: int
    height: int
    aspect_ratio: str
    prompt: str
    model: str
    generated_at: datetime
    review_state: Literal["pending-review", "approved-prototype", "discarded"] = "pending-review"
    provenance: list[CreativeProvenance] = Field(default_factory=list)
    image_filename: str
    source_creative_id: str | None = None
    owner_username: str | None = None


def provenance_from_context(context: RetrievedBusinessContext) -> CreativeProvenance:
    return CreativeProvenance(
        business_id=context.business_id,
        brand_id=context.brand_id,
        source_name=context.source_name,
        source_url=context.source_url or context.source_uri,
        source_type=context.source_type,
        language=context.language,
        retrieved_at=context.retrieved_at,
    )


BRAND_VISUAL_PROFILES: dict[str, dict[str, str]] = {
    "talent-hive": {
        "name": "Talent Hive",
        "palette": "blue #2453d4, deep navy #0f1f4d, soft blue #dfe7fb",
        "tone": "professional, energetic and collaborative",
        "restriction": "Show only an abstract team-building, escape-box or gamified-workshop scene grounded in the evidence. Do not claim guaranteed outcomes.",
    },
    "wayddh": {
        "name": "WAYDDH",
        "palette": "teal #1f7a70, dark teal #123d3a, pale teal #ddf1ee",
        "tone": "clear, contemporary and business-focused",
        "restriction": "Use only services or concepts present in the retrieved corporate-PDF evidence. Do not invent clients, metrics, awards or services.",
    },
    "coll-amunt": {
        "name": "Coll Amunt!",
        "palette": "blue #176b9a, deep blue #12354b, pale blue #dceef7",
        "tone": "local, welcoming and community-oriented",
        "restriction": "Use only the selected brand evidence; do not introduce unverified venues, promotions or logos.",
    },
}


def build_visual_prompt(
    *,
    brand_id: str,
    brief: str,
    copy: str,
    style: str,
    creative_format: MetaCreativeFormat,
    contexts: list[RetrievedBusinessContext],
) -> str:
    profile = BRAND_VISUAL_PROFILES.get(brand_id)
    if profile is None:
        raise ValueError(f"Unknown brand_id '{brand_id}'")
    evidence = "\n".join(f"- {item.text}" for item in contexts) or "- No retrieved brand evidence. Keep the visual generic and avoid factual or branded claims."
    return "\n".join(
        [
            "Create one editorial social-media visual, without publishing it.",
            f"Brand: {profile['name']} ({brand_id}).",
            f"Brand palette: {profile['palette']}. Tone: {profile['tone']}.",
            f"Requested style: {style.strip() or 'editorial'}.",
            f"Brief: {brief.strip()}.",
            f"Approved or provisional copy (use as visual direction only; do not render it as text): {copy.strip()}.",
            f"Final placement: {creative_format.platform}/{creative_format.placement}/{creative_format.format}, {creative_format.aspect_ratio}.",
            "Retrieved brand evidence (supporting context, not a visual asset or identity source):",
            evidence,
            f"Restriction: {profile['restriction']}",
            "Do not add logos, readable copy, claims, numerical results, named clients, proprietary visual assets or factual details absent from the evidence.",
        ]
    )


def normalize_image(image_bytes: bytes, target: MetaCreativeFormat) -> bytes:
    """Centre-crop the provider canvas and save the exact final Meta dimensions."""
    try:
        from io import BytesIO

        with Image.open(BytesIO(image_bytes)) as image:
            output = ImageOps.fit(
                image.convert("RGB"),
                (target.width, target.height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            buffer = BytesIO()
            output.save(buffer, format="PNG", optimize=True)
            return buffer.getvalue()
    except Exception as error:
        raise CreativeGenerationError("OpenAI returned an image that could not be normalized") from error


class CreativeService:
    def __init__(self, generator: ImageGenerator, storage: CreativeStorageSettings) -> None:
        self.generator = generator
        self.storage = storage
        self.storage.directory.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        *,
        creative_id: str,
        brand_id: str,
        brief: str,
        copy: str,
        style: str,
        target: MetaCreativeFormat,
        contexts: list[RetrievedBusinessContext],
        owner_username: str,
        source_creative_id: str | None = None,
    ) -> CreativeRecord:
        prompt = build_visual_prompt(
            brand_id=brand_id, brief=brief, copy=copy, style=style,
            creative_format=target, contexts=contexts,
        )
        normalized = normalize_image(self.generator.generate(prompt=prompt, size=target.provider_size), target)
        filename = f"{creative_id}.png"
        (self.storage.directory / filename).write_bytes(normalized)
        return CreativeRecord(
            id=creative_id, brand_id=brand_id, brief=brief, copy_text=copy, style=style,
            platform=target.platform, placement=target.placement, format=target.format,
            width=target.width, height=target.height, aspect_ratio=target.aspect_ratio,
            prompt=prompt, model=self.generator.model, generated_at=datetime.now(timezone.utc),
            provenance=[provenance_from_context(item) for item in contexts],
            image_filename=filename, source_creative_id=source_creative_id, owner_username=owner_username,
        )
