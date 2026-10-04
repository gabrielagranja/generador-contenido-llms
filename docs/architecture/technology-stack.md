# Approved MVP technology stack

**Decision status:** Approved provisionally on 4 October 2026. Recheck provider availability, API permissions, pricing, and free-tier terms when implementation begins.

## Product scope this stack supports

- Generate platform-specific copy for **Instagram and LinkedIn**.
- Generate one accompanying image and let the content manager preview and revise it.
- Connect one authorized **Instagram Professional** account for the first publishing integration.
- Require a clear human confirmation before each Instagram publish. No unattended or scheduled publishing in the first slice.
- Offer a voice mode for briefing, drafting, and revising content.
- Use a small RAG pipeline for approved business information.
- Compare two text model configurations using the same evaluation briefs.

The first functional slice is one representative/authorized business, Instagram feed image posts, and LinkedIn copy. Direct LinkedIn publishing is outside the first slice.

## Stack

| Layer | Choice | Responsibility |
| --- | --- | --- |
| Web client | Next.js, React, TypeScript | Brief editor, channel selector, draft/image preview, voice controls, OAuth connection and human approval UI. |
| API backend | Python 3.11+, FastAPI, Pydantic | Validates requests, orchestrates generation and retrieval, handles OAuth callbacks, and exposes controlled publishing actions. |
| LLM application framework | LangChain | Prompt templates, chat-model adapters, and the retrieval chain used for the rubric's framework/RAG evidence. |
| Primary text model | Groq via `langchain-groq` | Draft and adapt content for Instagram and LinkedIn. Use the free tier during development where current quotas allow. |
| Comparison text model | Gemini via `langchain-google-genai` | Run the same brief and prompt set as Groq for a small, documented quality comparison. |
| RAG | Chroma persistent local store, with local multilingual Sentence Transformers embeddings | Retrieve relevant approved business facts, tone guidance, product details, restrictions, and examples without a separate embeddings API call. |
| Image generation | Gemini API, `gemini-3.1-flash-image`, through Google's Gen AI SDK | Generate one social image from the approved brief/copy and provide it for preview. |
| Voice agent | Gemini Live API through the Google Gen AI SDK | Bidirectional voice interaction for entering a brief and asking for revisions. Voice tools can draft, generate an image, and revise; they cannot publish without the explicit approval step. |
| Initial social connector | Instagram Platform API with OAuth | Connect one client-authorized Business or Creator account and publish approved feed content. Keep LinkedIn generation separate from the initial publishing connector. |
| Application data | SQLite + SQLAlchemy | Persist the single-business profile, drafts, and connection metadata for the proof of concept. |
| Secret handling | Environment secrets; encrypt persisted OAuth tokens with a server-side encryption key | Keep API keys and social tokens out of the repository and browser bundle. Never commit `.env`. |
| Media storage | Persistent local media directory for local development; object-storage adapter for hosted deployment | Preserve generated images and provide the upload flow required by the selected social API. Choose the hosted storage provider when deployment constraints are known. |
| Tests and packaging | pytest, GitHub Actions, Docker Compose | Run unit/API tests with external providers mocked, then package the web client and API for reproducible local setup. |

## Boundaries and operating rules

- The LLM service exposes one provider-neutral text-generation interface so the primary provider can be changed without rewriting the UI.
- Keep the social connector behind a separate service interface. Request only permissions required for the chosen Instagram action.
- The content manager reviews both text and image. A visible final confirmation is required before a post is sent to Instagram.
- Treat model output as a draft. Do not invent product facts; retrieve factual claims from the business profile or ask for clarification.
- Use synthetic or explicitly approved business data while evaluating free API tiers. The current Gemini pricing page marks Free Tier content as used to improve products; verify data terms and account settings before sending real client data.
- Check current quotas in the provider consoles. Groq free-tier requests are rate-limited; handle quota errors with a useful message and retry guidance.
- Gemini 3.1 Flash Image currently lists a paid rate equivalent to about **$0.067 per 1K image**. Budget one image per draft initially and recheck prices before implementation.
- Use fake/mocked OAuth responses in automated tests; test actual publishing only with an authorized test/professional account.
- The hosted demo must use HTTPS, a persistent place for required state/media, and WebSocket support for the voice session. Hosting vendor is not selected yet.

## Evaluation plan

Use the same small set of representative briefs for Groq and Gemini text generation. Score each output for factual fidelity to retrieved context, platform fit, tone, usefulness, editing effort, latency, and recorded API cost/usage. Keep representative inputs, prompts, outputs, and scores in the repository without exposing client secrets or unapproved business data.

## Verified provider documentation

- [LangChain ChatGroq integration](https://reference.langchain.com/python/langchain-groq/chat_models/ChatGroq)
- [LangChain Google Gen AI integration](https://reference.langchain.com/python/langchain-google-genai/langchain_google_genai)
- [Chroma Python client and persistent client](https://docs.trychroma.com/reference/python)
- [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini Live API quickstart](https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk)
- [Meta Instagram API collection](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api)
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-06)
