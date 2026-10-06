# Proposal

## Status and human approval

- Status: Approved
- Issue: #23 — [STORY] Generate channel-adapted content
- Parent epic: #10
- Depends on: approved Issue #22 contract in `openspec/changes/expert-content-generation/`
- Human approval: Approved in the project conversation; implementation is authorized.

## Plan objective

Define the minimum contract for producing editable text drafts tailored to Instagram and Facebook from the approved Issue #22 structured brief.

## Objective

Provide grounded, reviewable copy with explicit channel adaptation, versioned prompt templates and synthetic examples, while preserving the approved format and publication boundaries.

## Scope

### Included

- Text drafts for `instagram` and `facebook`.
- Versioned templates for each channel.
- Channel-specific tone, structure, CTA and readability guidance.
- Editable draft sections for caption, CTA, evidence references, assumptions and review notes.
- Text or creative-plan output for the approved `single_image`, `carousel` and `reel` formats.
- Examples based only on the existing F-01, F-02 and F-03 synthetic fixtures.

### Excluded

- Image generation, image editing, carousel rendering and video generation.
- Instagram/Facebook publication, scheduling, OAuth and platform API calls.
- Web-interface changes.
- New brief, fact-status, audience or format contracts; Issue #22 remains authoritative.
- RAG retrieval, analytics learning, performance guarantees and unapproved real business data.

## Acceptance criteria

- Templates consume the approved `GuidedBrief` without redefining its fields or fact statuses.
- Each selected channel produces a visibly adapted editable draft and records the template identifier/version.
- Drafts preserve the grounded core message and expose evidence, assumptions and review needs.
- Unsupported business facts, benefits, testimonials, statistics, deadlines, scarcity, credentials and guarantees are omitted or qualified, never invented.
- F-01, F-02 and F-03 cover confirmed, unknown and ambiguous inputs across the approved channels and formats.
- The contract requires no visual asset, publication action or interface change.

## Rubric

This contract scopes content-generation behavior related to Issue #22. It does not claim completion of LLM, framework or RAG evidence; those require implementation and recorded evaluation evidence.

## Tests and verification

- OpenSpec active-change and SDD required-field validation passed.
- The service and focused tests for template selection and channel adaptation passed with mocked providers.
- Review grounding, channel fit, editability and excluded capabilities.

## Open questions and blockers

- Evaluation against F-01, F-02 and F-03 remains pending.
- Language selection remains inherited from the open question in Issue #22.
- Unverified numeric platform constraints must not become fixed template rules.

## Approval

Approved for implementation. The contract remains active until fixture evaluation and Issue #23 closure evidence are complete.
