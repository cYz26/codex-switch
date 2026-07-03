# Internal Profile Document Procedure Check

Date: 2026-07-03

## Question

Confirm whether switching to the `internal` profile follows the Lark document
procedure so that internal mode uses the internal Codex binary and the matching
Azure ModelHub API configuration.

## Document Evidence

Source document:
`https://bytedance.larkoffice.com/docx/OOYBdDO2MoSU7nxb8iLcQAWMnPf`

Fetched revision: `4321`

Relevant document points:

- `CLI 安装`: internal mode must use the script-installed internal Codex CLI.
- `CLI 安装`: the install writes internal Azure provider configuration to
  `~/.codex/config.toml`, with ModelHub base URL
  `https://aidp.bytedance.net/api/modelhub/online`, `wire_api = "responses"`,
  and an AK in query params.
- `Desktop 安装`: Desktop must first have the internal CLI installed, then use
  a LaunchAgent-based `CODEX_CLI_PATH` override to force Desktop onto the
  internal CLI path.
- Referenced Wiki `GfnEwy3u3ixJ9bk0bvxco8msnIb`: writes
  `~/Library/LaunchAgents/com.openai.codex-cli-path.plist` to run
  `/bin/launchctl setenv CODEX_CLI_PATH <absolute codex path>`, then restarts
  Codex Desktop.

## Local Evidence

Current profile state:

- Active profile is `openai-official`, not `internal`.
- Current LaunchAgent `CODEX_CLI_PATH` points to
  `/Applications/Codex.app/Contents/Resources/codex`.
- Current running app-server is
  `/Applications/Codex.app/Contents/Resources/codex app-server
  --analytics-default-enabled`.

Stored internal profile state:

- Internal manifest `codex_bin`:
  `/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex`
- Internal manifest `app_cli_path`:
  `/Users/cY/.codex-switch/bin/codex-internal-app`
- Both internal `codex_bin`, internal app wrapper, and bundled official binary
  report `codex-cli 0.142.5`.
- Internal home config and internal profile config both set:
  - `model = "gpt-5.5-2026-04-24"`
  - `model_provider = "azure"`
  - Azure base URL `https://aidp.bytedance.net/api/modelhub/online`
  - `wire_api = "responses"`
  - `api-version = "2025-04-01-preview"`
  - AK query param present, value not recorded.

Implementation mapping:

- `codex-switch internal` persists the Desktop CLI binding by writing the same
  LaunchAgent `CODEX_CLI_PATH` mechanism described by the document.
- For internal Desktop, `codex-switch` intentionally points the LaunchAgent to
  `codex-internal-app`, not directly to the internal Codex binary. That wrapper
  sets `CODEX_HOME=/Users/cY/.codex-switch/homes/internal`, synchronizes safe
  shared settings, then delegates normal CLI calls to the stored internal
  `codex_bin`; for `app-server`, it starts the internal app-server through the
  compatibility proxy.

## Conclusion

The stored `internal` profile follows the document's required contract, with an
extra codex-switch wrapper layer for Desktop compatibility and profile-home
isolation. The current live machine is intentionally back on `openai-official`,
so live Desktop is not currently using the internal binding.

The observed Azure resource mismatch is therefore not caused by missing the
document's local setup steps. It occurs after the internal binary and Azure
provider are selected, during Responses tool-result follow-up routing inside
AIDP/internal backend.

## Validation Commands

```bash
python3 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json
lark-cli docs +fetch --doc "https://bytedance.larkoffice.com/docx/OOYBdDO2MoSU7nxb8iLcQAWMnPf" --scope outline --max-depth 4 --detail with-ids --format json
lark-cli docs +fetch --doc "https://bytedance.larkoffice.com/docx/OOYBdDO2MoSU7nxb8iLcQAWMnPf" --scope section --start-block-id PTnEdueAio34bRxAEKYcqVUpnpe --doc-format markdown --format json
lark-cli docs +fetch --doc "https://bytedance.larkoffice.com/docx/OOYBdDO2MoSU7nxb8iLcQAWMnPf" --scope section --start-block-id YgncdqG1modanExlPfVcDyL3nUy --doc-format markdown --format json
lark-cli docs +fetch --doc "GfnEwy3u3ixJ9bk0bvxco8msnIb" --doc-format markdown --format json
codex-switch --skip-self-update status
```
