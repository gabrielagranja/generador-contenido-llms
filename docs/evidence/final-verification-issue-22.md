# Issue #22 — final verification evidence

Status: representative offline verification completed for audience relevance,
brand fit and editable output. The evidence uses the approved synthetic
fixtures and mocked generation boundary; it makes no claim about engagement or
hosted-model quality.

## Representative cases

| Case | Audience relevance | Brand fit | Editability |
|---|---|---|---|
| F-01 complete brief | The confirmed local-resident situation and repair decision context are passed into the drafting prompt. | The clear, calm and practical constraints are passed into the prompt and unsupported claims remain prohibited. | Caption, evidence references, assumptions and review notes are returned as separate editable fields. |
| F-02 audience unknown | Unknown audience material remains an assumption; the fixture requires focused questions before audience-specific claims. | Warm/informative constraints and exclusions are retained in the fixture contract without demographic or dietary invention. | The bounded draft path returns editable text while keeping unresolved assumptions visible. |
| F-03 ambiguous offer/objective | Ambiguous audience and objective stay unresolved until clarified; the fixture requires a bounded plan rather than a fabricated audience. | Welcoming/accessibility constraints and prohibited claims remain visible while Instagram and Facebook use separate templates. | Both channel drafts are separate editable text objects with channel-specific metadata and review notes. |

## Executable evidence

- `tests/test_channel_adapted_fixtures.py` runs F-01, F-02 and F-03 and checks
  audience-state assumptions, versioned channel templates, non-empty captions
  and review metadata.
- `tests/test_channel_adapted_drafting.py` checks that audience context and
  brand constraints reach the prompt, that Instagram/Facebook prompts differ,
  and that the returned draft can be revised without losing evidence metadata.
- `docs/evidence/mvp-evaluation-issue-25.md` records the complementary factual
  grounding and RAG evidence for the same drafting boundary.

## Limitations

These are deterministic provider-mock checks, not a human preference study or
semantic audience-relevance score. They verify that supplied audience and brand
context is preserved, that unknowns remain visible, and that the output is
reviewable/editable; they do not prove market performance.
