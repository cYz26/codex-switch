# Risks

- Profile switching rewrites live Codex workstation files; regressions can affect both CLI and Codex Desktop startup.
- Auth boundaries are sensitive: official `auth.json` must not leak into internal app homes, while file-auth profiles must still restore auth correctly.
- `config.toml` merging needs to preserve non-auth shared state such as plugins, marketplaces, hooks, MCP servers, projects, UI preferences, and feature flags while stripping profile-specific model/provider keys from the shared base.
- LaunchAgent and app-wrapper changes are macOS-specific and can be hard to validate in isolated tests.
- Shell wrapper behavior depends on environment variables such as `CODEX_SWITCH_HOME`, `CODEX_SWITCH_SCRIPT`, `CODEX_SWITCH_PYTHON`, and `CODEX_CLI_PATH`.
- Release packaging can accidentally include stale generated files if source changes are not followed by `scripts/package-release.sh`.
- Existing tests are broad for profile flows, but they use fake Codex binaries and do not fully exercise a real Codex Desktop process.
