# Contributing and Agent Workflow

This repository uses OpenSpec-based Specification-Driven Development.

1. Read the canonical project documents under docs/.
2. Identify or create the GitHub Issue.
3. Create openspec/changes/<change-name>/ with proposal, delta specs, design and tasks.
4. Record unknown scope as pending questions; do not infer answers.
5. Obtain explicit human approval.
6. Implement only the approved tasks, in order.
7. Run OpenSpec validation, the required-field validator and configured code tests.
8. Update evidence and traceability.
9. Archive the completed OpenSpec change only after verification and CI.

Pull requests MUST link the Issue, OpenSpec change, verification evidence and any open questions. Commit and branch conventions are deferred to a separate approved OpenSpec change. Instagram publication always requires explicit human confirmation.

## Branch and commit conventions

For each implementation change, create a branch named:

```
[type]/[issue-number]-[short-slug]
```

Allowed branch types are `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `build`, `revert` and `spike`.

Every non-merge commit MUST have a title of at most 72 characters:

```
[type]([optional-scope]): [summary] (#[issue-number])
```

Its description MUST include:

```
Why: concise reason for the change.
Issue: #[issue-number]
```

CI validates the source branch and relevant non-merge commits. It reports violations and never rewrites commits, renames branches, approves pull requests or publishes content. GitHub rulesets are not enabled by this workflow.
