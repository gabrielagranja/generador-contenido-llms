import { test } from "node:test";
import assert from "node:assert/strict";
import type { DraftPreparationStatus as S } from "../domain/types.ts";
import {
  afterBriefChange,
  afterTextChange,
  approve,
  buildSyntheticCopy,
  missingBriefFields,
  requestChanges,
  resubmit,
  statusFromDraft,
} from "../domain/editorial.ts";
import { getBriefDefaults } from "../domain/fixtures.ts";

const all: S[] = ["not-prepared", "draft", "pending-review", "brief-changed", "changes-requested", "approved"];

test("approval is only reachable from pending review", () => {
  for (const status of all) {
    assert.equal(approve(status), status === "pending-review" ? "approved" : status);
  }
});

test("requesting changes only applies to pending review", () => {
  for (const status of all) {
    assert.equal(requestChanges(status), status === "pending-review" ? "changes-requested" : status);
  }
});

test("resubmitting returns to pending review, never to approved", () => {
  assert.equal(resubmit("changes-requested"), "pending-review");
  for (const status of all.filter((s) => s !== "changes-requested")) {
    assert.equal(resubmit(status), status);
  }
});

test("changing the brief invalidates review and approval", () => {
  assert.equal(afterBriefChange("pending-review"), "brief-changed");
  assert.equal(afterBriefChange("approved"), "brief-changed");
  assert.equal(afterBriefChange("draft"), "draft");
  assert.equal(afterBriefChange("not-prepared"), "not-prepared");
});

test("editing copy never approves and invalidates text that was approved", () => {
  assert.equal(afterTextChange("pending-review"), "pending-review");
  assert.equal(afterTextChange("approved"), "brief-changed");
  assert.equal(afterTextChange("draft"), "draft");
});

test("a changed brief cannot be approved without a new review", () => {
  assert.equal(approve("brief-changed"), "brief-changed");
});

test("opening a stored draft never grants approval it did not have", () => {
  assert.equal(statusFromDraft("draft"), "draft");
  assert.equal(statusFromDraft("review"), "pending-review");
  assert.equal(statusFromDraft("approved"), "approved");
});

test("a brief with empty required fields is rejected", () => {
  const brief = getBriefDefaults("collamunt_a");
  assert.equal(missingBriefFields(brief), false);
  assert.equal(missingBriefFields({ ...brief, objective: "  " }), true);
  assert.equal(missingBriefFields({ ...brief, audience: "" }), true);
  assert.equal(missingBriefFields({ ...brief, campaign: "" }), true);
});

test("synthetic copy is labelled as a prototype draft", () => {
  const copy = buildSyntheticCopy("Coll Amunt!", getBriefDefaults("collamunt_a"));
  assert.match(copy, /^Borrador de prototipo · datos sintéticos/);
});
