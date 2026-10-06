# Issue #24.3 — approved final text copy/export evidence

The editorial service exposes `copy_final` and `export_final` as text-only handoff operations.

- Both operations accept only `approved_final` content.
- The returned payload contains the exact approved caption plus `content_id`, channel, and format metadata.
- Generated or pending-review content is rejected with `EditorialTransitionError`; the source state is not changed.
- The payload contains no prompt, credential, hidden instruction, or unapproved business-data field.
- No CMS, media, publication, or persistent file export is introduced; the contract is limited to a safe in-memory text handoff.

Evidence: `tests/test_editorial_review.py` covers successful copy/export and rejection for generated and pending content.
