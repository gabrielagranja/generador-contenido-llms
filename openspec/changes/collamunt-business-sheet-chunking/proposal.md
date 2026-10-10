# Proposal

## Status and human approval

- Status: Pending
- Issue: #97 — Chunk Coll Amunt business sheets by sentence instead of fixed 500 characters
- Human approval: Pending

## Objective

Split Coll Amunt business sheets by paragraph and sentence, up to
`COLLAMUNT_SHEET_CHUNK_SIZE = 800` characters, instead of applying fixed
500-character chunks.

## Plan objective

Define and verify a deterministic, sentence-aware ingestion strategy for Coll
Amunt business sheets while keeping retrieval-quality validation explicitly
pending.

## Scope

### Included

- Deterministic paragraph- and sentence-aware chunking for Coll Amunt business sheets.
- Business-name and source metadata preservation for every generated chunk.
- Tests for short sheets, sentence boundaries, oversized sentences and business isolation.
- Rebuilding the local Chroma index with `scripts/ingest_collamunt.py` after approval.

### Excluded

- Changes to embedding models or retrieval ranking.
- Changes to browser behavior, API contracts or publication workflows.
- Committing anything under `.local/`.

## Acceptance criteria

- Business sheets are split by paragraph and sentence up to the configured limit.
- Each chunk preserves the correct business and source metadata.
- The 800-character limit remains an explicit open question until the 14 expert queries are evaluated.

## Rubric

The change is limited to deterministic ingestion and preserves business
identity, source traceability and reproducibility.

## Open questions and blockers

- The embedding model reads approximately 128 tokens. Validate whether 800 characters improves retrieval quality against the expert's 14 queries.
- The local index must be rebuilt with `scripts/ingest_collamunt.py` after the Python dependencies are available.
- The repository does not contain the expert's 14-query evaluation set, so recall, relevance, citation quality and cross-business contamination cannot yet be compared empirically.

## Verification

- Run `python -m pytest -q`.
- Run `python scripts/validate_sdd_contract.py`.
- Run `git diff --check`.
- Rebuild and inspect the local Chroma index without committing `.local/`.

## Tests and verification

- Full pytest, SDD contract validation and `git diff --check` must pass.
- Retrieval quality must be evaluated with the expert's 14 queries after index rebuild.
- The configured tokenizer reports a 128-token maximum. With the business-name prefix included, measured chunks are 86 at 500 characters (17 above 128 tokens; 19.8%) and 59 at 800 characters (35 above 128 tokens; 59.3%).

## Approval

Pending explicit human approval.
