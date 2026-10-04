# LLM Content Generation MVP

> A portfolio project that explores and validates an LLM-assisted social-content workflow for a network of 20+ small businesses.

## Status

**Current phase: Discovery & validation.** The initial channels and a provisional implementation stack have been selected; implementation scope and external account access still need to be made reproducible.

This repository documents an end-to-end solo product-development process: marketing and product discovery, UX/UI design, LLM application development, evaluation, and portfolio communication.

## Real-world context

The project is grounded in a real content-management workflow for a network of more than 20 small local businesses.

- **Primary user:** a digital content manager and copywriter who coordinates social communication across the network.
- **Potential secondary users:** business owners or staff with limited social-media confidence. Their role—information contributor, reviewer, approver, or direct user—must be validated.
- **Content audience:** each business's customers and local community. They consume the content but are not expected to use the MVP directly.

## Problem hypothesis

Business information can arrive incomplete, unstructured, or late. Turning it into accurate, channel-appropriate copy may require repeated clarification, adaptation, review, and rework.

The hypothesis is that a guided, human-in-the-loop workflow with reusable business context can help the content manager transform a lightweight brief into editable, platform-specific content more efficiently than the current process or generic AI prompting alone.

This is a hypothesis, not a conclusion. The project will compare the proposed workflow with current workarounds and general AI tools.

## MVP scope

The initial functional slice lets the content manager:

1. Capture a structured brief: topic, audience, platform, business context, and optional notes.
2. Identify missing or ambiguous information before generation.
3. Generate editable copy adapted to **Instagram and LinkedIn**.
4. Retrieve relevant, approved business context through a small RAG pipeline.
5. Generate and preview one image for an Instagram feed post.
6. Use an optional voice mode to enter briefs and request draft revisions.
7. Connect one authorized Instagram Professional account and publish only after explicit human approval.

The first slice uses one representative/authorized business. LinkedIn content generation is included; direct LinkedIn publishing is not part of the first slice. Voice interaction can create and revise drafts, but it cannot publish without the same explicit approval step.

## Approved provisional technology stack

| Layer | Choice | Responsibility |
| --- | --- | --- |
| Web client | Next.js, React, TypeScript | Brief and draft UI, image preview, voice controls, OAuth connection, and approval flow. |
| Backend | Python 3.11+, FastAPI, Pydantic | Request validation, generation/RAG orchestration, OAuth callbacks, and controlled publishing actions. |
| LLM framework | LangChain | Prompt templates, model adapters, and RAG workflow. |
| Text models | Groq primary; Gemini comparison | Generate channel-specific drafts and compare both providers on the same briefs. Free quotas are limited and must be checked. |
| RAG | Chroma local store + local multilingual embeddings | Retrieve business facts, tone, products, restrictions, and approved examples. |
| Image generation | Gemini API, Gemini 3.1 Flash Image | Generate a draft image for preview. Current API pricing is about $0.067 per 1K image; verify pricing before implementation. |
| Voice | Gemini Live API | Bidirectional voice interaction for creating and revising content. |
| Social integration | Instagram Platform API with OAuth | Connect one authorized Business or Creator account; user confirms each publish. |
| Persistence and delivery | SQLite, encrypted OAuth tokens, persistent media storage, pytest, GitHub Actions, Docker Compose | Store MVP data safely, test the application, and make local setup reproducible. |

The detailed rationale, provider documentation, cost notes, privacy boundaries, and evaluation plan are in [Technology Stack](docs/architecture/technology-stack.md).

**Decision boundary:** Instagram and LinkedIn are content-generation channels. Only Instagram is in the first direct-publishing integration. Human approval is required for each post; there is no unattended or scheduled publishing in the first slice.

## Product principles

- **Human editorial control:** AI assists; the content manager makes the final decision.
- **Accuracy before speed:** unclear or missing business information should be surfaced.
- **Low-cost and extensible:** select technology deliberately, prioritising local or free-tier options where feasible.
- **Evidence-led scope:** validate the user problem before expanding features.
- **Professional traceability:** decisions, research evidence, tests, and limitations remain visible in the repository.
- **Privacy-aware evaluation:** use synthetic or explicitly approved business data when testing provider free tiers.

## Academic brief and assessment risks

The bootcamp brief requires a functional content-generation proof of concept, a web interface, generative models and an LLM application framework, low-cost choices, Git/GitHub practices, a Kanban board, documentation, a live demo, a Medium article, and a technical presentation.

The brief presents RAG as an advanced capability while the rubric assigns it significant weight. The initial stack includes **lightweight RAG**, image generation, and a comparison of two text-model configurations to address the assessment direction without introducing a large multi-agent system. Confirm with the instructor what depth of RAG evidence is expected.

Image generation, Instagram OAuth/publishing, LinkedIn adaptation, and voice mode extend the original text-first project direction. The first implementation slice is deliberately limited to one business, one Instagram professional account, and one Instagram feed-image workflow.

## Project workspace

- [GitHub Project — LLM Content Generation MVP](https://github.com/users/gabrielagranja/projects/1): Kanban, work plan, roadmap, phases, and status.
- [Backlog](https://github.com/gabrielagranja/generador-contenido-llms/issues): epics, stories, tasks, research, and decision spikes.
- [Milestones](https://github.com/gabrielagranja/generador-contenido-llms/milestones): delivery and presentation deadlines.
- [Labels](https://github.com/gabrielagranja/generador-contenido-llms/labels): work type and priority classification.
- [Project workflows](https://github.com/users/gabrielagranja/projects/1/workflows): automation rules for issue and pull-request status changes.

## Project automation

GitHub Project workflows reduce administrative work while keeping product decisions manual:

- Open repository Issues are automatically added to the Project as `Todo`.
- Sub-issues are added automatically.
- Linking or reopening work moves it to `In Progress`.
- Merged pull requests and closed items move work to `Done`.
- Moving an item to `Done` closes the linked Issue.

Phase, priority, scope, and product decisions are intentionally not automated.

## Key dates

| Milestone | Date | Notes |
| --- | --- | --- |
| MVP delivery | **13 October 2026, 12:00 PM** | Europe/Madrid (CEST) |
| Repository presentation | **14 October 2026** | 10-minute technical presentation |

## Planned evaluation

The MVP will be assessed against the existing workflow using a real or representative content request. Candidate measures include:

- time to an editorially useful draft;
- number of clarification questions and revision rounds;
- factual errors or missing details;
- adaptation to selected platform and audience;
- image usefulness and suitability for the Instagram channel;
- voice-mode usefulness for entering or revising a brief;
- editorial quality assessment by the primary user;
- latency and approximate model/API usage for the compared configurations.

Automated tests should mock external API calls. Real image/voice/social API smoke tests should use an authorized test account and approved sample data.

## Repository conventions

- GitHub Issues are the source of truth for planned work.
- The Project tracks status and phase; issues hold the acceptance criteria and evidence.
- Work is organised as **Epic → Story → Task/Spike** where useful.
- Branches and descriptive commits will accompany implementation.
- Documentation, research, design, implementation, testing, and presentation materials will be added as the project evolves.

## Current next step

Turn the approved stack into runnable local setup and implementation tasks. Verify access requirements for the Instagram test account, provider quotas and terms, and hosting support for HTTPS, WebSockets, and persistent media before deploying the live demo.
