# Issue #24.1/#24.2 — review and regeneration evidence

This evidence covers the editorial state, review and manual-edit boundary from
#24.1. Regeneration lineage (#24.2) is now covered by the focused evidence in
`tests/test_editorial_review.py`; copy/export (#24.3) is covered by `docs/evidence/issue-24-3-copy-export.md`.

## Implemented lifecycle

`EditableTextDraft` remains the generated provider output. The new
`EditorialContent` wrapper makes the lifecycle explicit:

`generated_draft` → `pending_human_review` → `approved_final`

Only `EditorialReviewService.approve(..., reviewer_ref=...)` can create
`approved_final`, and approval records a fingerprint of the exact draft text.

## Review and editing behavior

- `record_feedback` stores human feedback as `request_regeneration` while
  keeping the item pending; it does not call an LLM or regenerate content.
- `manual_edit` changes caption/CTA only while pending, preserves evidence and
  assumptions, clears a stale review record, and never approves automatically.
- Invalid state transitions, empty feedback, empty captions and missing reviewer
  references raise `EditorialTransitionError` without promoting content.

## #24.2 regeneration evidence

- Feedback regeneration creates a new pending item with source ID, trigger,
  feedback and source fingerprint while leaving the source unchanged.
- Changed-input regeneration records only approved brief/channel/format fields,
  preserves evidence/provenance metadata and returns to human review.
- Invalid input fields and provider failures leave the source item pending and
  unapproved.

## Evidence

`tests/test_editorial_review.py` covers initial state, explicit submission to
review, approval/fingerprint, feedback, invalid transitions, manual editing
without implicit approval, feedback/changed-input regeneration and safe
provider failure handling. RAG retrieval and export boundaries are unchanged.
