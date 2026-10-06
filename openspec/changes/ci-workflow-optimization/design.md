# Design: Required CI efficiency

## Approach

1. Keep both workflow triggers for `pull_request` and `push` to `dev`; use workflow concurrency keyed by pull request number or ref so newer commits cancel older runs.
2. Remove the explicit unittest discovery step from SDD Harness because the configured pytest command discovers all current `unittest.TestCase` classes.
3. Configure the Python setup action to cache pip dependencies from `requirements.txt`. Leave the global OpenSpec npm installation uncached unless the repository provides a stable npm lockfile in scope.
4. Replace the two pull-request Git Convention validator steps with one invocation supplying `--branch` and `--range`. Keep the push range invocation for direct `dev` pushes.
5. Design the post-merge push decision so a skipped duplicate is represented by a successful job/check, not by a path-filtered or skipped required job. The implementation must use only GitHub-provided event/API data and must not alter branch protection.

## Required check preservation

The job display names remain unchanged:

- `Validate OpenSpec governance`
- `Validate branch and commit conventions`

No path filters will be added. No protection rules will be changed.

## Verification boundary

After approval, validate only the changed workflow YAML and affected test/contract behavior. Confirm the two job names and both event paths in the workflow files, then verify a PR targeting `dev` through GitHub Actions if repository connectivity and permissions permit.

## Safety and open questions

The post-merge detection must not rely solely on commit-message text, because that could misclassify direct pushes. If the repository API cannot provide a reliable association in workflow context, retain the push validation rather than weakening a required check.
