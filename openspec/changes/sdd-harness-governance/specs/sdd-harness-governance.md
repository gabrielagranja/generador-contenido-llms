# SDD Harness Governance Delta Specification

## ADDED Requirements

### Requirement: project-local OpenSpec workflow

The repository SHALL define a project-local OpenSpec schema that produces proposal, specification, design and tasks artifacts.

The schema MUST require proposal completion before design and tasks are treated as ready.

The schema MUST be stored in the repository so that agents do not depend on one local machine configuration.

#### Scenario: agent starts a new change

GIVEN an agent has an approved GitHub Issue
WHEN it starts a new implementation change
THEN the project SHALL provide a project-local artifact workflow for proposal, specifications, design and tasks.

### Requirement: mandatory change contract fields

Every active OpenSpec change SHALL contain a proposal with Issue, plan objective, acceptance criteria, rubric status, tests/evidence, scope, open questions and human approval status.

The rubric field MUST either identify an official criterion or state No aplica with a concrete reason.

The validator MUST reject empty required fields and unresolved template placeholders.

#### Scenario: complete contract passes validation

GIVEN an active change contains all mandatory fields with substantive values
WHEN the contract validator runs
THEN the change SHALL pass required-field validation.

#### Scenario: incomplete contract fails validation

GIVEN an active change omits the Issue or human approval status
WHEN the contract validator runs
THEN the change MUST fail validation and report the missing field.

### Requirement: human approval gate

An implementation change SHALL declare one of Pending, Approved or Rejected as its approval status.

An agent MUST NOT mark implementation tasks complete while the change status is Pending or Rejected.

The validator MUST reject a change with completed implementation tasks and a non-Approved status.

#### Scenario: pending change is protected

GIVEN a change has approval status Pending
WHEN an agent requests implementation instructions
THEN the workflow SHALL state that human approval is required before implementation.

### Requirement: AI-assisted OpenSpec review

The CI workflow SHALL run OpenSpec validation for all active changes and report its result as an assisted consistency check.

OpenSpec validation MUST NOT be represented as formal proof that application behaviour is correct.

#### Scenario: OpenSpec inconsistency is reported

GIVEN an active OpenSpec change has invalid artifacts
WHEN CI runs OpenSpec validation
THEN CI MUST fail and report the validation result.

### Requirement: CI verification boundary

The CI workflow SHALL run schema validation, OpenSpec validation, required-field validation and the configured application test command.

If no configured application test command exists, CI MUST report that code tests are not configured rather than claim that tests passed.

The workflow MUST NOT publish to Instagram or Facebook, approve a scope, change roadmap priorities, or archive a change automatically.

#### Scenario: no code-test command is configured

GIVEN the repository has no configured code-test command
WHEN the CI workflow runs
THEN it SHALL report the missing configuration as an explicit non-passing or skipped-with-warning state according to the approved design.

### Requirement: agent-neutral guidance

The repository SHALL document the workflow in instructions readable by Codex, Claude and other agents.

The guidance MUST require agents to record scope gaps as open questions and wait for human approval.

#### Scenario: scope gap is detected

GIVEN an agent encounters a requirement that is not defined
WHEN it prepares a change proposal
THEN it SHALL record the gap as an open question and SHALL NOT invent a decision.
