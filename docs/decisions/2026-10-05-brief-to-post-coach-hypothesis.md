# Decision Record — Brief-to-Post Coach Hypothesis

**Date:** 2026-10-05  
**Issue:** #22  
**Status:** Approved product hypothesis; market and workflow validation required

## Context

A generic social-copy generator may still leave a small-business content manager with the hardest work: identifying what is known about customers, defining the audience, choosing a message and deciding what format and CTA fit. The project needs a useful distinction without claiming an unverified competitive advantage.

## Options considered

1. Generate copy directly from a short prompt.
2. Ask the user to fill out a complete marketing brief before generation.
3. Guide the user through a few focused questions, derive a provisional audience hypothesis from customer evidence, label facts versus assumptions, and turn the result into an editable post and optional test hypothesis.

## Decision

Adopt option 3 as the product hypothesis to validate. The agent should provide the method while the business user supplies the facts. It must make evidence status visible and never present inferred audience details or unsupported claims as confirmed facts.

This is a hypothesis for product discovery, not a claim that no other application provides similar functionality.

## Consequences and affected documents

- Issue #22 and OpenSpec change `openspec/changes/expert-content-generation/` define the proposed behavior and acceptance criteria.
- `docs/assumptions.md` remains authoritative for unresolved scope and evidence questions.
- `docs/evaluation-plan.md` should measure question relevance, usefulness of the audience hypothesis, editability, accuracy, platform fit and time to a usable draft.
- The approved initial content formats are single-image, carousel and Reel; Stories are deferred. See docs/decisions/2026-10-05-initial-meta-formats.md. Carousel/Reel deliverables are creative plans; the only rendered visual asset in scope is one Instagram feed image.

## Revisit trigger

Revisit after discovery with the primary content manager, comparison against current workarounds/competitors, or evaluation showing that users do not value or understand the guided hypothesis workflow.
