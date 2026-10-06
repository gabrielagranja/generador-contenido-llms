# Tasks

## Implementation

- [x] 1. Add the editorial content state model and explicit human-review transition from generated draft to pending review; keep approval human-only. (Issue #24.1)
- [x] 2. Add review records for approval or regeneration requests, including feedback, reviewer text fingerprint and invalid-transition errors. (Issue #24.1)
- [x] 3. Add feedback/changed-input regeneration orchestration with source-draft lineage, allowed input snapshots and preserved GuidedBrief/RAG metadata. (Issue #24.2)
- [x] 4. Add the manual-edit boundary so edits remain pending review and cannot implicitly approve content. (Issue #24.1)
- [x] 5. Add copy/export handling for exact approved-final text only, with safe rejection of pending or generated content. (Issue #24.3)

## Verification

- [x] 6. Run focused mocked tests for lifecycle states, explicit approval, manual-edit non-approval, invalid transitions and provider-error safety. (Issue #24.1)
- [x] 7. Run focused mocked tests for feedback/changed-input regeneration, source lineage, allowed input boundaries and RAG metadata preservation. (Issue #24.2)
- [x] 8. Run focused mocked tests for approved-final copy/export and rejection of unapproved content. (Issue #24.3)
- [x] 9. Run OpenSpec schema/active-change validation, SDD required-field validation and the configured application test command; record evidence and limitations. (Issue #24.1–#24.3)

Tasks 1, 2, 3, 4, 5, 6, 7 and 8 are complete for the approved #24.1-#24.3 scope.
Task 9 is complete; the full Issue #24 contract is verified and ready for human closure. The OpenSpec change remains active and is not archived in this step.
