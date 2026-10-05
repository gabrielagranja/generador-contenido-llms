# Rubric Requirements and Traceability

Authority: canonical source of truth for assessment requirements, known weights, interpretation decisions and project evidence.

Status: The project owner confirms the official rubric is available. The repository previously treated it as missing; that status was incorrect. This file now records all rubric requirements and facts currently captured in the project. The full criterion wording and any weights not recorded below must be transcribed from the official source before delivery readiness is declared.

## Confirmed rubric facts

- RAG carries 18% of the rubric. The project brief describes RAG as advanced, so the required depth and evidence need clarification.
- Image support and selection/comparison of two LLMs appear as higher-level rubric requirements in the project notes.
- The traceability matrix must cover LLMs, framework, RAG, UI, Git, Kanban, demo, article and presentation (Issue #16).
- Docker may support the medium-level rubric; its exact criterion and weight are not recorded yet (Issue #34).
- No other numeric rubric weights are currently captured in the repository. Do not infer them.

## Requirement-to-evidence mapping

| Rubric area | Requirement captured in the project | Project evidence and issues | Weight/status |
|---|---|---|---|
| LLMs and model strategy | Select and justify model configuration; two-LLM selection/comparison appears as a higher-level requirement. | Stack decision and model candidates in Issue #20; conditional comparison using the same briefs and quality, latency and cost in Issue #33. | Weight not captured; scope clarification sent to instructor. |
| Application framework | Framework selection is an assessed area. | Stack and rationale in Issue #20 and docs/architecture/technology-stack.md. | Weight and exact wording not captured. |
| RAG | RAG is an assessed area; compare contextual retrieval with generation without retrieved context. | 18% weight noted in Issues #11 and #30; consented business context, traceable sources and comparison against no-context prompting in Issue #32. | 18%; required depth/evidence clarification sent to instructor. |
| Image support | Image support appears as a higher-level requirement; choose generation, attributed retrieval or explicit deferral. | One Instagram feed-image generation/preview in Issue #15 and Issue #20; options and constraints in Issue #31. | Weight and minimum scope not captured; clarification sent to instructor. |
| UI | UI is an assessed area. | UX and application foundation work in Issues #8, #17–#21. | Weight and exact wording not captured. |
| Git | Git practices are an assessed area. | Branch/commit conventions, validator and CI evidence in Issue #38 and docs/decisions/2026-10-04-git-conventions.md. | Weight and exact wording not captured. |
| Kanban | Kanban/project-board practice is an assessed area. | GitHub Project #1 is the operational board; roadmap and issue status provide evidence. | Weight and exact wording not captured. |
| Demo | A demonstrable working result is an assessed area. | Delivery readiness in Issue #36; repository demonstration in Issue #29. | Weight and exact wording not captured. |
| Article | A written portfolio article is an assessed area. | Portfolio narrative and Medium article outline in Issue #28. | Weight and exact wording not captured. |
| Presentation | A project presentation is an assessed area. | Ten-minute repository presentation in Issue #29. | Weight and exact wording not captured. |
| Docker | Docker may support a medium-level rubric outcome. | Conditional containerization and reproducible local run path in Issue #34. | Exact criterion and weight not captured. |

## Instructor clarification

The project owner sent a clarification question through Discord on 2026-10-05. It asks what implementation and evidence are sufficient for an individual project, including whether RAG must be compared with a no-retrieval baseline and whether image support and two-model comparison are required or may remain enhancements. Record the instructor's answer here and update the linked issues before freezing scope.

## Source-of-truth rules

- Every design, OpenSpec change, issue and evaluation plan that touches an assessed capability MUST reference this file.
- New or changed rubric requirements and weights MUST be recorded here before they are reflected elsewhere.
- The official rubric MUST NOT be described as unavailable.
- Never infer criterion wording, requirements or weights that are not present in the official source.
- Complete the exact wording and remaining weights from the official rubric before closing Issue #16 or declaring rubric traceability complete.
