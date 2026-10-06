# Optimize required CI execution

## Status and human approval

- Status: Approved
- Issue: #12 — Quality, evaluation & delivery
- Decision record: 2026-10-06 — user approval recorded in project conversation

## Plan objective

Reduce GitHub Actions time and repeated validation on `dev` while preserving all required coverage and check contexts.

## Objective

Optimize only `.github/workflows/sdd-harness.yml` and `.github/workflows/git-conventions.yml` by removing duplicate test discovery, consolidating convention validation, cancelling superseded PR runs, adding low-maintenance dependency caching, and avoiding full reruns after PR integration into `dev`.

## Scope

### Included

- The two requested GitHub Actions workflows.
- The existing authoritative pytest command and validator CLI behavior.
- Required check names and direct-push validation.

### Excluded

- `main`, branch-protection rules, scripts, application code, unrelated workflows, and path filters.

## Acceptance criteria

- The SDD Harness executes the configured authoritative test command once; pytest still discovers all existing `unittest.TestCase` suites.
- The Git Conventions workflow validates the pull-request branch and commit range with one validator invocation.
- New commits cancel older in-progress runs for the same pull request.
- Python dependency caching uses `requirements.txt` as its key without introducing an unrelated lockfile or custom maintenance.
- A push to `dev` associated with a pull request does not repeat the complete PR validation, while direct pushes retain necessary validation.
- The required check names remain `Validate OpenSpec governance` and `Validate branch and commit conventions`.
- No path filters, protection changes, main-branch changes, merges, or unrelated workflow changes are introduced.

## Rubric

No aplica: this CI-only change is linked to delivery-quality Issue #12 and has no separate product rubric criterion in the requested scope.

## Tests and verification

- Validate both workflow files as YAML.
- Run the SDD contract validator.
- Run the affected contract and Git convention test modules.
- Verify the two required job names, PR triggers, direct `dev` push path, concurrency, and PR-associated push gate.
- Verify the resulting checks on a pull request targeting `dev` when repository connectivity permits.

## Open questions and blockers

- Resolved: GitHub's `listPullRequestsAssociatedWithCommit` API is used for push-event association, with `pull-requests: read` permission.
- Resolved: if the push is associated with a pull request, the existing job remains present and succeeds after the gate while expensive validation steps are skipped; direct pushes execute normally.

## Approval

Approved on 2026-10-06. Implementation may proceed in `tasks.md` order.
