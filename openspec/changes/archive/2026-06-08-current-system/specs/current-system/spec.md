# Specification Delta: Current System Baseline

## ADDED Requirements

### Requirement: Current System Baseline

The system SHALL support the behavior described by this change after the plan is approved.

#### Scenario: Planned behavior

- GIVEN the active change `current-system`
- WHEN implementation is completed
- THEN the verified behavior matches this requirement and evidence is recorded.

#### Scenario: Completion contract

- GIVEN the active change `current-system`
- WHEN Codex claims the work is complete
- THEN Target State, Acceptance Criteria, and Validation Commands have recorded evidence
- AND no required Capability Slice remains todo without a blocker.
