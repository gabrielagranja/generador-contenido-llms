# Proposal

## Status and human approval

- Status: Approved
- Human approval: Approved in the project conversation on 2026-10-05.
- Issue: #22 — [STORY] Capture a structured content brief
- Decision record: docs/decisions/2026-10-05-brief-to-post-coach-hypothesis.md

## Plan objective

Advance the content-generation MVP (parent epic #10) by defining an expert guided workflow that helps the content manager turn incomplete small-business information into accurate, editable content for Instagram and Facebook.

## Objective

The agent should do more than write captions: it should ask focused questions, help the user reason about their audience from real customer evidence, choose a suitable strategy and format, and return a reviewable post with assumptions clearly marked. The proposed differentiator is a transparent brief-to-post coach; its value and differentiation remain hypotheses to validate, not market-uniqueness claims.

## Scope

### Included

- Instagram and Facebook content generation/adaptation; LinkedIn remains outside this stage.
- Guided discovery of offer/topic, goal, audience, customer needs and objections, brand voice, platform, format, proof and constraints.
- Separation of confirmed, inferred and unknown facts.
- Goal-led selection of message, copy approach, optional formula, platform format and CTA.
- Knowledge guidance for copy structure, styles and formulas; visual effectiveness; mobile-first legibility; brand coherence; accessibility; social-search wording; testing; and truthful persuasion.
- Approved first formats: single-image post, carousel and Reel. Stories are deferred. Carousel and Reel outputs are content/creative plans; full carousel image-set or video rendering is out of scope.
- Editable output with per-platform copy, CTA, visual direction, relevant overlay/script, assumptions, and optional test variant.
- Human approval before Instagram publication remains required.

### Excluded

- Stories in the first stage.
- Automatic Facebook publishing, unattended/scheduled publishing, and unapproved account access.
- LinkedIn generation/publishing in this stage.
- Claims that a formula, visual tactic, AI content, or the proposed product differentiator guarantees performance.
- Encoding unverified numeric Meta requirements as fixed rules.

## Acceptance criteria

- Missing material information is identified and the agent asks focused questions without repeating approved profile facts.
- If the user does not know the audience, the agent helps form a provisional hypothesis from real customer situations, questions, purchase/use roles and objections, marking evidence status.
- The strategy maps goal → audience situation → need/desire/objection → core message → platform/format → angle → CTA.
- Copy approaches (direct response/benefit-led, narrative/emotional, educational/authority, disruptive/entertaining), formulas (AIDA, PAS/PASTOR, 4 Cs, BAB, 4 Ps, open loops), and persuasion principles are optional tools matched to context.
- Copy and visual guidance use a hook, concise readable body, direct CTA, complementary brief image text, mobile legibility, contrast, one focal point, brand guidance and accessibility when applicable.
- Platform adaptation is explicit when both Instagram and Facebook are selected.
- No unsupported business fact, testimonial, statistic, result, scarcity, deadline, credential, guarantee or product benefit is invented.
- The output separates platform/format/goal, audience status, evidence, message, copy, CTA, visual direction, assumptions and optional A/B hypothesis.
- Numeric Meta format and safe-zone rules are verified against current official guidance before enforcement.
- Evaluation measures accuracy, audience hypothesis quality, relevance of questions, platform/format fit, editability, revision effort and time to useful draft.
- The approved format set is single-image feed post, carousel and Reel for Instagram/Facebook content generation/adaptation; Stories are deferred. The existing Instagram single-image generation/preview remains the only rendered visual asset capability in this slice.

## Rubric

No aplica — the official rubric and weights remain pending in the repository.

## Tests and verification

- Automated: run the SDD required-field validator and OpenSpec schema/active-change checks after the contract is complete; application tests will be defined with implementation and external providers mocked.
- Manual/evidence: review fixed representative briefs across confirmed, inferred and unknown audience cases; inspect factual grounding, brand fit, platform and format adaptation, accessibility and editing usefulness.
- External data: use synthetic or explicitly approved business data; verify changing Meta specifications against official documentation before encoding them.
- Record limitations and evaluation evidence against Issue #22.

## Open questions and blockers

- Confirm whether the user chooses language explicitly or the agent defaults to the language of the brief/profile.
- Verify current official Meta requirements for placements, dimensions, safe zones and media constraints at implementation time.
- Keep the differentiator as a hypothesis until competitor and user-workflow validation is complete.

## Approval

Approved on 2026-10-05 after the user approved the consolidated scope and criteria in the project conversation. Implementation MAY proceed in tasks.md order. This approval includes content/creative plans for single-image posts, carousels and Reels; it does not include complete carousel media rendering, video generation, Stories or Facebook publishing.
