# Tasks: Runnable Web Application Foundation

The contract is Approved on 2026-10-04. Implementation follows this order.

- [x] Confirm the package-manager and local-process decisions: npm and two documented terminals.
- [x] Change the proposal status to Approved after human approval of the exact contract and channel scope.
- [x] Scaffold the Python 3.11+/FastAPI/Pydantic API under `apps/api/` with a deterministic readiness endpoint.
- [x] Scaffold the Next.js/React/TypeScript client under `apps/web/` with a foundation page that reads API readiness.
- [x] Add environment configuration and a safe `.env.example`; verify no secrets are tracked.
- [x] Add the provider-neutral LangChain integration boundary with a deterministic mock adapter.
- [x] Add foundation tests for configuration, readiness, client/API boundary and no-network behavior.
- [ ] Configure `.github/sdd-harness.yml` with `python -m pytest -q` as the authoritative application test command.
- [ ] Document prerequisites, setup, run, test commands, structure and scope boundaries.
- [ ] Run OpenSpec validation, required-field validation and `python -m pytest -q`; record evidence.
- [ ] Perform a clean-checkout smoke test for client and API startup; record evidence.
- [ ] Update the issue with evidence, synchronize canonical specs if behavior changed, and close only after acceptance criteria are verified.
