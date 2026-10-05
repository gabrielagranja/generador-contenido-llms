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
3. Generate editable content packages adapted to **Instagram and Facebook** for single-image posts, carousels and Reels.
4. Retrieve relevant, approved business context through a small RAG pipeline.
5. Generate and preview one image for an Instagram feed-image post; carousels and Reels receive slide-by-slide or scene-by-scene creative plans.
6. Use an optional voice mode to enter briefs and request draft revisions.
7. Connect one authorized Instagram Professional account and publish only after explicit human approval.

The first slice uses one representative/authorized business. Instagram is the priority channel and Facebook is the second content-generation/adaptation channel. Initial content formats are single-image posts, carousels and Reels; Stories and LinkedIn are deferred. Direct Facebook publishing is outside the first slice. Voice interaction can create and revise drafts, but it cannot publish without the same explicit approval step.

## Product direction beyond the first slice

The first slice validates a human-reviewed workflow for generating accurate, editable content for one representative business. The longer-term product direction is an editorial management tool for local-business networks: it should help a non-technical content manager maintain reliable business information, plan a varied editorial calendar, and create content grounded in traceable evidence.

This direction is a product hypothesis for future discovery and planning. It does not expand the approved first-slice scope above or claim that these capabilities are implemented.

### Knowledge that people can maintain

Business owners and content managers should work through familiar tools—not directly with databases, embeddings, or vector stores. A future workflow may provide a simple web form to add or update a business profile and an import path for existing spreadsheets or CSV files. The application would validate and normalize those inputs, retain their source and approval status, and update its searchable knowledge automatically.

The knowledge base may include approved business profiles, stories, products and services, values, campaigns, images, local events, and carefully selected local news or public statistics. Retrieval should keep source identifiers and relevant excerpts so reviewers can check what supports a generated claim. Documents, chunks, and embeddings are implementation details hidden behind the application.

The current MVP stack below uses a small local Chroma store. A production storage choice—including whether structured records and vector search should share PostgreSQL with pgvector—remains to be evaluated against usability, deployment, cost, privacy, and maintenance needs before it is adopted.

### Editorial strategy, history, and feedback

The longer-term workflow separates three responsibilities:

1. **Knowledge and evidence:** retrieve relevant, approved information and expose its sources.
2. **Editorial planning:** apply a human-approved line of editorial, content categories, campaign priorities, and deterministic rotation rules to suggest what to cover, which business or topic to feature, and why.
3. **Performance feedback:** retain publication history and, when authorized analytics are available, relate engagement measures to content type, business, topic, format, and date.

The language model drafts and adapts content from the selected brief and evidence. It does not independently set the editorial strategy, guarantee engagement, or publish without the existing human approval rule. Any future balance targets or automatic use of analytics require validation and an approved scope change.

### Candidate data sources and integrations

A staged, low-dependency approach is preferred for investigation:

- Start with the business information already available, entered through a future form or imported from a spreadsheet.
- Evaluate selected RSS/Atom feeds from municipal, business-association, and local-news sources for timely local context.
- Maintain an application-owned editorial calendar for campaigns, local events, and relevant dates; calendar synchronization can be considered if it solves a validated workflow need.
- Assess official public datasets, such as INE or datos.gob.es, only for specific local economic or demographic context that improves content decisions.
- Defer social-platform analytics, trend services, and paid news aggregators until access, terms, coverage, privacy, cost, and user value are verified.

These are candidate sources, not current dependencies. No third-party feed or API is assumed to be available, free for production, or appropriate for automatic ingestion. Retrieved external material must be curated, dated, attributable, and checked before it is used as evidence.

### Possible evolution

A sensible sequence to investigate is: reliable business knowledge and traceable retrieval; a human-controlled editorial taxonomy and calendar; history and deterministic rotation; curated local context; then authorized performance analytics and carefully evaluated feedback. Each stage needs a GitHub Issue and an approved OpenSpec contract before implementation. The official assessment rubric and current first-slice boundary remain authoritative.

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

**Decision boundary:** Instagram and Facebook are the initial content-generation channels. Instagram is the priority channel and the only direct-publishing integration in the first slice. Facebook content is generated/adapted but not published automatically. LinkedIn is out of scope unless a validated B2B need reopens it. Human approval is required for each Instagram post; there is no unattended or scheduled publishing in the first slice.

## Product principles

- **Human editorial control:** AI assists; the content manager makes the final decision.
- **Accuracy before speed:** unclear or missing business information should be surfaced.
- **Low-cost and extensible:** select technology deliberately, prioritising local or free-tier options where feasible.
- **Evidence-led scope:** validate the user problem before expanding features.
- **Professional traceability:** decisions, research evidence, tests, and limitations remain visible in the repository.
- **Privacy-aware evaluation:** use synthetic or explicitly approved business data when testing provider free tiers.

## Academic brief and assessment requirements

The official rubric is recorded in [Rubric traceability](docs/rubric-traceability.md). It totals 100 points:

| Competence | Weight |
|---|---:|
| C1 Communication | 12 % |
| C2 Version-control project management | 16 % |
| C3 Team management | 18 % |
| C4 NLP/AI model | 54 % |

C4 requires use of LLM models, an LLM application framework and a RAG architecture. Each indicator is worth 18 %. Image generation, two-model comparison and Docker remain product choices; they are not rubric requirements. The project will record the instructor's guidance on the evidence expected for RAG in a solo project.

Image generation, Instagram OAuth/publishing, Facebook adaptation, and voice mode extend the original text-first project direction. The first implementation slice supports single-image, carousel and Reel content packages; generated visual assets remain limited to one Instagram feed-image preview. Stories and LinkedIn are deferred.

## Project source of truth

The repository uses OpenSpec-based Specification-Driven Development.

- [Project charter](docs/project-charter.md): vision, user, principles and MVP outcome.
- [MVP scope](docs/scope.md): canonical in-scope and out-of-scope boundary.
- [Roadmap](docs/roadmap.md): plan-level phases and priorities.
- [Assumptions and open questions](docs/assumptions.md): unresolved decisions that require human approval.
- [Decision records](docs/decisions/): approved material decisions.
- [Evaluation plan](docs/evaluation-plan.md): cases, measures and evidence.
- [Rubric traceability](docs/rubric-traceability.md): plan, Issue, OpenSpec, tests and rubric evidence.
- [Daily logs](docs/daily/): operational progress; they do not replace decision records.
- [OpenSpec workspace](openspec/): implementation contracts and archive.
- [Contributing workflow](CONTRIBUTING.md): proposal, approval, implementation and verification rules.

No implementation change starts without an approved OpenSpec contract linked to a GitHub Issue. Instagram publication always requires explicit human confirmation.

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
