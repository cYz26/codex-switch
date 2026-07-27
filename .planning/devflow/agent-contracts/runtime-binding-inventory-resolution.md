# Agent Task Contract

## Goal
Implement dependency-ready canonical-runtime-binding tasks 1.1-1.4 through strict vertical TDD: add a pure, injected Desktop inventory; recognize only the verified current ChatGPT.app host as healthy; keep Codex.app migration-only and ChatGPT Classic excluded; and resolve one immutable official/internal runtime binding without accepting stale active observations, managed shims, raw internal Desktop paths, or recursive backends as authority.

## Worker ID
`runtime-binding-inventory-resolution`

## Scope
Allowed write set for worker `runtime-binding-inventory-resolution` only:
- `scripts/codex_switch_runtime_binding.py`
- `scripts/test_codex_runtime_binding.py`

This contract may start only after main marks `transactional-profile-state` focused verification and review complete.

Read-only inputs: `openspec/changes/canonical-runtime-binding/`, final TPS transaction/store/home/wrapper seams, constants/path helpers, existing profile tests, and current ChatGPT/Codex/Classic evidence.

Forbidden: do not edit any existing production module, legacy test, OpenSpec/control-plane/evidence file, generated artifact, or documentation. You are not alone in the repository: preserve all unrelated/main-agent changes and adapt to the accepted final TPS seam.

## Constraints
Implement the approved frozen types `DesktopInventory`, `RuntimeBindingContext`, `RuntimeBinding`, `RuntimeObservation`, `RuntimeAttestation`, and `BindingFinding` only to the extent needed for inventory/resolution; observation/attestation behavior may remain explicit dependency-ready stubs if not exercised by tasks 1.x. Keep dependency direction leaf-only: the new module may consume standard library and stable leaf/store/home data but must not import running-app, status, Doctor, verify, bindings, switching, or transaction. Do not re-export it through `codex_switch_core.py`.

Desktop discovery uses injected exact roots, never arbitrary App globbing or live fallback. A healthy current host requires the exact ChatGPT.app root fixture, bundle id `com.openai.codex`, a regular executable main binary at `Contents/MacOS/ChatGPT`, and a regular executable bundled CLI at `Contents/Resources/codex`. ChatGPT Classic is excluded by product identity even if the fixture deliberately contains an executable `codex`. Codex.app may be recorded only as a migration observation; it cannot certify a healthy official binding when ChatGPT.app is absent or invalid. Current ChatGPT wins when both fixtures exist.

Official binding sets shell/Desktop/backend to the verified ChatGPT bundled CLI and never accepts PATH, active.json, LaunchAgent, GUI env, or a path beneath the managed store/shim as fallback authority. Internal binding always resolves Desktop to the deterministic managed launcher, backend to the validated manifest `codex_bin`, and `requires_proxy=True`; raw manifest `app_cli_path` is migration drift, not authority. Reject missing/relative/non-regular/non-executable backend paths, the managed shim/launcher as recursive backend, and any backend resolving beneath managed wrapper/shim locations. The public `official` alias is normalized only where the accepted context already defines it; do not broaden arbitrary profile behavior. Use stable finding codes from the OpenSpec design and do not embed environment-specific wording in assertions.

All App bundles/backends are temporary fixtures. Do not read or mutate `/Applications`, PATH ownership, live processes, launchctl, profiles, network, install, release, or Git state. Use Python standard library only and `apply_patch` for edits.

## Verification
Add and run focused RED then GREEN tests for: exact current ChatGPT acceptance; wrong identity, missing main, missing CLI, directory/non-executable variants; Classic exclusion even with fake executable Codex CLI; legacy Codex migration-only; current-over-legacy; no-current fail-closed; official shell/Desktop/backend equality; managed-shim fallback rejection; internal managed launcher plus backend; raw internal app-path migration drift; recursive backend/shim rejection; and stale active observation non-authority. Tests must inject `DesktopRoots` and temporary plist/bundle/backend fixtures and never inspect the real workstation. Finish with the complete new suite on Python 3.9 and 3.12, dual-version compile checks, `openspec validate canonical-runtime-binding --strict --no-interactive`, and `git diff --check`; do not run legacy/full TPS suites from this read/write slice unless main requests them after integration.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus changed files; exact commands run with ordered RED/GREEN test logs and validation results; all test names; Desktop fixture matrix; official/internal resolution matrix; stable finding codes; dependency-import check; dual-version suite/compile results; strict OpenSpec and diff results; residual risks; unverified areas; and incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`. Do not mark OpenSpec tasks or update shared control-plane/evidence files; main owns those after independent review.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before accepting another current host/bundle identity, exposing arbitrary bundle roots as healthy product behavior, changing a public CLI/persistence contract, editing an existing production consumer, weakening managed-shim/recursive-backend rejection, expanding the write set, touching live Desktop/process state, adding a dependency, or bypassing a failing test. If the final TPS API no longer supplies the required context without a shared-file edit, report the exact seam and wait for main integration rather than importing upward.
