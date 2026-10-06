# Channel-Adapted Editable Text Drafts

## Purpose

Define the delta needed for Issue #23 on top of the approved Issue #22 brief and grounding contracts.

## ADDED Requirements

### Requirement: Consume the approved brief

The system MUST and SHALL accept the Issue #22 `GuidedBrief` and MUST and SHALL preserve its platform, format and fact-status constraints.

#### Scenario: Valid guided brief

- GIVEN a validated brief selects Instagram or Facebook
- WHEN drafting starts
- THEN the system selects the corresponding versioned channel template
- AND it does not redefine or silently fill material facts.

### Requirement: Versioned templates

The system MUST and SHALL use an immutable template identifier and version for each selected channel.

#### Scenario: Template selection

- GIVEN a supported channel and approved format are selected
- WHEN a draft is returned
- THEN the output records the template identifier and version
- AND the instructions match the selected channel.

### Requirement: Grounded editable output

The system MUST and SHALL return editable text separated from evidence, assumptions and review notes.

#### Scenario: Unsupported claim

- GIVEN a proposed benefit, result, testimonial, statistic, deadline, scarcity, credential or guarantee lacks evidence
- WHEN text is drafted
- THEN the system omits or qualifies the claim
- AND SHALL NOT invent a replacement business fact.

### Requirement: Channel adaptation

The system MUST and SHALL adapt wording and structure for Instagram and Facebook while preserving the grounded core message.

#### Scenario: Both channels selected

- GIVEN both channels are selected
- WHEN drafts are returned
- THEN each channel has its own editable text package and template version
- AND the packages do not assume identical copy is optimal.

### Requirement: Approved format boundary

The system MUST and SHALL support text or creative-plan output only for `single_image`, `carousel` and `reel`.

#### Scenario: Visual or publication request

- GIVEN a request requires rendered media, publication or scheduling
- WHEN this contract is used
- THEN the system stays within the editable text/plan boundary
- AND SHALL NOT render, publish or schedule content.

### Requirement: Synthetic examples

The system MUST and SHALL be testable with F-01, F-02 and F-03 without real business data.

#### Scenario: Unknown or ambiguous input

- GIVEN the fixture contains unknown material information
- WHEN drafting is attempted
- THEN the result asks focused questions or returns a bounded editable draft with visible assumptions
- AND SHALL NOT present unknown information as fact.
