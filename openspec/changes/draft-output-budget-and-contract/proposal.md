# Proposal

## Status and human approval

- Status: Approved
- Issue: #99 — Add configurable draft output-token budget and contract
- Decision record: Human approval received in the task conversation on 2026-10-10.

## Plan objective

Reduce draft-generation token consumption and cost by introducing a configurable provider-level output-token budget while preserving the existing RAG, review, channel-isolation, and provider-selection contracts.

## Objective

The current draft pipeline does not configure a maximum output-token limit. This change proposes an initial default of 350 output tokens and an absolute maximum of 600 so that provider requests have an explicit, testable output budget.

These values are proposals and require validation with representative Instagram and Facebook drafts before being treated as production settings.

## Scope

### Included

- Add configuration for a default maximum output-token budget of 350.
- Enforce an absolute maximum of 600.
- Pass the validated budget to the Groq model adapter.
- Preserve the current temperature of 0.2, default model, and mock/Groq provider selection.
- Add concise, channel-aware generation contracts for Instagram and Facebook.
- Preserve factual grounding, source attribution, Spanish default output, configured Catalan support, human review metadata, and editorial state transitions.
- Validate configuration and provider-adapter behavior with mock or fake providers only.

### Excluded

- RAG retrieval, chunking, grounding, or source metadata changes.
- Changes to human approval or editorial state transitions.
- Client-side truncation after generation.
- Provider calls from tests.
- Changes to the default model, temperature, provider selection, or UI copy.

## Acceptance criteria

- The default output-token budget is applied when no override is configured.
- Valid configured values are accepted up to 600.
- Invalid, non-positive, or over-600 values are rejected safely.
- The Groq adapter receives the validated maximum output-token value.
- Mock generation remains deterministic.
- Instagram and Facebook retain distinct output contracts.
- RAG grounding and review metadata are unchanged.
- The existing Python, SDD, diff, web, and applicable OpenSpec validations pass.

## Rubric

No aplica — this is a low-cost implementation refinement to an already defined drafting and review capability, not a new rubric capability.

## Tests and verification

- Automated: `python -m pytest -q` with focused configuration, adapter, channel-contract, grounding, and review tests.
- Automated: `python scripts/validate_sdd_contract.py` and applicable OpenSpec validation.
- Automated: `git diff --check`.
- Web verification: `npm run typecheck`, `npm test`, and `npm run build` in `apps/web`.
- External data: no Groq calls; use mock or fake providers exclusively.
- Manual/evidence: record representative output-budget observations and unresolved production-setting questions after approval.

## Open questions and blockers

- Are 350 default tokens and 600 absolute tokens appropriate for representative Instagram and Facebook drafts?
- Does the configured Groq model interpret the output limit consistently across channels?
- Should the budgets be adjusted after offline representative evaluation?
- Human approval is required before implementation.

## Approval

Approved. Human approval: Approved in the task conversation on 2026-10-10. Implementation may proceed within the approved scope.
