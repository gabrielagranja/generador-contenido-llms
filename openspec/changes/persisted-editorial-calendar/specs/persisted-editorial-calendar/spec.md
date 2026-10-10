## ADDED Requirements

### Requirement: Read-only persisted calendar
The web client SHALL render persisted editorial plans and MUST not schedule or publish content.

#### Scenario: Load saved plans
- GIVEN persisted plans exist
- WHEN the calendar view opens
- THEN it shows dated plan item metadata from the plans API.

### Requirement: Explicit calendar loading failures
The calendar SHALL expose loading, empty and error states.

#### Scenario: Plans API unavailable
- GIVEN the plans API request fails
- WHEN the calendar view opens
- THEN the user sees an actionable error and no lifecycle state changes.

### Requirement: Validated plan saving
Content Studio SHALL send only validated plan payloads to the plans API.

#### Scenario: Save a plan
- GIVEN a validated editorial plan
- WHEN the user saves it
- THEN it is persisted without generating, approving, scheduling or publishing content.
