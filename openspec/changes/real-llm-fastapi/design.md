# Design

## Boundary

The API owns provider credentials and creates the configured generator. The browser sends a validated `GuidedBrief` to FastAPI and receives only editable draft data. `DeterministicMockAdapter` remains the default when no provider key is configured.

## Runtime flow

1. Content Studio maps its local form to the approved `GuidedBrief` shape.
2. `POST /drafts` validates the request with Pydantic.
3. `build_text_generator` selects the mock or `ChatGroq` implementation from environment settings.
4. `ChannelAdaptedDraftService` builds the versioned channel prompt and returns editable text plus review metadata.
5. The API marks the response `pending_human_review`; no approval, copy/export or publication action is performed.

## Configuration and safety

- `python-dotenv` loads the ignored local `.env` for development.
- `GROQ_API_KEY` is never sent to Next.js, returned in responses or written to logs.
- CI and tests use the mock or an injected fake generator.
- Provider failures are represented as controlled API errors; unsupported content remains subject to the existing grounding and review rules.

## Verification boundary

The endpoint contract is verified with synthetic briefs and an injected generator. One manual Groq smoke test verifies the real provider path; it does not become an automated test and does not store the returned content as production evidence without review.
