# Issue #32 — representative offline RAG generation runs

Status: reproducible local evidence. The generation output in these records is
from a deterministic mock generator; it is not evidence from a hosted model.

## Run RAG-E2E-PDF-001

- Test: `RagGenerationEndToEndTests.test_pdf_brief_retrieval_generation_and_evidence`
- Brief/query: `weekday breakfast box explain the offer accurately local residents`
- `business_id`: `synthetic-bakery-a`
- Source: `pdf`, `business-guide`, version `v1`
- Retrieved chunk: `business-guide-v1-p0001-c0001`
- Provenance: `synthetic-business-context.pdf`, page `1`
- Mock output: `Weekday breakfast box includes bread and fruit.`
- Grounding: supported; evidence provenance includes business, source, chunk and page.

## Run RAG-E2E-API-001

- Test: `RagGenerationEndToEndTests.test_api_brief_retrieval_generation_and_evidence`
- Brief/query: `weekday breakfast box explain the offer accurately local residents`
- `business_id`: `business-a`
- Source: `api`, `jsonplaceholder-post-7`, version `post-v1`
- Retrieved chunk: `jsonplaceholder-post-7-post-v1-0001`
- Provenance: `https://api.example.test/posts/7`, retrieved at `2026-10-06T10:00:00+00:00`
- Mock output: `Bread and fruit are included.`
- Grounding: supported; evidence provenance includes business, source, chunk and URI.

## Run RAG-E2E-UNSUPPORTED-001

- Test: `RagGenerationEndToEndTests.test_business_isolation_and_unsupported_claim_are_explicit`
- Brief/query: `weekday breakfast box explain the offer accurately local residents`
- `business_id`: `synthetic-bakery-a`
- Claim: `The box costs five euros.`
- Retrieved sources: synthetic PDF chunks with no price statement.
- Mock output: `No unsupported price claim included.`
- Grounding: unsupported; the claim is listed in `unsupported_claims` and marked
  `UNSUPPORTED` in the generation prompt.
- Isolation check: requesting `synthetic-bakery-b` returns no evidence from
  `synthetic-bakery-a`; injecting an A context into a B draft raises
  `ValueError`.

These records are backed by offline tests and contain no real business data,
credentials, network response or hosted-model result. They are intended to be
linked from Issue #25/#32 during evaluation review.
