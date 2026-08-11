## Purpose

Defines the canonical DevFlow workflow-provider ownership and the recoverable
brownfield migration contract that removes retired providers from active
project discovery without losing project history or unrelated work.

## ADDED Requirements

### Requirement: Canonical workflow providers
The project SHALL use OpenSpec for canonical behavior artifacts, DevFlow for
workflow routing and execution evidence, and only triggered members of the
six-item DevFlow-pinned Matt allowlist for bounded engineering capabilities.
An untriggered Matt capability MUST NOT be installed merely to satisfy an
inventory count. Project-local GSD and Superpowers skills, hooks, agents, and
runtime configuration MUST NOT remain in active discovery or runtime paths
after migration.

#### Scenario: Fresh task discovers the canonical provider set
- **WHEN** a new Codex task starts after the completed refresh
- **THEN** project-local discovery exposes the current DevFlow skills, exactly six OpenSpec 1.7 skills, and only the approved Matt primitives whose capabilities were triggered
- **THEN** the current five-item Matt set remains valid and `domain-modeling` remains absent because `domain-language-modeling` was skipped
- **THEN** no project-local GSD or Superpowers workflow provider is active

### Requirement: Durable project guidance
The tracked `AGENTS.md` SHALL contain the current DevFlow ownership, routing,
execution, generated-artifact, verification, and legacy-configuration rules.
The migration MUST preserve the codex-switch-specific internal binary upgrade
compatibility contract and MUST configure workflow mode as `full-openspec`.

#### Scenario: Generated guidance is reconciled
- **WHEN** the latest DevFlow template differs from the active project guidance
- **THEN** durable template rules are merged into tracked `AGENTS.md`
- **THEN** project-specific internal binary guidance remains present
- **THEN** no `AGENTS.md.generated` file remains as a competing source of truth

### Requirement: Recoverable legacy-provider migration
Before moving any legacy-provider artifact, the project MUST record an exact
source-to-quarantine contract and prove ownership. Migration SHALL move only
the approved, ownership-verified paths into an isolated recoverable quarantine
and SHALL retain a rollback mapping and terminal receipt. Physical quarantine
purge MUST remain a separate Human Gate.

#### Scenario: Approved legacy artifacts are deactivated
- **WHEN** the provider migration executes against the preflight-attested paths
- **THEN** the approved legacy DevFlow duplicates, GSD provider surfaces, and Superpowers links are absent from active discovery and runtime paths
- **THEN** each moved source has an exact recoverable quarantine destination
- **THEN** no ambiguous or user-authored artifact is moved

#### Scenario: Ownership changes during migration
- **WHEN** a source path is missing, changes type, changes expected content, or gains an unapproved child before its move
- **THEN** migration stops before moving that path or any dependent provider surface
- **THEN** the existing project state remains recoverable and the mismatch is reported

### Requirement: Historical and unrelated state preservation
The migration MUST preserve `.planning` history, the GSD migration journal,
the active parity implementation and artifacts, profile and credential data,
running application state, dependencies, and Git history.

#### Scenario: Provider refresh is isolated from parity work
- **WHEN** the provider migration completes
- **THEN** pre-existing parity worktree paths have identical content to their pre-migration snapshot
- **THEN** the `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT` gate remains unchanged
- **THEN** no profile switch, application restart, dependency change, commit, push, release, or archive occurs

### Requirement: Completion evidence
The refresh SHALL be complete only when fresh diagnostics report a current
official skill layout with zero `legacy_duplicate` and zero
`manual_review_required` items, workflow validation and cache-drift Doctor are
healthy, the new and active OpenSpec changes pass strict validation, and the
scoped Git audit contains only approved refresh files plus preserved unrelated
work.

#### Scenario: Migration reaches a verified terminal state
- **WHEN** all approved migration tasks and final checks finish successfully
- **THEN** the migration receipt records exact commands, results, changed paths, retained paths, rollback instructions, and restart/new-task guidance
- **THEN** no required cleanup or provider-ownership conflict remains active
