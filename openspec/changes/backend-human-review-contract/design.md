# Design: Backend human-review transport contract

The existing `EditorialReviewService` remains the sole owner of lifecycle
invariants. FastAPI adapts its result to HTTP and a small in-memory repository
stores records by opaque ID. Chroma remains retrieval-only and is never used as
editorial state storage.

Each generated channel draft is stored separately, with `brand_id` and
`business_id` copied from the request and all existing draft fields retained,
including evidence provenance and supported/unsupported claims. The repository
is process-local and deliberately does not claim restart durability.

`POST /drafts/{content_id}/review` accepts only `approve` or
`request_regeneration`. Both require a declared, unverified `reviewer_ref`;
feedback is required for the regeneration request. `PATCH /drafts/{content_id}`
uses the existing manual-edit service and keeps the item pending. No endpoint
publishes, schedules or exports a non-approved item.

Missing IDs return 404 and service transition failures return 409. Pydantic
validation errors remain 422. The opaque `content_id` provides logical record
segregation only; it is not an authenticated tenant boundary. Because this
iteration introduces no authentication or identity verification, the API does
not claim to authorize a caller for a `business_id`, and clients must not treat
the preserved business metadata as an access-control decision.
