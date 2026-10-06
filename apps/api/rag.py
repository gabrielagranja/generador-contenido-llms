"""Origin-neutral local document ingestion and RAG index boundary."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata
from typing import Any, Literal

from apps.api.config import RagLocalSettings

SourceType = Literal["pdf", "api"]
DEFAULT_PDF_CHUNK_SIZE = 500
DEFAULT_PDF_CHUNK_OVERLAP = 50


@dataclass(frozen=True)
class CanonicalBusinessRecord:
    """Minimum consented business record accepted by the local index."""

    business_id: str
    source_id: str
    source_version: str
    consent_ref: str
    text: str

    def __post_init__(self) -> None:
        for field_name in (
            "business_id",
            "source_id",
            "source_version",
            "consent_ref",
            "text",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "CanonicalBusinessRecord":
        """Create a record from the fixture-compatible mapping shape."""

        return cls(
            business_id=values["business_id"],
            source_id=values["source_id"],
            source_version=values["source_version"],
            consent_ref=values["consent_ref"],
            text=values["text"],
        )


@dataclass(frozen=True)
class CanonicalDocumentChunk:
    """Origin-neutral document chunk accepted by the RAG ingestion boundary."""

    business_id: str
    source_type: SourceType
    source_id: str
    source_version: str
    consent_ref: str
    text: str
    chunk_id: str
    source_file: str | None = None
    page_number: int | None = None
    source_uri: str | None = None
    retrieved_at: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "business_id",
            "source_id",
            "source_version",
            "consent_ref",
            "text",
            "chunk_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.source_type not in ("pdf", "api"):
            raise ValueError("source_type must be 'pdf' or 'api'")
        if self.source_type == "pdf":
            if not self.source_file or self.page_number is None or self.page_number < 1:
                raise ValueError("PDF chunks require source_file and positive page_number")
        if self.source_type == "api" and not self.source_uri:
            raise ValueError("API chunks require source_uri")


def pdf_to_canonical_chunks(
    *,
    business_id: str,
    source_id: str,
    source_version: str,
    consent_ref: str,
    pages: Sequence[dict[str, Any]],
    source_file: str,
) -> list[CanonicalDocumentChunk]:
    """Normalize parser output into chunks without opening or parsing a PDF.

    Each page mapping must contain ``text`` and ``page_number``. A future PDF
    parser can provide those mappings directly; the index remains independent
    of that parser.
    """

    chunks: list[CanonicalDocumentChunk] = []
    for page in pages:
        page_number = page["page_number"]
        for position, text in enumerate(
            _split_text_deterministically(page["text"], DEFAULT_PDF_CHUNK_SIZE, DEFAULT_PDF_CHUNK_OVERLAP),
            start=1,
        ):
            chunks.append(
                canonical_pdf_chunk(
                business_id=business_id,
                source_id=source_id,
                source_version=source_version,
                consent_ref=consent_ref,
                text=text,
                source_file=source_file,
                page_number=page_number,
                chunk_position=position,
            )
            )
    return chunks


def _split_text_deterministically(text: str, max_chunk_size: int, overlap: int) -> list[str]:
    """Split normalized text on word boundaries with a character overlap."""

    if not isinstance(max_chunk_size, int) or max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be a positive integer")
    if not isinstance(overlap, int) or overlap < 0 or overlap >= max_chunk_size:
        raise ValueError("overlap must be an integer from 0 to max_chunk_size - 1")

    normalized = " ".join(text.split())
    if not normalized:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(start + max_chunk_size, len(normalized))
        if end < len(normalized):
            boundary = normalized.rfind(" ", start + 1, end + 1)
            if boundary > start:
                end = boundary
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(normalized):
            break
        start = end - overlap
        while start < len(normalized) and normalized[start].isspace():
            start += 1
    return chunks


def parse_pdf_to_canonical_chunks(
    pdf_path: str | Path,
    *,
    business_id: str,
    source_id: str,
    source_version: str,
    consent_ref: str,
    max_chunk_size: int = DEFAULT_PDF_CHUNK_SIZE,
    overlap: int = DEFAULT_PDF_CHUNK_OVERLAP,
) -> list[CanonicalDocumentChunk]:
    """Extract and chunk a local PDF, returning only canonical document chunks.

    Extraction is text-only and page-oriented. Empty pages are ignored; OCR,
    network access and indexing are intentionally outside this function.
    """

    from pypdf import PdfReader

    path = Path(pdf_path)
    reader = PdfReader(str(path))
    chunks: list[CanonicalDocumentChunk] = []
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        for chunk_position, text in enumerate(
            _split_text_deterministically(page_text, max_chunk_size, overlap),
            start=1,
        ):
            chunks.append(
                canonical_pdf_chunk(
                    business_id=business_id,
                    source_id=source_id,
                    source_version=source_version,
                    consent_ref=consent_ref,
                    text=text,
                    source_file=str(path),
                    page_number=page_number,
                    chunk_position=chunk_position,
                )
            )
    return chunks


def api_response_to_canonical_chunks(
    *,
    business_id: str,
    source_id: str,
    source_version: str,
    consent_ref: str,
    response: Sequence[dict[str, Any]],
    source_uri: str,
    retrieved_at: str | None = None,
) -> list[CanonicalDocumentChunk]:
    """Normalize already retrieved API content; this function performs no I/O."""

    return [
        canonical_api_chunk(
            business_id=business_id,
            source_id=source_id,
            source_version=source_version,
            consent_ref=consent_ref,
            text=item["text"],
            source_uri=source_uri,
            retrieved_at=retrieved_at,
            chunk_position=position,
        )
        for position, item in enumerate(response, start=1)
    ]


def _legacy_record_to_chunk(record: CanonicalBusinessRecord) -> CanonicalDocumentChunk:
    """Keep the original synthetic fixture shape ingestible during migration."""

    return canonical_api_chunk(
        business_id=record.business_id,
        source_id=record.source_id,
        source_version=record.source_version,
        consent_ref=record.consent_ref,
        text=record.text,
        source_uri=f"synthetic://{record.source_id}",
    )


def normalize_documents(
    documents: Sequence[CanonicalDocumentChunk | CanonicalBusinessRecord],
) -> list[CanonicalDocumentChunk]:
    """Return canonical chunks from new sources or the legacy fixture model."""

    return [
        document
        if isinstance(document, CanonicalDocumentChunk)
        else _legacy_record_to_chunk(document)
        for document in documents
    ]


def canonical_pdf_chunk(
    *,
    business_id: str,
    source_id: str,
    source_version: str,
    consent_ref: str,
    text: str,
    source_file: str,
    page_number: int,
    chunk_position: int = 1,
) -> CanonicalDocumentChunk:
    """Normalize parser output from one PDF page into the canonical model."""

    return CanonicalDocumentChunk(
        business_id=business_id,
        source_type="pdf",
        source_id=source_id,
        source_version=source_version,
        consent_ref=consent_ref,
        text=text,
        chunk_id=f"{source_id}-{source_version}-p{page_number:04d}-c{chunk_position:04d}",
        source_file=source_file,
        page_number=page_number,
    )


def canonical_api_chunk(
    *,
    business_id: str,
    source_id: str,
    source_version: str,
    consent_ref: str,
    text: str,
    source_uri: str,
    retrieved_at: str | None = None,
    chunk_position: int = 1,
) -> CanonicalDocumentChunk:
    """Normalize an already retrieved API payload without making network calls."""

    return CanonicalDocumentChunk(
        business_id=business_id,
        source_type="api",
        source_id=source_id,
        source_version=source_version,
        consent_ref=consent_ref,
        text=text,
        chunk_id=chunk_id_for(source_id, source_version, chunk_position),
        source_uri=source_uri,
        retrieved_at=retrieved_at,
    )


@dataclass(frozen=True)
class RetrievedBusinessContext:
    """Canonical, reviewable result returned by scoped local retrieval."""

    query: str
    business_id: str
    chunk_id: str
    text: str
    score: float
    source_id: str
    source_version: str
    consent_ref: str
    embedding_model: str
    source_type: SourceType | None = None
    source_file: str | None = None
    page_number: int | None = None
    source_uri: str | None = None
    retrieved_at: str | None = None


@dataclass(frozen=True)
class GroundingProvenance:
    """Source identity retained when a claim is supported."""

    business_id: str
    source_id: str
    source_version: str
    chunk_id: str
    consent_ref: str
    source_type: SourceType | None = None
    source_file: str | None = None
    page_number: int | None = None


@dataclass(frozen=True)
class GroundingResult:
    """Deterministic grounding decision for one claim."""

    claim: str
    supported: bool
    evidence: str | None
    provenance: GroundingProvenance | None
    reason: str


_GROUNDING_STOP_WORDS = {"a", "an", "and", "is", "the", "to"}


def _grounding_terms(value: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return {
        term
        for term in re.findall(r"[a-z0-9]+", normalized.lower())
        if term not in _GROUNDING_STOP_WORDS
    }


def ground_claim(
    claim: str,
    contexts: Sequence[RetrievedBusinessContext],
) -> GroundingResult:
    """Check a claim against retrieved text using deterministic lexical support.

    This is intentionally a narrow grounding boundary for synthetic fixtures,
    not a general factuality or semantic entailment system.
    """

    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("claim must be a non-empty string")

    claim_terms = _grounding_terms(claim)
    for context in contexts:
        context_terms = _grounding_terms(context.text)
        if claim_terms and claim_terms.issubset(context_terms):
            return GroundingResult(
                claim=claim,
                supported=True,
                evidence=context.text,
                provenance=GroundingProvenance(
                    business_id=context.business_id,
                    source_id=context.source_id,
                    source_version=context.source_version,
                    chunk_id=context.chunk_id,
                    consent_ref=context.consent_ref,
                    source_type=context.source_type,
                    source_file=context.source_file,
                    page_number=context.page_number,
                ),
                reason="All claim terms are present in the retrieved evidence.",
            )

    return GroundingResult(
        claim=claim,
        supported=False,
        evidence=None,
        provenance=None,
        reason="No retrieved evidence contains all claim terms.",
    )


def chunk_id_for(
    source_id: str,
    source_version: str,
    chunk_position: int = 1,
) -> str:
    """Return the stable ID for a single full-record chunk."""

    if not source_id.strip() or not source_version.strip():
        raise ValueError("source_id and source_version must not be empty")
    if not isinstance(chunk_position, int) or chunk_position < 1:
        raise ValueError("chunk_position must be a positive integer")
    return f"{source_id}-{source_version}-{chunk_position:04d}"


class LocalEmbeddingFunction:
    """Adapt a local SentenceTransformer model to Chroma's embedding protocol."""

    def __init__(
        self,
        settings: RagLocalSettings,
        model_factory: Callable[..., Any] | None = None,
    ) -> None:
        if model_factory is None:
            from sentence_transformers import SentenceTransformer

            model_factory = SentenceTransformer

        self.model_name = settings.embedding_model
        self.revision = settings.embedding_revision
        self._model = model_factory(
            self.model_name,
            revision=self.revision,
        )

    def __call__(self, input: Sequence[str]) -> list[list[float]]:
        vectors = self._model.encode(
            list(input),
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        if hasattr(vectors, "tolist"):
            return vectors.tolist()
        return [list(vector) for vector in vectors]


def build_local_embedding(
    settings: RagLocalSettings,
    model_factory: Callable[..., Any] | None = None,
) -> LocalEmbeddingFunction:
    """Build the configured local embedding function, with test injection."""

    return LocalEmbeddingFunction(settings, model_factory=model_factory)


class LocalChromaIndex:
    """Initialize one persistent local Chroma collection and ingest records."""

    def __init__(
        self,
        settings: RagLocalSettings,
        embedding_function: Any | None = None,
        chroma_client: Any | None = None,
    ) -> None:
        settings.validate()
        self.settings = settings
        self.embedding_function = (
            embedding_function
            if embedding_function is not None
            else build_local_embedding(settings)
        )

        if chroma_client is None:
            import chromadb

            chroma_client = chromadb.PersistentClient(
                path=str(settings.chroma_persist_directory)
            )

        self.client = chroma_client
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection,
            embedding_function=self.embedding_function,
        )

    def ingest(
        self,
        records: Sequence[CanonicalDocumentChunk | CanonicalBusinessRecord],
    ) -> list[str]:
        """Normalize and upsert canonical document chunks.

        Chroma's upsert semantics make repeated ingestion of the same stable ID
        idempotent while still allowing synthetic businesses to coexist.
        """

        records = normalize_documents(records)
        chunk_ids = [record.chunk_id for record in records]
        if len(chunk_ids) != len(set(chunk_ids)):
            raise ValueError("records must not contain duplicate source/version chunks")
        if not records:
            return []

        texts = [record.text for record in records]
        embeddings = self.embedding_function(texts)
        embedding_model = f"{self.settings.embedding_model}@{self.settings.embedding_revision}"
        metadata = [
            {
                "business_id": record.business_id,
                "source_id": record.source_id,
                "source_version": record.source_version,
                "consent_ref": record.consent_ref,
                "chunk_id": chunk_id,
                "embedding_model": embedding_model,
                "source_type": record.source_type,
                **(
                    {"source_file": record.source_file, "page_number": record.page_number}
                    if record.source_type == "pdf"
                    else {"source_uri": record.source_uri, "retrieved_at": record.retrieved_at}
                ),
            }
            for record, chunk_id in zip(records, chunk_ids)
        ]
        self.collection.upsert(
            ids=chunk_ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadata,
        )
        return chunk_ids

    def query(
        self,
        query: str,
        business_id: str,
        top_k: int,
    ) -> list[RetrievedBusinessContext]:
        """Retrieve scoped records with provenance and Chroma distance scores."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if not isinstance(business_id, str) or not business_id.strip():
            raise ValueError("business_id must be a non-empty string")
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        query_embedding = self.embedding_function([query])[0]
        response = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"business_id": business_id},
            include=["documents", "metadatas", "distances"],
        )
        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]
        ids = response.get("ids", [[]])[0]

        results: list[RetrievedBusinessContext] = []
        for index, (text, metadata, distance) in enumerate(
            zip(documents, metadatas, distances)
        ):
            result_metadata = metadata or {}
            results.append(
                RetrievedBusinessContext(
                    query=query,
                    business_id=result_metadata["business_id"],
                    chunk_id=result_metadata.get("chunk_id", ids[index]),
                    text=text,
                    score=float(distance),
                    source_id=result_metadata["source_id"],
                    source_version=result_metadata["source_version"],
                    consent_ref=result_metadata["consent_ref"],
                    embedding_model=result_metadata["embedding_model"],
                    source_type=result_metadata.get("source_type"),
                    source_file=result_metadata.get("source_file"),
                    page_number=result_metadata.get("page_number"),
                    source_uri=result_metadata.get("source_uri"),
                    retrieved_at=result_metadata.get("retrieved_at"),
                )
            )
        return results[:top_k]


__all__ = [
    "CanonicalBusinessRecord",
    "CanonicalDocumentChunk",
    "DEFAULT_PDF_CHUNK_OVERLAP",
    "DEFAULT_PDF_CHUNK_SIZE",
    "GroundingProvenance",
    "GroundingResult",
    "LocalChromaIndex",
    "LocalEmbeddingFunction",
    "RetrievedBusinessContext",
    "canonical_api_chunk",
    "canonical_pdf_chunk",
    "build_local_embedding",
    "api_response_to_canonical_chunks",
    "chunk_id_for",
    "ground_claim",
    "normalize_documents",
    "parse_pdf_to_canonical_chunks",
    "pdf_to_canonical_chunks",
]
