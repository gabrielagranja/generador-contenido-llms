# Design

## Contract relationship

This is a delta to the approved Issue #22 contract. Issue #22 remains the source of truth for `GuidedBrief`, `EditableContentPackage`, fact statuses, the objective-to-CTA chain, approved channels and approved formats. This change adds only textual channel adaptation and versioned templates.

## Minimal flow

1. Accept a validated `GuidedBrief` and its visible fact provenance.
2. Select the immutable template version for each requested channel.
3. Supply the objective, audience context, core message, format, angle, CTA and grounded facts to the template.
4. Return an editable text package with channel, format, template version, caption, CTA, evidence references, assumptions and review notes.
5. Keep unknown or inferred material information visible; omit or qualify unsupported claims.

The flow produces copy and format-specific creative-plan text only. It does not render media, publish, schedule or modify the interface.

## Versioned templates

| Template ID | Version | Channel | Approved formats |
| --- | --- | --- | --- |
| `social.instagram.text-draft` | `1.0.0` | Instagram | `single_image`, `carousel`, `reel` |
| `social.facebook.text-draft` | `1.0.0` | Facebook | `single_image`, `carousel`, `reel` |

Each template version records its channel instructions, accepted Issue #22 fields, output sections and grounding safeguards. Changes to those instructions create a new version and never silently mutate an existing version.

## Channel adaptation

- Instagram: concise hook, scannable caption, direct CTA and optional functional keywords/hashtags.
- Facebook: conversational opening, enough context for the feed, direct CTA and readable structure.
- Both: preserve the same grounded core message while adapting wording and presentation; do not duplicate text blindly or add facts.

These are contextual heuristics, not performance guarantees. Numeric placement, dimension or safe-zone rules remain outside this contract unless officially verified.

## Editable output boundary

The package may contain caption copy, CTA, complementary single-image overlay text, carousel slide-copy outline, or Reel scene/script/subtitle text plan. It must not contain rendered assets, access tokens, publication instructions or automatic publishing actions.

## Examples and tests

Reuse F-01, F-02 and F-03 from the approved #22 fixtures. Test a complete confirmed brief, an audience-unknown brief and an ambiguous offer/objective. Unknown or ambiguous cases may return focused questions or a bounded editable draft, but never fabricated facts.
