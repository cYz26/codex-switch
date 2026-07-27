# Stale Profile Plugin Cache Refresh Plan

**Goal:** Make `codex-switch` automatically refresh only provably stale enabled
plugin caches through the target profile runtime before one-key verification and
Doctor.

**Architecture:** Extend `codex_switch_plugins.py` with structured catalog
entries, deterministic source/cache manifests, canonical product-profile
runtime resolution, and a running-target safety gate. Keep the existing
`repair-plugins` and one-key CLI boundaries.

**Tech Stack:** Python standard library, Bash wrapper, `unittest`, existing
runtime-binding/process observation modules.

## Global Constraints

- Preserve unrelated worktree changes and existing missing/unavailable plugin
  behavior.
- Do not mutate live workstation profiles during implementation verification.
- Do not refresh project-local DevFlow/OpenSpec configuration.
- Add no dependency and perform no App lifecycle, install, release, Git, or
  archive action.

## Target State

`repair-plugins` verifies the canonical target CLI, refreshes marketplace and
catalog state in the target `CODEX_HOME`, compares inspectable enabled plugin
sources with their catalog-version caches, and calls `plugin add` only for
missing available or confirmed stale selectors. One-key switches inherit that
behavior before verification and Doctor.

## Completion Contract

- [x] Every delta-spec scenario has a focused regression.
- [x] Stale inspectable caches refresh once; current caches are no-ops.
- [x] Missing, unavailable, dry-run, and uninspectable behavior is truthful.
- [x] Canonical CLI/version/home and running-target safety are verified.
- [x] Focused, full, compatibility, OpenSpec, syntax, and diff checks pass.

## 1. Contract and RED Evidence

- [x] 1.1 Create and strictly validate proposal, design, delta spec, and this
  executable task list with no open decision.
- [x] 1.2 Add isolated CLI fixtures and RED tests for stale local cache refresh,
  current cache no-op, runtime-residue equivalence, source/version mismatch,
  missing compatibility, unavailable compatibility, and dry-run truthfulness.
- [x] 1.3 Add RED tests proving canonical runtime selection, `--version`,
  explicit target `CODEX_HOME`, uninspectable-source skip, and active target
  app-server blocking.
- [x] 1.4 Add RED one-key regression proving stale refresh occurs after switch
  and before verification and Doctor.
- [x] 1.5 Record exact expected RED failures in the verification receipt before
  production edits.

## 2. Catalog and Cache Comparison

- [x] 2.1 Replace selector-only JSON reduction with structured catalog entries
  that retain selector, safe version, and optional absolute local source.
- [x] 2.2 Implement deterministic tree manifests with relative type, SHA-256,
  symlink target, executable bit, and bounded runtime-residue exclusions.
- [x] 2.3 Classify enabled plugins as missing, unavailable, current, stale, or
  uninspectable without duplicate install actions.

## 3. Runtime and Repair Integration

- [x] 3.1 Resolve product-profile plugin maintenance through
  `resolve_store_runtime_binding`, preserve custom-profile fallback, and verify
  the selected CLI with target `CODEX_HOME`.
- [x] 3.2 Integrate stale candidates into `repair_profile_plugins` while
  preserving disable-unavailable and dry-run behavior.
- [x] 3.3 Observe running processes only for stale candidates and fail closed
  with remediation when the target app-server chain is active.
- [x] 3.4 Make all focused RED tests GREEN and inspect the implementation diff
  for scope and duplicate ownership.

## 4. Documentation and Evidence

- [x] 4.1 Update bounded CLI help/README text to describe missing plus confirmed
  stale refresh, canonical target runtime, and active-App remediation.
- [x] 4.2 Record RED/GREEN commands, changed files, scope exclusions, and
  residual risks under `.planning/devflow/verification/`.
- [x] 4.3 Update this execution ledger after fresh evidence; keep the existing
  legacy `.planning/STATE.md` read-only and do not synthesize
  `.planning/devflow/STATE.md` as an implicit project-state migration.

## 5. Final Verification

- [x] 5.1 Run focused plugin/one-key tests and the full
  `scripts/test_codex_profile_switch.py` suite with bytecode disabled.
- [x] 5.2 Run Python 3.9 and 3.12 compilation/tests available on the machine,
  shell syntax, strict OpenSpec validation, workflow-state validation, and
  `git diff --check`.
- [x] 5.3 Inspect final status/diff, confirm no live profile or project refresh
  occurred, remove the temporary retired-hook compatibility shim, and report
  the required ChatGPT restart.

## Execution Ledger

- Current item: complete
- Continuation: auto-until-terminal
- Result: 23/23 tasks complete; source verified but not installed or applied to
  live profile caches.
- State note: the validator still reports the pre-existing read-only legacy
  root-state warning. This change did not migrate project workflow state or
  replace the active `schema-scoped-app-proxy` ownership.
- Approved write set:
  `scripts/codex_switch_plugins.py`,
  `scripts/test_codex_profile_switch.py`, bounded CLI/README text, this change,
  and one verification receipt/state update.
- Human Gates: dependency addition, App lifecycle automation, destructive cache
  cleanup, project migration, install/release, Git effects, or archive.

## Acceptance Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_stale_local_plugin_cache
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/codex_switch_plugins.py
/opt/homebrew/bin/python3.12 -m py_compile scripts/codex_switch_plugins.py
openspec validate refresh-stale-profile-plugin-caches --strict
python3 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/validate_workflow_state.py \
  --repo /Users/cY/dev/codex-switch --json
bash -n scripts/codex-switch
git diff --check
```
