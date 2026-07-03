# Internal Bin Rollback 0.142.4 Smoke

Date: 2026-07-03

## Request

Try switching `internal` to the previous internal Codex release because the
latest internal Codex binary may be causing the Azure Responses resource
mismatch.

## Release Evidence

GitHub `SDGLBL/codex` releases show:

- Latest internal release: `internal-rust-v0.142.5`
- Previous internal release: `internal-rust-v0.142.4`

Local update check before rollback:

```text
Current: codex-cli 0.142.5
Latest release tag: internal-rust-v0.142.5
Update: not needed
```

## Local Change

`/Users/cY/.local/bin/codex` was already present and reported:

```text
codex-cli 0.142.4
```

The internal profile was rebound with:

```bash
codex-switch --skip-self-update set-bin --preserve-app-cli internal /Users/cY/.local/bin/codex
codex-switch --skip-self-update internal --skip-update-check --skip-doctor --no-status
```

`--preserve-app-cli` kept the Desktop wrapper:

```text
app_cli_path=/Users/cY/.codex-switch/bin/codex-internal-app
```

The generated shell shim and Desktop wrapper now delegate to:

```text
/Users/cY/.local/bin/codex
```

## Verification

Working-tree verifier command:

```bash
./scripts/codex-switch --skip-self-update verify internal --app-server-smoke --responses-tool-smoke --report
```

Result:

```text
App-server smoke: passed
Responses tool smoke: passed
Verification report: /Users/cY/.codex-switch/verification/20260703T125615Z-internal.json
```

The report has no smoke diagnostics and only contains running Desktop process
mismatches:

```text
running Codex Desktop pid 18518 has CODEX_CLI_PATH=/Applications/Codex.app/Contents/Resources/codex, but active profile internal expects /Users/cY/.codex-switch/bin/codex-internal-app
running Codex app-server pid 18860 uses /Applications/Codex.app/Contents/Resources/codex, but active profile internal expects /Users/cY/.codex-switch/bin/codex-internal-app
```

Installed `codex-switch` was refreshed from the working tree afterward:

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
```

Installed `verify --help` now includes `--app-server-smoke` and
`--responses-tool-smoke`.

## Current State

`codex-switch --skip-self-update status` reports:

- Active profile: `internal`
- Active configured CLI: `/Users/cY/.local/bin/codex`
- Shim codex version: `codex-cli 0.142.4`
- Active configured App CLI: `/Users/cY/.codex-switch/bin/codex-internal-app`
- LaunchAgent `CODEX_CLI_PATH`:
  `/Users/cY/.codex-switch/bin/codex-internal-app`
- Running Desktop/app-server still use the official bundle until Desktop is
  fully quit and reopened.

The current process `PATH` still resolves `codex` first from
`/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex`, which
is `codex-cli 0.142.5`. The profile manifest, switch shim, and Desktop wrapper
now point to 0.142.4; this PATH ordering should be treated as a separate shell
environment detail if CLI invocations from the current terminal matter.

## Conclusion

The rollback experiment is positive at the profile-command level: with
`codex-cli 0.142.4`, both app-server startup smoke and Responses tool-follow-up
smoke pass. The remaining validation blocker is not the model call; it is that
the currently running Codex Desktop process must be completely quit and
reopened to inherit the internal wrapper.
