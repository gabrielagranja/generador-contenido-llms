"""Ingest independent Talent Hive and WAYDDH demo sources into local Chroma."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from apps.api.config import RagLocalSettings  # noqa: E402
from apps.api.demo_brands import WAYDDH_PDF_PATH, load_demo_brand_chunks  # noqa: E402
from apps.api.rag import LocalChromaIndex  # noqa: E402


def main() -> None:
    if not WAYDDH_PDF_PATH.exists():
        raise SystemExit(
            f"Falta la fuente corporativa local de WAYDDH: {WAYDDH_PDF_PATH}. "
            "Coloca el PDF existente en .local/rag/sources/ antes de indexar."
        )
    chunks = load_demo_brand_chunks(WAYDDH_PDF_PATH)
    index = LocalChromaIndex(RagLocalSettings())
    ids = index.ingest(chunks)
    manifest_path = ROOT / ".local" / "rag" / "demo-brands-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "brands": sorted({chunk.brand_id for chunk in chunks}),
                "chunk_count": len(ids),
                "source_names": sorted({chunk.source_name for chunk in chunks}),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print({"brands": sorted({chunk.brand_id for chunk in chunks}), "chunks": len(ids)})


if __name__ == "__main__":
    main()
