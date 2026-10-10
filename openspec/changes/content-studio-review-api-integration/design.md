# Design

The browser uses a small typed HTTP boundary for `/drafts`, `/drafts/{id}`,
`/drafts/{id}/review` and `PATCH /drafts/{id}`. The API is the source of truth
for records created by Content Studio. The browser may keep a session index for
navigation, but never treats a local state change as approval.

Each generated response is associated by array position with its returned
`content_id`. Retrieval and mutation responses replace the visible draft only
after validation. A request sequence token invalidates responses after a brand
or commerce context changes. HTTP failures are retained as actionable messages
and do not promote the previous state.

Feedback is required for `request_regeneration`; this operation records the
review decision and does not start generation. `PATCH` keeps
`pending_human_review`, and approval is only reflected after the API returns
`approved_final`.
