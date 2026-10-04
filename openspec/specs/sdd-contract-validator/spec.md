# SDD Contract Validator Specification

## Purpose

Preserve the distinction between active OpenSpec change contracts and completed archived contracts in the project-local deterministic validator.

## Requirements

### Requirement: standard archive exclusion

The required-field validator SHALL exclude only the directory named `archive` when it is a direct child of the configured OpenSpec changes root.

The validator MUST continue to inspect every other non-hidden directory beneath that root as an active change.

Archived directories and files MUST remain untouched by validation.

#### Scenario: archived contract is present

GIVEN the changes root contains `archive/2026-10-04-sdd-harness-governance/`
WHEN required-field validation runs
THEN the validator SHALL NOT require active-change artifacts from the `archive` directory.

#### Scenario: valid active change remains checked

GIVEN the changes root contains an `archive` directory and one valid active change
WHEN required-field validation runs
THEN the active change SHALL pass validation.

#### Scenario: invalid active change remains rejected

GIVEN the changes root contains an `archive` directory and one active change missing an Issue reference
WHEN required-field validation runs
THEN the validator MUST fail and report the active change error.

### Requirement: regression coverage

The validator test suite SHALL include fixtures or temporary directories covering standard archive exclusion and active-change enforcement.

The tests MUST run in the existing SDD GitHub Actions workflow.

#### Scenario: CI regression check

GIVEN the archive-exclusion implementation is complete
WHEN the SDD workflow runs
THEN the validator tests SHALL pass and the workflow MUST report success.
