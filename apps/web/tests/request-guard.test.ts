import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequestGuard } from "../domain/request-guard.ts";
import { createDraft, RequestCancelledError } from "../domain/review-api.ts";

const originalFetch = globalThis.fetch;
test.afterEach(() => { globalThis.fetch = originalFetch; });

test("a new request aborts the previous one and only the latest stays current", () => {
  const guard = createRequestGuard();
  const first = guard.begin();
  const second = guard.begin();
  assert.equal(first.signal.aborted, true);
  assert.equal(first.isCurrent(), false);
  assert.equal(second.isCurrent(), true);
});

test("createDraft passes cancellation through distinctly", async () => {
  const guard = createRequestGuard();
  globalThis.fetch = (_input, init) => new Promise((_resolve, reject) => {
    init!.signal!.addEventListener("abort", () => reject(new DOMException("aborted", "AbortError")));
  });
  const handle = guard.begin();
  const pending = createDraft({
    brief: { topic_or_offer: "x", objective: "x", audience_context: "x", business_context_refs: ["s"], platforms: ["instagram"], format: "single_image", brand_and_constraints: undefined, notes: "n", facts: [] },
    ragEnabled: false,
    signal: handle.signal,
  });
  guard.cancel();
  await assert.rejects(pending, (error) => error instanceof RequestCancelledError);
});
