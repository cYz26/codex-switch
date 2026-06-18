# Design

## Target State

`running_codex_processes()` reports only actual Codex app-server processes. A textual mention of `codex app-server` inside another process argument is ignored, preventing status/doctor output from leaking long JSON payloads.

## Approach

Tighten `app_server_command_path()` from substring splitting to a regex anchored at the start of the `ps` args line. The accepted command path must end in a Codex-like executable basename (`codex` or `codex-*`) and be immediately followed by `app-server` as the next token.

## Non-goals

- Do not change Desktop wrapper launch behavior.
- Do not suppress legitimate stale app-server warnings.
