# Design: Remote Script Runner

## Target State

`run.sh` is a standalone shell script suitable for direct remote execution. It
resolves the release tarball URL, downloads or copies the bundle into
`$CODEX_SWITCH_LIB_DIR/current` (default:
`~/.local/share/codex-switch/current`), validates that
`scripts/codex-switch` exists and is executable, and then `exec`s that wrapper
with the original command arguments.

## Architecture Decisions

| Decision | Rationale | Alternatives Considered |
|---|---|---|
| Use a stable local implementation directory | The internal Desktop wrapper records the implementation `scripts/` path; a temp extraction directory would break after the remote script exits. | Extract to temp and execute once, which works for simple status commands but breaks Desktop wrapper refreshes. |
| Keep runner separate from installer | Direct execution and persistent PATH installation have different contracts. | Add command mode to `install.sh`, which would make installer behavior harder to reason about. |
| Support `CODEX_SWITCH_TARBALL_URL`, `CODEX_SWITCH_VERSION`, `CODEX_SWITCH_SOURCE_DIR`, and `CODEX_SWITCH_LIB_DIR` | Matches existing install override patterns and makes tests deterministic. | Hard-code latest GitHub release only. |

## Data Flow

1. User pipes `run.sh` from a release URL into `bash -s -- <codex-switch args>`.
2. `run.sh` resolves the tarball URL from `CODEX_SWITCH_TARBALL_URL`, a pinned
   `CODEX_SWITCH_VERSION`, or latest release.
3. The script extracts or copies the source into
   `$CODEX_SWITCH_LIB_DIR/current`.
4. The script executes `current/scripts/codex-switch` with the original args.

## Compatibility

- Existing `install.sh` behavior is unchanged.
- Existing `scripts/codex-switch` command behavior is unchanged.
- `run.sh` intentionally does not create or update `~/.local/bin/codex-switch`.

## Testing

- Add a regression test that creates a fake release tarball with a minimal
  `scripts/codex-switch`, runs `run.sh` with `CODEX_SWITCH_TARBALL_URL`, and
  asserts args are passed through.
- Assert the release is installed into a stable `current` directory.
- Assert the runner does not create the public install symlink.

## Acceptance Criteria

- [x] Remote invocation can execute `status`, `internal`, `official`, and other
      wrapper commands by passing args through.
- [x] Extracted implementation path is stable across the invoked process.
- [x] Release packaging emits `dist/run.sh`.
- [x] Existing tests and syntax checks pass.
