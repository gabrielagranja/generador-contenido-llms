# Issue #24.1 — explicit human review evidence

This evidence covers only the editorial state, review, feedback and manual-edit
boundary. Regeneration lineage (#24.2) and copy/export (#24.3) are not
implemented here.

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

## Evidence

`tests/test_editorial_review.py` covers initial state, explicit submission to
review, approval/fingerprint, feedback, invalid transitions and manual editing
without implicit approval. Provider, RAG retrieval, regeneration and export
boundaries are unchanged.
