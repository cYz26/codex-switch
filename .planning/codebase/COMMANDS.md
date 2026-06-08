# Commands

## Primary Verification

- `python3 scripts/test_codex_profile_switch.py` - runs the unit/regression suite for profile capture, switching, app CLI binding, doctor checks, and wrapper behavior.
- `bash -n scripts/codex-switch` - validates the public shell wrapper syntax.
- `bash -n scripts/codex_env_setup` - validates the workstation environment helper syntax.
- `bash -n install.sh` - validates installer shell syntax.
- `python3 - <<'PY' ... PY` with `compile(path.read_text(), str(path), "exec")` over `scripts/*.py` - checks Python syntax without writing `__pycache__`.
- `git diff --check` - checks staged or working-tree diff whitespace before commit.

## Packaging

- `scripts/package-release.sh` - rebuilds `dist/codex-switch/` and `dist/codex-switch.tar.gz` from README, SKILL, VERSION, agents, evals, and scripts.

## Runtime Smoke Checks

- `python3 scripts/codex_profile_switch.py --help` - confirms the Python CLI entrypoint imports and argument parsing work.
- `scripts/codex-switch version` - prints the packaged CLI version through the shell wrapper.
- `scripts/codex-switch status` - inspects active profile, shell Codex resolution, and Codex Desktop app CLI binding against the real workstation store.

## DevFlow

- `python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json` - validates DevFlow workflow state.
- `python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json` - checks DevFlow project-local migration drift.
