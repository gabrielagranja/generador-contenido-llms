# Content Studio review API integration

## ADDED Requirements

### Requirement: API-backed editorial synchronization

The Content Studio MUST and SHALL use the Human Review API as the source of truth for
generated drafts and MUST and SHALL preserve the association between each returned
draft and its `content_id`.

#### Scenario: multiple drafts retain identity

- GIVEN the API returns multiple drafts and matching content IDs
- WHEN Content Studio receives the response
- THEN each displayed draft is associated with its matching ID and metadata.

#### Scenario: confirmed edit remains pending

- GIVEN a draft is pending human review
- WHEN Content Studio receives a successful PATCH response
- THEN it displays the returned text and keeps the backend editorial state.

#### Scenario: explicit review decision

- GIVEN a content ID and non-empty reviewer reference
- WHEN the user approves or requests regeneration
- THEN Content Studio sends the corresponding API decision and updates only
  after the response is confirmed.

### Requirement: stale response safety

The client MUST ignore a response belonging to a previous brand or commerce
selection and MUST surface 404, 409, 422, 503, network and timeout failures
without optimistic approval.

#### Scenario: context changes during a request

- GIVEN an API request is in flight
- WHEN the selected commerce changes before the response arrives
- THEN the response does not overwrite the newly selected context.
