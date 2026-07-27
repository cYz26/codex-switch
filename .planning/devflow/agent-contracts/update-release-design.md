# Agent Task Contract

## Goal
Produce an implementation-ready, read-only design map for fail-safe package/install/self-update/release promotion, ordered internal update policy, fail-closed plugin catalog handling, and bounded/sanitized verification.

## Worker ID
`update-release-design`

## Scope
Allowed read-only scope: inspect `scripts/codex-switch`, `install.sh`, `run.sh`, `scripts/package-release.sh`, `scripts/release_auto.py`, `.github/workflows/auto-release.yml`, `scripts/codex_switch_plugins.py`, `scripts/codex_switch_verify.py`, existing tests, and relevant OpenSpec artifacts.
Forbidden: do not modify any repository path; do not install, self-update, disable plugins, create or push tags/releases, commit, or push.

## Constraints
All validation must be isolatable in temporary directories. Promotion keeps last-known-good until a success handshake. Version comparison never downgrades a healthy newer internal binary. Catalog parse uncertainty is not an empty catalog. Verification output is structured, bounded, timed out, and sanitized. No production dependency.

## Verification
Not applicable: this is a read-only explorer task; verify by tracing failure propagation and ordering, identifying exact isolated test harnesses, and reporting inspected files and residual risks.

## Evidence
Report status, changed files (`none` for this read-only task), inspected files and line-level findings, commands run, test logs or validation results (`not run` with rationale), proposed module/interface seams, dependency-ordered TDD cases, workflow ordering/reconciliation risks, unverified areas, and review needs.

## Human Gate
Wait for main-agent review before an actual installation, destructive tag/release mutation, plugin disable write, public API or compatibility expansion, any scope expansion, a new production dependency, file modification, or skipping validation under the read-only verification contract.
