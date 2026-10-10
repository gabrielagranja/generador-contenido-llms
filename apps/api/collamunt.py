"""Official Coll Amunt! PDF source adapter and stable business identities."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from pathlib import Path
from typing import Any, Sequence

from apps.api.rag import (
    CanonicalDocumentChunk,
    pdf_to_canonical_chunks,
    sha256_file,
)

COLLAMUNT_SOURCE_URI = (
    "https://www.collamunt.cat/wp-content/uploads/2017/04/"
    "2025-Coll-Amunt-Llibre-_compressed.pdf"
)
COLLAMUNT_SOURCE_FILE = "2025-Coll-Amunt-Llibre-_compressed.pdf"
COLLAMUNT_SOURCE_ID = "collamunt-llibre"
COLLAMUNT_SOURCE_VERSION = "2025"
COLLAMUNT_CONSENT_REF = "public-official-collamunt-source"

# The page labels are transcribed from the official PDF's page headings. The
# page number is part of the source identity, while the slug is stable across
# reruns and independent of OCR spelling noise.
COLLAMUNT_BUSINESS_PAGES: dict[int, str] = {
    3: "Pelu Sonia",
    4: "Centre d'Estètica Alma",
    5: "Vifeca Electrodomèstics",
    6: "Sellos Barcelona",
    7: "El Raconet de la Dori",
    8: "Fruit Vallcarca",
    9: "Forn de Pa Rosa",
    10: "Informàtica BCN",
    11: "Farmàcia Hermínia Reguera",
    12: "Clínica Dental Drs. Méndez",
    13: "Papereria Canigó",
    14: "Tave Sabateries",
    15: "La Tapeta del Coll",
    16: "Pack Santuari",
    17: "Perruqueria Mari & Fali",
    18: "Marbra Gestió",
    19: "Formes Joiers",
    20: "Condis - Carmel",
    21: "Canicats",
    22: "Hay Pan",
    23: "De Capa Puntes",
    24: "Coviran",
    25: "Agreste",
    26: "Farmàcia Joan Fuentellobet",
    27: "El Rincón del Cazador",
    28: "Cristaleria Camacho",
    29: "Duca",
    30: "EcoLL",
    31: "Bar Restaurante Reencuentro",
    32: "Wayd Digital Hub",
    33: "Farmàcia Reig",
    34: "Bar Santuari",
    35: "Farmàcia El Coll",
}


@dataclass(frozen=True)
class CollAmuntIngestion:
    """Deterministic, auditable result of preparing the official source."""

    source_file: str
    source_sha256: str
    page_count: int
    chunk_count: int
    business_ids: tuple[str, ...]
    chunks: tuple[CanonicalDocumentChunk, ...]


def stable_business_id(name: str) -> str:
    """Create a stable ASCII identifier from a PDF business heading."""

    normalized = (
        unicodedata.normalize("NFKD", name)
        .encode("ascii", "ignore")
        .decode()
        .lower()
    )
    slug = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    if not slug:
        raise ValueError("business name must contain letters or numbers")
    return f"coll-amunt-{slug}"


def collamunt_business_id_for_page(page_number: int) -> str:
    if page_number in COLLAMUNT_BUSINESS_PAGES:
        return stable_business_id(COLLAMUNT_BUSINESS_PAGES[page_number])
    if page_number in {1, 2, 36}:
        return "coll-amunt"
    raise ValueError(f"no Coll Amunt business mapping for page {page_number}")


def build_collamunt_chunks(
    pdf_path: str | Path,
    pages: Sequence[dict[str, Any]],
) -> CollAmuntIngestion:
    """Assign official PDF pages to the association or one named business."""

    path = Path(pdf_path)
    digest = sha256_file(path)
    chunks: list[CanonicalDocumentChunk] = []
    for page in pages:
        page_number = int(page["page_number"])
        business_id = collamunt_business_id_for_page(page_number)
        page_chunks = pdf_to_canonical_chunks(
            business_id=business_id,
            source_id=COLLAMUNT_SOURCE_ID,
            source_version=COLLAMUNT_SOURCE_VERSION,
            consent_ref=COLLAMUNT_CONSENT_REF,
            pages=[page],
            source_file=COLLAMUNT_SOURCE_FILE,
            source_uri=COLLAMUNT_SOURCE_URI,
            source_sha256=digest,
        )
        chunks.extend(page_chunks)
    return CollAmuntIngestion(
        source_file=COLLAMUNT_SOURCE_FILE,
        source_sha256=digest,
        page_count=len(pages),
        chunk_count=len(chunks),
        business_ids=tuple(sorted({chunk.business_id for chunk in chunks})),
        chunks=tuple(chunks),
    )


__all__ = [
    "COLLAMUNT_BUSINESS_PAGES",
    "COLLAMUNT_CONSENT_REF",
    "COLLAMUNT_SOURCE_FILE",
    "COLLAMUNT_SOURCE_ID",
    "COLLAMUNT_SOURCE_URI",
    "COLLAMUNT_SOURCE_VERSION",
    "CollAmuntIngestion",
    "build_collamunt_chunks",
    "collamunt_business_id_for_page",
    "stable_business_id",
]
