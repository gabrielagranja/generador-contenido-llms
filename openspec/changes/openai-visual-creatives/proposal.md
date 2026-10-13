# Proposal

## Status and human approval

- Status: Approved
- Issue: #124 — Implementar creatividades visuales con OpenAI Images
- Human approval: explicit task approval in the project conversation on 2026-10-13.

## Plan objective

Deliver a demonstrable local visual-creative flow today without expanding into publishing, export or media campaigns.

## Objective

Add review-only visual creative generation while keeping Ollama as the editorial-copy provider. Images are generated server-side through a configurable GPT Image model and remain local until a human approves them in the prototype.

## Scope

- `POST /creatives`, regeneration, discard, prototype approval and authenticated local image retrieval.
- A canonical Meta format catalogue derived from the existing UI aspect-ratio contract; provider canvases are cropped/resized to final dimensions.
- Brand-isolated RAG provenance, with WAYDDH's corporate PDF and Talent Hive's documented team-building context.
- Content Studio controls for generation, preview and review actions.

## Exclusions

Publishing, exporting, automatic approval, browser-visible OpenAI credentials, DALL·E 3, generated video and automatic factual/visual invention.

## Acceptance criteria

- API keys remain backend-only and absence of `OPENAI_API_KEY` is actionable.
- A created image is `pending-review`, records the model/prompt/provenance and uses exact final format dimensions.
- Retrieval is filtered by `brand_id`; no cross-brand context is added to the prompt.
- OpenAI/provider failures are surfaced as specific API/UI errors without credentials.

## Rubric

No aplica — this is an approved MVP extension of the existing Content Studio review workflow, not a new evaluation rubric.

## Tests and verification

Use fake image providers and isolated temporary storage for backend tests. Run the full Python suite, frontend tests/typecheck/build, Git conventions, SDD validation, OpenSpec validation and `git diff --check` before requesting review.

## Open questions and blockers

The selected account must have access to the configured GPT Image model. The implementation reports a provider error rather than choosing a different model or falling back to a synthetic asset.

## Approval

Approved by the explicit implementation request for Issue #124 on 2026-10-13.
