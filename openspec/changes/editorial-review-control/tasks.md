# Tasks

## Implementation

- [ ] 1. Add the editorial content state model and explicit human-review transition from generated draft to pending review; keep approval human-only. (Issue #24.1)
- [ ] 2. Add review records for approval or regeneration requests, including feedback, reviewer text fingerprint and invalid-transition errors. (Issue #24.1)
- [ ] 3. Add feedback/changed-input regeneration orchestration with source-draft lineage, allowed input snapshots and preserved GuidedBrief/RAG metadata. (Issue #24.2)
- [ ] 4. Add the manual-edit boundary so edits remain pending review and cannot implicitly approve content. (Issue #24.1)
- [ ] 5. Add copy/export handling for exact approved-final text only, with safe rejection of pending or generated content. (Issue #24.3)

## Verification

- [ ] 6. Run focused mocked tests for lifecycle states, explicit approval, manual-edit non-approval, invalid transitions and provider-error safety. (Issue #24.1)
- [ ] 7. Run focused mocked tests for feedback/changed-input regeneration, source lineage, allowed input boundaries and RAG metadata preservation. (Issue #24.2)
- [ ] 8. Run focused mocked tests for approved-final copy/export and rejection of unapproved content. (Issue #24.3)
- [ ] 9. Run OpenSpec schema/active-change validation, SDD required-field validation and the configured application test command; record evidence and limitations. (Issue #24.1–#24.3)

No task is complete. Do not implement until this proposal is approved by an authorized human.
