# Visual creatives

## ADDED Requirements

### Requirement: Review-only visual generation

The system SHALL generate a local visual creative through a configured GPT Image model and SHALL keep it pending human review. It MUST NOT publish or export it automatically.

#### Scenario: A generated creative uses the selected Meta contract

- GIVEN a valid selected brand, brief, copy and supported format
- WHEN `POST /creatives` succeeds
- THEN the response includes final width, height, aspect ratio, model, prompt, provenance and `pending-review`
- AND no publication or export occurs.

### Requirement: Isolated provenance

The system SHALL retrieve image context only for the requested `brand_id` and preserve source provenance.

#### Scenario: WAYDDH creative

- GIVEN `brand_id` is `wayddh`
- WHEN the creative is generated
- THEN only WAYDDH RAG evidence is included in the visual prompt and response provenance.

### Requirement: Human review actions

The system SHALL support regeneration, discard and prototype-only approval without automatic publishing.

#### Scenario: Regeneration

- GIVEN a pending creative
- WHEN it is regenerated
- THEN the new creative remains `pending-review` and references its source creative.
