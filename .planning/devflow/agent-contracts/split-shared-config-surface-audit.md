# Agent Task Contract

## Goal
Produce a read-only, exhaustive classification of Codex App/CLI configuration and home-state surfaces for the internal-CLI/official-App split, identifying what must be shared, synchronized, independently materialized, or remain profile-local.

## Worker ID
`split-shared-config-surface-audit`

## Scope
Write set: none. All repository writes are forbidden. Allowed read-only scope: inspect `README.md`, `SKILL.md`, `scripts/codex_switch_config.py`, `scripts/codex_switch_home_sync.py`, `scripts/codex_switch_transaction.py`, `scripts/codex_switch_app_wrapper.py`, `scripts/codex_switch_store.py`, relevant tests, and the active `independent-app-cli-profiles` OpenSpec artifacts. Forbidden: do not modify any repository or workstation path; do not install/remove/update plugins or skills; do not switch profiles, restart ChatGPT, invoke launchctl mutation, commit, push, release, archive, or cleanup.

## Constraints
Classify both TOML keys/tables and filesystem entries. Preserve auth, sessions, history, logs, sqlite, credentials, provider/model, runtime/process, and remote-routing isolation unless evidence proves a safe shared-settings subset. Distinguish shared desired configuration from physical plugin cache and runtime-derived state.

## Verification
Read-only verification: use concrete `rg -n`, `sed -n`, and `find` commands only. Map every discovered surface to current owner, proposed owner, synchronization direction, conflict rule, failure behavior, and existing or missing test coverage. Cite file and line evidence. Tests are not run because this worker makes no changes; record that rationale.

## Evidence
Return status, changed files (`none`), inspected files, commands run, test logs or validation results (`not run` with the read-only rationale), a configuration matrix, missing tests, compatibility risks, incidental findings with recommended classification, unverified areas, and review needs.

## Human Gate
Main-agent review is required before adopting any classification. Stop and report for these concrete review triggers: sharing credentials, sessions, model/provider settings, destructive migration, a new dependency, live mutation, or any repository/workstation write outside this read-only contract.
