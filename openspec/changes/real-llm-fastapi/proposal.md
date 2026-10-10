# Proposal

## Status and human approval

- Status: Approved
- Issue: #20 — [STORY] Select an extensible, low-cost technical stack
- Parent epic: #9
- Human approval: Approved by the user's instruction to integrate a real LLM and expose generation through FastAPI.

## Plan objective

Close the first live-provider boundary while preserving the provider-neutral LangChain contract, the offline mock and the human-review gate.

## Objective

Allow Content Studio to request an editable channel-adapted draft from FastAPI. The API keeps Groq credentials server-side, returns reviewable content and remains runnable without credentials through the deterministic mock.

## Scope

### Included

- Groq integration through the existing `TextGenerator` boundary and LangChain adapter.
- Environment-backed provider, model, timeout and temperature settings.
- `POST /drafts` with the approved `GuidedBrief` request contract.
- Next.js Content Studio request, loading state and error handling.
- Review-state response metadata; generation never approves or publishes content.
- Mocked provider tests and local setup documentation.

### Excluded

- Image generation, voice, OAuth, Instagram publication and scheduling.
- Browser-side provider calls or exposure of API keys.
- Replacing the approved `GuidedBrief`, RAG contract or editorial-review state machine.
- Provider comparison or production hosting.

## Acceptance criteria

- With `LLM_PROVIDER=groq` and a valid local `GROQ_API_KEY`, `POST /drafts` returns an editable draft through LangChain and the selected channel template.
- Without provider credentials, the API remains runnable with the deterministic mock and no network call is made by tests.
- Invalid briefs return a validation error; provider configuration failures return a controlled service error without exposing secrets.
- Content Studio sends only the structured brief to the API and displays the returned caption as pending human review.
- The API response includes provider/model metadata but never includes the configured API key.

## Rubric

- C4.1, use of an LLM model: direct implementation evidence through the Groq adapter and a real local smoke run.
- C4.2, use of an LLM application framework: LangChain remains the application-facing adapter and runnable boundary.
- The change does not claim completion of C4.3; RAG remains governed by Issue #32.

## Tests and verification

- Run OpenSpec and SDD required-field validation.
- Run API contract tests with a fake LangChain-compatible generator.
- Run the web typecheck and configured application tests with external providers mocked.
- Perform one authorized local Groq smoke run using synthetic brief data and record provider/model/latency without recording the secret.

## Open questions and blockers

- The active Groq model identifier must be selected from the provider's current catalog and configured locally.
- Human evaluation of the live output remains part of Issue #25 and final delivery readiness.
- No real business data should be sent until the approved data-handling boundary is confirmed.

## Approval

Approved for implementation in the feature branch. The contract remains active until verification evidence and the Issue #20 update are complete.
