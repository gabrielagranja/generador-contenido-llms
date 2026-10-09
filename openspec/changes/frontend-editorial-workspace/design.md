# Design: Frontend Editorial Workspace Redesign

## Architecture

`app/page.tsx` renders `components/Workspace.tsx`, which owns the local state and composes `AppShell` (Sidebar, Topbar, BrandSwitcher) with `Dashboard`, `DraftsView`, `HistoryView`, `ContentStudio` (BriefEditor, ContentPreview, ReviewActions) and `PlaceholderView`. Drafts prepared in the browser session remain listed for that session. Shared UI: `EditorialStatus`, `PostArt`, `Kicker`. Domain code lives in `domain/` (`types`, `fixtures`, `editorial`); `lib/` is avoided because it is git-ignored.

## Styling

`styles/tokens.css` defines neutral platform tokens. CSS Modules scope component styles. Brand colours are injected as `--brand-*` custom properties on the shell and only colour brand artefacts (monogram, rule, synthetic post art, active accents).

## Editorial rules

Transitions are pure functions in `domain/editorial.ts` and are covered by tests. The local prototype state set is narrower than the production lifecycle (`approved` is local only) and the UI says so. Editing a brief invalidates review/approval; editing text that was locally approved also invalidates that approval. No copy, export or publish action is exposed.
