# Design: SDD Harness Governance

## Technical approach

The implementation will fork the OpenSpec built-in spec-driven schema into a project-local schema under openspec/schemas/. The local schema will retain the proposal, specs, design and tasks artifacts while adding instructions and Markdown templates for the required project contract fields.

A small Python validator will inspect active changes in openspec/changes/. It will check field presence, placeholders, rubric form, explicit approval status and the relationship between approval status and completed tasks. The validator will be deterministic and agent-neutral; it will not use an LLM or infer semantic correctness.

GitHub Actions will install the pinned OpenSpec CLI and Python runtime, validate the schema, run OpenSpec validation, run the Python validator and run an application-test adapter. The adapter will fail clearly when there is no approved test command rather than masking the absence of tests.

## Components

| Component | Responsibility |
|---|---|
| Project-local OpenSpec schema | Defines artifact order, template paths and agent instructions. |
| Markdown templates | Make mandatory fields visible and consistent. |
| Python contract validator | Enforces deterministic minimum fields and approval gates. |
| Test fixtures | Demonstrate accepted and rejected contracts. |
| GitHub Actions workflow | Runs schema, OpenSpec, contract and application-test checks. |
| CONTRIBUTING guidance | Explains the workflow without locking it to a particular agent. |

## Validation rules

The validator will treat these as failures:

- missing or blank mandatory sections;
- template markers such as TODO, Pending or angle-bracket placeholders in required values;
- a rubric section without an official criterion or a concrete No aplica reason;
- completed implementation tasks while approval is not Approved;
- a missing Issue reference;
- a missing plan objective or test/evidence section.

The validator will not decide whether a proposal is valuable, whether an acceptance criterion is sufficient, or whether an OpenSpec review proves code correctness.

## CI test-command adapter

The initial adapter will look for an explicitly configured project command. Its exact contract is pending approval:

- Option A: a repository file declaring the command.
- Option B: conventional manifests such as package.json or pyproject.toml.
- Option C: CI requires an explicit command input before it is enabled.

Recommendation: Option A, because it is explicit, portable and cannot silently choose an incorrect test suite.

## Safety boundaries

- No secrets are required by the harness.
- No social publishing or external provider call is allowed in the workflow.
- CI is a quality gate, not human approval.
- GitHub rulesets remain a manual repository-administration decision.
