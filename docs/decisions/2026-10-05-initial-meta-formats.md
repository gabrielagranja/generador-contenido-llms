# Decision Record — Initial Meta Content Formats

**Date:** 2026-10-05  
**Issue:** #15 and #22  
**Status:** Approved

## Context

The MVP needs a small, useful set of content formats for Instagram and Facebook. The existing technical scope includes generating and previewing one Instagram feed image, while the content-generation workflow should support more than a single static layout.

## Options considered

1. Limit content generation to a single-image feed post.
2. Support single-image posts, carousels and Reels, with Stories deferred.
3. Add every Meta placement and format, including Stories, in the first slice.

## Decision

Adopt option 2. Instagram is the priority channel and Facebook is the second generation/adaptation channel. Initial content packages support:
- single-image feed post;
- carousel, with a cover hook and slide-by-slide content/visual direction;
- Reel, with a concise scene/script outline, on-screen text and subtitle guidance.

Stories are deferred. Full carousel image-set generation and rendered video generation are not included. The existing image-generation capability remains one Instagram feed-image generation and preview. Facebook content is generated/adapted but not published automatically. Every Instagram publication still requires explicit human confirmation.

## Consequences and affected documents

- Canonical scope is updated in docs/scope.md.
- Issue #15 records the platform/format decision; Issue #22 records the guided expert-generation acceptance criteria.
- The OpenSpec contract openspec/changes/expert-content-generation/ defines behavior and implementation tasks.
- docs/assumptions.md and docs/evaluation-plan.md record the approved scope and evaluation cases.
- Current dimensions, placement limits and safe zones remain subject to verification against official Meta guidance at implementation time.

## Revisit trigger

Revisit if user discovery, implementation feasibility, the official rubric or current Meta constraints show that the selected formats are not useful or cannot be delivered within the MVP.
