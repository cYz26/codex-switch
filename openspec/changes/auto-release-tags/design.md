# Design: Automatic release tags and packaging

## Release Planner

Add `scripts/release_auto.py` as a small Python helper with two subcommands:

- `plan`: inspect the latest semantic `vX.Y.Z` tag, list changed files from
  that tag to `HEAD`, classify release-relevant files, and report the next
  patch tag.
- `bump --tag vX.Y.Z`: update `VERSION` to `X.Y.Z`.

The planner is intentionally local and deterministic so both tests and GitHub
Actions use the same release decision. It treats the following as
release-relevant:

- `install.sh`, `run.sh`, `SKILL.md`
- `.github/workflows/release.yml` and `.github/workflows/auto-release.yml`
- non-test files under `scripts/`
- files under `agents/`

It skips `.planning/**`, `openspec/**`, `README.md`, `.gitignore`, `VERSION`,
and `scripts/test_*.py` when those are the only changed files.

## GitHub Actions Flow

Add `.github/workflows/auto-release.yml` with:

- `on.push.branches: ["main"]` and `workflow_dispatch`
- `permissions.contents: write`
- `actions/checkout` with `fetch-depth: 0`
- planner step that writes `release_required`, `latest_tag`, and `next_tag` to
  `GITHUB_OUTPUT`
- verification and packaging steps that run only when release is required
- `VERSION` bump commit, `vX.Y.Z` tag creation, and push to `main` plus the tag
- release creation/upload in the same workflow run

The workflow publishes assets itself because GitHub's `GITHUB_TOKEN` event
recursion guard means a tag pushed by the workflow should not be relied on to
start the existing tag release workflow.

The existing `.github/workflows/release.yml` stays in place for human-pushed
tags and manual reruns.

## Verification

Regression tests cover:

- runtime/script changes after the latest tag require a release and propose the
  next patch tag
- planning-only changes after the latest tag do not require a release
- `bump --tag` writes the expected `VERSION`
- the auto-release workflow contains branch trigger, write permission, planner,
  version bump, tag push, packaging, and release upload steps

Full verification uses:

```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
python3 -m json.tool evals/evals.json >/dev/null
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```
