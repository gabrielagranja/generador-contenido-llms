# Design: Archive Exclusion in the Contract Validator

## Approach

Modify only the active-change directory iteration in `scripts/validate_sdd_contract.py`. The loop will skip the exact child name `archive`, matching the OpenSpec archive location `openspec/changes/archive/`.

Add tests that construct a temporary changes root with both an archive child and active fixture directories. This exercises the root-level iteration rather than only individual change validation.

## Safety and boundaries

The condition is deliberately exact: it does not ignore names that merely contain the word archive, and it does not alter parsing or validation of active contract fields. No archived file is changed, moved or deleted.

## Verification

Run the existing unit tests and SDD workflow. Confirm the validator no longer reports missing artifacts for the archive directory while still rejecting the current invalid fixture.

## Open questions

None. The proposed change restores the active/archive boundary already declared in the project documentation and in OpenSpec's standard lifecycle.
