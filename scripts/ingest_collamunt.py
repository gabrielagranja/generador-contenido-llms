"""Download-free local ingestion for the official Coll Amunt! PDF.

The PDF itself belongs in ignored .local/rag/sources/. This command only writes
the local Chroma collection and a non-secret manifest beside that source.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from apps.api.collamunt import build_collamunt_chunks
from apps.api.config import RagLocalSettings
from apps.api.rag import LocalChromaIndex, extract_pdf_pages


PDF_PATH = ROOT / ".local" / "rag" / "sources" / "2025-Coll-Amunt-Llibre-_compressed.pdf"
PAGES_PATH = ROOT / ".local" / "rag" / "collamunt_pages.json"
MANIFEST_PATH = ROOT / ".local" / "rag" / "collamunt-manifest.json"


def load_pages() -> list[dict[str, object]]:
    if PAGES_PATH.exists():
        return json.loads(PAGES_PATH.read_text(encoding="utf-8"))
    pages = extract_pdf_pages(PDF_PATH)
    PAGES_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAGES_PATH.write_text(
        json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return pages


def main() -> None:
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing official source: {PDF_PATH}")
    ingestion = build_collamunt_chunks(PDF_PATH, load_pages())
    index = LocalChromaIndex(RagLocalSettings())
    ids = index.ingest(ingestion.chunks)
    MANIFEST_PATH.write_text(
        json.dumps(
            {
                "source_file": ingestion.source_file,
                "source_sha256": ingestion.source_sha256,
                "source_type": "pdf",
                "source_id": "collamunt-llibre",
                "source_version": "2025",
                "source_uri": "https://www.collamunt.cat/wp-content/uploads/2017/04/2025-Coll-Amunt-Llibre-_compressed.pdf",
                "consent_ref": "public-official-collamunt-source",
                "page_count": ingestion.page_count,
                "chunk_count": len(ids),
                "business_count": len(ingestion.business_ids),
                "business_ids": list(ingestion.business_ids),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        {
            "pages": ingestion.page_count,
            "chunks": len(ids),
            "businesses": len(ingestion.business_ids),
            "sha256": ingestion.source_sha256,
            "first_ids": ids[:3],
        }
    )


if __name__ == "__main__":
    main()
