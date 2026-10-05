# Roadmap

Authority: canonical plan-level sequence. GitHub Project #1 remains the operational board for status and ordering.
Bootstrap issue: #37.
Status: baseline. The official rubric is transcribed in docs/rubric-traceability.md and is the assessment source of truth.

## Phase 1 — Discovery and product direction

Issues #1–#6: brief, workflow, business research, alternatives, support programmes, and discovery gate.

## Phase 2 — Product definition and UX

Issues #7–#8 and #14–#19: scope, traceability, workflow, wireframes, prototype and UX testing.

## Phase 3 — Application foundation

Issues #9 and #20–#21: stack, runnable web/API foundation, environment handling and setup. Issue #21 task 1 is verified: the minimal FastAPI/Pydantic API scaffold and deterministic `/readiness` endpoint run without provider credentials. Task 2 is also verified: the minimal Next.js/React/TypeScript client builds successfully and reads the local readiness endpoint with explicit ready/unavailable states. Task 3 is verified: safe local environment examples and ignored secret files are in place without provider credentials.

## Phase 4 — Content-generation slice

Issues #10 and #22–#24: structured brief, channel-adapted generation, review, editing and regeneration.

## Phase 5 — C4 implementation and product enhancements

Implement the three required C4 indicators through Issues #20, #21, #23, #25 and #32: LLM model, LLM application framework and RAG architecture. Manage image support, two-model comparison and Docker as product decisions in Issues #31, #33 and #34.

## Phase 6 — Quality, delivery and portfolio

Issues #12–#13 and #25–#29, #35–#36: evaluation, documentation, demo, presentation, portfolio narrative and readiness. Validate every C1–C4 indicator against docs/rubric-traceability.md.

## Cross-cutting SDD harness

Issue #37 establishes the source-of-truth structure. A dedicated OpenSpec harness change must be approved before implementing validators or CI.

## Pending synchronization

- Import Project #1 phases, ordering and status.
- Record the instructor's answer about the expected evidence depth for RAG in a solo project.
- Resolve product decisions in Issues #31, #33 and #34.
