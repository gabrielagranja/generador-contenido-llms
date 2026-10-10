import { test } from "node:test";
import assert from "node:assert/strict";
import { canStartGeneration, generationStateLabels, parseDraftResponse } from "../domain/draft-generation.ts";

function response(body: unknown, status = 200): Pick<Response, "ok" | "status" | "json"> {
  return { ok: status >= 200 && status < 300, status, json: async () => body };
}

test("a valid API response returns editable copy pending human review", async () => {
  const result = await parseDraftResponse(response({ review_state: "pending_human_review", drafts: [{ caption: " Texto real de la API " }] }));
  assert.deepEqual(result, { copy: "Texto real de la API", reviewState: "pending_human_review" });
});

test("loading state prevents duplicate generations", () => {
  assert.equal(canStartGeneration("idle"), true);
  assert.equal(canStartGeneration("loading"), false);
  assert.equal(generationStateLabels.loading, "Generando…");
});

test("API errors remain visible to the caller", async () => {
  await assert.rejects(parseDraftResponse(response({ detail: "Servicio no disponible" }, 503)), /Servicio no disponible/);
});

test("an empty response is rejected", async () => {
  await assert.rejects(parseDraftResponse(response({ review_state: "pending_human_review", drafts: [] })), /borrador editable/);
});

test("an invalid editorial state is rejected and cannot auto-approve", async () => {
  await assert.rejects(parseDraftResponse(response({ review_state: "approved", drafts: [{ caption: "Texto" }] })), /pendiente de revisión humana/);
});

test("malformed HTTP responses are rejected", async () => {
  await assert.rejects(parseDraftResponse({ ok: true, status: 200, json: async () => { throw new Error("invalid json"); } }), /respuesta no válida/);
});
