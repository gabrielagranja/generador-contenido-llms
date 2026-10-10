## ADDED Requirements

### Requirement: Explicit local provider selection
The API SHALL support explicit Ollama selection through the existing TextGenerator interface and MUST preserve mock/Groq behavior without automatic cloud fallback.

#### Scenario: Local generation
- GIVEN LLM_PROVIDER=ollama and an explicit model and valid endpoint
- WHEN a draft is requested
- THEN the API sends a nonstreaming local chat request with the configured timeout, temperature and validated output budget
- AND returns the actual provider/model with pending human review and existing grounding metadata.

### Requirement: Controlled local provider failure
The API SHALL report controlled local provider failures and MUST avoid silently calling Groq.

#### Scenario: Unavailable or malformed local response
- GIVEN the configured Ollama service is unavailable or returns invalid message content
- WHEN generation is requested
- THEN the API returns a controlled error without persisting an approved draft or invoking another provider.

### Requirement: Offline verification
Automated tests SHALL use fake transports and MUST avoid real provider calls or downloads.

#### Scenario: Verification without Ollama
- GIVEN no installed Ollama service or model
- WHEN the automated suite runs
- THEN configuration, request budget, response and failure behavior are verified offline.
