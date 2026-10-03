# LLM Content Generation MVP

> A portfolio project that explores and validates an LLM-assisted social-content workflow for a network of 20+ small businesses.

## Status

**Current phase: Discovery & validation.**

This repository documents an end-to-end solo product-development process: marketing and product discovery, UX/UI design, LLM application development, evaluation, and portfolio communication. The MVP scope will be finalised from research evidence before implementation begins.

## Real-world context

The project is grounded in a real content-management workflow for a network of more than 20 small local businesses.

- **Primary user:** a digital content manager and copywriter who coordinates social communication across the network.
- **Potential secondary users:** business owners or staff with limited social-media confidence. Their role—information contributor, reviewer, approver, or direct user—must be validated.
- **Content audience:** each business's customers and local community. They consume the content but are not expected to use the MVP directly.

## Problem hypothesis

Business information can arrive incomplete, unstructured, or late. Turning it into accurate, channel-appropriate copy may require repeated clarification, adaptation, review, and rework.

The hypothesis is that a guided, human-in-the-loop workflow with reusable business context can help the content manager transform a lightweight brief into editable, platform-specific content more efficiently than the current process or generic AI prompting alone.

This is a hypothesis, not a conclusion. The project will compare the proposed workflow with current workarounds and general AI tools.

## MVP direction under validation

The candidate MVP is a text-first web application that lets the content manager:

1. Capture a structured content brief: topic, audience, platform, business context, and optional notes.
2. Identify missing or ambiguous information before generation.
3. Generate editable, channel-adapted draft copy.
4. Review, edit, regenerate, and copy or export the final content.

The first scope will use one real business case and one or two channels. Automated publishing, image generation, voice, multilingual support, complex multi-agent systems, and large-scale RAG are not assumed to be part of the first functional slice.

## Product principles

- **Human editorial control:** AI assists; the content manager makes the final decision.
- **Accuracy before speed:** unclear or missing business information should be surfaced.
- **Low-cost and extensible:** select technology deliberately, prioritising local or free-tier options where feasible.
- **Evidence-led scope:** validate the user problem before expanding features.
- **Professional traceability:** decisions, research evidence, tests, and limitations remain visible in the repository.

## Delivery roadmap

| Phase | Purpose |
| --- | --- |
| Ideation & planning | Analyse the brief, constraints, assumptions, and evaluation criteria. |
| Discovery & validation | Understand the current workflow, local businesses, alternatives, and the problem worth solving. |
| Product definition | Decide users, JTBD, value proposition, scope, success measures, and technical direction. |
| UX/UI design | Design and test the brief-to-review workflow before building it. |
| MVP development | Build the web interface, LLM workflow, prompts, and human-review loop. |
| Testing & evaluation | Evaluate quality, factual reliability, usefulness, and time-to-draft. |
| Portfolio & presentation | Prepare documentation, article, demo, and technical presentation. |

## Academic brief and assessment risks

The bootcamp brief requires a functional content-generation proof of concept, a web interface, generative models and an LLM application framework, low-cost choices, Git/GitHub practices, a Kanban board, documentation, a live demo, a Medium article, and a technical presentation.

A key decision remains open: the brief presents RAG as an advanced capability, while the assessment rubric assigns it significant weight. The same uncertainty applies to image support and comparing two LLM configurations. These requirements are recorded as a dedicated research spike and will be confirmed with the instructor before the scope is frozen.

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
- editorial quality assessment by the primary user.

## Repository conventions

- GitHub Issues are the source of truth for planned work.
- The Project tracks status and phase; issues hold the acceptance criteria and evidence.
- Work is organised as **Epic → Story → Task/Spike** where useful.
- Branches and descriptive commits will accompany implementation.
- Documentation, research, design, implementation, testing, and presentation materials will be added as the project evolves.

## Current next step

Complete discovery evidence, confirm the assessment expectations for RAG/images/model comparison, and define the smallest testable MVP scope before writing implementation tasks in detail.
