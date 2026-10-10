# Spec Delta

## Purpose

Define a bounded, configurable output-token contract for channel-specific draft generation without changing grounding, review, or provider-selection behavior.

## ADDED Requirements

### Requirement: Configurable output budget

The draft-generation configuration MUST expose a default maximum output-token budget of 350 and an absolute maximum of 600.

#### Scenario: Default budget is used

GIVEN no output-token override is configured
WHEN a draft-generation request is prepared
THEN the provider adapter receives a maximum output-token value of 350

#### Scenario: Valid override is used

GIVEN an output-token override is configured with a positive value no greater than 600
WHEN a draft-generation request is prepared
THEN the provider adapter receives that configured value

#### Scenario: Invalid override is rejected

GIVEN an output-token override is zero, negative, non-numeric, or greater than 600
WHEN application configuration is loaded
THEN configuration loading fails safely with a clear validation error

### Requirement: Provider-level enforcement

The Groq model adapter SHALL receive the validated maximum output-token budget as a provider/model configuration value.

#### Scenario: Groq adapter receives the budget

GIVEN the Groq provider is selected and a valid output budget is configured
WHEN the model adapter is constructed
THEN the Groq model configuration contains the expected maximum output-token value

#### Scenario: No post-generation truncation

GIVEN the provider returns generated text
WHEN the draft response is assembled
THEN the application does not truncate the text as a substitute for provider-level output limiting

### Requirement: Channel-aware concise contracts

The drafting prompt SHALL include concise, channel-specific output guidance for Instagram and Facebook while preserving factual grounding, source attribution, Spanish as the default output language, configured Catalan support, and prohibition of unsupported commercial claims.

#### Scenario: Instagram contract remains isolated

GIVEN an Instagram draft request
WHEN the prompt is assembled
THEN it contains the Instagram-specific concise output contract and does not apply the Facebook contract

#### Scenario: Facebook contract remains isolated

GIVEN a Facebook draft request
WHEN the prompt is assembled
THEN it contains the Facebook-specific concise output contract and does not apply the Instagram contract

### Requirement: Existing review and grounding contracts remain unchanged

The draft pipeline SHALL preserve retrieved evidence, supported and unsupported claim metadata, human-review state, and editorial state transitions when an output budget is configured.

#### Scenario: Grounding metadata is preserved

GIVEN a RAG-enabled draft request with a valid output budget
WHEN the draft is generated through a mock or fake provider
THEN grounding evidence and unsupported-claim metadata remain available and unchanged

#### Scenario: Human review remains required

GIVEN a draft generated with an output budget
WHEN the draft is returned
THEN it remains an editable draft requiring the existing human-review flow
