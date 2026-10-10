# Real LLM generation through FastAPI

## ADDED Requirements

### Requirement: Provider-neutral real generation

The API MUST and SHALL support a configured Groq chat model behind the existing `TextGenerator` interface and MUST retain the deterministic mock when no provider is configured.

#### Scenario: Groq provider configured

- GIVEN `LLM_PROVIDER=groq`, a non-empty `GROQ_API_KEY` and an active `GROQ_MODEL`
- WHEN the API builds its text generator
- THEN it uses a LangChain-compatible Groq runnable
- AND the provider credential remains server-side.

#### Scenario: Offline default

- GIVEN no provider credential is configured
- WHEN the API builds its text generator
- THEN it uses the deterministic mock
- AND no external provider call is required.

### Requirement: Draft API contract

The API MUST and SHALL expose `POST /drafts` accepting a validated `GuidedBrief` and MUST return editable channel-adapted drafts with provider/model metadata and `pending_human_review` state.

#### Scenario: Valid brief

- GIVEN a valid guided brief selecting an approved platform and format
- WHEN the client posts it to `/drafts`
- THEN the response contains editable caption text, template metadata and review notes
- AND the response state is `pending_human_review`.

#### Scenario: Invalid brief

- GIVEN a brief that fails the approved Pydantic contract
- WHEN the client posts it to `/drafts`
- THEN the API returns a validation error
- AND it does not invoke the generator.

### Requirement: Credential and approval boundary

The API MUST and SHALL NOT return provider credentials and MUST NOT mark generated content as approved or publish it.

#### Scenario: Generated content

- GIVEN a provider returns draft text
- WHEN the API responds
- THEN no API key appears in the response
- AND the content remains pending human review.
