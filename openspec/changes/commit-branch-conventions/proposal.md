# Define and Enforce Branch and Commit Conventions

## Status and human approval

- Status: Approved
- Issue: #38 — Define and enforce branch and commit conventions
- Decision record: Human approval recorded on 2026-10-04 for the proposed branch, title and description policy; implementation may proceed without GitHub rulesets.

## Plan objective

Support the Application foundation objective (#9, #21) with a reproducible development workflow that keeps branches and commits traceable to their work items.

## Objective

Define an agent-neutral convention for branch names, commit titles and commit descriptions, and prepare an automated validator that reports non-compliance without rewriting repository history.

## Scope

### Included

- Proposed naming format for implementation branches.
- Proposed Conventional Commit-style format for commit titles.
- Proposed required structure for commit descriptions, including rationale and Issue reference.
- Proposed validation in pull requests and pushes to `dev`.
- Documentation, positive fixtures and negative fixtures for the validator.
- Clear reporting of the invalid branch, commit title or commit body.

### Excluded

- Rewriting existing branches, commits or pull-request history.
- Automatic merge, approval or Issue closure.
- Automatic creation or enforcement of GitHub repository rulesets.
- Changes to application behavior, social-content publishing or roadmap priorities.

## Acceptance criteria

- The approved convention defines valid and invalid examples for branch names, commit titles and commit descriptions.
- The validator checks the pull-request source branch and relevant non-merge commits without modifying history.
- CI fails with a clear, actionable message when a proposed rule is violated.
- CI validates the implementation with positive and negative fixtures.
- The convention retains a direct Issue reference for each implementation branch and commit.
- GitHub rulesets remain a separate, explicitly approved administrative decision.

## Rubric

No aplica — the official rubric has not been supplied. This workflow-quality change will be remapped if a rubric criterion becomes applicable.

## Tests and verification

- Unit tests for valid and invalid branch names, commit titles and commit bodies.
- Integration-style tests that supply a commit range to the validator.
- CI evidence from a pull request and a push to `dev` after approval.
- Manual review that the workflow never rewrites history, approves work or publishes content.

## Open questions and blockers

- Proposed branch pattern: `[type]/[issue-number]-[short-slug]`, with types `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `build`, `revert` and `spike`.
- Proposed commit title: `[type]([optional-scope]): [summary] (#[issue-number])`; title length is proposed at 72 characters or fewer.
- Proposed commit description for every validated commit: a substantive `Why:` line and an `Issue: #[issue-number]` line.
- Human decision required: approve these proposed values, amend them, or request a less strict description rule before implementation.
- Human decision required: decide later whether proven CI checks should be supplemented with GitHub rulesets.

## Approval

Approved on 2026-10-04. Implementation may proceed in tasks.md order; GitHub rulesets remain a separate administrative decision.
