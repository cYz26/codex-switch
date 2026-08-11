# Agent Task Contract

## Goal
Create tests-only RED coverage for task 8.1, 8.3, and 8.4 of `independent-app-cli-profiles`: internal CLI preflight ordering, explicit `sync-shared`, App-running pending behavior, and one shared diagnostic report.

## Worker ID
`split-shared-lifecycle-red`

## Scope
- Allowed write set for worker `split-shared-lifecycle-red` only:
  - `scripts/test_codex_shared_lifecycle.py`
- Allowed read-only scope: runtime binding, parser, status, Doctor, verify, release tests, and the active OpenSpec.
- Primary-owned shared paths: production code, existing tests, OpenSpec/control-plane files, docs, and integration remain main-owned.
- Forbidden: do not modify any path outside the named write set; do not touch live state, run real backend/plugin/network/process mutation, switch profiles, restart the App, change dependencies, run Git writes, release, archive, clean up, or perform a destructive effect.

## Constraints
Use fake exec/reconcile/runtime activity adapters and isolated stores. Cover functional preflight before backend execution; blocked reconcile means backend log empty; no-op executes once; `--help`/`--version` read-only; `sync-shared --dry-run` zero writes; App-running CLI-originated change becomes pending; stopped-App apply; conflict zero-write; status/Doctor/verify consume identical generation and stable finding codes. Preserve current `os.execve` design; do not propose or test a supervisor/watcher/daemon.

## Verification
Run only the new test file. The required terminal result is RED because lifecycle/public CLI integration is absent. Record exact test count/failures/errors and run `git diff --check -- scripts/test_codex_shared_lifecycle.py`.

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
The worker must wait for human review before expanding scope, touching forbidden files, changing process/TTY/signal semantics, introducing a supervisor/App wrapper/watcher/daemon, touching live state, using network, adding a dependency, editing production/existing-test/control-plane files, or causing an external effect.
