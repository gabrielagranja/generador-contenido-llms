# Required CI efficiency

## MODIFIED Requirements

### Requirement: authoritative application test execution

The SDD Harness SHALL run the configured application test command as the sole test discovery invocation when that command is present. It MUST retain discovery of the repository's existing unittest suites through the configured pytest command.

#### Scenario: configured pytest covers unittest suites

GIVEN the configured command is `python -m pytest -q`
WHEN the SDD Harness runs application tests
THEN it SHALL execute the test suite once through that command
AND SHALL NOT run a separate `unittest discover` invocation.

### Requirement: consolidated pull-request convention validation

The Git Conventions workflow SHALL invoke `validate_git_conventions.py` once for each pull request, passing both the source branch and the pull-request commit range, and SHALL continue validating newly pushed commits on `dev`.

#### Scenario: pull request validation

GIVEN a pull request targets `dev`
WHEN the Git Conventions workflow runs
THEN one validator invocation SHALL validate both the branch and commit range
AND the check name SHALL remain `Validate branch and commit conventions`.

### Requirement: superseded pull-request run cancellation

Both required workflows SHALL cancel an in-progress run for the same pull request when a newer commit triggers a replacement run.

#### Scenario: new pull-request commit

GIVEN a pull request has an in-progress workflow run
WHEN a newer commit is pushed to that pull request
THEN the older run SHALL be cancelled
AND the newer run SHALL retain the same required check name.

### Requirement: non-duplicative dev push validation

The workflows SHALL avoid repeating the complete pull-request validation on a `dev` push that is attributable to a pull request, while retaining the necessary validation for a direct push to `dev`. Required checks SHALL conclude successfully and SHALL NOT become pending because of path or event filters.

#### Scenario: direct push to dev

GIVEN commits are pushed directly to `dev` without an associated pull request
WHEN the workflows run
THEN the necessary push validation SHALL execute
AND both required check names SHALL remain available.

#### Scenario: pull-request integration push

GIVEN a pull request has already passed the required checks
WHEN its merge produces a push to `dev`
THEN the workflows SHALL not repeat the complete pull-request validation
AND the required check contexts SHALL conclude without blocking the branch.

### Requirement: low-maintenance dependency caching

The SDD Harness SHOULD cache Python dependencies using the existing requirements file as the cache key when supported by the setup action. It SHALL NOT add a cache mechanism whose key or invalidation requires unrelated lockfiles or custom maintenance.

#### Scenario: requirements change

GIVEN `requirements.txt` changes
WHEN the SDD Harness runs
THEN the dependency cache key SHALL change and dependencies SHALL be reinstalled.
