# Coll Amunt business sheet chunking

## ADDED Requirements

### Requirement: sentence-aware business sheet chunks

The ingestion pipeline MUST and SHALL split Coll Amunt business sheets by paragraph and
sentence up to `COLLAMUNT_SHEET_CHUNK_SIZE`, whose initial value is 800
characters, instead of fixed 500-character chunks.

#### Scenario: short business sheet

- GIVEN a business sheet whose normalized text fits within the configured limit
- WHEN the sheet is ingested
- THEN it produces one chunk containing the sheet text and business metadata.

#### Scenario: long business sheet

- GIVEN a business sheet containing multiple paragraphs or sentences beyond the configured limit
- WHEN the sheet is ingested
- THEN chunks end at paragraph or sentence boundaries whenever possible and preserve source metadata.

#### Scenario: oversized sentence

- GIVEN a single sentence longer than the configured limit
- WHEN the sheet is ingested
- THEN it is split deterministically at word boundaries without exceeding the limit.

### Requirement: business isolation

The ingestion pipeline MUST and SHALL keep each business sheet's chunks associated with
the correct stable business ID, page number and source digest.

#### Scenario: mixed source pages

- GIVEN business-sheet pages and association pages in one source document
- WHEN the source is ingested
- THEN business sheets use sentence-aware chunking while association pages retain generic chunking.

### Requirement: retrieval validation remains pending

The project MUST and SHALL record validation of the 800-character limit against the
expert's 14 queries as an open question until the local index is rebuilt and
the retrieval quality is assessed.

#### Scenario: evaluation queries not yet available

- GIVEN the expert's 14-query evaluation set is unavailable or the local index has not been rebuilt
- WHEN the proposed 800-character chunk size is reviewed
- THEN retrieval quality remains explicitly unvalidated and human approval stays pending.
