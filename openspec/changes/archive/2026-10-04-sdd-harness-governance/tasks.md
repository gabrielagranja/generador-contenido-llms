# Tasks: SDD Harness Governance

## Phase 2 implementation tasks

- [x] 1. Confirm the CI trigger policy and exact scope of commit/branch validation. CI runs on pull requests and pushes to dev; commit/branch rules are deferred.
- [x] 2. Fork the built-in OpenSpec spec-driven schema into openspec/schemas/sdd-governance.
- [x] 3. Add schema instructions and templates for proposal, delta specs, design and tasks.
- [x] 4. Point openspec/config.yaml to the project-local schema.
- [x] 5. Define the explicit application-test command configuration file.
- [x] 6. Implement the deterministic Python contract validator.
- [x] 7. Add valid and invalid validator fixtures and automated tests.
- [x] 8. Add a GitHub Actions workflow for schema, OpenSpec, contract and application-test validation.
- [x] 9. Update CONTRIBUTING guidance with approved PR guidance and a reference to the deferred commit/branch convention change.
- [x] 10. Run the full local verification set.
- [x] 11. Push the workflow and confirm a GitHub Actions run.
- [x] 12. Update traceability, daily log and Issue #37 with evidence.
- [x] 13. Archive this change after CI passes and human verification confirms the acceptance criteria.

## Preconditions

- Approved on 2026-10-04.
- CI runs on pull requests and pushes to dev.
- Commit and branch checks are deferred to a separate OpenSpec change.
