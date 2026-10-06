# Proposal

## Status and human approval

- Status: Pending
- Issue: #32 — [STORY] Implement scoped business-context RAG
- Parent epic: #11
- Rubric: C4.3, “Uso de arquitecturas RAG”, obligatorio y valorado en 18 %
- Human approval: Pending

## Plan objective

Define the smallest local RAG slice that retrieves consented business context with traceable sources so generated copy can ground factual claims.

## Objective

Provide a reproducible, provider-independent business-context retrieval boundary using a local Chroma store and local multilingual embeddings. The initial design must make retrieved evidence inspectable without expanding into publication, analytics or interface work.

## Scope

### Included

- A small local Chroma collection scoped to an explicitly identified business.
- Ingestion of short synthetic or explicitly consented text records only.
- A pinned/configured multilingual embedding model running locally, with no embedding-provider API calls.
- Source and chunk metadata sufficient to trace every retrieved passage to its consented source record and version.
- Similarity retrieval returning passages, identifiers, metadata and scores for grounding.
- A retrieval boundary that can be injected into the existing text-generation flow without changing the `GuidedBrief` contract.
- Synthetic examples and focused verification of source traceability, business scoping and claim support.

### Excluded

- Real business data until explicit consent and handling rules are recorded.
- Automatic web crawling, external knowledge ingestion or unverified sources.
- Publication, scheduling, analytics, learning loops or interface changes.
- Provider-hosted embeddings, provider calls required for retrieval, multi-tenant administration and broad enterprise search.
- Claims that retrieval alone proves factual correctness or improves engagement.

## Acceptance criteria

- A synthetic consented record can be indexed locally in Chroma with business, source, version, consent and chunk metadata.
- A query returns only records from the requested business scope and includes traceable source identifiers.
- The embedding path is multilingual and local, versioned/configurable, and does not call an external embedding provider.
- A generated factual claim can be checked against the retrieved approved passage; unsupported claims are flagged or omitted by the grounding boundary.
- Retrieval output is deterministic enough to reproduce with the same local index, embedding configuration and query.
- Examples use synthetic businesses and no credentials or personal data.
- The design preserves C4.3 as a required rubric criterion while leaving evaluation evidence to Issue #25 and final verification to Issue #36.

## Rubric

This contract directly targets C4.3, the mandatory RAG-architecture indicator. It does not claim the rubric evidence is complete until implementation, evaluation and traceable run evidence are recorded.

## Tests and verification

- Run OpenSpec active-change and SDD required-field validation.
- Use a local, deterministic test index with synthetic records and mocked or local-only embeddings.
- Verify business scoping, source traceability, repeatable retrieval and supported/unsupported claim handling.
- Record representative evaluation evidence in Issue #25 after implementation.

## Open questions and blockers

- The instructor response requesting clarification on expected RAG evidence remains pending. It may refine the evaluation depth or evidence format, but it does not block this initial design and does not make C4.3 optional.
- Confirm the exact local multilingual embedding model and resource limits during implementation without changing the contract boundary.
- Confirm retention and deletion handling before any real business data is introduced.

## Approval

Pending explicit human approval. No application implementation may begin until approval is recorded.
