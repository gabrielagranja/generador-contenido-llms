# Proposal

## Status and human approval

- Status: Pending
- Issue: #23 — [STORY] Generate channel-adapted content
- Parent epic: #10
- Depends on: approved Issue #22 contract (`expert-content-generation`)
- Human approval: Pending

## Objective

Define the smallest implementation slice that turns an approved `GuidedBrief` into editable text drafts adapted for Instagram and Facebook, using versioned prompt templates and fixed synthetic examples.

## Plan objective

Advance the approved Issue #22 brief into the next minimal content-generation slice while preserving its grounding, channel and format boundaries.

## Scope

### Included

- Text-only draft generation for the approved `instagram` and `facebook` channels.
- A versioned template for each supported channel, with a shared grounded input contract from Issue #22.
- Channel-specific instructions for tone, structure, CTA and concise readability while preserving the approved strategy and facts.
- Editable output containing the selected channel, format, caption text, CTA, evidence references, assumptions and review notes.
- Synthetic examples covering a confirmed brief, an audience-unknown brief and an ambiguous brief, using the existing F-01, F-02 and F-03 fixtures.
- Tests that verify template selection, version metadata, channel adaptation and rejection or omission of unsupported claims.

### Excluded

- Image generation, image editing, carousel rendering or video generation.
- Instagram or Facebook publication, scheduling, OAuth or platform API calls.
- Changes to the web interface.
- New discovery, fact, audience or format contracts; those remain defined by Issue #22.
- RAG retrieval, analytics learning, performance guarantees and real business data without explicit approval.

## Acceptance criteria

- The generator consumes the approved `GuidedBrief` and does not redefine its fields or fact statuses.
- The selected channel determines a versioned template and visible channel-specific adaptation.
- A draft remains editable and separates caption, CTA, evidence/assumptions and review notes.
- Unsupported business facts, benefits, testimonials, statistics, deadlines, scarcity, credentials and guarantees are not invented.
- Instagram and Facebook drafts preserve the same grounded core message while allowing channel-specific wording and structure.
- The examples and tests use only F-01, F-02 and F-03 synthetic data and cover the approved single-image, carousel and Reel formats as text/creative-plan outputs.
- No visual asset, publication action or interface change is required by this contract.

## Verification

- Validate the OpenSpec change and SDD required fields.
- Test each template version against the three existing synthetic fixtures.
- Inspect generated text for grounding, channel fit, editability and absence of publication/visual behavior.

## Rubric

This change is scoped to the content-generation behavior associated with the approved Issue #22 contract. It does not by itself claim completion of LLM, application-framework or RAG rubric evidence; those require implementation and recorded evaluation evidence.

## Tests and verification

- Run OpenSpec active-change and required-field validation.
- Run the focused application tests with external provider calls mocked after approval and implementation.
- Review F-01, F-02 and F-03 outputs for grounding, channel adaptation, editability and excluded capabilities.

## Open questions and blockers

- Human approval of this proposal is required before implementation.
- The exact copy language-selection behavior remains inherited from the Issue #22 open question.
- Current platform constraints must not be converted into fixed numeric rules without official verification.

## Approval boundary

This proposal is not approved yet. No application implementation may begin until the user explicitly approves this contract.

## Approval

Pending explicit human approval. Once approved, implementation MAY proceed in `tasks.md` order; publication, visual generation and interface changes remain excluded.
