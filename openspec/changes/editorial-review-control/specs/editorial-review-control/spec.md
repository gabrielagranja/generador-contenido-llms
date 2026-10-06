# Editorial review control

## Purpose

Define the minimal editorial lifecycle around generated channel-adapted text
for Issue #24 without adding publication, collaboration or advanced history.

## ADDED Requirements

### Requirement: explicit human review

The system MUST represent generated content as `generated_draft`, route it to
`pending_human_review`, and require an explicit human action before assigning
`approved_final`.

#### Scenario: generated draft enters review

- GIVEN the existing drafting boundary returns non-empty text
- WHEN an editorial item is created
- THEN the item is represented as `generated_draft` and then `pending_human_review`
- AND it is not represented as final or approved.

#### Scenario: human approval is explicit

- GIVEN an item is `pending_human_review`
- WHEN a human approves the exact current text and metadata
- THEN the item becomes `approved_final`
- AND generation, saving, copying, exporting or voice interaction alone SHALL NOT approve it.

#### Scenario: manual edit remains pending

- GIVEN an item is `pending_human_review`
- WHEN a human edits its text or CTA
- THEN the edited item remains `pending_human_review`
- AND the changed text requires a new explicit approval.

### Requirement: feedback and changed-input regeneration

The system MUST allow regeneration from meaningful human feedback or changed
approved brief/channel/format inputs, and SHALL preserve a traceable link to
the source draft.

#### Scenario: feedback requests regeneration

- GIVEN a `pending_human_review` item with human feedback
- WHEN regeneration is requested
- THEN a new `generated_draft` is created with source draft identity, feedback and source text fingerprint
- AND the new item enters `pending_human_review`
- AND the source item is not silently approved or overwritten.

#### Scenario: approved inputs request regeneration

- GIVEN a draft and a changed existing `GuidedBrief`, selected platform, format or approved constraint
- WHEN regeneration is requested
- THEN the changed input snapshot is recorded as the trigger
- AND the new item preserves the existing grounding and fact-status safeguards
- AND the result requires fresh human review.

#### Scenario: unsupported input change is rejected

- GIVEN a regeneration request attempts to introduce an unapproved business fact or unsupported claim
- WHEN regeneration is validated
- THEN the request is rejected or the claim remains explicitly unsupported
- AND no item becomes `approved_final`.

### Requirement: final text copy and export

The system MUST permit copy/export of the exact text of an `approved_final`
item and SHALL reject copy/export of generated or pending content as final.

#### Scenario: approved final text is copied or exported

- GIVEN an item is `approved_final`
- WHEN copy/export is requested
- THEN the exact approved text and selected channel/format metadata are returned
- AND no hidden prompt, credential or unapproved business data is included.

#### Scenario: pending text cannot be exported as final

- GIVEN an item is `generated_draft` or `pending_human_review`
- WHEN copy/export is requested as final content
- THEN the operation returns an invalid-state error
- AND the item remains unapproved.

### Requirement: safe failures and lineage

The system MUST preserve safe state and traceability when a transition,
source identity, input set or generation provider call is invalid or fails.

#### Scenario: invalid transition or provider failure

- GIVEN a missing source draft, invalid state transition, empty feedback/input change or provider error
- WHEN the operation is attempted
- THEN no item is promoted to `approved_final`
- AND the last valid source state and lineage remain available
- AND the caller receives an actionable error.

#### Scenario: grounded lineage is preserved

- GIVEN a draft uses RAG retrieval or confirmed/inferred/unknown fact metadata
- WHEN it is manually edited, reviewed or regenerated
- THEN evidence references, provenance, assumptions and unsupported-claim metadata remain attached to the relevant item
- AND regeneration continues through the existing channel/RAG boundary.

## Scope boundary

This contract does not define automatic publishing, scheduling, advanced version
history, multi-user collaboration, CMS integration, analytics or media export.
