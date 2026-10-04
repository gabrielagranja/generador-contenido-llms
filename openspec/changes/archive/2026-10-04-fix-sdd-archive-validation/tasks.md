# Tasks: Archive Exclusion in the Contract Validator

## Phase 2 implementation tasks

- [x] 1. Confirm the proposal is Approved and retain the archive as historical evidence.
- [x] 2. Add a regression test for a changes root that contains an archive directory and an active change.
- [x] 3. Update the validator to skip only the direct archive child.
- [x] 4. Verify that invalid active fixtures still fail.
- [x] 5. Run the complete SDD workflow and record CI evidence.
- [x] 6. Update Issue #39, traceability and the daily log with verification evidence.
- [x] 7. Archive this correction after CI passes and human verification confirms the acceptance criteria.

## Preconditions

- The human approval status in `proposal.md` is Approved.
- The correction does not mutate archived contracts or relax checks for active changes.
