# Synthetic brief fixtures

These fixtures are fixed, synthetic test inputs for Issue #22. They contain no real business data, credentials, customer data or approved external sources. They are intended to compare the generic baseline and guided workflow defined in the design, not to validate engagement or publication.

## Coverage matrix

| Fixture | Task 9 situation | Channel(s) | Format | Primary purpose |
| --- | --- | --- | --- | --- |
| `F-01` | Complete brief with known audience | Instagram | `single_image` | Check direct drafting, fact grounding and editable image guidance. |
| `F-02` | Audience unknown | Facebook | `carousel` | Check focused audience discovery, inferred status and slide-plan adaptation. |
| `F-03` | Offer and objective ambiguous | Instagram + Facebook | `reel` | Check objective clarification, cross-channel adaptation and Reel plan output. |

Together the fixtures cover both approved generation channels and all approved formats. They do not test Stories, direct Facebook publishing, rendered carousel media or rendered video.

## F-01 — Complete audience and offer

### Synthetic brief

- **Business:** `Negocio Sintético A`, a fictional neighbourhood repair service.
- **Topic/offer:** free 15-minute diagnosis for a household appliance that is not working.
- **Objective:** prompt local people who already have the problem to request a diagnosis.
- **Audience:** local residents who own the appliance, are deciding whether to repair it and are looking for a trustworthy first step.
- **Need/objection:** uncertainty about whether repair is worthwhile and concern about unexpected cost.
- **Platform:** Instagram.
- **Format:** single-image feed post.
- **Brand/constraints:** clear, calm and practical; do not claim savings, expertise, availability or results that are not listed here.
- **Approved synthetic facts:** the diagnosis lasts 15 minutes and is free; the fixture provides no location, opening hours, prices, testimonials or performance statistics.

### Expected guided behavior

- Treat topic, objective, audience situation and offer details as `CONFIRMED` from this fixture.
- Do not ask for audience discovery unless a material contradiction appears.
- Do not invent location, urgency, credentials, repair success rate or price claims.
- Return one editable caption, complementary overlay suggestion, visual direction, CTA and review assumptions.

## F-02 — Audience unknown

### Synthetic brief

- **Business:** `Negocio Sintético B`, a fictional local food shop.
- **Topic/offer:** a new seasonal soup is available.
- **Objective:** `UNKNOWN`; the user only says “make people notice it”.
- **Audience:** `UNKNOWN`; no purchaser, user, decision-maker or referrer is supplied.
- **Need/objection:** `UNKNOWN`.
- **Platform:** Facebook.
- **Format:** carousel.
- **Brand/constraints:** warm and informative; do not infer dietary preferences, health benefits or customer demographics.
- **Approved synthetic facts:** the soup is seasonal and available in the fictional shop; ingredients, price, schedule, location, dietary properties and customer examples are not supplied.

### Expected guided behavior

- Ask focused questions about the desired outcome, real customer situation, need/objection and any supported ingredients or offer details that would affect the message.
- Keep audience conclusions `UNKNOWN` until evidence is supplied; a provisional audience hypothesis is `INFERRED` only when its evidence and reason are recorded.
- Do not claim health, freshness, popularity, affordability or dietary suitability.
- After sufficient answers, return a Facebook carousel plan with cover hook, slide progression and closing CTA; otherwise return the questions and an editable bounded draft only if the user accepts the assumptions.

## F-03 — Ambiguous offer and objective

### Synthetic brief

- **Business:** `Negocio Sintético C`, a fictional neighbourhood learning studio.
- **Topic/offer:** “new autumn activities”; the user does not specify whether this means an event, a class or an information session.
- **Objective:** `UNKNOWN`; the user asks to “get more interest”.
- **Audience:** families, adults or local organisations are all possible; no role or situation is confirmed.
- **Need/objection:** `UNKNOWN`.
- **Platforms:** Instagram and Facebook.
- **Format:** Reel.
- **Brand/constraints:** welcoming and accessible; do not invent dates, teachers, credentials, prices, outcomes, places or registration deadlines.
- **Approved synthetic facts:** only the phrase “new autumn activities” is supplied; all other offer and audience details are unknown.

### Expected guided behavior

- Ask whether the objective is awareness, enquiries, registration or another outcome, and clarify the activity, audience role and next action before making a specific promise.
- Mark the topic/offer, objective, audience and CTA as `UNKNOWN` until clarified; do not convert “more interest” into a confirmed goal.
- Once clarified, preserve the core message while adapting the presentation for Instagram and Facebook.
- Return a Reel scene/script and subtitle plan, with any unresolved assumptions visible. Do not render or publish video.

## Comparison protocol

For each fixture, run the generic baseline and guided condition with the same input facts, platform and format. Record the observable signals defined in the design: unsupported claims, audience relevance, question/revision count, time to a usable editable draft, platform/format fit, accessibility/readiness and reviewer preference. A fixture result is not a performance claim and must not be used as evidence of engagement or market uniqueness.
