## ADDED Requirements

### Requirement: Durable editorial content
The API SHALL persist reviewable editorial content locally and MUST restore it without changing its validated lifecycle, review data or evidence metadata.

#### Scenario: Restart preserves a draft
- GIVEN a draft has been generated or edited and saved
- WHEN a new store instance opens the same configured database
- THEN it restores the same content ID, review state, reviewer data, brand/business metadata and evidence provenance.

### Requirement: Durable editorial plans
The API SHALL persist validated editorial plans and MUST preserve strategy version, dated items and targets.

#### Scenario: Read a saved plan
- GIVEN a validated plan is saved
- WHEN the calendar integration requests that plan
- THEN it receives the validated plan with its dates and item metadata intact.

### Requirement: Local-only verification
Automated tests SHALL use isolated temporary databases and MUST not use an external database or provider.

#### Scenario: Offline persistence test
- GIVEN an isolated temporary database
- WHEN draft and plan persistence tests run
- THEN they verify durable behavior without network access.
