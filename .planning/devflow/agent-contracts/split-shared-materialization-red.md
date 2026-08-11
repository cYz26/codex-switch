# Agent Task Contract

## Goal
Create tests-only RED coverage for task 7.1 and 7.3 of `independent-app-cli-profiles`: App-originated Plugin add/update/disable/remove, explicit portable/backend-managed artifact policy, independent target cache materialization, no-op fast path, and rollback-safe failure behavior.

## Worker ID
`split-shared-materialization-red`

## Scope
- Allowed write set for worker `split-shared-materialization-red` only:
  - `scripts/test_codex_shared_materialization.py`
- Allowed read-only scope: `codex_switch_plugins.py`, config/store/runtime modules, fake plugin fixtures, and the active OpenSpec.
- Primary-owned shared paths: production code, existing tests, control-plane files, docs, and integration remain main-owned.
- Forbidden: do not modify any path outside the named write set; do not touch live homes, run a live plugin command, use network, switch profiles, restart the App, change dependencies, run Git writes, release, archive, clean up, or perform a destructive effect.

## Constraints
Use isolated homes and fake backend/catalog adapters only. Test add/enable; same-selector source version/tree change; disable/remove retaining cache; `portable_exact`; `backend_managed` compatible divergence receipt; unavailable/unverified catalog; target process running; distinct non-symlink cache roots; plugin-contributed Skill availability; config rollback and backend-not-ready on failure; unchanged generation zero config write/catalog/network/install. Assert public results and receipts, not incidental internal call order except the required materialize-before-config-ready ordering.

## Verification
Run only the new test file. The required terminal result is RED because materialization integration is not implemented. Record exact count/failures/errors and run `git diff --check -- scripts/test_codex_shared_materialization.py`.

## Evidence
The worker must report:

- canonical status `DONE`
- changed files
- tests mapped to OpenSpec scenarios
- commands run
- test logs or validation results and expected RED causes
- unverified areas
- risk notes and review needs

## Human Gate
The worker must wait for human review before expanding scope, touching forbidden files, copying a live cache, using unpinned live network activity, adding a dependency, editing production/existing-test/control-plane files, sharing a mutable cache, cleaning up, running a destructive migration, or touching external state.
