# Proposal

## Status and human approval

- Status: Pending
- Issue: #102 — Optional local Ollama provider
- Human approval: pending review of this contract.

## Plan objective

Finish the existing MVP editorial flow with a local text provider and minimal cost, without adding product capabilities.

## Objective

Select Ollama explicitly behind the existing TextGenerator interface so Content Studio and RAG reuse the current generation and review pipeline.

## Scope

Included: API-side LLM_PROVIDER=ollama, OLLAMA_BASE_URL (default http://127.0.0.1:11434), required OLLAMA_MODEL, validated HTTP(S) endpoint without credentials, bounded requests using LLM_TIMEOUT_SECONDS, output budget mapped to num_predict, temperature, actual provider/model metadata, controlled failures, local setup documentation and fake-provider tests. Reuse httpx and the existing LangChain runnable boundary; no new provider SDK is required.

Excluded: model installation/download, automatic fallback to Groq, real LLM calls in tests, model comparison, UI redesign, RAG changes, review-state changes, persistence and calendar implementation (separate changes), publication and branch deletion.

## Acceptance criteria

- Explicit Ollama selection works without a Groq key; existing mock/Groq behavior is preserved.
- A nonempty locally installed model is required; no model is chosen or downloaded implicitly.
- A nonstreaming local chat request receives the existing prompt, temperature and validated num_predict budget (350 default, maximum 600).
- The configured timeout is applied; network, HTTP and malformed-response failures produce a controlled API error without automatic cloud fallback.
- POST /drafts reports the selected provider/model and preserves pending_human_review, grounding and evidence.
- Python, SDD, OpenSpec and Git Conventions checks pass; existing frontend checks pass.

## Rubric

No aplica — optional provider replacement within the existing C4 text-generation workflow, not a new rubric capability.

## Tests and verification

Fake HTTP transport and injected generators verify request parameters, response handling, timeout/unavailable service and provider selection without network calls. Run full Python tests, required-field validator, OpenSpec validation, git diff --check and frontend typecheck/tests/build. A real local smoke test is separate evidence and requires an available Ollama service/model; do not report it as verified from mocks.

## Open questions and blockers

The installed local model and available hardware are unknown. OLLAMA_MODEL remains explicit rather than assuming a commercial-data-safe or installed model. Contract approval is pending. No installation is necessary for offline implementation verification.

## Approval

Pending. Implementation starts after explicit human approval of this contract.
