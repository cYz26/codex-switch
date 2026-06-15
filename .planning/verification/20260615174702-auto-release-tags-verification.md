# Verification: automatic release tags and packaging

Date: 2026-06-15

## Scope

Verify the `auto-release-tags` change, which adds automatic patch release
publication for release-relevant `main` pushes while skipping planning,
OpenSpec, verification, and docs-only changes.

## Implementation Summary

- Added `scripts/release_auto.py` with deterministic release planning and
  `VERSION` bumping.
- Added `.github/workflows/auto-release.yml` to run on `main` pushes and manual
  dispatch.
- The automatic workflow verifies release source, bumps `VERSION`, commits the
  bump, creates the next patch tag, pushes `main` and the tag, packages release
  assets, and publishes the release in the same workflow run.
- Kept `.github/workflows/release.yml` for manually pushed `v*` tags and manual
  release reruns.
- Documented automatic release criteria in `README.md`.

## Capability Evidence

GitHub Actions supports push branch/tag filters and manual dispatch. GitHub also
documents that events created with a workflow `GITHUB_TOKEN` do not create new
workflow runs except `workflow_dispatch` and `repository_dispatch`, so this
change publishes release assets in the same workflow run that creates the bot
tag instead of relying on a second tag-triggered workflow.

## Commands And Results

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_auto_release_plan_detects_runtime_change_and_next_patch_tag \
  CodexProfileSwitchTests.test_auto_release_plan_skips_planning_only_changes \
  CodexProfileSwitchTests.test_auto_release_bump_updates_version_for_tag \
  CodexProfileSwitchTests.test_auto_release_workflow_creates_tag_and_release_assets \
  CodexProfileSwitchTests.test_release_workflow_uploads_required_assets
```

Result: `Ran 5 tests`, `OK`.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: `Ran 60 tests in 17.006s`, `OK`.

```bash
python3 -m py_compile scripts/*.py
```

Result: exit 0.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: exit 0.

```bash
python3 -m json.tool evals/evals.json >/dev/null
```

Result: exit 0.

```bash
openspec validate --all --strict --no-interactive
```

Result: `Totals: 5 passed, 0 failed (5 items)`.

```bash
scripts/package-release.sh
```

Result: wrote `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz` and exited
0.

```bash
git diff --check
```

Result: exit 0.

```bash
python3 scripts/release_auto.py plan --json
```

Result: release planning reports `release_required: true`, `latest_tag:
v0.1.3`, `next_tag: v0.1.4`, and `next_version: 0.1.4` for current `main`
content after the latest release tag.

## Remaining Risk

The workflow contract is validated statically and with local planner tests. The
actual GitHub workflow run can only be proven after this branch lands on
`main`. Archive remains closed by gate.
