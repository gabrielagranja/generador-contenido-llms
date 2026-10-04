# Spec Delta

## Purpose

Provide an invalid contract fixture.

## ADDED Requirements

### Requirement: invalid fixture

The fixture SHALL fail validation.

#### Scenario: fixture is incomplete

GIVEN an incomplete fixture
WHEN the validator runs
THEN validation MUST fail
