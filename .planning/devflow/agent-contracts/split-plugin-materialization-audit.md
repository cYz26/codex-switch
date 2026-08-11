# Agent Task Contract

## Goal
Determine how App-side Plugin and Skill additions or upgrades can become directly usable by the internal CLI on its next invocation while the two CODEX_HOME plugin caches remain physically independent.

## Worker ID
`split-plugin-materialization-audit`

## Scope
Write set: none. All repository writes are forbidden. Allowed read-only scope: inspect `scripts/codex_switch_plugins.py`, `scripts/codex-switch`, `scripts/codex_switch_verify.py`, plugin/cache manifests under the current official and internal homes, current CLI help output, release packaging, and relevant tests. Forbidden: do not invoke plugin add/remove/marketplace upgrade, write config/cache state, use network installers, switch profiles, restart ChatGPT, commit, push, release, archive, or cleanup.

## Constraints
Separate shared desired state from independent materialization. Determine whether current selector/catalog/cache records expose exact version, revision, source, and digest; do not invent unsupported platform hooks or assume a cache path is portable across backend versions. Existing running-process safety and fail-closed stale-cache rules remain mandatory.

## Verification
Read-only verification: use concrete `rg -n`, `sed -n`, `find`, `stat`, `shasum`, and CLI `--help` commands only. Trace App mutation evidence through config/catalog/cache inputs to the internal `repair-plugins` seam and identify exact public-seam RED tests for add, upgrade, disable/remove, unavailable/incompatible source, no-op, and already-running session cases. Tests are not run because this worker makes no changes; record that rationale.

## Evidence
Return status, changed files (`none`), inspected files/paths, commands run, test logs or validation results (`not run` with the read-only rationale), sanitized command results, observed schemas/fields, recommended desired-state record, lifecycle seam, missing tests, compatibility risks, unverified areas, and review needs.

## Human Gate
Main-agent review is required before adopting the desired-state record or lifecycle seam. Stop and report for these concrete review triggers: live plugin mutation, network installation, credential exposure, sharing a mutable cache directory, dependency addition, destructive cache replacement, or any source change.
