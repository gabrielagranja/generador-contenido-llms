# Proposal

## Status and human approval

- Status: Approved
- Issue: #22 — Capture a structured content brief (related parent; editorial planning is explicitly identified there as a later product capability)
- Decision record: Pending

## Plan objective

Extend the Phase 4 content-generation slice with a planning-only editorial mix
contract for the Coll Amunt! MVP. The contract must support the 80/20 rule,
the Three-Thirds model and future named, configurable mixes without changing
the existing `GuidedBrief`, channel-adapted drafting, RAG, or human-review
contracts.

## Objective

Give a content manager a reproducible way to choose a content-mix strategy,
turn it into a bounded plan for Instagram and Facebook, and see whether a
planning cycle follows the intended allocation. A mix is an editorial planning
heuristic, not a promise of reach, engagement or conversion.

## Scope

### Included

- A versioned strategy definition with named buckets and integer percentage
  allocations that total 100.
- Built-in 80/20 and Three-Thirds presets, plus a custom strategy with
  user-defined bucket names and percentages.
- Planning for the Coll Amunt! MVP on Instagram and Facebook, with the
  existing single-image, carousel and Reel format boundary.
- Deterministic slot allocation for a requested cycle size, including the
  rounding/remainder rule and a visible allocation summary.
- Assignment of an existing editorial item or `GuidedBrief` reference to a
  mix bucket without copying or redefining its business facts, evidence,
  platform, format or review state.
- Validation of bucket assignments, cycle dates, selected platforms and
  strategy version before a plan is returned.

### Excluded

- Generating copy, visual media or new business claims.
- Replacing `GuidedBrief`, channel-adapted text, RAG/source provenance or
  editorial review contracts.
- Automatic scheduling, publication, analytics learning or engagement
  guarantees.
- Stories, LinkedIn, direct Facebook publishing, multi-business administration
  and multi-tenant planning.

## Acceptance criteria

- The contract defines the 80/20 and Three-Thirds presets unambiguously and
  permits future configurable mixes without code changes to the plan shape.
- The canonical identifiers are `VALUE` and `PROMOTIONAL` for 80/20, and
  `EDUCATIONAL`, `COMMUNITY` and `PROMOTIONAL` for Three-Thirds.
- A strategy cannot be saved or used when bucket names are empty/duplicated,
  percentages are invalid, or the total is not exactly 100%.
- For the same strategy version, cycle size and deterministic ordering, slot
  allocation is reproducible; remainder slots are assigned by documented
  largest-remainder ordering with stable tie-breaking. For 10 posts, 80/20
  allocates `VALUE=8` and `PROMOTIONAL=2`; Three-Thirds allocates
  `EDUCATIONAL=4`, `COMMUNITY=3` and `PROMOTIONAL=3`.
- A plan is bounded to Instagram/Facebook and the approved formats, and does
  not invent or silently alter a `GuidedBrief` or source evidence.
- Every planned item retains its bucket, strategy version, platform/format,
  source item reference and current review state; publication still requires
  the existing explicit human approval.
- The contract exposes planned-versus-actual counts without treating the
  ratio as a performance claim.
- Automated fixtures cover both presets, custom mixes, invalid definitions,
  rounding, platform/format rejection and preservation of evidence/review
  metadata.

## Rubric

No aplica directly to this planning contract. The official 24-indicator rubric
and all C4 requirements remain authoritative in `docs/rubric-traceability.md`;
this change does not replace or downgrade the LLM, LangChain or RAG evidence
required there. Any future evaluation evidence will be linked to the existing
Issue #22/#25/#32 evidence paths rather than altering rubric weights.

## Tests and verification

- Automated: OpenSpec schema/required-field validation and focused unit tests
  for presets, custom allocation, stable rounding and metadata preservation.
- Manual/evidence: review the plan examples against Coll Amunt! Instagram and
  Facebook use cases and record the result before implementation approval.
- External data: no external calls; use synthetic Coll Amunt! fixtures and
  existing approved RAG/evidence references only.

## Open questions and blockers

- Canonical Three-Thirds labels are confirmed as `EDUCATIONAL`, `COMMUNITY`
  and `PROMOTIONAL`.
- Confirm a dedicated GitHub issue for editorial planning, or approve using
  Issue #22 as the related parent for this contract.

## Approval

Approved by the user on 2026-10-08 for contract completion and repository
delivery. This approval covers the OpenSpec artifacts only; application
implementation remains a separate future task.
