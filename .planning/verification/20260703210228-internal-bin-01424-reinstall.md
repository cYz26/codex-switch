# Internal Bin 0.142.4 Reinstall

Date: 2026-07-03

## Request

Re-run the internal Codex binary download/install flow for the previous
internal release instead of reusing the existing local 0.142.4 binary.

## Preflight

DevFlow plugin-project migration was checked in sync-only mode. It still
reports `migration_pending` for official skill-layout migration conflicts and
legacy duplicates, but runtime/stored DevFlow versions match and no migration
apply was run.

The internal install AK was present in the environment; its value was not
printed or recorded.

Dry-run command:

```bash
codex-switch --skip-self-update update-internal --version 0.142.4 --install-dir /Users/cY/.local/bin --dry-run
```

Dry-run confirmed:

- installer: `https://github.com/SDGLBL/codex/releases/latest/download/install.sh`
- install dir: `/Users/cY/.local/bin`
- model: `gpt-5.5-2026-04-24`
- Azure base URL: `https://aidp.bytedance.net/api/modelhub/online`
- pinned version: `0.142.4`

Backup created before reinstall:

```text
/Users/cY/.codex-switch/backups/20260703T210044-pre-reinstall-internal-0.142.4
```

Preinstall binary:

```text
codex-cli 0.142.4
before_sha256=8bdbbf4b1a3b391425fcda4e86537805e51ddea97d896a563eaa1494c4eef6f1
```

## Reinstall

Command:

```bash
codex-switch --skip-self-update update-internal --version 0.142.4 --install-dir /Users/cY/.local/bin
```

Installer output confirmed:

```text
Resolved version: 0.142.4
Downloading Codex CLI
Downloading bundled rg
Installing to /Users/cY/.local/bin
Configured config.toml. Run `codex` to use the internal Azure provider.
Codex CLI 0.142.4 installed successfully.
Internal Codex after update: codex-cli 0.142.4
```

Postinstall binary:

```text
codex-cli 0.142.4
after_sha256=8bdbbf4b1a3b391425fcda4e86537805e51ddea97d896a563eaa1494c4eef6f1
```

The matching hash means the previously present local 0.142.4 binary was not
corrupt; nevertheless the download/install flow was fully re-run.

## Rebind and Activation

Commands:

```bash
codex-switch --skip-self-update set-bin --preserve-app-cli internal /Users/cY/.local/bin/codex
codex-switch --skip-self-update internal --skip-update-check --skip-verify --skip-doctor --no-status
```

Current internal profile binding:

```text
codex_bin=/Users/cY/.local/bin/codex
app_cli_path=/Users/cY/.codex-switch/bin/codex-internal-app
codex_home=/Users/cY/.codex-switch/homes/internal
```

Generated wrappers:

```text
/Users/cY/.codex-switch/bin/codex -> /Users/cY/.local/bin/codex
/Users/cY/.codex-switch/bin/codex-internal-app CODEX_BIN=/Users/cY/.local/bin/codex
```

Current live/internal configs all use:

```text
model=gpt-5.5-2026-04-24
provider=azure
base=https://aidp.bytedance.net/api/modelhub/online
wire=responses
ak_present=True
```

## Verification

Command:

```bash
codex-switch --skip-self-update verify internal --app-server-smoke --responses-tool-smoke --report
```

Result:

```text
App-server smoke: passed
Responses tool smoke: passed
Verification report: /Users/cY/.codex-switch/verification/20260703T130213Z-internal.json
```

The report still has `ok=false` only because the already-running Desktop
process and app-server are still using the official app bundle:

```text
/Applications/Codex.app/Contents/Resources/codex
```

They must be fully quit and reopened to inherit:

```text
CODEX_CLI_PATH=/Users/cY/.codex-switch/bin/codex-internal-app
```

## Remaining Caveat

The current shell `PATH` still resolves bare `codex` first from:

```text
/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex
```

That binary reports `codex-cli 0.142.5`. The active profile manifest, switch
shim, and Desktop wrapper now point to the reinstalled 0.142.4 binary, but
bare `codex` in the current terminal remains affected by PATH ordering.
