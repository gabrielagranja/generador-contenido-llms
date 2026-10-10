# Tasks

## Governance

- [x] 1. Obtain explicit human approval for this OpenSpec change.
- [x] 2. Resolve or record the output-budget and provider-behavior open questions.

## Implementation

- [x] 3. Add validated default and absolute output-token settings without changing provider selection, model, temperature, or timeout defaults.
- [x] 4. Pass the validated output budget to the concrete Groq adapter.
- [x] 5. Add concise isolated Instagram and Facebook generation-contract guidance.
- [x] 6. Preserve RAG grounding, provenance, unsupported-claim metadata, human review, and editorial state behavior.

## Verification

- [x] 7. Add mock/fake-provider tests for defaults, valid overrides, invalid configuration, Groq adapter arguments, deterministic mock output, and both channel contracts.
- [x] 8. Add or update tests proving grounding and review metadata remain unchanged.
- [x] 9. Run `python -m pytest -q`.
- [x] 10. Run `python scripts/validate_sdd_contract.py` and applicable OpenSpec validation.
- [x] 11. Run `git diff --check`.
- [x] 12. Run `npm run typecheck`, `npm test`, and `npm run build` in `apps/web`.
- [ ] 13. Record representative offline evidence and remaining production-setting limitations.

Do not start these tasks until proposal approval is Approved.
