# Rubric source of truth

## Context and Issue

Issue: #16.

The project owner supplied the complete official workbook, rubrica_autoevaluacion.xlsx, on 2026-10-05. Earlier repository records incorrectly described the rubric as unavailable or only partially known.

## Options considered

1. Keep a partial summary and treat missing requirements as open assumptions.
2. Transcribe the official requirements, weights and evidence links into the canonical rubric traceability document.

## Decision and approval status

Approved by the project owner through the instruction to make the rubric requirements part of the source of truth on 2026-10-05.

The project adopts option 2. docs/rubric-traceability.md is the canonical repository record of all 24 official indicators, their weights and their evidence mapping.

## Consequences and affected documents

- C1 is 12 %, C2 is 16 %, C3 is 18 % and C4 is 54 %.
- C4 requires LLM models, an LLM application framework and a RAG architecture. Each indicator is 18 %.
- Image generation, comparison of two LLMs and Docker are product decisions. They are not rubric requirements.
- The roadmap, scope, assumptions, evaluation plan, active OpenSpec proposals and relevant Issues must use the canonical rubric mapping.

## Revisit trigger

Update the canonical traceability document if the official rubric changes or if the instructor clarifies an interpretation that affects the evidence required for an indicator.
