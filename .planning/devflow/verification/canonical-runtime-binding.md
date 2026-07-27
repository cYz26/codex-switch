# Canonical Runtime Binding Verification

## Completion Claim

Status: `COMPLETE`.

Inventory/resolution, process observation/attestation, lifecycle and diagnostic
consumers, transactional internal rebind, and all final completion gates are
complete. Product behavior remains limited to official/internal; explicit
historical fixtures remain compatibility-only and do not become canonical
product bindings.

## Constraints Preserved

- Product behavior is limited to `openai-official` (plus its accepted
  `official` alias) and `internal`; no arbitrary profile is promoted.
- `/Applications/ChatGPT.app` with bundle id `com.openai.codex` is the sole
  current healthy official host shape.
- `Codex.app` is recorded only as migration evidence, and ChatGPT Classic is
  always excluded.
- All discovery and backend tests use injected temporary fixtures. No live App,
  profile, launchctl, install, update, release, network, or Git effect ran.

## Slice 1 - Inventory and Resolution

Outcome: `DONE`.

### TDD Log

| Stage | Command | Exit | Result |
|---|---|---:|---|
| RED | `/usr/bin/python3 scripts/test_codex_runtime_binding.py -q` | 1 | `ModuleNotFoundError: codex_switch_runtime_binding` before implementation |
| GREEN 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v` | 0 | 17/17 passed |
| GREEN 3.12 | `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12 scripts/test_codex_runtime_binding.py -v` | 0 | 17/17 passed |
| Compile | dual-interpreter `python -m py_compile` for module and test | 0 | both passed |
| Dependency | AST import-direction guard | 0 | leaf-only; no running/status/Doctor/verify/bindings/switch/transaction imports |
| Contract | `validate_agent_task_contract.py --contract ...runtime-binding-inventory-resolution.md --json` | 0 | `ok: true`, zero errors, zero missing sections |
| OpenSpec | `openspec validate canonical-runtime-binding --strict --no-interactive` | 0 | valid |
| Whitespace | tracked and untracked `git diff --check` variants | 0 | no diagnostics |

### Desktop Fixture Matrix

| Fixture | Expected | Evidence |
|---|---|---|
| Valid ChatGPT plist, main, bundled CLI | current healthy host | `test_discovery_accepts_current_chatgpt` |
| Wrong ChatGPT bundle id | fail closed | `test_discovery_rejects_current_chatgpt_with_wrong_identity` |
| Missing main or CLI | fail closed | two direct missing-member tests |
| Directory/non-executable main or CLI | fail closed | four subcases in `test_discovery_rejects_directory_and_non_executable_members` |
| ChatGPT Classic with executable fake CLI | excluded | `test_discovery_excludes_chatgpt_classic_even_with_codex_cli` |
| Codex.app fixture | migration-only, never healthy | `test_discovery_marks_legacy_codex_as_migration_only` |
| Current and legacy together | current wins, legacy retained as evidence | `test_discovery_current_chatgpt_wins_over_legacy_codex` |

### Resolution Matrix

| Profile/input | Binding result | Evidence |
|---|---|---|
| Official plus verified current host | shell/Desktop/backend all bundled ChatGPT CLI | `test_official_resolution_uses_bundled_cli_for_full_chain` |
| Official with no verified current host | error | `test_official_resolution_fails_closed_without_verified_current_host` |
| Official with only managed PATH shim | `binding.official.managed_shim_rejected` | direct test |
| Internal with valid external backend | shell/backend use backend; Desktop uses managed launcher; proxy required | direct test |
| Internal raw `app_cli_path` | migration finding; launcher remains authoritative | direct test |
| Internal missing/relative/directory/non-executable backend | error | four subcases |
| Internal backend at/below managed bin | recursive-backend error | three subcases |
| Stale active record | finding only; manifest-derived binding unchanged | direct test |
| Unsupported profile | error; no new product behavior | alias/unsupported test |

### Stable Finding Codes Introduced

- `desktop.current.plist_invalid`
- `desktop.current.bundle_id_mismatch`
- `desktop.current.main_invalid`
- `desktop.current.cli_invalid`
- `desktop.legacy.migration_only`
- `desktop.classic.excluded`
- `binding.profile.unsupported`
- `binding.official.current_host_unavailable`
- `binding.official.managed_shim_rejected`
- `binding.internal.backend_invalid`
- `binding.internal.recursive_backend`
- `binding.internal.raw_app_cli_migration_drift`
- `binding.internal.app_cli_drift`
- `binding.observation.active_stale`

## Changed Files So Far

- `scripts/codex_switch_runtime_binding.py`
- `scripts/test_codex_runtime_binding.py`

## Slice 1 Checkpoint Risks (Resolved Later)

- `RuntimeObservation` and `RuntimeAttestation` are dependency-ready shapes only;
  tasks 2.x must supply and verify the full process/environment/launchctl chain.
- No existing consumer has been migrated yet; tasks 3.x own that integration.
- Internal staged rebind and rollback remain tasks 4.x.

Incidental findings: none. Next outcome: `CONTINUE_NEXT_ITEM`.

## Slice 2 - Process Observation and Attestation

Outcome: `DONE`.

### TDD Log

| Stage | Command | Exit | Result |
|---|---|---:|---|
| RED parser/attestation | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v` | 1 | 29 tests ran; 5 expected failures and 6 expected errors exposed fixed-regex, host-marker, chain, and fingerprint gaps |
| GREEN 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -q` | 0 | 30/30 passed |
| GREEN 3.12 | `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12 scripts/test_codex_runtime_binding.py -q` | 0 | 30/30 passed |
| Legacy focused | six existing parser/proxy tests via `python -m unittest` | 0 | 6/6 passed |
| Legacy full 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_profile_switch.py -q` | 0 | 123/123 passed |
| Static | dual compile, strict OpenSpec, tracked/untracked diff checks | 0 | all passed |

### Parser / Observation Evidence

- Token-aware parsing accepts `-c key=value` and multiple supported global
  option/value pairs before `app-server`.
- A preceding `exec` subcommand, shell payload, malformed quoting, unknown
  pre-subcommand token, or `--` boundary fails closed.
- Desktop recognition comes from `DesktopInventory` main executables. No fixed
  `/Applications/Codex.app/Contents/MacOS/Codex` marker remains in the running
  process module.
- `collect_runtime_observation()` freezes process, GUI env, LaunchAgent, and
  managed-launcher fingerprint evidence. A supplied snapshot is reused by the
  status printer and the Doctor/verify running-process helper; the direct
  collection-count regression proves one inventory scan for all three views.

### Attestation Matrix

| Observation | Result/code |
|---|---|
| Official ChatGPT main plus bundled child | healthy |
| Internal launcher env, proxy parent, requested child backend | healthy |
| Correct launcher with stale child | `attestation.app_server.backend_mismatch` |
| Correct backend without proxy parent | `attestation.internal.proxy_bypass` |
| Stale LaunchAgent | `attestation.launch_agent.cli_mismatch` |
| Running Desktop with unset GUI env | `attestation.gui_env.unset` |
| Running legacy Codex.app | `attestation.desktop.legacy_running` |
| Managed launcher fingerprint drift | `attestation.internal.launcher_fingerprint_mismatch` |

Additional stable codes are `attestation.desktop.host_mismatch` and
`attestation.gui_env.cli_mismatch`. Attestation findings are de-duplicated by
code/expected/observed identity, and health fails on any error finding.

## Changed Files So Far

- `scripts/codex_switch_runtime_binding.py`
- `scripts/codex_switch_running_app.py`
- `scripts/test_codex_runtime_binding.py`

## Slice 2 Checkpoint Queue (Completed Below)

- Tasks 3.x must make lifecycle/status/Doctor/verify construct the canonical
  context and pass the shared observation through their public orchestration.
- Tasks 4.x must supply a generated expected launcher fingerprint and prove the
  staged rebind/rollback chain.

Next outcome: `CONTINUE_NEXT_ITEM`.

## Slice 3 - Lifecycle and Diagnostic Consumers

Outcome: `DONE`.

### TDD and Integration Evidence

- Init without explicit CLI input resolves the verified ChatGPT.app bundled
  Codex binary for both official shell and Desktop intent. Explicit
  `--app-cli-path` remains an isolated compatibility contract and no longer
  accidentally inherits `codex_bin` from PATH.
- Internal capture and both shared/snapshot switch modes record the managed
  `codex-internal-app` launcher, while the manifest backend remains the shell
  and app-server child authority.
- Status, Doctor, and verify derive expected values from the same manifest
  binding, reuse a supplied immutable observation, and emit the same stable
  finding codes. A stale active record cannot override manifest intent.
- App-server smoke requires a matching initialize `result` with no `error`.
  The documented plugin-list authentication response after successful
  initialization remains accepted.
- The compatibility correction was proved by a 14-test focused legacy run:
  explicit official init, shell/Desktop switch, plugin repair, runtime smoke,
  Responses smoke, report sanitization, and one-key wrapper cases all passed.

## Slice 4 - Transactional Internal Rebind

Outcome: `DONE`.

### Rebind Contract and Rollback Evidence

- `set-bin internal` rejects missing, non-executable, and recursive managed
  backends before mutation; raw internal `set-app-bin` and
  `--preserve-app-cli` are rejected with remediation.
- The candidate launcher is rendered in a private stage, verified to retain the
  proxy/backend chain, and exercised through initialize/initialized/plugin-list
  with a temporary CODEX_HOME. The proxy child receipt proves the exact backend
  and app-server route before promotion.
- Manifest and launcher are promoted under the store lock with a durable
  `prepared -> committed` rebind journal. Catchable failure restores the old
  pair; prepared recovery rolls back, committed recovery rolls forward, and
  foreign concurrent target state fails closed while retaining evidence.
- Dry-run reports a pending rebind without recovery writes. A symlink rebind
  marker is rejected without following or modifying its target.
- Both rebind and ordinary product internal switch persist a lowercase
  SHA-256 of the generated launcher. Doctor recomputes it and reports
  `attestation.internal.launcher_fingerprint_mismatch` after byte drift.
- Successful rebind reports that ChatGPT must be fully restarted. No live
  backend or Desktop binding was changed by these tests.

## Slice 5 - Final Verification

Outcome: `DONE`.

| Gate | Result |
|---|---|
| Runtime binding Python 3.9 | 53/53 passed |
| Runtime binding Python 3.12 | 53/53 passed |
| Transaction regression Python 3.9 | 207/207 passed |
| Transaction regression Python 3.12 | 207/207 passed |
| Legacy CLI Python 3.9 | 123/123 passed |
| Legacy CLI Python 3.12 | 123/123 passed |
| Strict OpenSpec | `canonical-runtime-binding` valid |
| Shell syntax | wrapper, env setup, installer, runner, package script passed |
| Python AST | 43 files passed under Python 3.9 and 3.12 |
| Import smoke | 17 changed modules passed under Python 3.9 and 3.12 |
| Source integrity | `git diff --check` passed |
| Obsolete authority scan | no old current Codex.app CLI constant, fixed main marker, or official resolver remains in production Python |

### Stable SHA-256 at Completion

- `scripts/codex_switch_runtime_binding.py`:
  `cd2fe9b6e7c0c19af601337398992aaf43020143323d8cce5cc26062b7383a7f`
- `scripts/codex_switch_running_app.py`:
  `ac4660756046ea925c480136190d383386caba78937dbe87473fb88a3a312667`
- `scripts/codex_switch_bindings.py`:
  `13dc2b6c5e17958f01d149bee944aa64fc7d52b1da0d10fad703c83ba4042d69`
- `scripts/codex_switch_transaction.py`:
  `3dd2da319fe3c1d179f5f17ae5cf0da611ff7248c16290bf1a17cf0d89215a22`
- `scripts/codex_switch_lifecycle.py`:
  `b740b2082747fe030eac173156b98892c76d859b34cbb8c1d4a62aee8515e995`
- `scripts/test_codex_runtime_binding.py`:
  `4eae754fcf4a14febea401b57c1429852e6f2a52656876550475bfec8eec5c87`

## Final Changed-File Scope

- Canonical resolver/observation: `codex_switch_runtime_binding.py`,
  `codex_switch_running_app.py`.
- Consumers: lifecycle, capture, switching, wrapper, status, Doctor, verify,
  path/constants/core, CLI help, plan, and current ChatGPT guidance.
- Rebind: bindings, wrapper/proxy smoke receipt, transaction rebind journal.
- Regressions: `test_codex_runtime_binding.py` plus narrow legacy expectation
  updates required by the canonical managed internal launcher.

## Residual Risk

- `Codex.app` remains observable only for migration diagnostics; it is not
  certified as current. ChatGPT Classic remains excluded.
- Explicit official paths created by legacy/test workflows remain supported as
  `explicit-compatibility`; canonical official behavior is ChatGPT.app-only.
- Process and GUI environment attestation is a point-in-time observation.
  Actual workstation restart/rebind remains a human-gated operational step and
  was deliberately not executed.

Incidental finding resolved: the rebind recovery marker now fails closed on a
symlink. Next outcome: `CONTINUE_NEXT_ITEM` for `schema-scoped-app-proxy`.

## Integration Repair Closure

The post-integration binding repair is complete. Internal product-profile
`codex_bin` resolution now rejects missing or empty manifest values instead of
falling back to an unrelated PATH binary, resolves symlink aliases to the
strict regular executable target, and uses that canonical backend for capture,
rebind, switch planning, launcher generation, and capability-receipt binding.
The transaction drift regression patches the canonical resolver boundary, so
it still proves a backend byte change after resolution is rejected before the
first transaction write.

Fresh final-source evidence:

- Runtime Binding: 55/55 on Python 3.12 and 55/55 on system Python 3.9.
- Transaction: 215/215 on Python 3.12.
- Complete profile suite: 195/195 on Python 3.12.
- Strict OpenSpec: 17/17 repository items.
- Bash syntax: 5/5 entrypoints.
- Python AST/import: 54/54 and 46/46 on both supported test runtimes.
- Workflow YAML: 2/2; release workflow contracts: 7/7.
- Isolated release package validation and `git diff --check`: passed.

This closes the reopened completion row and task 5.6. Live Desktop ownership
remains a rollout check and is not inferred from these source tests.
