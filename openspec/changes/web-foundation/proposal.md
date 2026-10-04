# Create Runnable Web Application Foundation

## Status and human approval

- Status: Approved
- Issue: #21 — [STORY] Create a runnable web application foundation
- Parent epic: #9 — [EPIC] LLM application foundation
- Plan phase: Phase 3 — Application foundation
- Branch: `feat/21-web-foundation`
- Human approval: Approved on 2026-10-04 in the project conversation after confirming the exact first-stage channel scope and local-development decisions.
- Approved decisions: npm is the JavaScript package manager; local development uses two documented terminals (FastAPI and Next.js).

## Plan objective

Deliver the reproducible technical base required by the Phase 3 roadmap so the MVP can be developed and run locally by Codex, Claude and other agents.

## Objective

Create a documented, runnable full-stack foundation aligned with the provisionally approved technology-stack decision: Next.js/React/TypeScript for the web client, Python 3.11+/FastAPI/Pydantic for the API, LangChain as the provider-neutral LLM integration point, and pytest for automated tests.

## Scope

### Included

- A minimal runnable web client and Python API foundation.
- A documented local setup and run path from a clean checkout.
- An API health/readiness endpoint and a minimal web page that can reach the local API.
- Environment-based configuration with a safe `.env.example`; no secrets in the repository.
- A provider-neutral LLM service boundary with a LangChain integration point, without live provider calls in baseline tests.
- A root pytest command recorded in `.github/sdd-harness.yml`.
- Automated tests for configuration, the API health path and the integration boundary, with external providers mocked.
- README or architecture documentation describing structure, setup, run commands, test commands and current boundaries.

### Excluded

- Instagram or Facebook API integration, OAuth and publishing.
- LinkedIn generation or publishing in the first stage; LinkedIn is deferred to a second stage.
- Image generation, voice interaction and production RAG retrieval.
- Multi-business or multi-tenant behavior.
- Production hosting, deployment and operational secrets.
- Docker or Docker Compose adoption until the pending Issue #34 decision is resolved.

### Channel decision

The first stage prioritizes Instagram and supports Facebook as the second generation/adaptation channel for small-commerce use cases. LinkedIn is explicitly deferred to a second stage. This foundation only prepares the application structure and does not implement channel generation or publishing.

## Acceptance criteria

- A clean checkout can install the documented dependencies and start the web client and API using documented commands.
- The web client renders a foundation page and the API exposes a deterministic health/readiness response without provider credentials.
- The code structure, environment handling and branch/commit conventions are documented.
- The API exposes a provider-neutral LLM integration boundary backed by the approved LangChain integration point, while baseline tests do not call external providers.
- `python -m pytest -q` is the authoritative application test command in `.github/sdd-harness.yml` and passes the configured foundation tests.
- No test, local run path or CI job publishes to Instagram or Facebook.
- Evidence for each criterion is recorded before the issue is closed.

## Rubric

No aplica — the official rubric and weights have not been supplied. This foundation contract records product and engineering evidence only and MUST be remapped if an official rubric criterion becomes available.

## Tests and verification

- OpenSpec schema and active-change validation.
- Required-field contract validation.
- `python -m pytest -q` for foundation unit/API tests and existing governance tests.
- Manual clean-checkout setup and run verification for the web client and API.
- Manual inspection that no provider credentials or social publishing call is required by the baseline path.
- CI run links and command output recorded in the daily log and issue.

## Open questions and blockers

- Docker/Docker Compose remains pending Issue #34 and is intentionally excluded.
- Hosting provider and production deployment are not selected.
- Provider credentials, quotas and data-handling terms must be rechecked when provider-backed features begin.

## Approval

Approved on 2026-10-04. Phase 2 implementation MAY proceed in tasks.md order. The approved contract does not authorize Instagram/Facebook publishing or any LinkedIn work.
