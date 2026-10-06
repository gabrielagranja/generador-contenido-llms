"""Explicit human review boundary for generated editorial content."""

from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, Field

from apps.api.drafting import EditableTextDraft


EditorialState = Literal[
    "generated_draft",
    "pending_human_review",
    "approved_final",
]
ReviewDecision = Literal["approve", "request_regeneration"]


class EditorialTransitionError(ValueError):
    """Raised when an editorial operation would violate the lifecycle."""


class HumanReview(BaseModel):
    """A human decision or feedback record for the current draft text."""

    decision: ReviewDecision
    feedback: str | None = Field(default=None, min_length=1)
    reviewer_ref: str | None = Field(default=None, min_length=1)
    reviewed_text_fingerprint: str = Field(min_length=1)


class EditorialContent(BaseModel):
    """Generated text plus its explicit editorial lifecycle state."""

    content_id: str = Field(min_length=1)
    state: EditorialState
    draft: EditableTextDraft
    review: HumanReview | None = None


class EditorialReviewService:
    """Apply only the Issue #24.1 review and manual-edit transitions."""

    @classmethod
    def from_generated_draft(
        cls, draft: EditableTextDraft, *, content_id: str
    ) -> EditorialContent:
        """Wrap provider output as a generated, not-yet-reviewed item."""

        return EditorialContent(
            content_id=content_id,
            state="generated_draft",
            draft=draft,
        )

    @classmethod
    def submit_for_review(cls, content: EditorialContent) -> EditorialContent:
        """Move a generated draft into the explicit human-review state."""

        cls._require_state(content, "generated_draft", "submit for review")
        return content.model_copy(update={"state": "pending_human_review"})

    @classmethod
    def record_feedback(
        cls,
        content: EditorialContent,
        *,
        feedback: str,
        reviewer_ref: str | None = None,
    ) -> EditorialContent:
        """Record human feedback without regenerating or approving content."""

        cls._require_state(content, "pending_human_review", "record feedback")
        if not feedback.strip():
            raise EditorialTransitionError("feedback must contain meaningful text")
        review = HumanReview(
            decision="request_regeneration",
            feedback=feedback,
            reviewer_ref=reviewer_ref,
            reviewed_text_fingerprint=cls.text_fingerprint(content),
        )
        return content.model_copy(update={"review": review})

    @classmethod
    def approve(
        cls, content: EditorialContent, *, reviewer_ref: str
    ) -> EditorialContent:
        """Approve exactly the current text through an explicit human action."""

        cls._require_state(content, "pending_human_review", "approve")
        if not reviewer_ref.strip():
            raise EditorialTransitionError("reviewer_ref is required for approval")
        review = HumanReview(
            decision="approve",
            reviewer_ref=reviewer_ref,
            reviewed_text_fingerprint=cls.text_fingerprint(content),
        )
        return content.model_copy(update={"state": "approved_final", "review": review})

    @classmethod
    def manual_edit(
        cls,
        content: EditorialContent,
        *,
        caption: str,
        cta: str | None = None,
    ) -> EditorialContent:
        """Edit pending text without changing it into an approved final."""

        cls._require_state(content, "pending_human_review", "manual edit")
        if not caption.strip():
            raise EditorialTransitionError("caption must contain meaningful text")
        edited_draft = content.draft.model_copy(update={"caption": caption, "cta": cta})
        return content.model_copy(
            update={"draft": edited_draft, "review": None, "state": "pending_human_review"}
        )

    @staticmethod
    def text_fingerprint(content: EditorialContent) -> str:
        """Return a stable fingerprint for the exact reviewable draft payload."""

        payload = content.draft.model_dump(mode="json")
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @staticmethod
    def _require_state(
        content: EditorialContent,
        expected: EditorialState,
        operation: str,
    ) -> None:
        if content.state != expected:
            raise EditorialTransitionError(
                f"cannot {operation} content in state {content.state!r}; "
                f"expected {expected!r}"
            )


__all__ = [
    "EditorialContent",
    "EditorialReviewService",
    "EditorialState",
    "EditorialTransitionError",
    "HumanReview",
]
