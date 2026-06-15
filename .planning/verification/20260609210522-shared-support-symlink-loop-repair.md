# Verification: shared support symlink loop repair

## Context

User reported that switching profiles produced:

```text
Error loading rules: failed to read rules files from /Users/cY/.codex/rules: Too many levels of symbolic links (os error 62)
```

Investigation found the shared support sync copied a top-level symlink from the
internal home back into the official home. A source entry such as
`~/.codex-switch/homes/internal/rules -> ~/.codex/rules` became
`~/.codex/rules -> ~/.codex/rules` when syncing back to the official home.
Local scan also found the same pattern already present for `skills`, `prompts`,
`memories`, and `skills.disabled`, so the fix needed to be general rather than
special-casing `rules`.

## Changes Verified

- Shared support sync now refuses to copy source symlinks that point into the
  target home.
- Shared support sync now refuses to propagate source symlinks that point to
  themselves.
- If the target already has a target-home/self-referential symlink for that
  entry, sync removes it instead of preserving the loop.
- Directory copies skip nested symlinks that point to themselves or back into
  the target home.
- Existing concrete target content is preserved when the only source entry is a
  target-home symlink back to that content.
- README and OpenSpec document the symlink-loop prevention contract.

## Validation

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_does_not_create_self_referential_rules_symlink \
  CodexProfileSwitchTests.test_shared_support_sync_removes_target_home_symlink_instead_of_copying_loop \
  CodexProfileSwitchTests.test_shared_support_sync_does_not_propagate_source_self_symlink
```

Result before fix: failed; the rules switch path and generic sync helper both
created or preserved symlink loops.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_uses_managed_home_and_backup_plan \
  CodexProfileSwitchTests.test_official_switch_syncs_shared_state_back_without_internal_runtime \
  CodexProfileSwitchTests.test_official_switch_does_not_create_self_referential_rules_symlink \
  CodexProfileSwitchTests.test_shared_support_sync_removes_target_home_symlink_instead_of_copying_loop \
  CodexProfileSwitchTests.test_shared_support_sync_does_not_propagate_source_self_symlink \
  CodexProfileSwitchTests.test_shared_support_directory_copy_skips_nested_target_home_symlinks \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state
```

Result after fix: 7 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 50 tests OK.

```bash
python3 -m py_compile scripts/codex_switch_home_sync.py scripts/test_codex_profile_switch.py
openspec validate independent-profile-homes --strict --no-interactive
bash -n scripts/codex-switch && bash -n install.sh && git diff --check
```

Results:

- Python compile: passed.
- OpenSpec validation: `Change 'independent-profile-homes' is valid`.
- Shell syntax: passed.
- `git diff --check`: passed.

## Local Runtime Scan

Current local homes were scanned for symlinks that point to themselves or back
inside the same home. The same profile-switch bug had already created
self-referential symlinks at:

- `/Users/cY/.codex/skills`
- `/Users/cY/.codex/prompts`
- `/Users/cY/.codex/memories`
- `/Users/cY/.codex/skills.disabled`

Those runtime artifacts were restored from the pre-corruption switch backup:

```text
/Users/cY/.codex-switch/backups/20260609T124333Z-switch-internal-to-openai-official
```

The cleanup wrote its own manifest:

```text
/Users/cY/.codex-switch/backups/20260609T130847Z-manual-symlink-loop-cleanup/repair.json
```

After cleanup, a scan of `/Users/cY/.codex`,
`/Users/cY/.codex-switch/homes/internal`, and
`/Users/cY/.codex-switch/homes/openai-official` found no exact
self-referential symlinks. The internal home still has expected symlinks back to
the restored official-home support directories.

## Residual Notes

- Archive remains closed by gate; this change was not archived.
