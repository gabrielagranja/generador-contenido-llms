# Design: Editorial review, regeneration and final-text control

## Context

Issue #24 extends the existing Issue #22 `GuidedBrief` and channel-adapted editable text boundary. The current generator returns review notes but does not define a lifecycle state or approval gate. This design adds only the contract needed to make human review explicit and to bound later regeneration and final-text copy/export work.

## Technical approach

Keep the existing provider-neutral drafting and RAG services as the source of generated text. Add a small editorial-control boundary around their result; it must not move retrieval, grounding or channel templates into a new subsystem.

### Content lifecycle

Each content item has one explicit lifecycle state:

| State | Meaning | Allowed next actions |
|---|---|---|
| `generated_draft` | Provider output exists and is not yet presented as a human-reviewed item. | Enter review; request regeneration with a valid changed input set or feedback record. |
| `pending_human_review` | The draft is visible as awaiting a human decision. Manual edits may be made, but the item is still not final. | Save a manual edit, approve explicitly, or request regeneration. |
| `approved_final` | A human explicitly approved the exact current text and its relevant metadata. | Copy/export; a later edit or regeneration must create a new non-final review item. |

Generation creates `generated_draft`; the editorial boundary moves it to
`pending_human_review` before it can be approved. Approval is an explicit
human action tied to the exact current text, selected platform/format and
grounding metadata. There is no implicit approval on generation, save, copy,
export, timeout or voice interaction.

### Review and feedback

The minimum review record is:

```yaml
review:
  decision: approve | request_regeneration
  feedback: optional non-empty human text
  reviewer_ref: opaque local reviewer reference or null
  reviewed_text_fingerprint: required fingerprint of the exact text reviewed
```

`request_regeneration` requires either meaningful feedback or an explicitly
changed allowed input. It never changes the source item in place. A manual
edit is stored as the current editable text of the pending item and keeps its
state `pending_human_review`; it is not a regeneration request and does not
approve the item.

### Regeneration and lineage

Regeneration creates a new `generated_draft` with a minimal lineage record:

```yaml
lineage:
  source_draft_id: required
  trigger: human_feedback | changed_inputs
  feedback: optional
  changed_inputs: optional snapshot of approved brief/channel/format fields
  source_text_fingerprint: required
```

The new item is immediately routed to `pending_human_review`. The source item
remains traceable and is not silently promoted, deleted or overwritten. This
is lineage for review safety, not a complex version-history or collaboration
feature.

Allowed changed inputs are the existing `GuidedBrief` values, selected
platform(s), approved format and approved business/brand constraints. New
business facts must enter through the existing confirmed/inferred/unknown and
RAG grounding rules; feedback cannot turn an unknown or unsupported claim into
a fact.

### Manual editing versus regeneration

- Manual editing changes only the editable text/CTA fields of the current
  pending item and preserves its evidence, assumptions, review notes and state.
- Regeneration invokes the existing provider-neutral drafting boundary with
  feedback or changed allowed inputs and creates a new lineage-linked item.
- Neither operation can set `approved_final`; only an explicit human approval
  action can do so.

### Copy and export

Copy/export accepts only an `approved_final` item and returns its exact approved
text, selected channel/format metadata and no hidden generation instructions.
Copy may target the clipboard and export may target a plain-text representation
in a later implementation; the contract does not prescribe a CMS, file store or
publishing integration. Attempts to copy/export generated or pending content
return a safe invalid-state error and do not imply approval.

### RAG, channel and publication boundaries

Every generated/regenerated item preserves the existing evidence references,
provenance, assumptions and unsupported-claim metadata. Regeneration continues
through the same RAG-grounded path when enabled and remains channel-specific
for Instagram and Facebook. Approval here is editorial approval of text; it is
not automatic Instagram publication. Existing explicit human publication
confirmation remains a separate required step.

## Decisions and trade-offs

- Three lifecycle states plus a review record are sufficient for the MVP; a
  separate rejected or archived state would add workflow complexity without an
  Issue #24 acceptance criterion.
- Minimal source linkage is required for regeneration safety, but full history,
  branching and collaboration are excluded.
- Approval is fingerprint-bound to prevent approving text different from the
  text the reviewer saw.
- Copy/export is intentionally downstream of approval and text-only.

## Validation strategy

Use synthetic F-01/F-02/F-03 briefs and mocked generators. Assert explicit
state transitions, review decisions, feedback/input lineage, unchanged source
items, preserved grounding metadata, manual-edit non-approval and approved-final
copy/export. Exercise invalid transitions and provider failures without network
or publication calls.

## Safety, privacy and operational boundaries

- Never infer approval from model output, a save, a copy/export action or voice.
- Never publish or schedule as part of this contract.
- Keep feedback and reviewer references free of secrets and unapproved business
  data in tests/evidence.
- Preserve the existing RAG business scope and unsupported-claim safeguards.
- On errors, preserve the last valid state and return an actionable error; do
  not produce an approved result.

## Open questions

- Pending human approval of this contract.
- Exact UI and transport for clipboard/plain-text export are implementation
  details after approval; no scope decision is required now.
