import { test } from "node:test";
import assert from "node:assert/strict";
import { brandContexts, briefDefaults, dashboardFixtures, draftFixtures, historyFixtures } from "../domain/fixtures.ts";

const mountain = /monta|ruta|senderis|excursi|outdoor|naturaleza/i;

test("Coll Amunt! is a Barcelona local business association, not an outdoors brand", () => {
  const coll = brandContexts.find((brand) => brand.id === "coll-amunt");
  assert.ok(coll);
  assert.match(coll.kind, /Barcelona/);
  assert.ok((coll.commerceOptions?.length ?? 0) >= 2);

  const texts = [
    coll.summary,
    ...(coll.commerceOptions ?? []).flatMap((c) => [c.summary, c.sector]),
    ...["collamunt_a", "collamunt_b"].flatMap((a) => [
      briefDefaults[a].objective,
      briefDefaults[a].audience,
      briefDefaults[a].campaign,
      ...(draftFixtures[a] ?? []).flatMap((d) => [d.title, d.copy]),
      ...dashboardFixtures[a].upcoming.map((i) => i.title),
    ]),
  ];
  for (const text of texts) assert.doesNotMatch(text, mountain, text);
});

test("every selectable context has its own brief, dashboard and drafts", () => {
  const accounts = brandContexts.flatMap((brand) =>
    brand.commerceOptions ? brand.commerceOptions.map((c) => c.account) : [brand.account],
  );
  assert.equal(new Set(accounts).size, accounts.length);
  for (const account of accounts) {
    assert.ok(briefDefaults[account], account);
    assert.ok(dashboardFixtures[account], account);
    assert.ok(draftFixtures[account], account);
  }
});

test("drafts never reference another context", () => {
  for (const [account, drafts] of Object.entries(draftFixtures)) {
    for (const draft of drafts) {
      if (account === "collamunt_a") assert.doesNotMatch(draft.copy, /Comercio sintético B|La Plaza/);
      if (account === "collamunt_b") assert.doesNotMatch(draft.copy, /Comercio sintético A|La Plaza/);
      if (account === "panaderialaplaza") assert.doesNotMatch(draft.copy, /Coll Amunt/);
    }
  }
});

test("associated businesses are explicitly synthetic", () => {
  const coll = brandContexts.find((brand) => brand.id === "coll-amunt");
  for (const commerce of coll?.commerceOptions ?? []) assert.match(commerce.name, /sintético/i);
});

test("history entries link to a draft in the same synthetic context", () => {
  for (const [account, entries] of Object.entries(historyFixtures)) {
    const draftIds = new Set((draftFixtures[account] ?? []).map((draft) => draft.id));
    for (const entry of entries) assert.ok(draftIds.has(entry.draftId), `${account}: missing ${entry.draftId}`);
  }
});
