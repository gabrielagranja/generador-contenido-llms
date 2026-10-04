# Tasks: SDD Harness Governance

## Phase 2 implementation tasks

- [ ] 1. Confirm the CI trigger policy and exact scope of commit/branch validation.
- [ ] 2. Fork the built-in OpenSpec spec-driven schema into openspec/schemas/sdd-governance.
- [ ] 3. Add schema instructions and templates for proposal, delta specs, design and tasks.
- [ ] 4. Point openspec/config.yaml to the project-local schema.
- [ ] 5. Define the explicit application-test command configuration file.
- [ ] 6. Implement the deterministic Python contract validator.
- [ ] 7. Add valid and invalid validator fixtures and automated tests.
- [ ] 8. Add a GitHub Actions workflow for schema, OpenSpec, contract and application-test validation.
- [ ] 9. Update CONTRIBUTING guidance with approved commit, branch and PR rules.
- [ ] 10. Run the full local verification set.
- [ ] 11. Push the workflow and confirm a GitHub Actions run.
- [ ] 12. Update traceability, daily log and Issue #37 with evidence.
- [ ] 13. Archive this change only after CI passes and human verification confirms the acceptance criteria.

## Preconditions

- Human approval of proposal, delta specification, design and tasks.
- Decision on CI trigger policy.
- Decision on whether commit/branch checks belong to this change.
