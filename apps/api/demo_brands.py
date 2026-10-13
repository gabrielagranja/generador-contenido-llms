"""Auditable local source adapters for the independent demo brands."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from apps.api.rag import (
    CanonicalDocumentChunk,
    canonical_api_chunk,
    extract_pdf_pages,
    pdf_to_canonical_chunks,
)

TALENT_HIVE_BRAND_ID = "talent-hive"
TALENT_HIVE_BUSINESS_ID = "talent-hive"
TALENT_HIVE_SOURCE_VERSION = "2026-10"
TALENT_HIVE_CONSENT_REF = "public-official-talent-hive-source"
TALENT_HIVE_SOURCES = (
    "https://thehive.barcelona/the-hive-escape-boxes/",
    "https://thehive.barcelona/blog/escape-room-empresas/",
)

WAYDDH_BRAND_ID = "wayddh"
WAYDDH_BUSINESS_ID = "wayddh"
WAYDDH_SOURCE_FILE = "2025-Coll-Amunt-Llibre-_compressed.pdf"
WAYDDH_SOURCE_ID = "wayddh-corporate-pdf"
WAYDDH_SOURCE_VERSION = "2025"
WAYDDH_CONSENT_REF = "local-official-wayddh-pdf-page-32"
WAYDDH_SOURCE_URI = "https://www.wayddh.com/marketing-digital/"
WAYDDH_PDF_PATH = Path(".local") / "rag" / "sources" / WAYDDH_SOURCE_FILE
WAYDDH_PDF_PAGE = 32


def build_talent_hive_chunks() -> list[CanonicalDocumentChunk]:
    """Return only claims explicitly allowed for the Talent Hive demo."""

    texts = [
        "Talent Hive ofrece formación, coaching, team building y soluciones gamificadas para empresas. Su catálogo incluye Escape Rooms, The Hive Escape Boxes y experiencias formativas.",
        "The Hive Escape Boxes son experiencias portátiles y personalizables para actividades de empresas. Una sesión dura entre 45 y 60 minutos y cada caja está pensada para equipos de 4 a 6 personas.",
    ]
    return [
        canonical_api_chunk(
            business_id=TALENT_HIVE_BUSINESS_ID,
            brand_id=TALENT_HIVE_BRAND_ID,
            source_id="talent-hive-official-pages",
            source_version=TALENT_HIVE_SOURCE_VERSION,
            consent_ref=TALENT_HIVE_CONSENT_REF,
            text=text,
            source_uri=TALENT_HIVE_SOURCES[index],
            source_name="The Hive Escape Boxes" if index == 1 else "Talent Hive official pages",
            language="es",
            chunk_position=index + 1,
        )
        for index, text in enumerate(texts)
    ]


def build_wayddh_chunks(
    pdf_path: str | Path,
    pages: Sequence[dict[str, Any]] | None = None,
) -> list[CanonicalDocumentChunk]:
    """Extract only the WAYDDH page from the existing corporate PDF source."""

    path = Path(pdf_path)
    page_payloads = list(pages) if pages is not None else extract_pdf_pages(path)
    wayddh_pages = [
        page for page in page_payloads if int(page["page_number"]) == WAYDDH_PDF_PAGE
    ]
    if not wayddh_pages or not " ".join(str(wayddh_pages[0].get("text", "")).split()):
        raise ValueError(
            f"No se encontró texto de WAYDDH en la página {WAYDDH_PDF_PAGE} de '{path}'. "
            "Revisa el PDF corporativo u OCR local antes de indexarlo."
        )
    return pdf_to_canonical_chunks(
        business_id=WAYDDH_BUSINESS_ID,
        brand_id=WAYDDH_BRAND_ID,
        source_id=WAYDDH_SOURCE_ID,
        source_version=WAYDDH_SOURCE_VERSION,
        consent_ref=WAYDDH_CONSENT_REF,
        pages=wayddh_pages,
        source_file=WAYDDH_SOURCE_FILE,
        source_uri=WAYDDH_SOURCE_URI,
    )


def load_demo_brand_chunks(
    pdf_path: str | Path = WAYDDH_PDF_PATH,
) -> list[CanonicalDocumentChunk]:
    """Build Talent Hive and, when present, WAYDDH demo chunks locally."""

    chunks = build_talent_hive_chunks()
    path = Path(pdf_path)
    if path.exists():
        chunks.extend(build_wayddh_chunks(path))
    return chunks


__all__ = [
    "TALENT_HIVE_BRAND_ID",
    "TALENT_HIVE_SOURCES",
    "WAYDDH_BRAND_ID",
    "WAYDDH_PDF_PAGE",
    "WAYDDH_PDF_PATH",
    "WAYDDH_SOURCE_URI",
    "build_talent_hive_chunks",
    "build_wayddh_chunks",
    "load_demo_brand_chunks",
]
