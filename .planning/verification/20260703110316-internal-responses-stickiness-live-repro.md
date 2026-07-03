# Internal Responses Resource Stickiness Live Repro

Date: 2026-07-03

OpenSpec changes: `internal-responses-resource-stickiness`,
`internal-app-protocol-compat`

## User Report

After switching to `internal`, Codex Desktop still showed:

```text
The requested item was created under a different Azure OpenAI resource. Use the same resource that created the item to access it.
```

## Findings

- The installed `codex-switch` initially came from the GitHub latest release
  path because `./install.sh` was run without `CODEX_SWITCH_SOURCE_DIR`.
  That installed bundle did not include the current working-tree
  `--responses-tool-smoke` verifier.
- On the 2026-07-03 20:00 CST recheck, installed
  `codex-switch --skip-self-update verify internal --responses-tool-smoke
  --report` failed before verification with `unrecognized arguments:
  --responses-tool-smoke`, confirming the installed bundle had drifted behind
  the working tree again.
- Running the working-tree wrapper directly reproduced the backend failure and
  wrote `/Users/cY/.codex-switch/verification/20260703T115956Z-internal.json`.
- The current working tree was installed explicitly with:

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
```

- After that, installed help showed:

```text
--responses-tool-smoke
--app-server-smoke
```

- The installed command was then re-run successfully and wrote
  `/Users/cY/.codex-switch/verification/20260703T120052Z-internal.json`.
- `codex-switch --skip-self-update status` showed the active profile had
  returned to `openai-official`, so internal verification also reported
  active-profile mismatch.
- The internal Responses smoke still reproduced and classified the backend
  failure as:

```text
internal Responses resource-stickiness failure; Responses context follow-up must stay on the same Azure OpenAI resource
```

## Commands

```bash
python3 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json
codex-switch --skip-self-update status
./scripts/codex-switch --skip-self-update verify internal --responses-tool-smoke --report
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
codex-switch --skip-self-update verify --help
codex-switch --skip-self-update verify internal --responses-tool-smoke --report
```

## Evidence

Verification reports:

```text
/Users/cY/.codex-switch/verification/20260703T110316Z-internal.json
/Users/cY/.codex-switch/verification/20260703T115956Z-internal.json
/Users/cY/.codex-switch/verification/20260703T120052Z-internal.json
```

Problems from latest installed-command report:

```text
active profile is openai-official, expected internal
internal: active CODEX_HOME is /Users/cY/.codex, expected /Users/cY/.codex-switch/homes/internal
internal: active shell CLI is /Applications/Codex.app/Contents/Resources/codex, expected /Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex
internal: internal Responses resource-stickiness failure; Responses context follow-up must stay on the same Azure OpenAI resource
```

Smoke diagnostics:

```json
{
  "kind": "azure_responses_resource_mismatch",
  "message": "Responses context follow-up must stay on the same Azure OpenAI resource",
  "accounts": [],
  "deployments": [],
  "model_request_ids": [],
  "tt_log_ids": []
}
```

## Conclusion

The visible Desktop error is not the previous plugin/list app-server crash and
not the Settings/Plugins/Skills sync issue. It is the internal backend/AIDP
Responses context resource-stickiness failure already modeled by
`internal-responses-resource-stickiness`.

Local repair completed in this session: the installed `codex-switch` now points
at the current working-tree implementation so the verifier and switch flags are
available locally.

Remaining repair owner: AIDP/internal backend routing must keep a Responses
context and its tool-result follow-up on the same Azure OpenAI resource, or
provide a sticky routing key supported by Codex Desktop/internal backend.

## Workflow State

DevFlow plugin-project migration sync-only still reports `migration_pending`
because of legacy `.codex/skills` duplicates/conflicts with `.agents/skills`.
No migration apply was run.
