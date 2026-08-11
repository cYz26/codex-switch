# Agent Task Contract

## Goal
Close the production Plugin materializer final-review blocker by refusing backend-managed cache receipts whose catalog/source compatibility is uninspectable, while preserving exact and independently materialized target-backend behavior.

## Worker ID
`split-shared-final-plugin-fixes`

## Stable Input Snapshot
- `scripts/codex_switch_plugins.py`: `d3fdf695751c12d4a2e8d391877f2e0255b9adb282e5a0cb4e49ffb3a56f7ee1`
- `scripts/test_codex_shared_materialization.py`: `e18d66108e73f181876e4b9028564b8f1867be51dd83c3befca807d4ba3fe74b`
- OpenSpec design: `19b0a6c8b85c840ecb5ae63f10a58959b4785cd82b19272548fbdc50b5f4a43e`
- OpenSpec spec: `6b507cfc85f2c3db0ce73da69425fa7159227df51862e174457b194666533089`

Stop before editing if the production hash differs. Tests/OpenSpec are read-only; main and another worker may edit only disjoint files.

## Scope
Allowed write set for worker `split-shared-final-plugin-fixes` only:
- `scripts/codex_switch_plugins.py`

Read plugin tests and adjacent catalog helpers as needed. Forbidden: all other writes, live profile/cache/App/backend/network operations, dependencies, cleanup, Git, release, or archive.

## Constraints
Read `.agents/skills/diagnosing-bugs/SKILL.md` and `.agents/skills/tdd/SKILL.md` fully. Preserve native target-backend installation, separate caches, retained versions, `portable_exact`, post-install attestation, and stable errors. The RED `test_production_materializer_rejects_uninspectable_managed_cache` must pass without invoking native add. Do not treat `classify_installed_plugin_cache(...)=uninspectable` as compatible; return a stable `shared_configuration.materialization.unverified_catalog` failure before receipt publication. Do not weaken existing direct production adapter tests.

## Verification
Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest scripts.test_codex_shared_materialization
PYTHONDONTWRITEBYTECODE=1 python3.12 -m py_compile scripts/codex_switch_plugins.py
git diff --check -- scripts/codex_switch_plugins.py
```

No live plugin/backend command is permitted.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` and report:
- changed files and final hashes;
- commands run;
- complete test logs or validation results with exact counts;
- RED cause and GREEN proof;
- unchanged behaviors;
- unverified areas;
- risk notes and incidental-finding classification.

## Human Gate
The worker must wait for human review and report `BLOCKED_AWAITING_HUMAN` before any scope/write-set expansion, touching a forbidden file, changing artifact-policy compatibility or a public API/CLI, adding a dependency, skipping validation, continuing with failing tests or unverified severe risk, mutating live state/cache/processes, invoking network/backend/plugin operations, deleting retained artifacts, or performing Git/install/release/archive/cleanup effects.

## Follow-up Amendment 2026-08-05

Stable inputs for this follow-up replace the original snapshot:

- `scripts/codex_switch_plugins.py`: `4860383318ce730f173d58e0a00fc8a5f72a251e91431ab52667fb51abfd0583`
- `scripts/test_codex_shared_materialization.py`: `8cbef96c486fd9310a1f8852c6a43bc6f18cf4f2d46055d7eeb7f61329f3358d`
- OpenSpec design: `211a9898509ccb3ec5b9834a3c0caa08c93b086eedbd35f4ab1cc42b9fa4eebe`
- OpenSpec spec: `390b86a3a51b2a4c0a0eb4e2c8ec29ffbfd7ee0ff85319443df7b4da5ba073a6`

Close these additional canonical REDs without editing tests:

1. Only `portable_exact` may take a catalog-free existing-artifact fast path.
   Every `backend_managed` candidate, even byte-identical to the source, must
   pass the target catalog and an inspectable compatibility classification.
2. After native add for an inspectable backend-managed entry, classify the
   installed cache again and require `current`; a successful/no-op add that
   leaves stale bytes must fail before receipt publication.
3. Production native add must return with target `config.toml` unchanged.
   It may restore an exact, expected plugin-selector activation delta, but any
   non-selector or otherwise unexpected config change must raise
   `shared_configuration.target_changed_during_plan` and preserve the changed
   file while removing only the operation-owned selector delta. Base the
   allowance on parsed/exact config evidence, not a broad whole-file overwrite.

Named REDs:

- `test_production_identical_managed_cache_still_requires_inspectable_catalog`
- `test_production_managed_stale_cache_must_be_current_after_native_add`
- `test_production_native_add_restores_only_expected_plugin_config_delta`
- `test_production_native_add_preserves_unexpected_config_drift`
