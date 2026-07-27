# Agent Task Contract

## Goal
Produce an implementation-ready, read-only design map for schema-scoped app-server compatibility transforms, semantic config recovery, canonical launcher home sync, and wrapper-to-proxy-to-fake-backend integration tests.

## Worker ID
`proxy-config-design`

## Scope
Allowed read-only scope: inspect `scripts/codex_switch_app_proxy.py`, `scripts/codex_switch_config.py`, `scripts/codex_switch_toml_*.py`, `scripts/codex_switch_app_wrapper.py`, `scripts/codex_switch_home_sync.py`, existing tests, generated local schema evidence, and relevant OpenSpec artifacts.
Forbidden: do not modify any repository path; do not run the real Desktop or send traffic to a live backend; do not write profile homes, create releases, commit, or push.

## Constraints
Transforms must be selected by RPC method, direction, known field path, and explicit capability. Current local `0.142.4` schema advertises canonical `dynamicTools`, `keyPath`, and `created-by-me-remote`; unknown payloads pass through semantically unchanged. Use standard-library-only code and one canonical home-sync policy.

## Verification
Not applicable: this is a read-only explorer task; verify by mapping supported message shapes, config entity identity, current test seams, and the isolated fake-backend E2E path, and report inspected files and residual risks.

## Evidence
Report status, changed files (`none` for this read-only task), inspected files and line-level findings, commands run, test logs or validation results (`not run` with rationale), proposed adapter/document interfaces, dependency-ordered TDD cases, compatibility risks, unverified areas, and review needs.

## Human Gate
Wait for main-agent review if a required transform cannot be justified by generated schema or existing compatibility evidence, a new TOML dependency appears necessary, live backend traffic would be required, files would be modified, or the read-only verification contract would be skipped.
