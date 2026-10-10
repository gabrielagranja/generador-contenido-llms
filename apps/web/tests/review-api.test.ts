import { test } from "node:test";
import assert from "node:assert/strict";
import { createDraft, reviewDraft, updateDraft, ReviewApiError } from "../domain/review-api.ts";

const originalFetch = globalThis.fetch;

test.afterEach(() => { globalThis.fetch = originalFetch; });

test("createDraft sends brand, business and RAG parameters to the API", async () => {
  let request: Request | undefined;
  globalThis.fetch = async (input, init) => {
    request = new Request(input, init);
    return Response.json({ review_state: "pending_human_review", drafts: [], content_ids: [] });
  };
  await createDraft({ brief: { topic_or_offer: "Oferta", objective: "Objetivo", audience_context: "Barrio", business_context_refs: ["store"], platforms: ["instagram"], format: "single_image", brand_and_constraints: undefined, notes: "Generated from Content Studio.", facts: [] }, brandId: "coll-amunt", businessId: "business-a", ragEnabled: true });
  const body = await request!.json() as Record<string, unknown>;
  assert.equal(request!.url, "http://127.0.0.1:8000/drafts");
  assert.deepEqual(body, { brief: { topic_or_offer: "Oferta", objective: "Objetivo", audience_context: "Barrio", business_context_refs: ["store"], platforms: ["instagram"], format: "single_image", notes: "Generated from Content Studio.", facts: [] }, rag_enabled: true, brand_id: "coll-amunt", business_id: "business-a", top_k: 3 });
});

test("review and edit use the backend content id and preserve explicit decisions", async () => {
  const calls: Request[] = [];
  globalThis.fetch = async (input, init) => { calls.push(new Request(input, init)); return Response.json({ content_id: "content-1", state: "pending_human_review", draft: { caption: "Editado", evidence_provenance: [], supported_claims: [], unsupported_claims: [] } }); };
  await updateDraft("content-1", "Editado");
  await reviewDraft("content-1", "request_regeneration", "reviewer-1", "Aclarar el beneficio");
  assert.equal(calls[0].method, "PATCH");
  assert.equal(calls[0].url, "http://127.0.0.1:8000/drafts/content-1");
  assert.deepEqual(await calls[1].json(), { decision: "request_regeneration", reviewer_ref: "reviewer-1", feedback: "Aclarar el beneficio" });
});

test("HTTP transition errors are actionable and retain their status", async () => {
  globalThis.fetch = async () => Response.json({ detail: "cannot approve" }, { status: 409 });
  await assert.rejects(reviewDraft("content-1", "approve", "reviewer-1"), (error: unknown) => error instanceof ReviewApiError && error.status === 409 && /Transición editorial inválida/.test(error.message));
});
