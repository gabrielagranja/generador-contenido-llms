# Versioned template examples

These examples reference only the synthetic F-01, F-02 and F-03 fixtures from Issue #22. They are contract examples, not generated copy.

| Template ID | Version | Channel | Formats |
| --- | --- | --- | --- |
| `social.instagram.text-draft` | `1.0.0` | Instagram | `single_image`, `carousel`, `reel` |
| `social.facebook.text-draft` | `1.0.0` | Facebook | `single_image`, `carousel`, `reel` |

```yaml
template_id: social.instagram.text-draft
template_version: 1.0.0
channel: instagram
format: single_image
caption: editable text
cta: editable next action or null
evidence_refs: []
assumptions: []
review_notes: []
```

## Fixture mapping

| Fixture | Template use | Required behavior |
| --- | --- | --- |
| F-01 | Instagram `1.0.0`, `single_image` | Use only confirmed diagnosis facts; return editable caption, CTA and overlay text suggestion. |
| F-02 | Facebook `1.0.0`, `carousel` | Keep audience/objective unknown; ask focused questions or return a bounded editable slide-copy plan. |
| F-03 | Both templates, `reel` | Preserve ambiguous offer/objective; return clarification or bounded script/subtitle text without invented details. |
