# Design

The Coll Amunt ingestion boundary will recognize pages that represent
individual business sheets and process them with a dedicated deterministic
chunker. Paragraphs remain intact when they fit within the configured limit.
Longer paragraphs are split at sentence boundaries, and a sentence that still
exceeds the limit falls back to deterministic word-boundary splitting.

The chunk size is configured as `COLLAMUNT_SHEET_CHUNK_SIZE = 800`. Each chunk
keeps the business name, stable business ID, source ID, source version, source
hash, page number and chunk position. Association pages continue using the
existing generic PDF chunking path.

The value of 800 characters is a pending retrieval-quality decision: the
embedding model reads approximately 128 tokens, so the implementation must be
validated against the expert's 14 queries after the local Chroma index is
rebuilt. The index is a local verification artifact and must not be committed.
