# Evaluation Plan

Authority: canonical evaluation protocol.
Status: baseline. The official rubric is confirmed and its known requirements are recorded in docs/rubric-traceability.md. Full criterion wording and weights beyond the recorded 18% RAG value still require transcription from the official source; the instructor clarification is pending.

## Rubric alignment

Use docs/rubric-traceability.md as the canonical requirement-to-evidence mapping. Evaluation cases and reports MUST cover the assessed areas that apply to the implemented slice, including model/framework choices, RAG, UI, Git, Kanban, demo, article and presentation.

RAG carries 18% in the rubric. Evaluate retrieval against a no-retrieval baseline using the same briefs and business facts. Record source traceability, factual accuracy, quality, latency and cost. The instructor clarification about minimum implementation/evidence for a solo project was sent via Discord on 2026-10-05.

Image support and two-LLM selection/comparison appear as higher-level rubric requirements. Their scope and evidence expectations are recorded as open in docs/rubric-traceability.md until the instructor reply is logged.

## Cases

Use a small, fixed set of representative, synthetic or approved briefs covering different local-business contexts, audiences and channels. The same briefs must be used when comparing configurations.

## Measures

- time to an editorially useful draft;
- clarification questions and revision rounds;
- factual errors or missing details;
- platform fit for Instagram and Facebook;
- editing effort;
- image usefulness for Instagram feed posts;
- carousel slide progression and creative-plan usefulness;
- Reel script/scene clarity, subtitle usefulness and sound-off comprehensibility;
- voice-mode usefulness, if implemented;
- latency and approximate model/API usage;
- human editorial assessment.

## Test policy

Automated tests MUST mock external providers. Real image, voice and social smoke tests require explicit authorization and approved data.

## Evidence

Store prompts, representative inputs, outputs, scores and limitations without secrets or unapproved business data. Link each evaluation to its Issue, rubric requirement and OpenSpec contract.
