# Design: Branch and Commit Conventions

## Approach

After approval, implement a repository-local Python validator so agents and developers use the same deterministic rules without depending on a workstation hook. Store rule parameters in a small checked-in configuration file and expose the validator through a dedicated GitHub Actions workflow.

The workflow will use full Git history. For pull requests it will validate the head branch and the commits in the pull-request range. For pushes to `dev`, it will validate the newly pushed non-merge commits. Merge commits will be excluded because their generated metadata is controlled by GitHub merge strategy; squash-merge titles remain covered through the pull-request title/commit policy during implementation.

## Validation model

- Parse branch names with a configured regular expression.
- Parse commit subjects and bodies with deterministic regular expressions and clear diagnostics.
- Require `Why:` and `Issue:` fields in each validated body.
- Confirm the Issue number is consistent between a commit subject and its body.
- Never amend commits, rename branches, approve PRs or mutate GitHub project state.
- Test the parser with repository fixtures before enabling CI enforcement.

## Proposed components

- `scripts/validate_git_conventions.py`: parser and command-line validator.
- `.github/git-conventions.yml`: explicit policy values and accepted types.
- `tests/test_validate_git_conventions.py` plus valid and invalid fixtures.
- `.github/workflows/git-conventions.yml`: validation on pull requests and pushes to `dev`.
- `CONTRIBUTING.md`: human and agent-facing examples.

## Trade-offs

A local hook gives earlier feedback but cannot be relied upon across Codex, Claude and other agents. CI is authoritative and portable, but reports violations after a push. The approved implementation may add optional local guidance later; it will not make developer setup a prerequisite.

GitHub rulesets can reject disallowed branch names server-side, but they are account-level administration and less suitable for inspecting commit bodies. Keep them outside this change until the CI validator is proven.

## Verification boundary

OpenSpec validation will review artifact consistency. Unit and integration-style tests will verify parsing behavior. A successful workflow proves that the checks ran; it does not prove that all future human-written descriptions are semantically useful beyond the deterministic requirements.

## Open questions

The proposed subject-length limit, exact accepted types and universal body requirement await approval in `proposal.md`. They are intentionally not enforced while this contract is Pending.
