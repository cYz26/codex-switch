# Agent Task Contract

## Goal
Produce a read-only deep-module architecture review for one canonical App/CLI shared-configuration interface, bidirectional change capture, independent materialization, conflict detection, and verification.

## Worker ID
`split-shared-config-architecture-review`

## Scope
Write set: none. All repository writes are forbidden. Allowed read-only scope: inspect configuration, home-sync, plugin repair, shell shim, App wrapper, transaction, status/Doctor/verify modules and the active OpenSpec change. Forbidden: do not modify files, introduce dependencies, mutate live state, run plugin installers, switch profiles, restart ChatGPT, commit, push, release, archive, or cleanup.

## Constraints
Prefer one deep module and one small interface over caller-specific merge logic. The module must preserve profile-specific and secret state, use atomic/recoverable writes, handle two writers without last-writer data loss, and let each runtime materialize its own cache. No native include/watcher capability may be assumed without evidence.

## Verification
Read-only verification: use concrete `rg -n`, `sed -n`, and `find` commands only. Compare at least three viable approaches against depth, locality, compatibility, direct-use semantics, crash recovery, conflict handling, and testability. Recommend one interface, adapters, transaction ownership, and dependency-ordered test seams. Tests are not run because this worker makes no changes; record that rationale.

## Evidence
Return status, changed files (`none`), inspected files, commands run, test logs or validation results (`not run` with the read-only rationale), comparison, recommendation, rejected alternatives, exact invariants, public test seams, risks, unverified areas, and review needs.

## Human Gate
Main-agent review is required before adopting the architecture. Stop and report for any scope expansion, public API or config-format compatibility break, destructive migration or cleanup of existing homes, new production dependency, live mutation, repository write, failing validation contract, unverified credential/session risk, or product decision not already resolved by the user's single-shared-source requirement.
