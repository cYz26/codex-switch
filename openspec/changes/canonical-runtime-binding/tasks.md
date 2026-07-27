# Canonical Runtime Binding Implementation Plan

**Goal:** Make one canonical binding and attestation interface own official ChatGPT Desktop discovery, internal managed launcher/backend intent, process observations, diagnostics, and rebind verification.

**Architecture:** `codex_switch_runtime_binding.py` exposes discovery, resolution, and attestation. Manifest/store data is intent; active/launchctl/process data is an immutable observation. Rebind stages a candidate and commits through the profile transaction seam.

**Tech Stack:** Python 3 standard library, macOS plist/process inspection, `unittest`, existing CLI.

## Global Constraints

- `/Applications/ChatGPT.app` with bundle id `com.openai.codex` and bundled executable `codex` is the only current healthy official host.
- Codex.app is migration observation only; ChatGPT Classic is never a candidate.
- Internal Desktop always uses the managed launcher/proxy plus separately attested backend.
- No live App start/stop/rebind/switch, release, commit, push, or production dependency.
- OpenSpec/control-plane/shared integration files remain main-agent owned.

## Target State

Init/capture/switch/set-bin/status/Doctor/verify resolve the same immutable binding. Current ChatGPT processes with global CLI options are observed, stale active/launchctl/process state becomes stable findings, and internal rebind either promotes a verified launcher/backend pair or leaves the previous pair intact.

## Completion Contract

- [x] Every binding and attestation scenario has a focused regression.
- [x] Official resolution never falls back to the managed PATH shim or ChatGPT Classic.
- [x] Fresh internal init/capture and normal one-key Doctor agree without skips.
- [x] A correct launcher with a stale child backend is rejected.
- [x] Initialize errors cannot pass smoke.
- [x] Focused, legacy, OpenSpec, syntax, and diff checks pass.
- [x] PATH/rebind symlink aliases are canonicalized before internal manifest,
  launcher, and capability-receipt binding.

## Critical Path

Desktop inventory → canonical binding → token-aware observation → shared attestation → lifecycle/diagnostic migration → transactional rebind.

## Incidental Finding Budget

One bounded RED/GREEN guard may cover another existing binding consumer. Custom-profile/direct `set-app-bin` behavior is not expanded; live bundle migration or a new host requires a Human Gate.

## 1. Desktop Inventory and Canonical Resolution

- [x] 1.1 Add RED adapter tests in `scripts/test_codex_runtime_binding.py`: current ChatGPT accepted, ChatGPT Classic rejected, Codex.app observation marked migration-only, current wins over legacy, and no verified current host fails closed.
- [x] 1.2 Create `scripts/codex_switch_runtime_binding.py` with `DesktopInventory`, `RuntimeBindingContext`, `RuntimeBinding`, `RuntimeObservation`, `RuntimeAttestation`, and `BindingFinding`; implement exact-root/plist/executable `ChatGPTDesktopHost` discovery and make 1.1 GREEN.
- [x] 1.3 Add RED resolution tests for official bundled shell/launcher/backend equality, managed-shim fallback rejection, internal managed launcher plus manifest backend, raw internal app path migration drift, recursive backend/shim rejection, and stale active-record non-authority.
- [x] 1.4 Implement `resolve_runtime_binding()` and validation invariants; make 1.3 GREEN without changing callers.

## 2. Process Observation and Attestation

- [x] 2.1 Add RED parser tests `test_app_server_parser_accepts_global_config_before_subcommand`, `test_app_server_parser_accepts_multiple_global_options`, `test_app_server_parser_rejects_exec_payload_mentions`, and `test_running_desktop_uses_host_executable` using the observed ChatGPT command shape.
- [x] 2.2 Replace the fixed regex/constant in `scripts/codex_switch_running_app.py` with token-aware subcommand parsing and host-derived main executable observations; make 2.1 GREEN.
- [x] 2.3 Add RED attestation tests for official direct chain, internal proxy chain, correct launcher/wrong backend, backend without proxy bypass, stale LaunchAgent, unset GUI env, legacy running host, and managed-launcher fingerprint drift.
- [x] 2.4 Implement `attest_runtime_binding()` with stable finding codes and one immutable process/environment/launchctl snapshot; migrate running-app helpers and make 2.3 GREEN.
- [x] 2.5 Add `test_diagnostic_process_inventory_is_collected_once` and refactor one-key diagnostic orchestration so status, Doctor, and verify reuse the supplied observation instead of rescanning.

## 3. Lifecycle and Diagnostic Consumers

- [x] 3.1 Add RED integration tests `test_init_defaults_official_to_chatgpt_bundled_codex`, `test_capture_internal_records_managed_launcher_binding`, and `test_fresh_internal_one_key_passes_doctor_without_skip`.
- [x] 3.2 Migrate `scripts/codex_switch_paths.py`, `scripts/codex_switch_lifecycle.py`, `scripts/codex_switch_app_wrapper.py`, and switch binding inputs to canonical resolution; remove official PATH fallback and raw internal Desktop intent; make 3.1 GREEN.
- [x] 3.3 Add RED tests `test_status_without_gui_env_prints_expected_binding`, `test_status_doctor_and_verify_share_finding_codes`, and `test_verify_manifest_expectation_wins_over_stale_active_record`.
- [x] 3.4 Migrate `scripts/codex_switch_status_app.py`, `scripts/codex_switch_doctor_active.py`, other Desktop Doctor/status helpers, and binding portions of `scripts/codex_switch_verify.py` to resolution/attestation; make 3.3 GREEN.
- [x] 3.5 Add RED `test_initialize_error_fails_app_server_smoke`; require a matching `result` with no `error` before initialized/plugin-list handling and make it GREEN while preserving the documented post-initialize plugin auth allowance.
- [x] 3.6 Add RED command-level regressions proving fresh internal capture stores
  the resolved PATH backend and a normal switch migrates a legacy symlink-valued
  manifest without relaxing capability-receipt no-follow checks.
- [x] 3.7 Canonicalize internal product-profile backend paths during
  capture/rebind and switch planning, commit legacy manifest migration with the
  refreshed launcher/receipt, and make 3.6 GREEN.

## 4. Transactional Internal Rebind

- [x] 4.1 Add RED tests for invalid/non-executable/recursive backend preflight, internal `set-app-bin` raw-backend rejection, staged launcher retaining proxy, failed smoke preserving manifest/launcher bytes, requested-backend child attestation, and successful restart-required observation.
- [x] 4.2 Refactor `scripts/codex_switch_bindings.py` so `set-bin internal` builds a candidate manifest, resolves it, and stages the managed launcher; no manifest or launcher promotion occurs before validation.
- [x] 4.3 Run bounded Desktop-like initialize/initialized/plugin-list smoke through the staged launcher, attest its child backend, and commit manifest plus launcher through the transaction seam; make 4.1 GREEN.
- [x] 4.4 Preserve official/direct compatibility outside the two product profiles without making it new healthy product behavior; document any rejected explicit app override with remediation.

## 5. Cleanup and Verification

- [x] 5.1 Remove old Codex.app current constants, fixed Desktop marker, PATH fallback authority, and duplicate expected-binding derivation after `rg` proves all product-profile callers use the canonical module.
- [x] 5.2 Run `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v` and require zero failures.
- [x] 5.3 Run `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` and require all legacy regressions to pass.
- [x] 5.4 Run `openspec validate canonical-runtime-binding --strict --no-interactive`, shell syntax, Python AST/import checks, and `git diff --check`.
- [x] 5.5 Record current/legacy adapter evidence, RED/GREEN logs, changed files, rebind rollback evidence, and residual migration risk in `.planning/devflow/verification/canonical-runtime-binding.md`.
- [x] 5.6 Re-run focused Runtime Binding/Profile tests, the complete profile
  suite, strict OpenSpec, syntax/import checks, and `git diff --check`; append
  the integration repair evidence before returning to `VER-001`.

## Execution Ledger

| Slice | Owner | Write Set | Evidence | Human Gate | Next Outcome | Status |
|---|---|---|---|---|---|---|
| Inventory/resolution | main | runtime binding module/test | adapter and invariant RED/GREEN | new host/identity | CONTINUE_NEXT_ITEM | done |
| Observation/attestation | main | running-app plus runtime test | real-shape parser/attestation log | ambiguous live behavior | CONTINUE_NEXT_ITEM | done |
| Consumers | main | lifecycle/status/Doctor/verify binding portions | shared finding log | public compatibility expansion | CONTINUE_NEXT_ITEM | done |
| Rebind | main with transaction seam review | bindings/wrapper plus runtime test | staged smoke/rollback log | live rebind | VERIFY_ACTIVE_CHANGE | done |
| Symlink canonicalization | main | paths/capture/bindings/transaction plus focused tests | capture and legacy-switch RED/GREEN | custom-profile expansion | VERIFY_ACTIVE_CHANGE | done; missing/empty backends fail closed and symlink aliases resolve to the executable target |
| Final verification | main | control plane/evidence | full commands | external effects | COMPLETE | done; runtime 55/55 on both runtimes, transaction 215/215, profile 195/195, strict/static/package gates green |

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate canonical-runtime-binding --strict --no-interactive
bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
git diff --check
```

## Risks / Rollback

- Historical Codex.app identity is not certified; it remains migration-only.
- Rebind depends on the transaction seam and must serialize overlapping files through main integration.
- Rollback restores previous source/manifest/launcher; no test mutates the real Desktop.
