# Issue #22 — accessibility verification

Status: verified at the text-contract level for the approved formats. No new
runtime behavior or rendered media was added.

## Verification matrix

| Check | Existing evidence | Result |
|---|---|---|
| Mobile legibility | `openspec/changes/expert-content-generation/design.md` requires a legible hierarchy, short complementary overlay text and mobile-first review for single-image content; carousel and Reel guidance requires readable slide/on-screen text. | Covered as a review heuristic; no rendered-media pixel test exists. |
| Textual clarity | `tests/test_channel_adapted_drafting.py` and `tests/test_channel_adapted_fixtures.py` verify non-empty editable captions and review notes for the representative channel/format fixtures. | Covered. |
| Accessible guidance when applicable | The approved design/specification requires alt-text guidance for important images, reading order and contrast checks for carousels, and readable subtitles for sound-off Reel viewing. | Covered in the content contract. |
| Information not dependent only on visuals | The output boundary is editable text (`caption`, `cta`, assumptions and review notes); the contract explicitly requires alt-text and subtitle guidance rather than relying on an image or audio track alone. | Covered at the text-contract level. |

## Limitations

This evidence does not claim WCAG conformance, visual contrast measurement or
screen-reader testing. Rendered images and video are outside the current
channel-adapted drafting boundary, so visual QA remains a follow-up when those
assets are implemented.

The aggregate OpenSpec verification task remains open because it also covers
audience relevance, brand fit and representative-case evaluation beyond this
accessibility-only check.
