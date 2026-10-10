import test from "node:test";
import assert from "node:assert/strict";
import { applyMoves, distribute, itemsByDate, monthGrid, sampleItems, SAMPLE_START, shiftMonth } from "../domain/calendar-layout.ts";

test("month grid has six Monday-first weeks and marks the month", () => {
  const grid = monthGrid(2026, 10);
  assert.equal(grid.length, 42);
  assert.equal(grid[0].date, "2026-10-26");
  assert.equal(grid.filter((cell) => cell.inMonth).length, 30);
});

test("shiftMonth crosses year boundaries", () => {
  assert.deepEqual(shiftMonth(2026, 11, 1), { year: 2027, month: 0 });
  assert.deepEqual(shiftMonth(2026, 0, -1), { year: 2025, month: 11 });
});

test("12 sample posts land on Monday, Wednesday and Friday of November", () => {
  const placed = distribute(sampleItems, SAMPLE_START);
  assert.equal(placed.length, 12);
  assert.equal(placed[0].date, "2026-11-02");
  assert.equal(placed[11].date, "2026-11-27");
  assert.ok(placed.every((item) => item.date.startsWith("2026-11")));
  assert.equal(new Set(placed.map((item) => item.date)).size, 12);
});

test("moving an item changes only its date", () => {
  const placed = distribute(sampleItems, SAMPLE_START);
  const moved = applyMoves(placed, { "sample-1": "2026-11-10" });
  assert.equal(moved[0].date, "2026-11-10");
  assert.equal(moved[1].date, placed[1].date);
  assert.equal(itemsByDate(moved).get("2026-11-10")?.length, 1);
});

test("sample mix is split in thirds and reports shares", async () => {
  const { summarizeMix } = await import("../domain/calendar-layout.ts");
  const summary = summarizeMix(distribute(sampleItems, SAMPLE_START));
  assert.equal(summary.total, 12);
  assert.deepEqual(summary.rows.map((row) => row.count), [4, 4, 4]);
  assert.deepEqual(summary.rows.map((row) => row.percent), [33, 33, 33]);
  assert.equal(summary.platforms.instagram, 8);
  assert.equal(summary.formats.reel, 4);
});

test("thirds targets match the 12-post split and balance flags gaps", async () => {
  const { thirdsTargets, balance } = await import("../domain/calendar-layout.ts");
  assert.deepEqual(thirdsTargets(12), { EDUCATIONAL: 4, COMMUNITY: 4, PROMOTIONAL: 4 });
  assert.equal(thirdsTargets(10).EDUCATIONAL + thirdsTargets(10).COMMUNITY + thirdsTargets(10).PROMOTIONAL, 10);
  const placed = distribute(sampleItems, SAMPLE_START);
  assert.equal(balance(placed, thirdsTargets(12)).balanced, true);
  const skewed = placed.map((item, index) => (index < 3 ? { ...item, bucket: "PROMOTIONAL" } : item));
  const result = balance(skewed, thirdsTargets(12));
  assert.equal(result.balanced, false);
  assert.match(result.message, /^Para equilibrar: cambia/);
  assert.equal(result.rows.find((row) => row.bucket === "PROMOTIONAL")?.diff, 2);
});
