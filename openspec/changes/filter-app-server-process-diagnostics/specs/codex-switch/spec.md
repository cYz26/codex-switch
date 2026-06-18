## ADDED Requirements

### Requirement: Running app-server diagnostics are bounded to Codex processes

`codex-switch` SHALL report running app-server diagnostics only for actual Codex app-server command invocations, not arbitrary process arguments that contain matching words in payload text.

#### Scenario: Payload text mentions app-server

- GIVEN a non-Codex helper process command line includes JSON or text containing `codex app-server`
- WHEN `codex-switch status` or `codex-switch doctor` scans running processes
- THEN the helper process is ignored as an app-server candidate
- AND its payload text is not printed as a stale app-server path.

#### Scenario: Codex app-server process is running

- GIVEN a command line starts with a Codex executable path followed by `app-server`
- WHEN `codex-switch status` or `codex-switch doctor` scans running processes
- THEN that command line is still reported as a running Codex app-server candidate.
