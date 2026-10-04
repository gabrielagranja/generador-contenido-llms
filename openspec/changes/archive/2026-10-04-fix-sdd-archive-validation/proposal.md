# Exclude Archived Changes from SDD Contract Validation

## Status and human approval

- Status: Approved
- Issue: #39 — Exclude archived OpenSpec changes from contract validation
- Decision record: The correction is required because standard OpenSpec archiving placed a completed change under `openspec/changes/archive/`, which the project-local validator currently scans as active.

## Plan objective

Support the Quality/delivery objective (#12) by keeping CI validation reliable after an approved OpenSpec change is archived.

## Objective

Correct the deterministic required-field validator so it scans active change directories only and preserves the standard OpenSpec archive directory as historical evidence.

## Scope

### Included

- Exclude exactly `openspec/changes/archive/` from active-change scanning.
- Add regression coverage for an archive directory alongside a valid active change.
- Re-run the full SDD CI workflow after the correction.

### Excluded

- Altering archived proposal, specification, design or task history.
- Weakening validation for any non-archive active change.
- Changing OpenSpec CLI behavior, CI triggers or GitHub rulesets.
- Application behavior or social-content publishing.

## Acceptance criteria

- A directory named `archive` directly beneath the configured changes root is not validated as an active change.
- A valid active change in the same changes root still passes validation.
- An invalid active change in the same changes root still fails validation.
- A regression test demonstrates both archive exclusion and active-change enforcement.
- The SDD workflow passes after the correction.

## Rubric

No aplica — the official rubric has not been supplied. This CI reliability correction will be remapped if a rubric criterion becomes applicable.

## Tests and verification

- Unit test with an archive child and a valid active change.
- Unit test that an invalid active change still reports errors.
- `openspec validate --all --json`, required-field validation and the complete SDD workflow.

## Open questions and blockers

- No scope decision is open: excluding the standard archive directory is required to preserve the existing stated meaning of active-change validation.
- Human approval recorded on 2026-10-04; implementation may proceed in tasks.md order.

## Approval

Approved on 2026-10-04. Implementation may proceed in tasks.md order.
