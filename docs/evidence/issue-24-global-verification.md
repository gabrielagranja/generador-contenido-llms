# Issue #24 — global verification evidence

This record verifies the merged #24.1, #24.2 and #24.3 implementation together.

## Acceptance criteria

| Criterion | Evidence | Result |
| --- | --- | --- |
| Human review is explicit | `EditorialContent` separates `generated_draft`, `pending_human_review` and `approved_final`; `approve` requires a non-empty reviewer reference. | Pass |
| Regeneration accepts feedback or changed inputs | `RegenerationRequest` validates the two triggers; `regenerate` records source draft ID, source fingerprint, feedback/changed inputs and preserves evidence, assumptions, review notes, provenance and unsupported-claim metadata. | Pass |
| Copy/export is limited to final approved text | `copy_final` and `export_final` require `approved_final` and return only the exact caption with content ID, channel and format metadata. | Pass |

## Required safeguards

- `manual_edit` keeps content in `pending_human_review` and clears the prior approval/feedback record; editing cannot approve implicitly.
- Invalid state transitions raise `EditorialTransitionError`.
- Regeneration returns a new pending-review item with lineage and preserved GuidedBrief/RAG-related draft metadata; provider failures preserve the source item.
- Generated and pending-review content cannot be copied or exported as final; the source state remains unchanged.
- Tests use synthetic content and do not publish, call a real LLM provider, write to a CMS or export media/files.

## Executed validation

- `npm.cmd exec --yes --package=@fission-ai/openspec@1.13.2 -- openspec schema validate sdd-governance`: passed.
- `npm.cmd exec --yes --package=@fission-ai/openspec@1.13.2 -- openspec validate --all --json`: 9/9 items passed, 0 failed. The existing informational archive warning for `required-ci-efficiency` is unrelated to this change.
- `python scripts/validate_sdd_contract.py`: passed.
- `python -m pytest -q`: 72 passed.
- `python -m pytest tests/test_api_foundation.py -q`: 6 passed.
- `npm.cmd run build` in `apps/web`: passed.
- `git diff --check`: passed.

## Limitations

The evidence is deterministic unit/smoke coverage over synthetic fixtures. It does not claim external-provider availability, production clipboard integration, CMS export, publication, or rubric completion beyond the Issue #24 acceptance criteria. The OpenSpec change remains active and Issue #24 remains open for human closure.
