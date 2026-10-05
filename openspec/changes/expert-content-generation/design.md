# Design

## Context

This design supports the approved proposal for Issue #22. It defines an implementation-neutral workflow for turning a business brief and approved business context into an editable, truthful Instagram or Facebook post. It does not authorize implementation or publication.

## Technical approach

Keep three information classes separate:

1. General expert knowledge: strategy, copy approaches/formulas, format guidance, visual heuristics, accessibility and quality rules.
2. Business facts: user-provided or explicitly approved profile facts and source provenance, retrieved through the existing RAG boundary where available.
3. Post-specific brief: topic, objective, audience context, platform, format, campaign and constraints.

Apply the following generation sequence:

1. Parse the request and collect confirmed facts from the message and approved profile.
2. Check whether offer/topic, objective, platform and format are known.
3. Ask the highest-value missing question or compact set of questions; do not repeat known information.
4. If audience knowledge is weak, ask about real customers: who buys, uses, decides or recommends; what situation prompts them; their questions, desired outcomes and objections.
5. Build a provisional audience hypothesis and label material statements CONFIRMED, INFERRED or UNKNOWN, with source/reason.
6. Validate an inference if it could change the audience, promise or CTA. For non-critical unknowns, state the assumption and allow an editable draft.
7. Select an angle, optional copy scaffold, channel-specific format and CTA from the objective and verified audience insight.
8. Generate the content package, run the quality gate, then return the draft and only the rationale needed for user review.

Do not infer sensitive personal traits from business anecdotes or substitute demographic stereotypes for customer evidence. Separate purchaser, user, decision-maker and referrer when roles differ.

### Strategy and copy knowledge

Map objective → audience situation → need/desire/objection → core message → platform/format → angle → CTA.

Choose among direct-response/benefit-led, narrative/emotional, educational/authority, and disruptive/entertainment approaches according to audience, brand and objective. Storytelling must use real supplied experiences. Humor must not demean the audience.

Use AIDA (Attention, Interest, Desire, Action), PAS/PASTOR (problem, agitation/amplification, solution, then where supported testimony/offer/response), 4 Cs (clear, concise, credible, convincing), BAB (before, after, bridge), 4 Ps (picture, promise, proof, push), and open loops as optional scaffolds. Do not force or name a formula in every output.

Use social proof, anchoring and reciprocity only when relevant and grounded. Urgency/scarcity requires a real deadline or quantity. Apply social-search keywords naturally. AI may support idea generation, research questions and hook variations; any externally sourced trend or business fact must be verified before use. A/B tests should compare a defined change and an objective-aligned metric.

### Visual and format knowledge

Use flexible heuristics: mobile-first composition, legible hierarchy and contrast, one main focal point, brand coherence, restrained logo placement and relevant accessibility cues. Human faces, authentic/UGC-style imagery, complementary text overlays, carousel continuation cues, F/Z reading and power words are optional creative ideas, not guaranteed performance drivers.

Keep on-image text brief (about 6–8 words as a starting guideline) and use no more than two typefaces where feasible. Do not duplicate the caption in the image. Provide subtitle guidance for video so it works sound-off and alt-text guidance for important images.

Approved first formats are single-image feed post, carousel and Reel; Stories are deferred. A single-image package has one focal visual, complementary overlay, caption and CTA. A carousel has a cover hook, coherent per-slide progression, a resolved ending/CTA and optional continuation cue. A Reel has a concise scene/script outline, opening hook, useful development, closing CTA and readable subtitle/on-screen text direction.

The approved format set is single-image feed posts, carousels and Reels for Instagram/Facebook content generation and adaptation. The existing rendered-media capability remains one Instagram feed-image generation/preview; carousel and Reel outputs are creative plans, not rendered image sets or video. Stories are deferred.

Treat 4:5, 1:1 and 9:16 dimensions, safe-zone percentages, a two-second stop-scroll target, F/Z pattern claims and any CTR/conversion uplift figures from the conversation as provisional heuristics or unverified claims. Verify current official Meta documentation before enforcing technical values. Do not promise reach, engagement or conversion.

### Structured output

The editable output should separate:
- objective, selected platform(s) and format;
- audience hypothesis and evidence status;
- core insight/message and its source;
- strategic angle and optional formula;
- caption adapted per selected platform, with CTA and relevant optional keywords/hashtags;
- visual direction and image prompt when image generation is requested and supported;
- overlay text for image, slide outline for carousel, or scene/script/subtitle plan for Reel;
- alt-text suggestion for image content;
- assumptions, validation question or omitted unsupported claim;
- optional A/B variant, hypothesis and one primary metric.

The user-facing response should present the useful content, not hidden reasoning or a lengthy internal analysis.

### Decisions and trade-offs

- Ask only questions that materially affect accuracy or strategy; too few questions risk generic or unsupported posts, while exhaustive intake creates friction.
- Permit provisional drafts for non-critical unknowns, but label assumptions and avoid unsupported claims.
- Adapt one idea for each chosen Meta channel instead of duplicating text blindly.
- Treat formulas and visual advice as flexible heuristics; fixed rules risk repetitive content and platform guidance changes.
- Keep “brief-to-post coach” as a testable product hypothesis; do not make an unsupported uniqueness claim.
- Preserve the existing explicit human approval requirement for each Instagram publication.

### Validation strategy

Use fixed synthetic or explicitly approved briefs across businesses/use cases, channel choices and evidence states. Evaluate audience-hypothesis evidence labels, question relevance, factual grounding, platform/format fit, brand voice, accessibility, editorial usefulness, editing/revision effort and time to usable draft. For variants, define one intended change and one primary objective-aligned metric. Treat observed engagement as correlation unless the evaluation design supports causal attribution.

### Safety, privacy and operational boundaries

- Never invent product facts, benefits, testimonials, data, deadlines, quantities, credentials or guarantees.
- Use only approved or user-provided business facts; retain source/provenance where available.
- Avoid sensitive audience inferences and manipulative pressure.
- Use synthetic or explicitly approved business data in provider evaluation.
- Mock external API calls in automated tests.
- Do not publish automatically; every Instagram post needs explicit human confirmation.
- Do not directly publish to Facebook, schedule posts, or access unapproved accounts under this proposal.

### Open questions

- Decide explicit versus inferred content-language selection.
- Verify live Meta technical and policy constraints from official sources at implementation time.
- Validate the product hypothesis against user workflow and competitor evidence.
