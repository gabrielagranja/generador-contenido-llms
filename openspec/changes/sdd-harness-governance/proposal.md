# Establish SDD Harness Governance

## Status and human approval

- Status: Pending human approval
- Issue: #37 — Establish project source of truth and OpenSpec SDD structure
- Decision record: Pending after Phase 1 review

## Plan objective

Establish a reliable, agent-neutral governance harness so that future changes are proposed, approved, implemented and verified with traceability.

## Objective

Add a project-local OpenSpec schema, templates, contract validator and GitHub Actions workflow that make the project source-of-truth rules executable.

## Scope

### Included

- Custom OpenSpec schema based on the built-in spec-driven workflow.
- Templates for proposal, delta specification, design and tasks.
- Required traceability fields: Issue, plan objective, acceptance criteria, rubric, tests/evidence, scope, open questions and human approval.
- A validator for required fields and approval gates.
- CI checks for schema validity, active OpenSpec changes, required fields and configured code tests.
- Contributing guidance for commits, branches and pull requests.

### Excluded

- Application features.
- Automatic changes to GitHub Project priorities or decisions.
- Automatic approval of scopes or specifications.
- Automatic Instagram or Facebook publishing.
- Enforcement of GitHub repository rulesets; that remains a separate human-admin action after the workflow is proven.

## Acceptance criteria

- Every active implementation change has the mandatory contract fields.
- A change marked Pending cannot be treated as ready to implement by the validator.
- The schema and templates are project-local and usable by Codex, Claude and other agents.
- CI runs OpenSpec validation, the required-field validator and configured tests when they exist.
- Missing application tests do not get silently reported as passing.
- The workflow does not publish content or alter roadmap priorities.

## Rubric

No aplica — the official rubric has not been supplied. This governance change records process evidence but MUST be remapped if the rubric introduces an applicable criterion.

## Tests and verification

- Positive and negative fixtures for the required-field validator.
- Schema validation.
- OpenSpec validation for active changes.
- Workflow syntax review and a CI execution after implementation.
- Manual review that the workflow cannot approve scope or publish content.

## Open questions and blockers

- Which branch events must run CI: pull requests only, push to dev, or both?
- Which exact code-test command is authoritative once the application manifests exist?
- Should commit-body rules be part of this change or a separate contract?
- The official rubric and Project #1 phase ordering are still unavailable.

## Approval

Pending. Do not implement the tasks until explicit human approval is recorded.
