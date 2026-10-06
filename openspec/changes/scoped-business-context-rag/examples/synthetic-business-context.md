# Synthetic business-context examples

These records are synthetic and contain no real business, customer or credential data. They illustrate the minimum metadata and grounding checks; they are not application fixtures yet.

## Records

| Business | Source | Version | Consent reference | Text |
| --- | --- | --- | --- | --- |
| `synthetic-bakery-a` | `menu-a` | `v1` | `synthetic-fixture` | “Weekday breakfast box includes bread and fruit. Price and availability are not specified.” |
| `synthetic-bakery-b` | `menu-b` | `v1` | `synthetic-fixture` | “Weekend breakfast box includes bread and fruit. Price and availability are not specified.” |

The overlapping phrase “breakfast box” is intentional. A query scoped to `synthetic-bakery-a` must never cite `menu-b`.

## Expected retrieval evidence

```yaml
business_id: synthetic-bakery-a
source_id: menu-a
source_version: v1
consent_ref: synthetic-fixture
chunk_id: menu-a-v1-0001
embedding_model: local-multilingual-model@revision
```

## Grounding examples

- Supported: “The weekday box includes bread and fruit” when the cited `menu-a` passage is retrieved.
- Unsupported: “The box costs five euros” because no price appears in either synthetic record; the claim must be omitted or flagged.
- Isolation: a result from `menu-b` is invalid for a query scoped to `synthetic-bakery-a`, even though the wording overlaps.
