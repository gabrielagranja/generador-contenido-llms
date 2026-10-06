# Design

## Boundary

This change adds a local retrieval boundary for approved business context. It consumes a query and business scope and returns grounded passages with provenance. It does not redefine `GuidedBrief`, generate copy, publish content or change the interface.

## Minimal local architecture

1. **Consent gate:** accept only synthetic or explicitly consented records with a stable `business_id`, `source_id`, `source_version` and `consent_ref`.
2. **Chunking:** split each short source record into stable chunks and assign a `chunk_id` derived from the source/version and chunk position.
3. **Embedding:** encode chunks with one configured multilingual embedding model executed locally. The model identifier and revision are stored with the index configuration.
4. **Chroma store:** persist vectors in a local Chroma collection scoped by environment and business. No remote vector database is required for the initial slice.
5. **Retrieval:** embed the query locally, retrieve a bounded top-k set, filter by the requested `business_id`, and return passage text, score and provenance metadata.
6. **Grounding handoff:** pass retrieved evidence to the existing generation boundary as cited context. Claims without support in the returned evidence remain unsupported and must be omitted or flagged.

## Record and retrieval contracts

Each indexed record must carry:

```text
business_id      stable synthetic or consented business scope
source_id        stable source record identifier
source_version   content version or revision
consent_ref      consent or synthetic-fixture reference
chunk_id         stable chunk identifier
text             chunk text
embedding_model  local model identifier and revision
```

Each retrieval result must carry:

```text
query
business_id
chunk_id
text
score
source_id
source_version
consent_ref
embedding_model
```

The generator must be able to cite `source_id`, `source_version` and `chunk_id` in the reviewable grounding context. A score ranks retrieval; it is not a truth or confidence guarantee.

## Scope and privacy safeguards

- The business filter is mandatory; a query for one business cannot return another business's records.
- Synthetic records are the default test data. Real records require explicit consent and must not be committed as fixtures.
- No crawling, automatic source discovery, personal-data enrichment or cross-business profile is included.
- Deletion or replacement must address the source version and all derived chunks in the local collection before real data is allowed.

## Verification strategy

Use two synthetic businesses with deliberately overlapping terms and one unsupported claim. Verify that the business filter prevents cross-scope leakage, source metadata survives retrieval, the same local setup reproduces the result, and the grounding handoff distinguishes supported from unsupported claims. Issue #25 records broader representative-brief evaluation; Issue #36 records final evidence.

## Instructor clarification

The instructor's requested clarification about RAG evidence depth is still unanswered. The initial design therefore records observable artifacts—index configuration, synthetic source records, retrieval results, citations and tests—while allowing the later evaluation contract to add evidence requirements if needed.
