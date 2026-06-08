# Design: Isolate Desktop Session State

## Target State

The internal Desktop app home remains a profile-specific `CODEX_HOME` that
receives a generated `config.toml` and no `auth.json`. Stable support assets
such as plugins, skills, caches, model catalogs, memories, prompts, rules, and
vendor imports can still be linked from the live home. Runtime conversation and
request state is owned by the profile app home and is not symlinked from the
live home.

## Architecture Decisions

| Decision | Rationale | Alternatives Considered |
|---|---|---|
| Exclude known runtime state by basename/pattern in the wrapper | Keeps the existing simple shell wrapper model and avoids touching live data. | Whitelist every shared directory, which is safer long-term but risks breaking currently shared support assets. |
| Remove only symlinks that point back into live `CODEX_HOME` | Cleans stale generated state without deleting real app-home files. | Unconditionally remove paths, which could delete profile-local sessions. |
| Keep config overlay logic unchanged | The reported failure is runtime history sharing, not config merge behavior. | Rework config layering, out of scope for this repair. |

## Data Flow

1. `codex-switch internal` refreshes the managed internal Desktop wrapper.
2. On app launch, the wrapper creates the profile app home.
3. The wrapper removes stale symlinks for excluded runtime names when those
   symlinks target live `CODEX_HOME`.
4. The wrapper links allowed stable live-home entries that do not already exist.
5. The Python config overlay folds shared app-home config changes back into the
   live shared config and writes the generated profile app config.
6. Codex starts with `CODEX_HOME` set to the profile app home.

## Runtime State Exclusion Contract

The wrapper must not share these live-home entries with the profile app home:

- `sessions`
- `session_index.jsonl`
- `history.jsonl`
- `archived_sessions`
- `log`
- `tmp`
- `.tmp`
- `process_manager`
- `node_repl`
- `shell_snapshots`
- `browser`
- `ambient-suggestions`
- `*.sqlite`
- `*.sqlite-shm`
- `*.sqlite-wal`
- `*.sqlite.corrupt.*`

## Compatibility

No live data is deleted. Existing generated symlinks are removed only from the
profile app home and only when they target the live `CODEX_HOME`. If Codex needs
one of the excluded directories, it can recreate a profile-local version under
the app home.

## Testing

- Add a regression test in `scripts/test_codex_profile_switch.py` that creates
  live runtime files and stale app-home symlinks, launches the refreshed wrapper,
  and asserts excluded state is not linked.
- Run the full Python regression suite plus syntax checks.

## Acceptance Criteria

- [x] Internal wrapper removes stale `sessions` and sqlite live symlinks.
- [x] Internal wrapper does not create new symlinks for excluded runtime state.
- [x] Internal wrapper still starts the configured profile Codex binary.
- [x] Shared config and stable asset behavior remains covered by existing tests.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
git diff --check
```
