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

### Guided discovery question map

The agent should use the following question order as a minimum useful interview. It should skip a question when the answer is already confirmed in the current brief or approved business context, and should ask only the highest-priority unanswered question or compact group of questions.

| Priority | Question area | Focused question | Required when | Result |
| --- | --- | --- | --- | --- |
| 1 | Topic or offer | What should this content communicate, feature or invite people to do? | No usable topic, offer or event is confirmed. | Topic/offer and relevant constraints. |
| 2 | Goal | What outcome matters for this piece: inform, attract interest, explain, build trust or prompt an action? | Different goals would materially change the message or CTA. | Explicit or user-confirmed goal. |
| 3 | Audience situation | Who is involved in the real customer situation, and what is happening when they need this? | Audience, purchaser, user, decision-maker or referrer is unknown or conflated. | Audience roles and concrete situation. |
| 4 | Need and objection | What need, desired outcome, question or hesitation should the content address? | The audience situation does not yet reveal a useful message or an objection may change the promise. | Need/desire/objection evidence. |
| 5 | Proof and source | What approved fact, example, product detail, experience or source supports the claim? | A draft would otherwise rely on a benefit, result, testimonial, statistic, credential, deadline or scarcity claim. | Claim evidence and provenance, or an explicit omission. |
| 6 | Brand and constraints | What tone, wording, exclusions, legal or accessibility constraints should be respected? | No usable profile guidance exists or the request introduces a material constraint. | Brand/constraint guidance or a reviewable assumption. |
| 7 | Channel and format | Which supported channel and format should carry the message: Instagram/Facebook, single-image, carousel or Reel? | Platform or format is missing, incompatible or would change the content package. | Selected channel(s) and format. |
| 8 | CTA and approval boundary | What should the audience do next, and what must remain subject to human review? | The goal does not determine a safe CTA or publication could be confused with approval. | CTA and explicit review boundary. |

If material uncertainty remains after this map, the agent must either ask for validation or produce an editable provisional draft with the uncertainty labelled. It may proceed with non-critical unknowns only when the user accepts the assumption and the draft does not state it as a fact.

### Confirmed, inferred and unknown fact model

Every material business, audience or post-specific statement should be represented with these fields:

| Field | Meaning |
| --- | --- |
| `statement` | The factual or audience-hypothesis claim in plain language. |
| `status` | Exactly one of `CONFIRMED`, `INFERRED` or `UNKNOWN`. |
| `source` | User brief, approved business context, cited source, or `none`. |
| `reason` | Why the status was assigned and what evidence supports it. |
| `scope` | Business, audience, offer, campaign or post-specific context to which it applies. |
| `validation_needed` | Whether user confirmation or source checking is required before using it as a claim. |

Status rules:

- `CONFIRMED` means the user explicitly supplied or approved the statement, or it comes from approved business context with traceable provenance. It may support copy subject to the normal quality and platform checks.
- `INFERRED` means a provisional hypothesis derived from confirmed evidence, such as an audience situation or objection. It must be labelled as an inference and validated before it changes a material promise, audience choice or CTA.
- `UNKNOWN` means the information is missing, ambiguous, stale or unsupported. It must not be presented as a fact; the agent should ask for evidence, omit the claim or state the assumption for review.

Allowed transitions are `UNKNOWN` to `CONFIRMED` after user or source confirmation, `UNKNOWN` to `INFERRED` only when the evidence and reasoning are recorded, and `INFERRED` to `CONFIRMED` only after confirmation. Contradicted or unresolved inferences return to `UNKNOWN`. The status applies to the claim itself, not to the confidence of the model, and should remain visible in the reviewable output when material.

### Goal-led decision guidance

The decision path must be explicit and reviewable. Each step uses the confirmed facts and clearly labelled inferences from the guided brief; it must not silently fill a material gap.

| Step | Decision | Guidance | Output |
| --- | --- | --- | --- |
| 1 | Objective | Identify the intended outcome in the user's terms, such as inform, attract interest, explain, build trust or prompt an action. Ask for clarification when different objectives would materially change the content. | One explicit or user-confirmed objective. |
| 2 | Audience situation | Select the relevant customer role and concrete situation: who buys, uses, decides or recommends, what triggers the need, and what question or objection exists. Keep audience hypotheses labelled until confirmed. | Audience situation, roles and evidence status. |
| 3 | Core message | Connect the objective to the audience's need, desired outcome or objection. Select one useful promise or message supported by confirmed facts; omit unsupported benefits or proof. | One core message and its supporting evidence. |
| 4 | Platform and format | Choose only an approved target: Instagram or Facebook, with a single-image feed post, carousel or Reel. Select the format that best carries the objective and message, not the format first. Adapt explicitly when both channels are selected. | Channel(s), format and package requirements. |
| 5 | Angle | Frame the core message for the audience situation and selected format, using a clear informational, benefit, narrative or other context-appropriate angle. Treat any scaffold as optional and keep the rationale editable. | One primary angle and optional alternative. |
| 6 | CTA | Choose the smallest credible next action that serves the objective and fits the channel, offer and evidence. Use urgency, scarcity or proof only when grounded in an approved fact. | Direct CTA, or an explicit reason for omitting one. |

Decision guardrails:

- A missing objective, audience situation or material support for the message blocks unsupported drafting; ask a focused question or state the unknown and omit the claim.
- The chain must remain traceable as `objective → audience situation → need/desire/objection → core message → platform/format → angle → CTA`.
- A platform or format choice must not introduce new business facts, audience traits or promises. If it would, return to discovery and label the missing information.
- When several choices are safe, prefer the simplest option that is useful, editable and aligned with the confirmed objective. Return one primary route and an optional alternative rather than an unexplained list.
- The user may revise any step; downstream decisions must be recalculated and the changed assumption made visible.

### Strategy and copy knowledge

Map objective → audience situation → need/desire/objection → core message → platform/format → angle → CTA.

#### Source boundary

This guidance is grounded in the approved Issue #22 proposal/design/specification, `docs/scope.md`, and the approved decision records for the brief-to-post coach hypothesis and initial Meta formats. A brief repository read did not identify a separate approved bibliography or source catalogue for copywriting, persuasion or visual heuristics. Therefore the guidance below is a contextual heuristic and contract boundary, not a claim of externally verified best practice. Task 7 remains responsible for verifying changing Meta technical and policy constraints against official documentation.

#### Selecting copy approaches and formulas

Choose the approach that best serves the confirmed objective, audience situation, evidence and selected channel/format. Return one primary approach and explain the choice in editable terms; do not force a formula or imply guaranteed performance.

| Context | Preferred approach | Optional scaffold | Safeguard |
| --- | --- | --- | --- |
| A clear offer or action is confirmed and the goal is response | Direct-response or benefit-led | 4 Ps or AIDA | State only benefits supported by confirmed facts; use a CTA proportionate to the offer. |
| A real customer or business experience is available and connection matters | Narrative or emotional | BAB or an open loop | Use supplied experiences only; do not invent a story, emotion or outcome. |
| The goal is explanation, trust or authority | Educational or authority-led | 4 Cs or AIDA | Distinguish expertise from credentials or results that have not been confirmed. |
| The audience and brand support attention through playfulness or contrast | Disruptive or entertaining | Open loop or a light AIDA structure | Avoid humiliation, stereotypes, unsupported shock and tactics that obscure the message. |
| A real problem and a supported solution are clear | Problem/solution framing | PAS or PASTOR | Agitation must not exaggerate harm; testimony, offer and response sections require evidence. |

Use formulas as optional scaffolds: AIDA for an attention-to-action progression, PAS/PASTOR for a grounded problem and solution, 4 Cs for clarity and credibility, BAB for a supported before/after/bridge, 4 Ps for picture/promise/proof/push, and open loops for curiosity that is resolved in the content. If no scaffold clearly improves the message, omit it.

#### Persuasion safeguards

- Treat social proof, anchoring and reciprocity as optional devices that require a relevant, approved fact.
- Use urgency or scarcity only for a real deadline, quantity or availability constraint; otherwise omit it.
- Never invent benefits, statistics, testimonials, credentials, guarantees, results or customer traits.
- Do not use sensitive audience inferences or pressure tactics. If an inference affects the promise or CTA, return to discovery and request validation.
- Keep the message editable and expose material assumptions, omitted claims and any proposed test hypothesis with one objective-aligned metric.

#### Visual criteria by platform and format

Apply visual guidance as flexible quality criteria, not performance guarantees. Keep the core message consistent across Instagram and Facebook while adapting presentation to the selected channel.

| Format | Selection criteria | Accessibility and review checks |
| --- | --- | --- |
| Single-image feed post | One focal point, complementary overlay text, clear hierarchy, mobile legibility, adequate contrast and restrained brand treatment. | Do not duplicate the caption in the image; provide alt-text guidance and keep the overlay editable. |
| Carousel | Cover hook, one useful progression per slide, coherent sequencing, readable slide text and a resolved ending with CTA. | Check contrast, reading order and continuation cues; deliver slide-by-slide creative direction, not a rendered image set. |
| Reel | Concise scene/script outline, useful development after the opening hook, readable on-screen text and a closing CTA. | Include subtitle guidance for sound-off viewing, accessible pacing and a reviewable script; deliver a creative plan, not rendered video. |

Across formats, prefer one primary focal point, legible hierarchy, sufficient contrast, brand coherence and relevant accessibility cues. Do not encode dimensions, safe-zone percentages, engagement targets or universal design claims as fixed rules before the official Meta verification in task 7.

Choose among direct-response/benefit-led, narrative/emotional, educational/authority, and disruptive/entertainment approaches according to audience, brand and objective. Storytelling must use real supplied experiences. Humor must not demean the audience.

Use AIDA (Attention, Interest, Desire, Action), PAS/PASTOR (problem, agitation/amplification, solution, then where supported testimony/offer/response), 4 Cs (clear, concise, credible, convincing), BAB (before, after, bridge), 4 Ps (picture, promise, proof, push), and open loops as optional scaffolds. Do not force or name a formula in every output.

Use social proof, anchoring and reciprocity only when relevant and grounded. Urgency/scarcity requires a real deadline or quantity. Apply social-search keywords naturally. AI may support idea generation, research questions and hook variations; any externally sourced trend or business fact must be verified before use. A/B tests should compare a defined change and an objective-aligned metric.

### Visual and format knowledge

Use flexible heuristics: mobile-first composition, legible hierarchy and contrast, one main focal point, brand coherence, restrained logo placement and relevant accessibility cues. Human faces, authentic/UGC-style imagery, complementary text overlays, carousel continuation cues, F/Z reading and power words are optional creative ideas, not guaranteed performance drivers.

Keep on-image text brief (about 6–8 words as a starting guideline) and use no more than two typefaces where feasible. Do not duplicate the caption in the image. Provide subtitle guidance for video so it works sound-off and alt-text guidance for important images.

Approved first formats are single-image feed post, carousel and Reel; Stories are deferred. A single-image package has one focal visual, complementary overlay, caption and CTA. A carousel has a cover hook, coherent per-slide progression, a resolved ending/CTA and optional continuation cue. A Reel has a concise scene/script outline, opening hook, useful development, closing CTA and readable subtitle/on-screen text direction.

The approved format set is single-image feed posts, carousels and Reels for Instagram/Facebook content generation and adaptation. The existing rendered-media capability remains one Instagram feed-image generation/preview; carousel and Reel outputs are creative plans, not rendered image sets or video. Stories are deferred.

Treat 4:5, 1:1 and 9:16 dimensions, safe-zone percentages, a two-second stop-scroll target, F/Z pattern claims and any CTR/conversion uplift figures from the conversation as provisional heuristics or unverified claims. Verify current official Meta documentation before enforcing technical values. Do not promise reach, engagement or conversion.

### Meta technical and policy verification

Verified against official Meta documentation on 2026-10-06. These constraints affect the approved Instagram/Facebook content scope and the planned Instagram publication boundary; they do not authorize implementation or automatic publication.

| Area | Confirmed constraint | Source |
| --- | --- | --- |
| Account eligibility | The Instagram Content Publishing guide covers professional Instagram accounts. Consumer accounts are not in the verified publishing scope. | [Meta: Content Publishing](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06; page last-updated marker: 2026-06-30. |
| Instagram Login permissions | The Instagram Login path lists `instagram_business_basic` and `instagram_business_content_publish` for publishing. | [Meta: Content Publishing with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/content-publishing), verified 2026-10-06. |
| Facebook Login permissions | The Facebook Login path lists `instagram_basic`, `instagram_content_publish` and `pages_read_engagement`. If the connected Page requires the documented Business Manager role condition, Meta also lists `ads_management` or `ads_read`. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Media input | The publishing request uses `image_url` or `video_url`; Meta fetches the media from the supplied URL, so it must be hosted on a publicly reachable server. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Single-image post | Image publishing is represented by a media container. Meta documents the `alt_text` field for image posts and explicitly notes that this field does not apply to Reels or Stories. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Carousel | A sequence is composed from media items marked with `is_carousel_item=true`, followed by a carousel container and publication. The guide confirms multi-image/video sequences but does not confirm a numeric item maximum in the verified page. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Reel | A Reel uses a video media container with `media_type=REELS` and `video_url`. The published media may report `media_type=VIDEO`; `media_product_type` identifies it as a Reel. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Publication flow | Media is created as a container, its status can be checked through the container status endpoint, and publication uses `/<IG_ID>/media_publish`. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Page publishing authorization | Meta states that publishing to a professional Instagram account connected to a Page requiring Page Publishing Authorization is blocked until that authorization is completed. | [Meta: Content Publishing with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing), verified 2026-10-06. |
| Content policy | Instagram's Community Guidelines require sharing content the user has taken or has the right to share, and prohibit spam and other content outside the guidelines; violations may lead to removal or account restrictions. | [Meta: Instagram Community Guidelines](https://www.facebook.com/help/477434105621119?locale=en_GB), verified 2026-10-06. |

Pending verification:

- The current numeric carousel item maximum was not recorded because it was not confirmed in the official page consulted.
- The current numeric content-publishing rate limit was not recorded; Meta exposes a `content_publishing_limit` endpoint, but no numeric quota was confirmed in the consulted page.
- Current dimensions, aspect ratios, safe zones, duration, file-size and codec limits for each approved format require a separate check of the relevant official media-reference pages before becoming implementation rules.
- Facebook remains a generation/adaptation channel in the approved MVP. Direct Facebook publishing was not added or inferred from the Instagram documentation.

### Guided brief and editable output schemas

These are implementation-neutral contracts for the approved brief-to-post workflow. They define the minimum information exchanged by discovery and drafting; they do not prescribe a database model, API transport or LLM vendor schema.

#### Input: `GuidedBrief`

| Field | Required state | Meaning and constraints |
| --- | --- | --- |
| `topic_or_offer` | Required before business-specific drafting | The subject, offer, event or information to communicate. If missing, discovery asks for it. |
| `objective` | Required before strategy selection | The desired outcome in user language, such as inform, explain, build trust or prompt an action. |
| `audience_context` | May be incomplete during discovery | Customer roles, situation, need/desire and objection. Purchaser, user, decision-maker and referrer remain distinct when they differ. |
| `business_context_refs` | Optional but required for retrieved facts | References to approved business context or user-provided facts used to ground claims; each material fact carries provenance. |
| `platforms` | Required before package generation | One or both approved values: `instagram`, `facebook`. |
| `format` | Required before package generation | Exactly one approved value: `single_image`, `carousel` or `reel`. Stories and other formats are excluded. |
| `brand_and_constraints` | Optional | Known tone, wording, exclusions, accessibility, legal or campaign constraints. Unknown material constraints remain labelled. |
| `facts` | Required for material claims | A list of fact records using the existing `statement`, `status`, `source`, `reason`, `scope` and `validation_needed` model. Status is only `CONFIRMED`, `INFERRED` or `UNKNOWN`. |

The input may be partial while discovery is active. `topic_or_offer`, `objective`, `platforms` and `format` must be confirmed or explicitly resolved before a package is presented as ready. Non-critical unknowns may remain only when they are visible and the draft is editable.

#### Output: `EditableContentPackage`

| Field | Required state | Meaning and constraints |
| --- | --- | --- |
| `strategy` | Required | The traceable chain: `objective`, `audience_situation`, `need_desire_objection`, `core_message`, `platforms`, `format`, `angle` and `cta`. |
| `evidence` | Required | Material fact records, their status and provenance, plus `assumptions`, `unknowns` and any `follow_up_questions`. Unsupported claims are omitted or flagged. |
| `platform_packages` | Required | One editable package per selected platform, preserving the core message while adapting copy and presentation. |
| `platform_packages[].copy` | Required | Caption or equivalent editable text, with a clear hook/body structure where appropriate and a direct CTA when supported by the objective. |
| `platform_packages[].visual_direction` | Required for visual formats | Focal point, hierarchy, contrast, brand guidance and accessibility cues. |
| `platform_packages[].format_detail` | Required | For `single_image`: complementary overlay text; for `carousel`: cover hook and slide outline; for `reel`: scene/script, on-screen text and subtitle guidance. These are plans except for the approved single Instagram feed-image preview capability. |
| `review` | Required | Material validation questions, editable assumptions and `instagram_publication_requires_explicit_confirmation: true`. The output never represents generation as publication approval. |
| `optional_test` | Optional | One defined variant, hypothesis and primary objective-aligned metric only when requested or useful. |

The output must not contain hidden reasoning, unsupported business facts, automatic publication instructions or fields for deferred capabilities such as Stories, direct Facebook publishing, multi-business administration or analytics-driven learning.

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

### Brief-to-post differentiator hypothesis

#### Hypothesis

For the same business facts, objective, channel and format, a guided brief-to-post workflow will help a content manager produce a more relevant and reviewable draft than a generic post generator because it asks only material discovery questions, makes audience evidence status visible and connects the confirmed objective to the message, format and CTA. The expected value is better grounding and less revision effort, not guaranteed engagement or a claim of market uniqueness.

#### Small comparative validation

Use a within-case comparison with three comparable case types: a complete brief with a known audience, a brief with an unknown audience, and a brief with an ambiguous offer or objective. Use the same synthetic or explicitly approved business facts, selected platform and approved format for both conditions.

1. **Baseline:** give the generic generator the available brief and approved facts with a neutral request to create the selected post. Do not add the guided question map.
2. **Guided condition:** run the approved discovery and decision flow, allowing focused questions and recording `CONFIRMED`, `INFERRED` and `UNKNOWN` statuses before drafting.
3. **Blind review:** have the content manager or reviewer assess the two outputs in a random order using the same short rubric. Record the time spent, clarification/revision actions and any unsupported claims.

#### Observable signals

- number of unsupported or untraceable business claims;
- audience relevance and usefulness of the audience hypothesis, rated with the same short scale;
- number and materiality of clarification questions and revision rounds;
- time to a usable editable draft;
- platform/format fit and accessibility/readiness review rating;
- reviewer preference and stated reason, without treating preference as proof of product-market value.

The hypothesis is supported only if the guided condition shows better grounding and audience relevance in most comparable cases without materially worse editability or revision effort. It is weakened or falsified if the generic condition performs as well or better on those signals, or if the guided questions add friction without improving reviewability. Three cases are an initial directional check, not a statistically conclusive result; expand only through an approved follow-up.

This validation stays within the MVP: it evaluates editable drafts and human review for the approved Instagram/Facebook formats. It does not require publication, analytics learning, automatic planning or engagement claims.

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
