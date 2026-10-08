"""Deterministic, evidence-preserving editorial content-mix planning (#70).

Planning only: this module never generates, approves, schedules or publishes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from apps.api.editorial_review import EditorialContent
from apps.api.models import GuidedBrief

Platform = Literal["instagram", "facebook"]
Format = Literal["single_image", "carousel", "reel"]


@dataclass(frozen=True)
class StrategyBucket:
    key: str
    label: str
    percentage: int

    def __post_init__(self) -> None:
        if not self.key or not self.key.strip() or not self.label or not self.label.strip():
            raise ValueError("bucket key and label cannot be empty")
        if type(self.percentage) is not int or not 0 <= self.percentage <= 100:
            raise ValueError("bucket percentages must be integers between 0 and 100")


@dataclass(frozen=True)
class ContentMixStrategy:
    strategy_id: str
    version: str
    buckets: tuple[StrategyBucket, ...]

    def __post_init__(self) -> None:
        if not self.strategy_id or not self.strategy_id.strip():
            raise ValueError("strategy_id cannot be empty")
        if not self.version or not self.version.strip():
            raise ValueError("version cannot be empty")
        if not self.buckets:
            raise ValueError("at least one bucket is required")
        keys = [bucket.key for bucket in self.buckets]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate bucket keys")
        if sum(bucket.percentage for bucket in self.buckets) != 100:
            raise ValueError("bucket percentages must sum to 100")

    def with_version(self, version: str, *, buckets: tuple[StrategyBucket, ...]) -> "ContentMixStrategy":
        """Return a new immutable strategy version; leave the old version untouched."""
        if version == self.version:
            raise ValueError("changed strategy requires a new version")
        return ContentMixStrategy(self.strategy_id, version, buckets)


EIGHTY_TWENTY = ContentMixStrategy(
    "eighty_twenty", "1.0.0",
    (StrategyBucket("VALUE", "Value and community", 80),
     StrategyBucket("PROMOTIONAL", "Promotion", 20)),
)
THREE_THIRDS = ContentMixStrategy(
    "three_thirds", "1.0.0",
    (StrategyBucket("EDUCATIONAL", "Educational and informative", 34),
     StrategyBucket("COMMUNITY", "Interaction and community", 33),
     StrategyBucket("PROMOTIONAL", "Promotion and brand", 33)),
)
PRESETS = {"eighty_twenty": EIGHTY_TWENTY, "three_thirds": THREE_THIRDS}


def allocate_slots(strategy: ContentMixStrategy, total: int) -> dict[str, int]:
    """Hamilton/largest remainder, with stable declared-bucket order for ties."""
    if type(total) is not int or total <= 0:
        raise ValueError("cycle size must be a positive integer")
    quotas = [total * b.percentage for b in strategy.buckets]
    counts = [quota // 100 for quota in quotas]
    remainder = total - sum(counts)
    order = sorted(range(len(quotas)), key=lambda i: (-(quotas[i] % 100), i))
    for i in order[:remainder]:
        counts[i] += 1
    return {bucket.key: count for bucket, count in zip(strategy.buckets, counts)}


class PlannedItem(BaseModel):
    """Immutable snapshot of source metadata, not an edited source document."""

    model_config = ConfigDict(frozen=True)

    source_ref: str = Field(min_length=1)
    source_kind: Literal["guided_brief", "editorial_content"]
    strategy_version: str = Field(min_length=1)
    bucket_key: str = Field(min_length=1)
    platform: Platform
    format: Format
    review_state: str | None = None
    evidence: dict[str, object] = Field(default_factory=dict)


class EditorialPlan(BaseModel):
    model_config = ConfigDict(frozen=True)

    strategy_id: str
    strategy_version: str
    total_slots: int = Field(gt=0)
    starts_on: date
    ends_on: date
    targets: dict[str, int]
    items: tuple[PlannedItem, ...] = ()

    @model_validator(mode="after")
    def validate_dates(self) -> "EditorialPlan":
        if self.ends_on < self.starts_on:
            raise ValueError("ends_on must not precede starts_on")
        return self

    def summary(self) -> dict[str, dict[str, int]]:
        actual = {key: 0 for key in self.targets}
        for item in self.items:
            actual[item.bucket_key] += 1
        return {
            key: {"target": target, "actual": actual[key],
                  "difference": actual[key] - target}
            for key, target in self.targets.items()
        }


def create_plan(strategy: ContentMixStrategy, total: int, *, starts_on: date,
                ends_on: date) -> EditorialPlan:
    return EditorialPlan(
        strategy_id=strategy.strategy_id, strategy_version=strategy.version,
        total_slots=total, starts_on=starts_on, ends_on=ends_on,
        targets=allocate_slots(strategy, total),
    )


def assign_item(plan: EditorialPlan, strategy: ContentMixStrategy, *,
                source: GuidedBrief | EditorialContent, source_ref: str,
                bucket_key: str, platform: str, format: str) -> EditorialPlan:
    """Attach source snapshot without mutating approval or evidence.

    This intentionally does not expose publication/approval actions.
    """
    if (plan.strategy_id, plan.strategy_version) != (strategy.strategy_id, strategy.version):
        raise ValueError("plan strategy version mismatch")
    if bucket_key not in plan.targets:
        raise ValueError("unknown bucket key")
    if platform not in ("instagram", "facebook") or format not in (
        "single_image", "carousel", "reel"
    ):
        raise ValueError("unsupported MVP platform or format")
    if not source_ref or not source_ref.strip():
        raise ValueError("source_ref is required")
    if len(plan.items) >= plan.total_slots:
        raise ValueError("plan cannot exceed its cycle size")

    if isinstance(source, EditorialContent):
        if platform != source.draft.channel or format != source.draft.format:
            raise ValueError("platform or format must match source draft")
        evidence = {
            "evidence_refs": source.draft.evidence_refs,
            "evidence_provenance": source.draft.evidence_provenance,
            "assumptions": source.draft.assumptions,
            "unsupported_claims": source.draft.unsupported_claims,
            "review_notes": source.draft.review_notes,
            "lineage": source.lineage.model_dump(mode="json") if source.lineage else None,
        }
        state = source.state
        kind = "editorial_content"
    elif isinstance(source, GuidedBrief):
        if platform not in source.platforms or format != source.format:
            raise ValueError("platform or format must match GuidedBrief")
        evidence = {"facts": [fact.model_dump(mode="json") for fact in source.facts],
                    "business_context_refs": list(source.business_context_refs)}
        state = None
        kind = "guided_brief"
    else:
        raise TypeError("source must be GuidedBrief or EditorialContent")

    item = PlannedItem(
        source_ref=source_ref, source_kind=kind, strategy_version=strategy.version,
        bucket_key=bucket_key, platform=platform, format=format,
        review_state=state, evidence=evidence,
    )
    return plan.model_copy(update={"items": (*plan.items, item)})


__all__ = [
    "StrategyBucket", "ContentMixStrategy", "EIGHTY_TWENTY", "THREE_THIRDS",
    "PRESETS", "allocate_slots", "PlannedItem", "EditorialPlan", "create_plan",
    "assign_item",
]
