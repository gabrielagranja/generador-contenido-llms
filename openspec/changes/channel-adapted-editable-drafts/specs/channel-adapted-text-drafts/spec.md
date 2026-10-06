# Channel-Adapted Editable Text Drafts

## Purpose

Define the minimal textual drafting capability for Issue #23 on top of the approved Issue #22 brief and grounding contracts.

## ADDED Requirements

### Requirement: Consume the approved brief

The system MUST and SHALL accept the Issue #22 `GuidedBrief` and MUST and SHALL preserve its platform, format and fact-status constraints.

#### Scenario: Valid guided brief

- GIVEN a validated `GuidedBrief` selects Instagram or Facebook
- WHEN text drafting starts
- THEN the system selects the corresponding versioned channel template
- AND it does not redefine or silently fill material brief facts.

### Requirement: Versioned channel templates

The system MUST and SHALL use an explicit immutable template identifier and version for each selected channel.

#### Scenario: Template is selected

- GIVEN a supported channel and approved format are selected
- WHEN a draft is produced
- THEN the output records the template identifier and version
- AND the template instructions are appropriate to that channel.

### Requirement: Grounded editable draft

The system MUST and SHALL return editable text separated from evidence, assumptions and review notes.

#### Scenario: Grounded copy

- GIVEN material claims have confirmed or explicitly labelled evidence
- WHEN the draft is returned
- THEN the caption and CTA use only supported claims
- AND unresolved assumptions remain visible for human review.

#### Scenario: Unsupported claim

- GIVEN a proposed benefit, result, testimonial, statistic, deadline, scarcity, credential or guarantee lacks evidence
- WHEN text is drafted
- THEN the system omits or qualifies the claim
- AND does not invent replacement business facts.

### Requirement: Channel adaptation

The system MUST and SHALL adapt wording and structure for Instagram and Facebook while preserving the grounded core message.

#### Scenario: Both channels selected

- GIVEN the brief selects Instagram and Facebook
- WHEN drafts are returned
- THEN each channel has its own editable text package and template version
- AND the packages share the supported core message without assuming identical copy.

### Requirement: Approved format boundary

The system MUST and SHALL support text or creative-plan output for `single_image`, `carousel` and `reel` only.

#### Scenario: Visual or publication capability requested

- GIVEN a request would require rendered media, publication or scheduling
- WHEN this change is used
- THEN the system returns the editable text/plan boundary
- AND does not render, publish or schedule content.

### Requirement: Synthetic examples

The system MUST and SHALL be testable with the existing synthetic F-01, F-02 and F-03 fixtures without real business data.

#### Scenario: Ambiguous brief

- GIVEN F-02 or F-03 contains unknown material information
- WHEN text drafting is attempted
- THEN the result asks for focused clarification or returns a bounded editable draft with visible assumptions
- AND does not present unknown information as fact.
