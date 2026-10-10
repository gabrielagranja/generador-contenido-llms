# Tasks

The contract is Approved. Implementation follows the ordered list below.

## Contract and configuration

- [x] Confirm Issue #20 linkage and the C4.1/C4.2 rubric mapping.
- [x] Add provider settings, safe `.env.example` values and local dotenv loading.
- [x] Add the `langchain-groq` dependency without removing the offline mock.

## Implementation

- [x] Implement the Groq adapter behind `TextGenerator`.
- [x] Expose `POST /drafts` with the validated `GuidedBrief` contract and review-state metadata.
- [x] Connect Content Studio to the API with loading and controlled error states.

## Verification and evidence

- [x] Add API contract tests with an injected fake generator.
- [x] Run Python compilation and web typecheck.
- [ ] Run the full configured Python suite after dependencies are installed.
- [ ] Perform and record one authorized Groq smoke run with synthetic data.
- [ ] Update Issue #20 and the C4 traceability evidence after the smoke run.
