# Design

## Context

This is a planning-layer delta related to Issue #22. The approved
`expert-content-generation`, `channel-adapted-content-contract`,
`scoped-business-context-rag` and `editorial-review-control` changes remain
the source of truth for briefs, drafting, evidence and approval. This change
only defines how a planning cycle allocates editorial slots and associates
already-valid content items with strategy buckets.

## Technical approach

Represent a strategy as an immutable version containing an identifier, a
human-readable name, an ordered list of buckets and integer percentages. A
bucket has a stable key, label and purpose. The built-in presets are:

| Preset | Buckets | Allocation |
|---|---|---:|
| `eighty_twenty` | `VALUE` / `PROMOTIONAL` | 80% / 20% |
| `three_thirds` | `EDUCATIONAL` / `COMMUNITY` / `PROMOTIONAL` | 34% / 33% / 33% |

The Three-Thirds preset uses 34/33/33 so the stored percentages total exactly
100 while preserving the intended near-equal thirds. The canonical labels are
`EDUCATIONAL`, `COMMUNITY` and `PROMOTIONAL`; the labels are strategy metadata,
not claims that every item has a particular business meaning.

For a cycle of N slots, calculate each exact quota as `N * percentage / 100`.
Allocate the floor of every quota first; assign remaining slots by descending
fractional remainder. If fractional remainders tie, assign earlier in the
strategy's declared bucket order; after a slot is assigned, continue through
the same deterministic ordering until all remaining slots are assigned. For
10 posts, 80/20 produces `VALUE=8` and `PROMOTIONAL=2`; Three-Thirds produces
`EDUCATIONAL=4`, `COMMUNITY=3` and `PROMOTIONAL=3` because the exact quotas
are 3.4, 3.3 and 3.3. A plan may contain fewer or more items than the target
cycle size while reporting both target quotas and actual counts; it must not
silently rebalance existing items.

Each planned item stores a reference to an existing content item or
`GuidedBrief`, the strategy version and bucket key, target platform and
approved format. The planner validates the referenced metadata but does not
clone or mutate it. Existing fact status, evidence references, assumptions,
unsupported-claim markers and review state pass through unchanged.

## Decisions and trade-offs

- Use integer percentages and exact-sum validation for portable, auditable
  plans; decimal weights and implicit normalization are rejected.
- Keep presets and custom strategies on one schema so future mixes are data
  configuration rather than a new planner branch.
- Use deterministic largest-remainder allocation instead of silently rounding
  each bucket independently, which could make totals exceed the cycle size.
- Treat Three-Thirds as an editorial heuristic and avoid asserting that a
  ratio improves performance.
- Keep planning separate from generation and publication so an allocation
  cannot bypass existing evidence or human-approval safeguards.

## Validation strategy

Use synthetic Coll Amunt! items across Instagram/Facebook and the three
approved formats. Verify exact preset definitions, including the 10-post
allocations above, custom strategy validation, cycle allocation for N=1, 3, 5
and 10, stable tie handling by declared bucket order, duplicate/unknown
bucket rejection, unsupported platform/format rejection, and preservation of
source and review metadata. Include an underfilled cycle to confirm actual
counts are reported rather than auto-generated.

## Safety, privacy and operational boundaries

The planner stores references and editorial metadata only; it does not ingest
new personal data, call external sources, publish, schedule or send content.
Current-information and approved business-context evidence remain governed by
their existing contracts. A failed validation must return an actionable error
without changing the source item or promoting its review state.

## Open questions

The canonical Three-Thirds labels are confirmed. A dedicated
editorial-planning GitHub issue may replace the related-parent linkage to Issue
#22 in a future change, but no duplicate issue should be created for this
contract.
