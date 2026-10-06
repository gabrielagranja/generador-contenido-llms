"""Pydantic models for the approved guided brief contract."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


FactStatus = Literal["CONFIRMED", "INFERRED", "UNKNOWN"]
Platform = Literal["instagram", "facebook"]
BriefFormat = Literal["single_image", "carousel", "reel"]


class BriefFact(BaseModel):
    """A material fact or audience hypothesis with visible provenance."""

    statement: str = Field(min_length=1)
    status: FactStatus
    source: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    scope: Literal["business", "audience", "offer", "campaign", "post"]
    validation_needed: bool


class GuidedBrief(BaseModel):
    """Structured input for the guided brief-to-content workflow."""

    topic_or_offer: str | None = Field(default=None, min_length=1)
    objective: str | None = Field(default=None, min_length=1)
    audience_context: str | None = Field(default=None, min_length=1)
    business_context_refs: list[str] = Field(default_factory=list)
    platforms: list[Platform] = Field(min_length=1)
    format: BriefFormat
    brand_and_constraints: str | None = Field(default=None, min_length=1)
    facts: list[BriefFact] = Field(default_factory=list)

    @field_validator("platforms")
    @classmethod
    def platforms_must_be_unique(cls, value: list[Platform]) -> list[Platform]:
        if len(value) != len(set(value)):
            raise ValueError("platforms must not contain duplicates")
        return value

