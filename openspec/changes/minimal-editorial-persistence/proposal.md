# Proposal

## Status and human approval

- Status: Pending
- Issue: #104 — Persist MVP editorial drafts and plans locally
- Human approval: pending review of this contract.

## Plan objective

Make the existing reviewable editorial flow survive an API restart so the final MVP can demonstrate a real draft-to-review lifecycle and dated plan without expanding product scope.

## Objective

Replace the current process-local storage boundary with a minimal SQLite-backed repository for editorial content and editorial plans, reusing existing Pydantic models, review transitions and content-mix planning.

## Scope

Included: one local SQLite database configured through an API-side path; persisted EditorialContent records and EditorialPlan records; create/get/save/list operations needed by existing draft/review endpoints and a minimal plans API; deterministic serialization of review state, metadata, RAG provenance and dated plan items; startup-safe schema creation; fake temporary-database tests and local setup documentation.

Excluded: authentication, multi-tenant authorization, migrations framework, publishing/scheduling, remote database, background jobs, calendar UI changes, new editorial states, RAG retrieval changes and external database connections.

## Acceptance criteria

- A generated draft, manual edit and approved/review state can be retrieved after a fresh store instance opens the same database.
- Existing transition rules, reviewer requirements, provenance and grounding data are unchanged.
- A plan made from existing editorial-planning models persists with its strategy version, targets and dated items.
- API defaults are safe for local development and tests can use isolated temporary databases.
- Existing mock/Groq/Ollama behavior and provider secrets remain outside persistence.
- Python, SDD, OpenSpec, Git Conventions, diff and applicable frontend checks pass.

## Rubric

No aplica — durability for the existing MVP workflow, not a new rubric capability.

## Tests and verification

Use temporary SQLite files and synthetic data. Run focused persistence/API tests plus the configured validators and frontend checks. No external LLM, database or publishing calls.

## Open questions and blockers

The final deployment storage path is not selected; the MVP uses a configurable local file only. Human approval is pending.

## Approval

Pending. Implementation starts after explicit human approval of this contract.
