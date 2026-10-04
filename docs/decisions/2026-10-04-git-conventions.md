# Decision: Git Branch and Commit Conventions

- **Date:** 2026-10-04
- **Status:** Accepted
- **Issue:** #38
- **OpenSpec change:** commit-branch-conventions

## Decision

The repository enforces the following through GitHub Actions:

- Implementation branches use `[type]/[issue-number]-[short-slug]`.
- Non-merge commits use `[type]([optional-scope]): [summary] (#[issue-number])`.
- Every validated commit body includes a substantive `Why:` line and an `Issue: #[issue-number]` line matching the title reference.
- The validator checks Issue availability with the repository-scoped GitHub Actions token.
- Pull requests validate their source branch and commit range; pushes to `dev` validate newly pushed non-merge commits.

## Consequences

CI reports violations without rewriting commits, renaming branches, merging or approving pull requests. Existing history is not changed.

GitHub rulesets are deliberately deferred. They require a separate human-approved administrative change after the CI checks have proven reliable.
