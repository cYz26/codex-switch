# Conventions

- Keep production code in `scripts/` dependency-light and compatible with the system Python used by macOS.
- Prefer small modules named `codex_switch_<area>.py`; route user-facing commands through `scripts/codex_profile_switch.py` or `scripts/codex-switch`.
- Use `SwitchError` for expected CLI failures and return user-readable messages rather than raw tracebacks.
- Use atomic writes and private file modes for profile store, live Codex config, auth, shim, LaunchAgent, and wrapper writes.
- Preserve existing profile store compatibility unless an OpenSpec change explicitly approves migration behavior.
- Treat `config.toml` as shared workstation config and `<profile>.config.toml` as the profile-specific auth/model layer.
- Keep `auth.json` handling explicit; do not copy official file auth into isolated internal app homes.
- Add or update `scripts/test_codex_profile_switch.py` tests before risky behavior changes.
- Keep shell wrapper and installer changes covered by `bash -n`.
- Do not hand-edit generated release output under `dist/`; update source files and rerun `scripts/package-release.sh`.
