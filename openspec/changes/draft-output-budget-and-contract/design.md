# Design

## Approach

Add a validated output-token setting to the existing LLM configuration model. Keep the current provider selection, model, temperature, timeout, and provider-neutral `TextGenerator` boundary unchanged except for passing the budget into the concrete Groq model configuration.

The mock adapter will continue to return deterministic output and will not emulate a hosted provider. Tests will use mock or fake adapters and inspect construction arguments rather than calling Groq.

The existing channel template boundary will gain concise, channel-specific contract language. The contract will reinforce grounded factual claims, source attribution, Spanish as the default language, configured Catalan support, and the prohibition on invented prices, opening hours, promotions, or dates. It will not alter retrieval, claim classification, review metadata, approval, or editorial planning.

## Configuration and validation

- Proposed default: 350 output tokens.
- Proposed absolute maximum: 600 output tokens.
- Positive integer validation is required.
- Values above 600 must fail during configuration loading.
- The proposed values remain subject to human approval and representative evaluation.

## Provider boundary

The Groq adapter will receive the validated budget through the model constructor’s provider-level maximum-output-token option. Generated text will not be truncated after the provider returns it.

The mock path remains provider-free and deterministic. The adapter contract should be tested without credentials and without network access.

## Verification boundaries

Focused tests will cover configuration defaults and invalid values, Groq-construction arguments using a fake or patched constructor, deterministic mock behavior, channel-specific prompt contracts, and preservation of grounding/review metadata. The full Python, SDD, diff, and web verification commands remain required.

## Risks and trade-offs

- A 350-token default may shorten some Facebook drafts more than desired.
- Provider SDK/LangChain option names may vary and must be verified against the installed dependency without making a live call.
- A provider limit bounds output generation but does not reduce prompt/input tokens.
- Concise prompt instructions may improve cost but could reduce stylistic richness if over-constrained.

## Open questions

- Validate 350 and 600 against representative Instagram and Facebook briefs.
- Confirm whether the configured Groq model honors the option consistently.
- Decide whether a later approved change should tune the budgets based on observed editability and factual quality.

## Approval gate

This design is proposed only. Implementation must not begin while the proposal remains `Status: Pending` and `Human approval: Pending`.
