# Frontend Editorial Workspace Redesign

## Status and human approval

- Status: Pending
- Issue: #18 — frontend editorial workspace (continuation of PRs #76–#80)
- Branch: `feat/18-editorial-workspace-redesign`
- Human approval: Pending. Implementation in this branch is a proposal for review; it MUST NOT be archived or treated as approved until the project owner approves this contract.

## Plan objective

Deliver the frontend foundation for the multi-brand editorial workspace as an incremental, reviewable change.

## Objective

Evolve the local frontend prototype into a distinctive, white-label, multi-brand editorial workspace, keeping all editorial rules defined by `editorial-review-control` and the local prototype boundaries.

## Scope

### Included

- Split the single-file client into reusable components, shared types, deterministic fixtures and pure editorial-transition functions.
- Platform design tokens (neutral) separated from brand tokens (applied per selected brand).
- App Shell with persistent brand/commerce switcher, navigation including labelled placeholders (Calendar, Library, Analytics, Brands & Stores, Settings), responsive drawer navigation, skip link and visible focus.
- Redesigned Dashboard, Drafts and Content Studio views with deterministic, labelled synthetic previews.
- Correct the synthetic Coll Amunt! fixtures: a local business association in Barcelona with clearly synthetic associated businesses.
- Focused automated tests for editorial transitions and fixture integrity.

### Excluded

- Real social-account connections, analytics, publication, copy/export, LLM calls or persistence.
- RAG navigation, dashboards or technical panels; RAG context is shown only as a discreet contextual note.
- New UI frameworks, animation libraries, web-font downloads or routing changes.
- Backend or API contract changes.

## Acceptance criteria

- Brand and commerce selection changes the dashboard, drafts and brief and never mixes contexts.
- Generating a draft, editing text or changing the brief never produces an approved state; approval is reachable only from pending review through an explicit action; invalid transitions leave the state unchanged.
- Approval in the prototype does not enable copy, export or publication.
- Synthetic data is labelled and never presented as live analytics or real businesses.
- `npm run build`, `npm run typecheck` and `npm test` pass in `apps/web`; existing Python tests are unaffected.

## Rubric

Supports C2 (repository workflow, branch and commit conventions) and the product-communication evidence for the MVP.

## Tests and verification

`npm --prefix apps/web test`, `npm --prefix apps/web run typecheck`, `npm --prefix apps/web run build`, OpenSpec validation, required-field validation, `python -m pytest -q`, and desktop/mobile screenshot review.

## Open questions and blockers

- Pending owner decision: should the web client tests be added to `.github/sdd-harness.yml` and CI? This proposal does not change the harness.
- Pending owner decision: should display fonts be self-hosted? This prototype uses system font stacks and adds no font downloads.
- Pending owner decision: should navigation move to routes? This prototype retains client-side view state; this is not a long-term routing decision.

## Approval

Pending human approval.
