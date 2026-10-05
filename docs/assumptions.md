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
| A-05 | RAG depth, image support and two-LLM comparison meet assessment needs. | Clarification pending | Official rubric facts are recorded in docs/rubric-traceability.md. RAG is weighted at 18%; image support and two-LLM selection appear as higher-level requirements. The clarification question was sent to the instructor via Discord on 2026-10-05; Issues #30–#33. |
| A-06 | Docker is worth including in the delivery slice. | Pending | Feasibility and Issue #34; consult the rubric mapping in docs/rubric-traceability.md. |
| A-07 | A hosted demo needs HTTPS, persistent state/media and WebSocket support. | Pending | Hosting investigation. |
| A-08 | The official assessment rubric exists and is a required project input. | Confirmed; repository mapping underway | The project owner confirmed rubric availability on 2026-10-05. Known requirements and evidence are in docs/rubric-traceability.md; complete exact wording and remaining weights must be transcribed from the official source. |
| A-09 | Initial content formats are single-image feed posts, carousels and Reels; Stories are deferred. Carousel/Reel deliverables are creative plans, not complete generated media. | Approved scope baseline | User approval 2026-10-05; see docs/decisions/2026-10-05-initial-meta-formats.md and Issue #15. |
| A-10 | Project #1 phases, ordering and status are synchronized with the roadmap. | Pending | Reconcile against GitHub Project #1; keep separate from the confirmed rubric. |

Agents MUST NOT convert a Pending item into a decision without approval. Agents MUST update docs/rubric-traceability.md whenever rubric requirements, weights or interpretations change. The official rubric MUST NOT be marked unavailable.
