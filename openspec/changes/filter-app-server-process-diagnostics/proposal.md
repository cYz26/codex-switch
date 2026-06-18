# Filter App Server Process Diagnostics

## Why

`codex-switch status` and `doctor` inspect running processes to warn when Codex Desktop is still using an old app CLI. The current scan matches any `" app-server"` substring in `ps` args, so unrelated helper processes whose JSON/text arguments mention `codex app-server` are misreported and can dump large conversation payloads into CLI output.

## What Changes

- Treat a process as a Codex app-server only when its command line starts with a Codex executable path followed by `app-server` as the invoked subcommand.
- Ignore unrelated process arguments that merely contain `codex app-server` in payload text.

## Impact

- Affects status/doctor diagnostics only.
- No profile store, config, auth, or switching mutation behavior changes.
