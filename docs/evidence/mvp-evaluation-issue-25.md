# Issue #25 — reproducible MVP evaluation protocol and results

Status: offline representative evaluation. All generation outputs in this
document are deterministic mock outputs; no hosted LLM, Internet request or
real business data was used.

Related evidence: Issue #32 RAG runs in
[`rag-issue-32-representative-runs.md`](rag-issue-32-representative-runs.md).

## Protocol

Each case uses the same sequence:

1. Build a synthetic `GuidedBrief` with a declared claim and channel.
2. Retrieve with `RagGroundedDraftService` using an explicit `business_id` and
   bounded `top_k`.
3. Pass only retrieved contexts to the provider-neutral generator mock.
4. Inspect the draft, evidence references, provenance and unsupported claims.

The result is `PASS` only when the observable condition in the case is met.
This protocol evaluates integration correctness and grounding controls; it
does not claim human preference, market usefulness or hosted-model quality.

## Representative results

| Case | Criterion | Observable result | Status |
|---|---|---|---|
| PDF supported / Instagram | factual accuracy, fidelity, traceability | `business-guide-v1-p0001-c0001` supports the bread/fruit claim; page 1 and file provenance are retained | PASS |
| PDF supported / Facebook | tone/channel boundary | Facebook draft is generated through the existing versioned Facebook template and retains the same PDF evidence reference | PASS |
| API supported | factual accuracy, fidelity, traceability | `jsonplaceholder-post-7-post-v1-0001` supports the included bread/fruit claim; URI and retrieval timestamp are retained | PASS |
| Unsupported price claim | hallucination control | `The box costs five euros.` is classified `unsupported`, added to review metadata and marked `UNSUPPORTED` in the generation prompt | PASS |
| Cross-business retrieval | isolation | querying `synthetic-bakery-b` returns no context from `synthetic-bakery-a`; injecting an A context into a B draft raises `ValueError` | PASS |
| Source-neutral handoff | architecture / C4.3 | PDF and API contexts use the same `RetrievedBusinessContext` and `RagGroundedDraftService` path | PASS |

## Verifiable test executions

- `tests/test_rag_generation.py`: PDF, API, unsupported, isolation and
  Instagram/Facebook end-to-end cases.
- `tests/test_rag_api_connector.py`: mocked HTTP, API normalization, shared
  Chroma retrieval and API grounding.
- `tests/test_local_rag_boundary.py`: PDF extraction, chunking, provenance,
  business scope and grounding.
- `tests/test_channel_adapted_drafting.py`: existing channel template and
  provider-neutral generation boundary.

The focused RAG/API/PDF/generation command is the reproducibility check for
this protocol. Its runtime is reported by the validation run, not presented as
production model latency. On the local validation run it completed in 2.136 s
including interpreter startup and reported 28 passing tests. No real LLM output
is asserted.

## Limitations

- The generator is a deterministic mock, so semantic quality, tone preference
  and human usefulness are integration proxies rather than model evaluation.
- Retrieval uses synthetic fixtures and mocked API responses; no external API
  reliability or authorization flow is evaluated.
- The lexical grounding check is deterministic evidence screening, not formal
  entailment or factuality certification.
- Production latency and time-to-draft are not measured here; only local test
  execution time may be reported.

## Rubric and issue mapping

- Issue #25 acceptance criteria: representative cases, results, limitations and
  hallucination controls are recorded here.
- Issue #32 acceptance criteria: consent-scoped local context, visible source
  traceability, checked factual claims and representative evaluation are backed
  by this document plus the RAG evidence document.
- C4.3 architecture evidence: the shared path is
  `Brief → retrieval → traced context → LangChain-compatible generation →
  grounding/evidence`, verified by the offline tests above.
