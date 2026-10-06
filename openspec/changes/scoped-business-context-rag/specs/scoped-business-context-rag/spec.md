# Scoped Business-Context RAG

## Purpose

Define a local, traceable RAG boundary for consented business context required by Issue #32 and rubric criterion C4.3.

## ADDED Requirements

### Requirement: Canonical documentary source model

The system MUST and SHALL operate on chunkable documentary/textual content and normalize every PDF or authorized API source to one canonical document-chunk model before indexing. The RAG core MUST NOT depend on the source origin.

#### Scenario: Source normalization

- GIVEN a PDF parser output or an already retrieved authorized API response
- WHEN the source is prepared for ingestion
- THEN it produces the same canonical chunk structure with `business_id`, `source_type`, `source_id`, `source_version`, `consent_ref`, `text` and stable `chunk_id`
- AND no HTTP call is required by the normalization boundary.

### Requirement: Origin-specific provenance

The system MUST and SHALL preserve source provenance through indexing and retrieval. PDF chunks MUST retain source file and page number. API chunks MUST retain endpoint/origin URI and `retrieved_at` or an equivalent reproducible version marker when available.

#### Scenario: Provenance survives indexing

- GIVEN canonical PDF and API chunks
- WHEN they are indexed and retrieved
- THEN their origin-specific provenance remains available with the passage and common source metadata.

### Requirement: Deterministic PDF extraction and chunking

The system MUST and SHALL extract PDF text page by page with a maintained text-only PDF parser, ignore completely empty pages, and produce deterministic chunks without OCR or an LLM. Chunk size and overlap MUST be configurable and have documented defaults. PDF chunk identifiers MUST include source identity, page number and chunk position.

#### Scenario: Repeatable local PDF parsing

- GIVEN the same local PDF and the same chunk-size and overlap configuration
- WHEN the parser runs twice
- THEN it returns the same text, page provenance and chunk identifiers
- AND a completely empty page produces no chunk.

### Requirement: Authorized API source connector

The system MUST and SHALL provide a small connector boundary for an authorized, documented JSON API that builds its request, validates the response, and maps useful textual fields to `CanonicalDocumentChunk`. The connector MUST preserve `business_id`, `source_type`, `source_id`, `source_version`, `source_uri`, `retrieved_at`, `chunk_id` and `consent_ref`, and MUST use the shared embeddings, Chroma, retrieval and grounding pipeline after normalization.

#### Scenario: Mocked API ingestion

- GIVEN a mocked JSONPlaceholder `GET /posts/{id}` response containing `id`, `title` and `body`
- WHEN the connector fetches and normalizes the response
- THEN it produces an API `CanonicalDocumentChunk` with deterministic source identity and endpoint provenance
- AND the test does not access the Internet.

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
