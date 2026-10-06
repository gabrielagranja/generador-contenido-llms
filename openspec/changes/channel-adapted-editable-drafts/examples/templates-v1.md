# Versioned text-template examples

These are contract examples only. They use the synthetic F-01, F-02 and F-03 briefs from Issue #22 and do not contain real business data or rendered media.

## Template metadata

| Template ID | Version | Channel | Approved formats |
| --- | --- | --- | --- |
| `social.instagram.text-draft` | `1.0.0` | Instagram | `single_image`, `carousel`, `reel` |
| `social.facebook.text-draft` | `1.0.0` | Facebook | `single_image`, `carousel`, `reel` |

## Shared output shape

```yaml
template_id: social.instagram.text-draft
template_version: 1.0.0
channel: instagram
format: single_image
caption: editable text
cta: editable next action or null
evidence_refs: [fact identifiers or source labels]
assumptions: []
review_notes: []
```

The Facebook example changes `template_id` and `channel` while preserving the grounded core message. The exact generated copy is implementation output, not part of this contract.

## Fixture coverage

| Fixture | Template use | Required boundary |
| --- | --- | --- |
| F-01 | Instagram `1.0.0` with `single_image` | Use only the confirmed diagnosis facts; return editable caption, CTA and overlay suggestion. |
| F-02 | Facebook `1.0.0` with `carousel` | Keep audience and objective unknown; ask focused questions or return a bounded editable slide-copy plan. |
| F-03 | Both templates with `reel` | Preserve unresolved offer/objective ambiguity; return clarification or a bounded script/subtitle plan without invented details. |
