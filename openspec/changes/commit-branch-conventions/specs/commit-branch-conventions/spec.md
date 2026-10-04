# Spec Delta

## Purpose

Define the proposed, human-approved repository behavior for branch names, commit titles and commit descriptions, together with non-destructive CI validation.

## ADDED Requirements

### Requirement: traceable branch names

After human approval, every implementation branch SHALL match `<type>/<issue-number>-<short-slug>`.

The `type` MUST be one of `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `build`, `revert` or `spike`.

The `issue-number` MUST be the decimal identifier of an existing GitHub Issue, and `short-slug` MUST be lowercase kebab-case describing the branch purpose.

The protected base branches `dev` and `main` MUST NOT be evaluated as implementation branch names.

#### Scenario: valid implementation branch

GIVEN an approved issue numbered 38
WHEN an agent creates a branch for the convention validator
THEN the branch SHALL be named `ci/38-enforce-git-conventions`.

#### Scenario: invalid implementation branch

GIVEN an implementation branch named `feature/fix-stuff`
WHEN the branch validator runs after approval
THEN it MUST fail and report the required `<type>/<issue-number>-<short-slug>` format.

### Requirement: traceable commit titles

After human approval, every validated non-merge commit SHALL have a title matching `<type>(<optional-scope>): <summary> (#<issue-number>)`.

The title `type` MUST be one of `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `build` or `revert`.

The summary MUST be substantive, and the complete title MUST contain at most 72 characters.

#### Scenario: valid commit title

GIVEN an approved Issue 38
WHEN a developer creates a CI commit
THEN the title SHALL be `ci: add git convention validation (#38)`.

#### Scenario: invalid commit title

GIVEN a commit title `update stuff`
WHEN the commit-title validator runs after approval
THEN it MUST fail and identify the expected title structure.

### Requirement: commit descriptions

After human approval, every validated non-merge commit MUST include a commit description with one substantive `Why:` line and one `Issue: #<issue-number>` line.

The Issue number in the description MUST match the Issue reference in the commit title.

#### Scenario: complete commit description

GIVEN a commit title referencing Issue 38
WHEN its body contains `Why: prevent untraceable changes in repository history.` and `Issue: #38`
THEN the commit SHALL pass commit-description validation.

#### Scenario: missing rationale

GIVEN a non-merge commit has no `Why:` line
WHEN the commit-description validator runs after approval
THEN it MUST fail and report the missing rationale.

### Requirement: non-destructive CI validation

After human approval, CI SHALL validate the source-branch name and non-merge commits in each pull request, and SHALL validate newly pushed non-merge commits on `dev`.

The validator MUST report each offending branch or commit without rewriting history, approving a pull request, merging work, closing Issues or publishing content.

CI MUST include positive and negative fixtures for the branch, title and description rules.

#### Scenario: pull request violates a rule

GIVEN a pull request contains a commit with an invalid title
WHEN the convention workflow runs
THEN CI MUST fail with the offending commit identifier and the violated rule.

### Requirement: approval-gated rollout

While this change is Pending or Rejected, the repository MUST NOT add or activate its branch/commit validator, CI workflow or GitHub ruleset.

A GitHub ruleset MUST remain a separate, explicit human administrative decision after CI validation is proven.

#### Scenario: proposal awaits approval

GIVEN the convention contract is Pending
WHEN an agent reads its tasks
THEN the agent SHALL wait for human approval and MUST NOT implement the validator.
