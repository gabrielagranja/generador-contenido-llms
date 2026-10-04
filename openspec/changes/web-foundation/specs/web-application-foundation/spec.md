# Web Application Foundation Specification

## ADDED Requirements

### Requirement: runnable full-stack foundation

The repository SHALL provide a runnable web foundation with a Next.js/React/TypeScript client and a Python 3.11+/FastAPI/Pydantic API aligned with the approved technology-stack decision.

#### Scenario: clean checkout starts the foundation

GIVEN a developer has a clean checkout and the documented local prerequisites
WHEN the developer follows the documented setup and run commands
THEN the web client and API SHALL start locally without requiring social-provider credentials.

#### Scenario: web client reaches the API

GIVEN the client and API are running locally
WHEN the developer opens the documented client URL
THEN the client SHALL render the foundation page and SHALL be able to obtain the API readiness response.

### Requirement: deterministic API readiness

The API SHALL expose a deterministic health or readiness endpoint that reports local application readiness without invoking an external provider.

#### Scenario: readiness succeeds without provider credentials

GIVEN no Groq, Gemini, Meta or other provider credentials are configured
WHEN a client requests the readiness endpoint
THEN the API SHALL return a successful response that identifies the local foundation as ready.

### Requirement: environment-safe configuration

The application MUST load runtime configuration from environment variables and MUST provide a safe `.env.example` containing names and non-secret examples only.

The repository MUST NOT contain real API keys, OAuth tokens or other provider secrets.

#### Scenario: missing optional provider credentials

GIVEN the application is started without provider credentials
WHEN the local foundation path is exercised
THEN the application SHALL remain usable for readiness and foundation checks and SHALL explain which credentials are required only for provider-backed features.

### Requirement: provider-neutral LLM boundary

The API SHALL expose a provider-neutral service boundary for future generation work and SHALL identify the approved LangChain integration point.

The foundation MUST keep external provider calls behind that boundary and MUST NOT invoke them during baseline automated tests.

#### Scenario: provider calls are isolated

GIVEN a foundation test exercises the LLM service boundary
WHEN the test runs with external providers unavailable
THEN the test SHALL use a mock or deterministic adapter and SHALL complete without a network call.

### Requirement: authoritative application tests

The repository SHALL configure `python -m pytest -q` as the authoritative application test command in `.github/sdd-harness.yml`.

#### Scenario: CI runs the configured test command

GIVEN the foundation test command is configured
WHEN the SDD harness runs its application-test adapter
THEN CI SHALL execute `python -m pytest -q` and SHALL report its actual result.

### Requirement: documented development contract

The repository SHALL document the project structure, prerequisites, environment setup, run commands, test command and known scope boundaries.

#### Scenario: another agent follows the documentation

GIVEN Codex, Claude or another agent reads the repository documentation
WHEN the agent prepares to run or extend the foundation
THEN the documentation SHALL identify the relevant client, API, configuration, tests and OpenSpec contract locations.

### Requirement: publication safety boundary

The foundation MUST NOT publish to Instagram or Facebook, schedule posts or bypass explicit human approval.

#### Scenario: no publishing is exposed by the foundation

GIVEN only the foundation change is implemented
WHEN a developer runs the local foundation or its tests
THEN no social-platform publication request SHALL be sent.
