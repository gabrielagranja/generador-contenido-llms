# Tasks

## Implementation

- [x] 1. Add process-local editorial storage separate from Chroma.
- [x] 2. Preserve brand, business, grounding and provenance metadata in content records.
- [x] 3. Expose draft retrieval, review status, explicit review decisions and manual edits.
- [x] 4. Return safe HTTP errors and require a declared reviewer for decisions.

## Verification

- [x] 5. Add focused API tests for creation, retrieval, lifecycle transitions, isolation and metadata preservation.
- [x] 6. Run focused tests, SDD/OpenSpec validation and `git diff --check`.

All tasks are complete for the approved 20.5.1 scope. Durable persistence and
identity verification remain outside this iteration.
