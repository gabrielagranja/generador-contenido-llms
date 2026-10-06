# Scoped Business-Context RAG

## Purpose

Define a local, traceable RAG boundary for consented business context required by Issue #32 and rubric criterion C4.3.

## ADDED Requirements

### Requirement: Consent-scoped local index

The system MUST and SHALL index only synthetic or explicitly consented business-context records in a local Chroma collection.

#### Scenario: Synthetic record ingestion

- GIVEN a record has `business_id`, `source_id`, `source_version` and `consent_ref`
- WHEN the record is ingested
- THEN it is chunked and stored with those metadata fields
- AND no external source or provider call is required.

### Requirement: Local multilingual embeddings

The system MUST and SHALL use a configured multilingual embedding model executed locally for indexing and retrieval.

#### Scenario: Embedding configuration

- GIVEN the local embedding model identifier and revision are configured
- WHEN a record or query is embedded
- THEN the same local configuration is used
- AND the retrieval path does not call a hosted embedding API.

### Requirement: Business-scoped retrieval

The system MUST and SHALL filter retrieval by the requested `business_id` and return a bounded ranked result set.

#### Scenario: No cross-business leakage

- GIVEN two businesses contain similar terms
- WHEN a query is made for one business
- THEN every result belongs to that business
- AND each result includes its similarity score and chunk identifier.

### Requirement: Traceable grounding evidence

The system MUST and SHALL return passage text and provenance sufficient to trace a result to its source record, version and consent reference.

#### Scenario: Supported factual claim

- GIVEN a claim is supported by a retrieved approved passage
- WHEN the generation boundary receives the retrieval result
- THEN the passage and provenance can be cited for review.

#### Scenario: Unsupported factual claim

- GIVEN a claim has no support in the retrieved context
- WHEN grounding is checked
- THEN the claim is flagged or omitted
- AND SHALL NOT be presented as retrieved business fact.

### Requirement: Reproducible local verification

The system MUST and SHALL expose enough configuration and result metadata to reproduce a retrieval against the same local index and embedding revision.

#### Scenario: Synthetic verification run

- GIVEN the approved synthetic records and fixed local configuration
- WHEN the same query is run twice
- THEN the result identifiers and provenance can be compared
- AND the run does not require publication, analytics or interface capabilities.
