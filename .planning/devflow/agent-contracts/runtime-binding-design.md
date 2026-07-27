# Agent Task Contract

## Goal
Produce an implementation-ready, read-only design map for one canonical Runtime Binding module serving switch, capture/init, status, doctor, verify, internal rebind, and running-process attestation.

## Worker ID
`runtime-binding-design`

## Scope
Allowed read-only scope: inspect `scripts/codex_switch_constants.py`, `scripts/codex_switch_paths.py`, `scripts/codex_switch_lifecycle.py`, `scripts/codex_switch_bindings.py`, `scripts/codex_switch_running_app.py`, `scripts/codex_switch_status*.py`, `scripts/codex_switch_doctor*.py`, `scripts/codex_switch_verify.py`, existing tests, and relevant OpenSpec artifacts.
Forbidden: do not modify any repository path; do not start, stop, rebind, or switch ChatGPT Desktop; do not write launchctl state, create releases, commit, or push.

## Constraints
`/Applications/ChatGPT.app` is the current canonical Desktop bundle. `/Applications/Codex.app` may only be a verified legacy migration adapter; ChatGPT Classic is not a Codex backend target. Internal Desktop must use the managed launcher/proxy and diagnostics must attest both launcher and backend. No production dependency.

## Verification
Not applicable: this is a read-only explorer task; verify by mapping every binding source and consumer, identifying exact expected interfaces and tests, and reporting inspected files and residual risks.

## Evidence
Report status, changed files (`none` for this read-only task), inspected files and line-level findings, commands run, test logs or validation results (`not run` with rationale), proposed module interface/adapters, dependency-ordered TDD cases, compatibility risks, unverified areas, and review needs.

## Human Gate
Wait for main-agent review before real Desktop mutation, adopting unsupported bundle identity assumptions, changing an unapproved public API or compatibility behavior, any scope expansion beyond the named findings, modifying files, or skipping validation under the read-only verification contract.
