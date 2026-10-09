# Frontend Editorial Workspace Specification

## ADDED Requirements

### Requirement: brand-independent workspace

The web client MUST separate platform identity from brand data and SHALL scope all dashboard, draft and brief content to the selected brand or associated business.

#### Scenario: switching context

GIVEN a brand with associated businesses is selected
WHEN the user selects another associated business
THEN the dashboard, drafts and brief SHALL show only that business's synthetic data.

### Requirement: local editorial governance in the interface

The web client SHALL NOT approve content by generation, manual editing or brief changes, and SHALL allow approval only from pending review through an explicit human action.

#### Scenario: brief changes after review

GIVEN a draft is pending review or approved in the prototype
WHEN the brief changes
THEN the state SHALL become brief-changed and the draft SHALL require a new review.

#### Scenario: editing approved text

GIVEN a draft is approved in the prototype
WHEN its text is edited
THEN its local approval SHALL be invalidated and it SHALL require a new review.

#### Scenario: invalid transition

GIVEN a draft is not pending review
WHEN approval is requested
THEN the state SHALL remain unchanged.

### Requirement: honest synthetic data

The web client SHALL label synthetic data, SHALL NOT present internal editorial counts as social analytics, and SHALL NOT enable copy, export or publication from the local prototype.

#### Scenario: placeholder sections

GIVEN a section is outside the functional MVP
WHEN the user opens it
THEN the page SHALL identify it as a placeholder without simulated functionality.

#### Scenario: session draft appears in the workspace

GIVEN a user prepares a synthetic draft
WHEN the user opens Borradores during the same browser session
THEN the draft SHALL appear with its current local editorial status and remain labelled as session-only data.
