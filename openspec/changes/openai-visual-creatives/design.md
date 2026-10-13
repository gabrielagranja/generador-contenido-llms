# Design

The image boundary uses a small `httpx` OpenAI Images adapter with a GPT Image model selected through `OPENAI_IMAGE_MODEL`. Its authorization header is never serialized, stored or returned.

The existing Content Studio format selector remains the source of platform and format. The backend resolves it to the canonical placement/dimensions, asks the provider for its nearest supported working canvas and uses a deterministic centre crop plus high-quality resize to final output pixels. Local PNGs live under ignored `.local/creatives` and are served only by an authenticated API route.

Each request queries Chroma with both `business_id` and `brand_id` equal to the selected brand. Retrieved source fields are retained as provenance; text is included only as supporting context, while the prompt instructs the image model not to invent ungrounded factual or visual claims.
