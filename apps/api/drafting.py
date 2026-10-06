"""Channel-adapted editable text drafting service."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field

from apps.api.llm import TextGenerator
from apps.api.models import GuidedBrief, Platform


@dataclass(frozen=True)
class TextTemplate:
    template_id: str
    version: str
    channel: Platform
    instructions: str


TEMPLATES: dict[Platform, TextTemplate] = {
    "instagram": TextTemplate(
        template_id="social.instagram.text-draft",
        version="1.0.0",
        channel="instagram",
        instructions=(
            "Use a concise hook, scannable caption, direct credible CTA and "
            "functional keywords only when grounded."
        ),
    ),
    "facebook": TextTemplate(
        template_id="social.facebook.text-draft",
        version="1.0.0",
        channel="facebook",
        instructions=(
            "Use a conversational opening, enough context for the feed, a "
            "readable structure and a direct credible CTA."
        ),
    ),
}


class EditableTextDraft(BaseModel):
    """Reviewable text output for one selected channel."""

    template_id: str
    template_version: str
    channel: Platform
    format: str
    caption: str = Field(min_length=1)
    cta: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    review_notes: list[str] = Field(default_factory=list)


class ChannelAdaptedDraftService:
    """Select a versioned channel template and request one editable draft."""

    def __init__(self, generator: TextGenerator) -> None:
        self._generator = generator

    def draft(self, brief: GuidedBrief) -> list[EditableTextDraft]:
        """Return one grounded, editable text draft for every selected channel."""

        return [self._draft_for_channel(brief, channel) for channel in brief.platforms]

    def _draft_for_channel(
        self, brief: GuidedBrief, channel: Platform
    ) -> EditableTextDraft:
        template = TEMPLATES[channel]
        prompt = self._build_prompt(brief, template)
        generated_text = self._generator.generate(prompt).strip()
        if not generated_text:
            raise ValueError("text generator returned an empty draft")

        evidence_refs = [fact.statement for fact in brief.facts if fact.status == "CONFIRMED"]
        assumptions = [
            fact.statement
            for fact in brief.facts
            if fact.status in {"INFERRED", "UNKNOWN"}
        ]
        review_notes = [
            "Review all inferred or unknown facts before approval.",
            "This draft is not a publication request.",
        ]

        return EditableTextDraft(
            template_id=template.template_id,
            template_version=template.version,
            channel=channel,
            format=brief.format,
            caption=generated_text,
            evidence_refs=evidence_refs,
            assumptions=assumptions,
            review_notes=review_notes,
        )

    @staticmethod
    def _build_prompt(brief: GuidedBrief, template: TextTemplate) -> str:
        facts = "\n".join(
            f"- [{fact.status}] {fact.statement} (source: {fact.source}; "
            f"scope: {fact.scope})"
            for fact in brief.facts
        ) or "- No business facts supplied."

        return (
            f"Template: {template.template_id} v{template.version}\n"
            f"Channel: {template.channel}\n"
            f"Format: {brief.format}\n"
            f"Topic or offer: {brief.topic_or_offer or 'UNKNOWN'}\n"
            f"Objective: {brief.objective or 'UNKNOWN'}\n"
            f"Audience context: {brief.audience_context or 'UNKNOWN'}\n"
            f"Brand and constraints: {brief.brand_and_constraints or 'UNKNOWN'}\n"
            f"Channel instructions: {template.instructions}\n"
            "Facts and evidence status:\n"
            f"{facts}\n"
            "Return only editable draft text. Never invent business facts, "
            "benefits, proof, deadlines, scarcity, credentials or guarantees. "
            "Keep inferred and unknown information out of factual claims. "
            "Do not render media, publish, schedule or request credentials."
        )


__all__ = ["ChannelAdaptedDraftService", "EditableTextDraft", "TEMPLATES"]
