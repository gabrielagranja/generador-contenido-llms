# Decision Record — SDD Harness Governance

**Date:** 2026-10-04  
**Issue:** #37  
**Status:** Approved

## Context

The project needs an agent-neutral, repository-local SDD harness before application development. The source-of-truth structure exists, but its minimum contract and verification rules needed executable checks.

## Options considered

1. Keep the built-in OpenSpec schema without project templates.
2. Add a project-local schema, deterministic validator and GitHub Actions workflow.
3. Enforce all governance, including commit/branch conventions, in one large change.

## Decision

Adopt option 2. CI runs on pull requests and pushes to dev. The project uses the local sdd-governance schema and a deterministic Python contract validator. Commit and branch conventions are deferred to a separate OpenSpec change.

## Consequences

- Future implementation changes must use the project-local templates and explicit approval status.
- CI validates the schema, active OpenSpec changes, required contract fields and the configured test command.
- Until an application test command is configured, CI emits an explicit warning and skipped state rather than claiming application tests passed.
- CI cannot approve scope, change roadmap priorities or publish social content.

## Evidence

- OpenSpec change: openspec/changes/sdd-harness-governance/
- Passing workflow run: https://github.com/gabrielagranja/generador-contenido-llms/actions/runs/37229401537

## Revisit trigger

Revisit when the official rubric, application test suite, or GitHub repository ruleset policy becomes available.
