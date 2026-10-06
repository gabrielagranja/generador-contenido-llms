# Design

## Relationship to Issue #22

Issue #22 is the source of truth for `GuidedBrief`, the `CONFIRMED`/`INFERRED`/`UNKNOWN` fact model, the objective-to-CTA strategy chain, approved channels and approved formats. This change consumes those contracts and adds only channel-adapted textual drafting. It must not copy or redefine them.

## Minimal flow

1. Receive a validated `GuidedBrief` and its visible fact provenance.
2. Resolve one versioned template for each selected channel.
3. Pass the objective, audience situation, core message, platform, format, angle, CTA and grounded facts to the template.
4. Produce an editable text package with the template version, channel, caption, CTA, evidence references, assumptions and review notes.
5. Refuse or qualify unsupported claims; unresolved material uncertainty remains visible and does not become a factual assertion.

The flow creates text and creative-plan guidance only. It does not render media, call social APIs or alter the user interface.

## Template contract

Each template is immutable by version and records:

- `template_id` and semantic `version`;
- target channel (`instagram` or `facebook`);
- accepted input fields from `GuidedBrief`;
- channel-specific instructions;
- output sections and grounding safeguards;
- compatible approved formats (`single_image`, `carousel`, `reel`).

Versioning is explicit: a change to channel instructions or output structure creates a new version rather than silently changing an existing one. The selected version is included in every draft for review and reproducibility.

## Channel adaptation

- Instagram: concise hook, scannable caption, direct CTA, optional functional keywords/hashtags, and format-specific text/creative-plan guidance.
- Facebook: conversational but clear opening, context sufficient for the feed, direct CTA and format-specific text/creative-plan guidance.
- Both channels: preserve the same grounded core message and evidence boundary; do not duplicate text blindly or introduce new facts.

The channel guidance is heuristic, not a performance guarantee. Any format-specific visual details remain provisional unless already confirmed by the Issue #22 contract.

## Output boundary

The output is an editable text draft package. It may include caption copy, CTA, a single-image overlay suggestion, carousel slide copy outline, or Reel scene/script/subtitle text plan. It must not include rendered assets, publication instructions, access tokens or automatic publishing actions.

## Test strategy

Use only F-01, F-02 and F-03 from Issue #22. Assert the selected template/version, channel adaptation, fact-status visibility, omission or qualification of unsupported claims, and preservation of editable sections. For unknown or ambiguous briefs, tests must accept a bounded question/review response rather than requiring a fabricated draft.
