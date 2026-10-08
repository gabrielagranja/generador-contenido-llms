# Editorial Content Mix Planning

## Purpose

Define an auditable planning contract for the 80/20 rule, the Three-Thirds
model and future configurable editorial mixes for the Coll Amunt! MVP.

The system MUST apply each ADDED requirement below.

## ADDED Requirements

### Requirement: Versioned content-mix strategies

The system SHALL represent a strategy as a versioned ordered set of named
buckets with integer percentages whose total is exactly 100.

#### Scenario: Built-in 80/20 strategy

- GIVEN a planner selects `eighty_twenty`
- WHEN the strategy is resolved
- THEN it returns `VALUE` at 80% and `PROMOTIONAL` at 20%
- AND it records a stable strategy identifier and version.

#### Scenario: Built-in Three-Thirds strategy

- GIVEN a planner selects `three_thirds`
- WHEN the strategy is resolved
- THEN it returns `EDUCATIONAL`, `COMMUNITY` and `PROMOTIONAL` at 34%, 33%
  and 33%
- AND the total is exactly 100%.

#### Scenario: Invalid strategy definition

- GIVEN a strategy has an empty or duplicate bucket key, a non-integer or
  negative percentage, or a total different from 100
- WHEN it is validated
- THEN the system rejects it with an actionable validation error
- AND it cannot be used to create a plan.

### Requirement: Configurable future mixes

The system SHALL accept a custom strategy using the same bucket and percentage
schema as the built-in presets.

#### Scenario: Custom strategy

- GIVEN a user defines named buckets and valid percentages totaling 100
- WHEN the strategy is saved
- THEN the system assigns or accepts an immutable version
- AND a plan can use it without changing the planning data shape.

#### Scenario: Strategy version is changed

- GIVEN a strategy already used by a plan
- WHEN its bucket names or percentages need to change
- THEN the system creates a new version
- AND existing plans retain the original strategy version and allocation.

### Requirement: Deterministic cycle allocation

The system SHALL calculate target slot counts for a requested positive cycle
size using largest-remainder allocation, assigning ties by stable strategy
bucket order.

#### Scenario: Remainder allocation

- GIVEN a valid strategy and cycle size N
- WHEN target slots are calculated
- THEN each bucket receives the floor of its exact quota first
- AND remaining slots are assigned by descending fractional remainder
- AND equal fractional remainders are resolved by the declared bucket order
- AND all target slot counts sum to N.

#### Scenario: Ten-post preset allocations

- GIVEN a 10-post cycle
- WHEN target slots are calculated for `eighty_twenty`
- THEN it returns `VALUE=8` and `PROMOTIONAL=2`
- WHEN target slots are calculated for `three_thirds`
- THEN it returns `EDUCATIONAL=4`, `COMMUNITY=3` and `PROMOTIONAL=3`

#### Scenario: Equal remainder tie

- GIVEN a valid strategy has two or more equal fractional remainders
- WHEN a remaining slot is assigned
- THEN the earlier bucket in the strategy declaration order receives it
- AND the result is reproducible for the same strategy version and cycle size.

#### Scenario: Same inputs are repeated

- GIVEN the same strategy version, cycle size and bucket order
- WHEN allocation is calculated twice
- THEN the bucket counts and ordering are identical.

### Requirement: Bounded plan items

The system SHALL limit MVP plans to Instagram or Facebook and the existing
`single_image`, `carousel` or `reel` formats.

#### Scenario: Valid Coll Amunt! item

- GIVEN a planned item references a valid `GuidedBrief` or existing editorial
  item for Instagram or Facebook and an approved format
- WHEN it is assigned to a strategy bucket
- THEN the plan records the source reference, platform, format, bucket key and
  strategy version
- AND the referenced brief/content metadata is not redefined or silently changed.

#### Scenario: Unsupported planning target

- GIVEN an item targets Stories, LinkedIn, another platform or an unsupported
  format
- WHEN it is added to an MVP plan
- THEN the system rejects the item
- AND the existing source item remains unchanged.

### Requirement: Evidence and review preservation

The system SHALL preserve the existing source item’s fact-status, evidence,
assumptions, unsupported-claim markers and editorial review state.

#### Scenario: Grounded item is planned

- GIVEN a source item contains RAG provenance or other approved evidence
- WHEN it is assigned to a mix bucket
- THEN the plan retains a reference to that evidence and its source metadata
- AND the planner does not create, remove or rewrite factual claims.

#### Scenario: Pending item is planned

- GIVEN a source item is `generated_draft` or `pending_human_review`
- WHEN it is assigned to a plan
- THEN it remains in that review state
- AND planning does not make it `approved_final` or publishable.

### Requirement: Allocation transparency

The system SHALL expose strategy version, target counts, actual counts, bucket
assignments and a difference summary for every plan.

#### Scenario: Underfilled or unbalanced cycle

- GIVEN actual assigned items do not match target counts
- WHEN the plan summary is returned
- THEN it shows target and actual counts per bucket and the difference
- AND it does not invent missing content or silently rebalance assignments.

#### Scenario: Performance interpretation

- GIVEN a user asks whether a mix guarantees reach, engagement or conversion
- WHEN the planner explains the strategy
- THEN it describes the mix as an editorial heuristic
- AND it makes no unsupported performance guarantee.

### Requirement: Human publication boundary

The system SHALL preserve the existing explicit human approval requirement for
Instagram publication and SHALL NOT schedule or publish from a mix plan.

#### Scenario: Plan is marked ready

- GIVEN a plan has all target slots assigned
- WHEN a publication or scheduling action is requested
- THEN the planner returns a boundary error or hands off to the existing
  human-review/publication flow
- AND no item is published or approved implicitly.
