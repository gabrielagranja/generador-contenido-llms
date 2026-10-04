# Design: Runnable Web Application Foundation

## Technical approach

Build the smallest reproducible full-stack skeleton that satisfies Issue #21 and the Phase 3 roadmap without pulling provider or social-platform behavior into the foundation.

The repository will use a clear client/API split:

- `apps/web/`: Next.js, React and TypeScript client.
- `apps/api/`: Python 3.11+, FastAPI and Pydantic API.
- `tests/`: Python tests, including the existing governance tests and new foundation tests.
- `docs/architecture/`: structure and local-operation notes.
- `.env.example`: non-secret configuration names and safe examples.

The exact JavaScript package manager and whether local development uses two terminals or one orchestrator remain explicit decisions. The implementation MUST record the selected decision in the setup documentation rather than silently assuming one.

## API boundary

The API will expose a deterministic readiness endpoint and a small provider-neutral LLM service interface. LangChain adapters belong behind that interface. The foundation will not make live Groq, Gemini, Meta or other external calls. Provider-backed behavior will be introduced by later approved OpenSpec changes.

Pydantic settings/configuration will read environment variables and distinguish local foundation behavior from provider-enabled behavior. Missing provider credentials will not block the readiness path, but provider-dependent paths must produce actionable configuration errors.

## Client boundary

The client will render a minimal foundation page, call the readiness endpoint through a documented local URL and display a useful ready/not-ready state. It will not contain social tokens, publishing actions or provider credentials.

## Testing strategy

The authoritative command will be `python -m pytest -q`. Tests will cover:

- configuration defaults and safe missing-credential behavior;
- API readiness response;
- client/API contract at the agreed boundary;
- deterministic LLM adapter behavior with mocks;
- no-network behavior for baseline tests.

External providers and social APIs will be mocked or omitted. The CI adapter will run this command and report its actual result.

## Documentation and evidence

README or architecture documentation will include prerequisites, setup, environment variables, run commands, test command, directory responsibilities, and explicit out-of-scope behavior. Verification evidence will link the CI run, test output and clean-checkout smoke test to Issue #21.

## Safety and change boundaries

- No real secrets are committed.
- No automatic Instagram or Facebook publishing is added.
- No production hosting decision is made.
- Docker remains excluded pending Issue #34.
- The LinkedIn/Facebook wording discrepancy is recorded as a separate decision; this design does not silently resolve it.
