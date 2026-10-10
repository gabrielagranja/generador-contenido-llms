# Proposal

## Status and human approval

- Status: Approved
- Issue: #20 — Content Studio review API integration
- Human approval: Approved by the user's implementation request for microiteration 20.5.2.

## Plan objective

Connect the existing Content Studio editorial flow to the
  process-local Human Review API without changing the approved UI boundary.
## Objective

Generation preserves every returned `content_id`;
  retrieval, manual edit, feedback and approval use the API; backend state is
  shown only after confirmation; stale responses cannot overwrite a selected
  brand or commerce.
## Scope

### Included

- Typed browser client and Content Studio synchronization.
- Preservation of API IDs and brand/business/grounding metadata.
- Confirmed edits and explicit review decisions.

### Excluded

- Publication, scheduling, authentication, durable persistence and provider-side regeneration.

## Acceptance criteria

- Generation preserves every returned `content_id`;
- Rubric status: covered by the existing editorial-review and backend review
  contracts; no new publication capability is introduced.
## Rubric

No aplica — covered by the existing editorial-review and backend review contracts.

## Tests and verification

- Frontend typecheck and tests, API tests, full pytest,
  production build, OpenSpec validation and `git diff --check`.
## Open questions and blockers

- Process-local backend persistence and declared
  `reviewer_ref` remain known MVP limitations.
## Approval

Approved for implementation in microiteration 20.5.2 by the requested change scope.
