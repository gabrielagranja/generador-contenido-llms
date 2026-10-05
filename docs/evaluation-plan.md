# Evaluation Plan

Authority: canonical evaluation protocol.
Status: baseline. The official rubric and evidence map are fully transcribed in docs/rubric-traceability.md.

## Rubric alignment

The plan must collect evidence for all four competencies. C4 has the largest weight: 54 % in total, split equally across use of LLM models, an LLM application framework and a RAG architecture.

For C4, record:

- a working content-generation flow that invokes an LLM model;
- visible, reproducible use of the chosen LLM application framework;
- a RAG flow over approved business context, including retrieved-source traceability and factual-grounding checks.

The rubric does not require image generation, two-model comparison or Docker. Evaluate those only when they remain in the product scope. A comparison between RAG and no-retrieval prompting can provide useful evidence of quality, but it is an evaluation choice pending the instructor's guidance rather than a rubric condition.

## Cases

Use a small, fixed set of representative, synthetic or approved briefs covering different local-business contexts, audiences and channels. The same briefs must be used when comparing configurations.

## Measures

- time to an editorially useful draft;
- clarification questions and revision rounds;
- factual errors or missing details;
- retrieved-context traceability and factual grounding for RAG;
- platform fit for Instagram and Facebook;
- editing effort;
- image usefulness for Instagram feed posts when image generation is in scope;
- carousel slide progression and creative-plan usefulness;
- Reel script/scene clarity, subtitle usefulness and sound-off comprehensibility;
- voice-mode usefulness when implemented;
- latency and approximate model/API usage;
- human editorial assessment.

## Test policy

Automated tests MUST mock external providers. Real image, voice and social smoke tests require explicit authorization and approved data.

## Evidence

Store prompts, representative inputs, outputs, scores and limitations without secrets or unapproved business data. Link each evaluation to its Issue, rubric criterion and OpenSpec contract. Use docs/rubric-traceability.md for the final evidence checklist.
