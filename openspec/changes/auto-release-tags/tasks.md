# Tasks: Automatic release tags and packaging

## Target State

Release-relevant changes merged to `main` automatically produce a verified
patch release. Planning/spec/docs-only changes do not publish. Existing manual
tag release publishing remains available.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [ ] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Release planner tests

**Status:** done

**Goal**
- Lock release detection, skip detection, version bumping, and workflow
  contract before production changes.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`
- `scripts/release_auto.py`
- `.github/workflows/auto-release.yml`

**Implementation**
- [x] Add failing tests for runtime changes requiring release.
- [x] Add failing tests for planning-only changes skipping release.
- [x] Add failing tests for `VERSION` bumping.
- [x] Add failing workflow contract test for automatic release.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_auto_release_plan_detects_runtime_change_and_next_patch_tag \
  CodexProfileSwitchTests.test_auto_release_plan_skips_planning_only_changes \
  CodexProfileSwitchTests.test_auto_release_bump_updates_version_for_tag \
  CodexProfileSwitchTests.test_auto_release_workflow_creates_tag_and_release_assets
```

### Slice 2: Planner implementation

**Status:** done

**Goal**
- Provide a deterministic local helper shared by tests and GitHub Actions.

**Files / Modules**
- `scripts/release_auto.py`

**Implementation**
- [x] Implement semantic tag parsing.
- [x] Implement changed-file detection from latest tag to `HEAD`.
- [x] Implement release-relevant file classification.
- [x] Implement JSON and GitHub-output plan rendering.
- [x] Implement `VERSION` bumping from a `vX.Y.Z` tag.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_auto_release_plan_detects_runtime_change_and_next_patch_tag \
  CodexProfileSwitchTests.test_auto_release_plan_skips_planning_only_changes \
  CodexProfileSwitchTests.test_auto_release_bump_updates_version_for_tag
```

### Slice 3: Automatic release workflow

**Status:** done

**Goal**
- Run release planning on `main` pushes and publish patch releases when needed.

**Files / Modules**
- `.github/workflows/auto-release.yml`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add `main` push and manual dispatch triggers.
- [x] Run planner with full git history.
- [x] Run release-equivalent verification when a release is required.
- [x] Bump `VERSION`, commit, tag, and push.
- [x] Package and publish release assets in the same workflow run.
- [x] Keep existing tag workflow unchanged for manual tag publishing.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_auto_release_workflow_creates_tag_and_release_assets \
  CodexProfileSwitchTests.test_release_workflow_uploads_required_assets
```

### Slice 4: Docs, state, and final verification

**Status:** done

**Goal**
- Document automatic publishing and record verification evidence.

**Files / Modules**
- `README.md`
- `.planning/STATE.md`
- `.planning/verification/`
- `openspec/changes/auto-release-tags/tasks.md`

**Implementation**
- [x] Document automatic release criteria and skip behavior.
- [x] Record verification evidence.
- [x] Update workflow state.
- [x] Mark completed task slices only after validation.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
python3 -m json.tool evals/evals.json >/dev/null
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

## Acceptance Criteria

- [x] Runtime/script changes after the latest tag require a release.
- [x] Planning/spec/docs-only changes do not require a release.
- [x] Automatic releases use the next patch version.
- [x] Automatic releases do not require a PAT or secret beyond `GITHUB_TOKEN`.
- [x] Assets are published from the same workflow run that creates the tag.
- [x] Existing `v*` tag release workflow remains available.
