# Proposal

## Status and human approval

- Status: Approved
- Issue: #24.4 — Backend human-review transport contract
- Decision record: User instruction for microiteration 20.5.1.

## Plan objective

Expose the approved editorial lifecycle through the smallest FastAPI transport
boundary needed by the Content Studio and local review tooling.

## Objective

Give every generated draft a stable identifier, preserve its business and RAG
metadata, and make human review explicit without adding publishing or auth.

## Scope

### Included

- Process-local creation and retrieval by `content_id`.
- Explicit review decisions, feedback and manual edits.
- Preservation of brand, business, provenance and grounding metadata.
- Actionable HTTP errors for missing records and invalid transitions.

### Excluded

- Durable database persistence, authentication, publishing, scheduling,
  regeneration provider calls and Chroma editorial state.

## Acceptance criteria

- Every POST `/drafts` result enters `pending_human_review` and receives a stable ID.
- GET and review endpoints preserve the current draft, business scope and RAG metadata.
- Approval requires a non-empty declared reviewer reference; edits and feedback never approve.
- Records are isolated by ID and no content is silently retrieved from another business.

## Rubric

No aplica — this is a focused backend contract iteration covered by the existing editorial-control rubric.

## Tests and verification

- Automated: focused FastAPI tests with controlled generators and no Groq calls.
- Contract: `scripts/validate_sdd_contract.py` and focused pytest.
- Manual/evidence: inspect response state, reviewer record and RAG provenance.
- External data: none; provider and Chroma are not invoked by review tests.

## Open questions and blockers

- Persistence across a Uvicorn restart remains intentionally open; the current store is process-local until a durable storage decision is approved.

## Approval

Approved by the explicit implementation request for microiteration 20.5.1.
