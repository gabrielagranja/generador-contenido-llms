"""Canonical creative formats shared by the image API and Content Studio.

The prior prototype already exposed these four visual contracts through
``PostArt.aspectFor``.  This module makes that contract explicit at the API
boundary so generated files retain the final Meta dimensions rather than the
image-provider working canvas.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetaCreativeFormat:
    platform: str
    placement: str
    format: str
    width: int
    height: int

    @property
    def aspect_ratio(self) -> str:
        return f"{self.width}:{self.height}"

    @property
    def provider_size(self) -> str:
        """Closest supported GPT Image canvas; final pixels are normalized locally."""
        ratio = self.width / self.height
        if ratio > 1.2:
            return "1536x1024"
        if ratio < 0.8:
            return "1024x1536"
        return "1024x1024"


# These final dimensions materialize the pre-existing 1:1, 4:5, 9:16 and
# 1.91:1 format contract.  The provider's three canvases are never exposed as
# Meta output dimensions.
META_CREATIVE_FORMATS = (
    MetaCreativeFormat("instagram", "feed", "single_image", 1080, 1080),
    MetaCreativeFormat("instagram", "feed", "carousel", 1080, 1350),
    MetaCreativeFormat("instagram", "reels", "reel", 1080, 1920),
    MetaCreativeFormat("facebook", "feed", "single_image", 1200, 628),
    MetaCreativeFormat("facebook", "feed", "carousel", 1080, 1350),
    MetaCreativeFormat("facebook", "reels", "reel", 1080, 1920),
)


def get_meta_creative_format(platform: str, placement: str, format: str) -> MetaCreativeFormat:
    normalized = (platform.strip().lower(), placement.strip().lower(), format.strip().lower())
    for item in META_CREATIVE_FORMATS:
        if (item.platform, item.placement, item.format) == normalized:
            return item
    supported = ", ".join(
        f"{item.platform}/{item.placement}/{item.format}" for item in META_CREATIVE_FORMATS
    )
    raise ValueError(f"Unsupported Meta creative format. Use one of: {supported}")
