# Proposal

## Status and human approval

- Status: Approved
- Issue: #106 — Connect editorial calendar to persisted plans and Content Studio
- Human approval: explicit approval in the task conversation on 2026-10-10.

## Plan objective

Finish the visible MVP workflow by displaying persisted editorial plans in the existing calendar view.

## Objective

Replace the calendar placeholder with a read-only plan view backed by FastAPI and let Content Studio save only already validated plans.

## Scope

Included: web API client for existing plans endpoints, loading/error/empty states, dated plan-item calendar rendering, and a save action for an existing validated plan. Reuse persisted plan and editorial-planning models.

Excluded: scheduling, publication, external calendar sync, new allocation rules, automatic content creation, drag/drop, new review states and changes to persistence.

## Acceptance criteria

- The calendar loads persisted plans and shows dates, platform, format, bucket and review-state source metadata.
- Empty/error states are explicit.
- Content Studio can save an existing validated plan without generating or approving content.
- No calendar action schedules or publishes.
- Existing frontend, Python, SDD, OpenSpec and diff checks pass.

## Rubric

No aplica — integration of existing MVP planning/persistence capabilities.

## Tests and verification

Use synthetic persisted plans and mocked fetch. No provider, publishing or external-calendar calls.

## Open questions and blockers

Visual density remains limited to the current MVP data model.

## Approval

Approved. Human approval received in the task conversation on 2026-10-10.
