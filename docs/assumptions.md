# Assumptions and Open Questions

Authority: canonical register of hypotheses and unresolved decisions.
Bootstrap issue: #37.
Assessment source of truth: docs/rubric-traceability.md.

| ID | Assumption or question | Status | Owner/evidence |
|---|---|---|---|
| A-01 | The primary user is a content manager/copywriter serving small local businesses. | Working assumption | Validate through discovery Issues #1–#5. |
| A-02 | Instagram is the priority channel and Facebook is the second generation/adaptation channel. | Approved scope baseline | Review with representative cases. |
| A-03 | Direct publication is limited to one authorized Instagram Professional account. | Approved scope baseline | Confirm API permissions and test account. |
| A-04 | Every Instagram publication requires explicit human confirmation. | Approved operating rule | Cover in implementation contract and tests. |
| A-05 | C4 requires a working LLM model, an LLM application framework and a RAG architecture. | Required by rubric | Each indicator is worth 18 %. Source and evidence map: docs/rubric-traceability.md; Issues #20, #21, #23, #25 and #32. |
| A-06 | Image support and comparison between two LLM configurations are useful product choices. | Product decision | They are not rubric requirements. Decide scope, budget and evaluation value in Issues #31 and #33. |
| A-07 | Docker is worth including in the delivery slice. | Product decision | It is not a rubric requirement. Assess reproducibility and feasibility in Issue #34. |
| A-08 | A hosted demo needs HTTPS, persistent state/media and WebSocket support. | Pending | Hosting investigation. |
| A-09 | The official assessment rubric is fully transcribed in the repository source of truth. | Confirmed | docs/rubric-traceability.md, based on rubrica_autoevaluacion.xlsx received on 2026-10-05. |
| A-10 | Initial content formats are single-image feed posts, carousels and Reels; Stories are deferred. Carousel/Reel deliverables are creative plans, not complete generated media. | Approved scope baseline | User approval 2026-10-05; see docs/decisions/2026-10-05-initial-meta-formats.md and Issue #15. |
| A-11 | Project #1 phases, ordering and status are synchronized with the roadmap. | Pending | Reconcile against GitHub Project #1. |

Agents MUST NOT convert a Pending item into a decision without approval. Agents MUST update docs/rubric-traceability.md whenever rubric requirements, weights or interpretations change.
