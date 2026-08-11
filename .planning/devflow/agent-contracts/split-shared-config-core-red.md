# Agent Task Contract

## Goal
Create tests-only RED coverage for task 6.1 and 6.3 of `independent-app-cli-profiles`: canonical Plugin/Skill projection, bootstrap/generation/baselines, conflict and pending state, secret rejection, personal-Skill ownership, and target-home Skill path rendering.

## Worker ID
`split-shared-config-core-red`

## Scope
- Allowed write set for worker `split-shared-config-core-red` only:
  - `scripts/test_codex_shared_configuration.py`
- Allowed read-only scope: current config/document/store/home-sync/plugin modules and the active OpenSpec change.
- Primary-owned shared paths: OpenSpec, ledger, state, verification, docs, existing tests, and production integration remain main-owned.
- Forbidden: do not modify any path outside the named write set; do not touch live profile homes, install, repair plugins, switch, restart the App, use network, change dependencies, run Git writes, release, archive, or clean up.

## Constraints
Test through the planned public seam `reconcile_shared_configuration(...)` and read-only `shared_configuration_report(...)`, not private helper details. Use isolated temporary stores/homes only. Cover official bootstrap; semantic no-op; single-side and identical change; divergent/delete-vs-modify conflict with zero writes; credential-like marketplace rejection; unstable source; personal-Skill missing/correct/real/foreign/dangling/self-link cases; source-cache path remap; project-local non-interference. Tests must expect stable finding/status values and must not weaken existing behavior.

## Verification
Run only the new test file. The required terminal result is RED because the planned production module/public seam does not yet exist. Record exact test count plus failures/errors and verify `git diff --check -- scripts/test_codex_shared_configuration.py`.

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
The worker must wait for human review before expanding scope, touching forbidden files, changing the public persistence schema, reading credential values, editing production or existing tests, using a shared write path, running a destructive fixture action, touching live state, changing a dependency, using network, or causing an external effect.
