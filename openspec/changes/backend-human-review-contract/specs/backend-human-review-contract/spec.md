# Backend human-review contract

## ADDED Requirements

### Requirement: reviewable draft identity and retrieval

The API MUST assign each generated channel draft a stable `content_id` and
MUST preserve its brand, business, editorial, provenance and grounding fields.

#### Scenario: generated draft is retrievable

- GIVEN POST `/drafts` returns a non-empty draft
- WHEN the caller requests GET `/drafts/{content_id}`
- THEN the same draft is returned with `pending_human_review`
- AND its business and source metadata are unchanged.

### Requirement: explicit review decisions

The API MUST require a non-empty declared reviewer reference for approval or a
feedback decision, and SHALL reject invalid lifecycle transitions.

#### Scenario: approval is explicit

- GIVEN a draft is pending human review
- WHEN a reviewer submits `approve` with a reviewer reference
- THEN the item becomes `approved_final`
- AND a second approval is rejected.

#### Scenario: manual edit is not approval

- GIVEN a draft is pending human review
- WHEN the caller edits its caption
- THEN the item remains `pending_human_review`.

### Requirement: safe scope and persistence boundary

The API MUST return 404 for an unknown content ID and MUST NOT use Chroma as
editorial state storage. The process-local implementation MUST document that
records are not durable across a service restart.

#### Scenario: unknown content is isolated

- GIVEN a content ID from another business or an unknown ID
- WHEN the caller retrieves it
- THEN no other business content is returned
- AND the response is an actionable 404.
