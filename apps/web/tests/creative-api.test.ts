import { test } from "node:test";
import assert from "node:assert/strict";
import { approveCreative, createCreative, discardCreative, regenerateCreative } from "../domain/creative-api.ts";
import { ReviewApiError } from "../domain/review-api.ts";

const originalFetch = globalThis.fetch;
const creative = {
  id: "creative-1", image_url: "/creatives/creative-1/image", prompt: "safe visual prompt",
  brand_id: "talent-hive", platform: "instagram", placement: "feed", format: "carousel",
  width: 1080, height: 1350, aspect_ratio: "1080:1350", model: "gpt-image-2.5-flare",
  generated_at: "2026-10-13T00:00:00Z", review_state: "pending-review", provenance: [],
};

test.afterEach(() => { globalThis.fetch = originalFetch; });

test("creative creation sends the selected Meta format and remains pending review", async () => {
  let request: Request | undefined;
  globalThis.fetch = async (input, init) => { request = new Request(input, init); return Response.json(creative); };
  const result = await createCreative({ brand_id: "talent-hive", brief: "Equipo", platform: "instagram", placement: "feed", format: "carousel", copy: "Copy", style: "editorial" });
  assert.equal(request!.url, "http://127.0.0.1:8000/creatives");
  assert.deepEqual(await request!.json(), { brand_id: "talent-hive", brief: "Equipo", platform: "instagram", placement: "feed", format: "carousel", copy: "Copy", style: "editorial" });
  assert.equal(result.review_state, "pending-review");
});

test("regenerate and review actions use the selected creative endpoint", async () => {
  const requests: Request[] = [];
  globalThis.fetch = async (input, init) => {
    const request = new Request(input, init); requests.push(request);
    return Response.json({ ...creative, review_state: request.url.endsWith("/discard") ? "discarded" : request.url.endsWith("/approve") ? "approved-prototype" : "pending-review" });
  };
  await regenerateCreative("creative-1", { brand_id: "talent-hive", brief: "Equipo", platform: "instagram", placement: "feed", format: "carousel", copy: "Copy", style: "editorial" });
  assert.equal(requests[0].url, "http://127.0.0.1:8000/creatives/creative-1/regenerate");
  assert.equal((await discardCreative("creative-1")).review_state, "discarded");
  assert.equal((await approveCreative("creative-1")).review_state, "approved-prototype");
});

test("OpenAI API errors remain specific instead of a generic connection message", async () => {
  globalThis.fetch = async () => Response.json({ detail: "OpenAI image generation timed out or is unavailable" }, { status: 502 });
  await assert.rejects(createCreative({ brand_id: "wayddh", brief: "PDF", platform: "instagram", placement: "feed", format: "carousel", copy: "Copy", style: "editorial" }), (error: unknown) => error instanceof ReviewApiError && /OpenAI image generation timed out/.test(error.message));
});
