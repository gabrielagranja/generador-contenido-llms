# Editorial review, regeneration and final-text control

## Status and human approval

- Status: Pending
- Human approval: Pending; this change prepares the contract and does not authorize application implementation until an authorized human approves it.
- Issue: #24 — [STORY] Review, edit and regenerate content
- Parent epic: #10 — [EPIC] Content generation MVP
- Decision record: Pending

## Plan objective

Prepare the smallest approved contract needed to make editorial control explicit after content generation, while preserving the existing editable, channel-adapted and RAG-grounded drafting boundaries.

## Objective

Represent the distinction between generated copy, copy awaiting human review and explicitly approved final text. Define the minimum feedback, regeneration, manual-edit and copy/export boundaries without implementing any application behavior in this change.

## Scope

### Included

- An explicit human-review state in the editorial flow.
- A review decision and optional human feedback attached to the reviewed draft.
- Regeneration from review feedback or changed approved brief/channel/format inputs, with minimal lineage to the source draft.
- A clear distinction between manual editing and regeneration.
- Copy/export of approved final text only.
- Preservation of existing GuidedBrief, channel adaptation, RAG provenance and publication-control boundaries.
- Synthetic representative cases and state-transition/error verification for the three Issue #24 criteria.

### Excluded

- Automatic publication, scheduling or approval by an LLM, voice command or regeneration request.
- Regeneration implementation beyond the defined contract, advanced editor UX or collaborative multi-user workflows.
- Complex version history, branching, CMS integration, analytics, performance learning or approval delegation.
- Image/video export, media rendering, direct Facebook publishing and any change to the approved format scope.
- Changes to RAG retrieval or grounding rules.

## Acceptance criteria

- Human review is explicit: every generated draft enters `pending_human_review`, and only an explicit human approval action may produce `approved_final`.
- Regeneration accepts either structured human feedback or changed approved brief/channel/format inputs, creates a new generated draft linked to its source, and returns it to `pending_human_review`.
- The final text can be copied or exported only from `approved_final`; pending or generated text cannot be represented as final output.
- Manual edits remain distinguishable from regeneration and never imply approval by themselves.
- Existing facts, assumptions, unsupported-claim warnings and RAG evidence provenance remain attached to each draft lineage; feedback or changed inputs cannot authorize invented business claims.
- Invalid transitions and provider failures leave the source content in its prior safe state and return an actionable error.

## Rubric

No new rubric indicator is introduced. The contract provides traceable evidence for the existing project practices around structured delivery, human editorial control and source-grounded content; rubric status remains pending until implementation and evidence exist. See `docs/rubric-traceability.md`.

## Tests and verification

- Automated: validate the state model, transition guards, feedback/input lineage, manual-edit boundary, approved-final copy/export boundary and RAG metadata preservation with provider calls mocked.
- Contract: run OpenSpec schema/active-change validation and `scripts/validate_sdd_contract.py`.
- Manual/evidence: exercise synthetic drafts for explicit review, feedback regeneration, changed-input regeneration and approved-final copy/export without real business data.
- Failure checks: verify invalid state transitions, missing source drafts, empty feedback/input changes and provider errors do not approve or lose the source draft.

## Open questions and blockers

- Pending human approval of this Issue #24 contract before implementation tasks can be marked complete.
- The eventual export container/transport is intentionally left to implementation; the contract requires final text fidelity and approval gating, not a CMS or publishing integration.

## Approval

Pending. Do not implement application behavior or mark implementation tasks complete until an authorized human approves this contract.
