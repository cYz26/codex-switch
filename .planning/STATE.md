---
workflow_version: 0.3.0
project_mode: brownfield
current_stage: verified

current_phase:
  id: 01-foundation
  status: planning

current_change:
  id: always-check-self-update
  status: verified

gates:
  workflow_initialized: true
  spec_approved: true
  plan_written: true
  tests_baseline_known: true
  implementation_done: true
  verification_passed: true
  state_updated: true
  archive_allowed: false

context_management:
  compact_policy: checkpoint_boundary
  last_checkpoint_id: 2026-06-08-change_archived-local-command-self-update
  last_checkpoint_file: .planning/checkpoints/2026-06-08-change_archived-local-command-self-update.md
  compact_recommended: false
  compact_status: not_needed
  last_compact_result_file: none
  compact_source: checkpoint
  compact_updated_at: 2026-06-08T12:58:56+08:00
  compact_skip_reason: none
  compact_error: none
  compact_after:
    - project_setup_completed
    - codebase_mapping_completed
    - design_saved
    - openspec_change_planned
    - phase_plan_saved
    - verification_passed
    - change_archived
    - phase_shipped
  skip_compact_for:
    - small_task_update
    - typo_fix
    - docs_only_micro_change
  require_before_compact:
    - state_updated
    - durable_context_written
    - next_action_recorded
    - risks_recorded
    - validation_recorded_if_applicable

goal_gate:
  required: false
  status: not_required
  reason: none
  suggested_goal: none

context_health:
  last_report: .planning/context-health/reports/20260629130742-context-health.json
  last_risk: medium
  last_confidence: medium
  last_decision: reconcile
  last_goal_status: aligned
  goal_summary: Official/internal independent home switching regression repaired and hardened. Doctor now accepts the managed internal Desktop app-server proxy chain, stale unavailable enabled plugin selectors have an explicit disable cleanup path, unavailable browser-use/local-personal dev-flow selectors were disabled in local config, pdf primary-runtime cache was refreshed, the generated local bundle was installed, internal Desktop config writes now preserve existing shared settings, current workstation configs were restored from the latest valid switch backup, the official unannotated runtime seed contamination regression is repaired broadly, source-profile plugin support snapshots now act as shared fallback after runtime narrowing, one-key switches now run target-profile verification before doctor, standalone verify supports safe repair, reports, and explicit runtime smoke, bidirectional shared settings shrink prevention is verified, and profile switches now preserve target-only Desktop/apps/memories/plugin/skill settings when the source runtime is narrowed.
---

# Workflow State

## Current Status

On 2026-06-29, the internal Desktop config-write regression was repaired.
Codex Desktop/app-server `config/value/write` and `config/batchWrite` calls are
now guarded in the internal app proxy by snapshotting the managed runtime
config before the write and restoring missing unrelated shared defaults after a
successful response, without overwriting the newly written Desktop value or
copying profile-specific model/provider settings from the snapshot. Regression
coverage was added for missing shared default restoration plus both app-server
config write methods.

The real workstation config was restored from
`/Users/cY/.codex-switch/backups/20260629T040238Z-switch-openai-official-to-internal/3-config.toml`
using the same merge helper. Pre-repair copies were saved in
`/Users/cY/.codex-switch/backups/20260629T043729Z-pre-config-preservation-repair/`.
Both `/Users/cY/.codex/config.toml` and
`/Users/cY/.codex-switch/homes/internal/config.toml` now validate as TOML and
again contain Desktop appearance settings, memories, restored enabled plugin
entries for `agent-kb@cy-codex-skills` and
`lark-feishu-ops@cy-codex-skills`, and the other missing shared support blocks
from the valid switch backup. The local release bundle was regenerated and
installed to `/Users/cY/.local/share/codex-switch/current`, and
`/Users/cY/.codex-switch/bin/codex-internal-app` now points `SWITCH_SCRIPTS` at
that installed bundle. The already-running Desktop app-server process must be
restarted by Codex Desktop before it loads the repaired proxy code.

On 2026-06-30, the official unannotated runtime seed contamination regression
was repaired. A real `codex-switch official` attempt had written
internal/Azure model-provider settings into the official profile layer and
canonical profile config even though the pre-switch official profile layer had
clean official `gpt-5.5` settings. The repair adds regression coverage for an
unannotated official runtime config that matches the internal source home,
skips that runtime seed when a clean explicit official profile layer exists,
and compares profile seeds after removing codex-switch managed comments. The
local bundle was rebuilt and installed, polluted official layer files were
backed up under
`/Users/cY/.codex-switch/backups/20260630111802-pre-official-layer-repair/`,
the clean layer was restored from
`20260630T025400Z-switch-internal-to-openai-official`, a real official switch
was verified to generate official `gpt-5.5` config without internal Azure
provider settings, and the workstation was switched back to `internal`.

On 2026-06-30, the repeated plugin/config loss after official-to-internal
switching was repaired more systemically. The root failure path was that
plugin support blocks were treated as shared config, while the canonical
profile config intentionally excluded them; if the current source home was
narrowed by another profile or Desktop write, switching back to `internal`
could use the old internal runtime only as the model/profile seed and discard
the runtime's marketplace/plugin/skill/hook blocks. The repair adds
profile-local plugin support snapshots named
`<profile>.plugin-support.config.toml`, merges previous runtime/snapshot
plugin support blocks as missing defaults when the source home lacks them, and
refreshes those snapshots from every generated runtime config, including the
managed internal Desktop wrapper path. The canonical profile config remains
profile-specific. Regression coverage was added for recovery from the target
runtime and from the profile-local snapshot after runtime loss, stale plugin
cleanup now updates snapshot files, and Desktop wrapper tests verify snapshot
refresh. Full profile-switch tests passed (90 tests), OpenSpec validated, the
local bundle was packaged and installed, and a real workstation
official-to-internal switch cycle ended active on `internal` with plugin repair
reporting no missing enabled plugins and doctor passing. The running Desktop
app-server process should still be restarted to load the updated proxy code.

After a Desktop restart on 2026-06-30, another gap was confirmed: the new
plugin-support snapshot mechanism prevented future loss only when at least one
current target runtime/snapshot still had the shared plugin blocks. The real
workstation's current official/internal runtime configs and snapshots had
already been narrowed, so the missing historical shared config was not
recovered. The official profile layer was also polluted again because the
previous official seed guard only skipped an unannotated provider runtime when
its profile seed exactly matched the internal source home; the real config was
similar but not identical. The repair now skips any unannotated
`openai-official` runtime seed containing `model_provider` when a clean
explicit official profile layer with `model` and no provider exists, and it
uses the source profile's `<profile>.plugin-support.config.toml` as shared
fallback defaults when switching profiles. Post-restart regressions were added
and verified. Current workstation configs were backed up under
`/Users/cY/.codex-switch/backups/20260630152911-pre-post-restart-shared-config-repair/`,
then restored from rich backup
`20260630T062435Z-switch-openai-official-to-internal/3-config.toml` and clean
official layers from
`20260630T065702Z-switch-internal-to-openai-official`. A real
`official -> internal` switch cycle passed. Final state: official runtime
`/Users/cY/.codex/config.toml` is `gpt-5.5` without `model_provider`;
internal runtime is Azure; both runtime/snapshot sets contain 5 marketplaces,
24 plugin blocks, and 43 hook trust blocks including agent-kb, lark-feishu-ops,
pdf, and game-design-workshop; `codex-switch --skip-self-update doctor`
passes.

Change `independent-profile-homes` has an additional verified repair for the
official/internal switch regression reported on 2026-06-24. The repair prevents
`openai-official` from using a contaminated managed runtime config as its
profile seed when a clean explicit `openai-official.config.toml` layer exists,
merges legacy profile-layer plugin support blocks into generated independent
home configs, refreshes target-home profile layers from validated runtime
configs, and adds active-profile plugin materialization checks plus
`repair-plugins <profile>` remediation. One-key `codex-switch internal` and
`codex-switch official` now run plugin repair after a successful switch and
before doctor; `--skip-plugin-repair` skips that repair step. Plugin
directories and caches remain profile-local; repair refreshes target-profile
plugin marketplace/catalog state, primes the available plugin catalog, and
installs missing enabled plugins through the target profile's configured Codex
binary only when those plugins appear in the refreshed available catalog.
Unavailable enabled plugins are skipped by repair and left for doctor to report
as active-profile materialization issues. One-key `internal --help` and
`official --help` now print help without running self-update, switch, plugin
repair, doctor, or status steps.

The repair was hardened again on 2026-06-24. `codex-switch doctor` and
`codex-switch status` now recognize the valid managed internal Desktop chain
where Codex Desktop starts `codex-internal-app`, that wrapper starts
`codex_switch_app_proxy.py`, and the proxy starts the configured internal
`codex_bin` child app-server. `repair-plugins <profile>` also has an explicit
`--disable-unavailable` cleanup path that disables missing enabled plugin
selectors only after a real catalog refresh proves they are unavailable. This
keeps normal doctor checks read-only, keeps default repair behavior
catalog-aware, and gives stale config a durable cleanup path.

The real workstation was repaired and remains active on `internal`: active
`CODEX_HOME` is `/Users/cY/.codex-switch/homes/internal`, LaunchAgent and GUI
`CODEX_CLI_PATH` point to `/Users/cY/.codex-switch/bin/codex-internal-app`,
installed `codex-switch --skip-self-update doctor` passes, and status reports
the running app-server as `/Users/cY/.local/bin/codex (via app proxy pid
29858)`. The stale unavailable `browser-use@openai-bundled` and
`dev-flow@local-personal-plugins` selectors were disabled in the live shared
config, managed internal runtime config, and internal profile layer; the
enabled `dev-flow@cy-codex-skills` cache remains present.
`pdf@openai-primary-runtime` was refreshed to `26.623.12021` and now matches
source in the updater cache verification. The source checkout passes
verification, and
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`; that
generated local bundle was explicitly installed to
`/Users/cY/.local/share/codex-switch/current`.

On 2026-06-30, the switch verification contract was implemented as change
`switch-verification-contract`. `codex-switch verify <profile>` now validates
target active state, runtime config, official provider contamination, Desktop
binding/process observations in the managed default context, plugin support
snapshots, optional runtime smoke, explicit exec smoke, and optional JSON
reports. `--repair=safe` refreshes profile-local plugin support snapshots and
uses the existing catalog-aware plugin repair path only when enabled plugins
are actually missing. One-key `codex-switch internal` and
`codex-switch official` now run a Verification section after plugin repair and
before doctor; `--skip-verify`, `--runtime-smoke`, `--exec-smoke <prompt>`,
and `--verification-report` control diagnostic and post-upgrade depth. The
full profile-switch test file passed 97 tests, OpenSpec validation passed 10
items, the release bundle was packaged and installed locally, installed
`codex-switch --skip-self-update verify internal --repair=safe --report`
passed, installed `codex-switch --skip-self-update verify internal
--repair=safe --runtime-smoke --report` passed, and installed
`codex-switch --skip-self-update doctor` passed.

Archive remains unavailable because the archive gate is closed.

On 2026-07-03, `independent-profile-homes` was extended with bidirectional
shared settings shrink prevention after switching `internal` on pinned
`0.142.4` and then back to `official` exposed missing Codex Desktop settings,
Plugins, and Skills configuration. The root cause was not the Settings UI:
wrapper startup and switch-time shared TOML generation treated a narrower
source profile config as an authoritative whole-table overlay. In practice,
`[desktop]` from the internal app home could replace the richer official
`[desktop]` table with only `followUpQueueMode`, and official switch
generation could rebuild official from a narrowed internal source while only
restoring plugin-support blocks from target runtime/snapshots. A third gap was
that plugin-support snapshot refresh could overwrite an existing rich
plugin/skill snapshot with an empty runtime-derived snapshot.

The repair changes shared TOML table overlay semantics to assignment-level
overlay: present source keys can update target keys, but missing source keys do
not delete target-only settings. Switch-time runtime config generation now
uses the target profile's last valid runtime config as full shared missing
defaults, not only marketplace/plugin/skill/hook defaults. Plugin-support
snapshot refresh now unions runtime-derived support with existing snapshots as
missing defaults, so runtime narrowing does not shrink richer snapshots without
an explicit deletion mechanism. OpenSpec scenarios and the task ledger were
updated under `independent-profile-homes`; verification evidence is recorded in
`.planning/verification/20260703215156-bidirectional-shared-settings-shrink-prevention.md`.

Verification for this repair: focused regressions failed before implementation
and passed after the fix; adjacent wrapper/plugin/official contamination
regressions passed, 14 tests; full
`python3 scripts/test_codex_profile_switch.py` passed, 120 tests;
`python3 -m py_compile scripts/*.py`, shell syntax checks,
`openspec validate independent-profile-homes --strict --no-interactive`,
`openspec validate --all --strict --no-interactive`, `git diff --check`, and
`scripts/package-release.sh` all passed. The local installed bundle was
refreshed with
`CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh`, and
installed `codex-switch --skip-self-update status` passed. That status check
also reported the pre-existing current-shell `PATH codex` mismatch and
recommended `eval "$(codex-switch shim-env)"` to align this shell.

On 2026-07-03, a new internal Azure Responses failure was diagnosed after an
internal-profile backend update surfaced the service message `The requested
item was created under a different Azure OpenAI resource. Use the same
resource that created the item to access it.` Fresh internal threads also
failed, so the symptom is not stale conversation state. A local plain-text
internal `codex exec --json` smoke succeeded, while a smoke that forced a shell
tool call and tool-result follow-up reproduced the error. Client tracing showed
the initial `/responses` request succeeded on
`x-account-id: globalttswedencentral010`, while the follow-up failed after
being routed to `x-account-id: globalttswedencentral053` for the same returned
deployment. The detailed sanitized evidence is recorded in
`.planning/verification/20260703112226-internal-azure-resource-stickiness-diagnosis.md`.

Current diagnosis: AIDP is not keeping a Responses context sticky to one Azure
OpenAI resource across tool-result follow-up requests. codex-switch does not
currently proxy model HTTP `/responses` traffic, so the durable upstream fix is
AIDP/backend resource stickiness or a supported sticky routing mechanism. The
local codex-switch gap is verification: `--runtime-smoke` does not exercise a
Responses tool-follow-up path, and `--exec-smoke` only catches the problem when
the caller supplies a tool-forcing prompt.

DevFlow project migration sync was re-run on 2026-07-03 before this repair.
The sync completed successfully and still reports `migration_pending` for the
official skill-layout migration, with legacy duplicates and conflicts between
`.codex/skills` and `.agents/skills`. Runtime and stored DevFlow versions are
both `0.3.0+codex.20260529145038`; no migration apply command was run because
the current repair does not need project-local skill-layout mutation.

The local repair was then implemented as OpenSpec change
`internal-responses-resource-stickiness`. `codex-switch verify <profile>` now
supports `--responses-tool-smoke`, which runs a deterministic ephemeral
`codex exec --json` smoke that forces a harmless shell tool call and
tool-result follow-up using the target profile `CODEX_HOME`. One-key
`codex-switch internal` and `codex-switch official` forward
`--responses-tool-smoke` into post-switch verification. Azure resource mismatch
output is diagnosed as an internal Responses resource-stickiness failure, and
JSON reports record only sanitized routing fields: `x-account-id`,
`x-account-deployment`, `x-model-request-id`, and `x-tt-logid`.

The scenario is documented in
`docs/troubleshooting/internal-azure-responses-resource-stickiness.md` and
linked from `README.md`. `scripts/package-release.sh` now includes `docs/` in
release bundles so the troubleshooting note ships with the installed tool.
Verification evidence is recorded in
`.planning/verification/20260703114321-internal-responses-resource-stickiness.md`.
The full profile-switch test file passed 102 tests, Python compile checks
passed, shell syntax checks passed, OpenSpec validated 11 items, `git diff
--check` passed, the release bundle was generated, and the local installed
codex-switch was refreshed from `/Users/cY/dev/codex-switch/dist/codex-switch`.
Installed help confirms `--responses-tool-smoke` is available for both
standalone `verify` and one-key switch flows.

## Next Action

Use
`codex-switch --skip-self-update verify internal --responses-tool-smoke --report`
after internal backend upgrades or when internal Desktop fails after a tool
call. If it reports an internal Responses resource-stickiness failure, hand the
sanitized account/deployment/request/log IDs to the AIDP/internal backend owner.
The upstream repair remains with AIDP or the internal backend: Responses
follow-up/retry requests that share context must be routed to the same Azure
OpenAI resource, or the backend must provide a supported sticky routing key.
Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened. Separate follow-ups remain available for
project-local DevFlow skill layout migration and external `gsd-core` update,
but they are outside this repair.

On 2026-07-03, the internal Desktop startup crash after `codex-switch i` was
diagnosed and repaired under OpenSpec change `internal-app-protocol-compat`.
Desktop logs showed the first internal app-server after the switch reported
`0.142.4`, initialized, routed `plugin/list`, then closed stdio with exit code
`241`. Desktop's retry reported `0.142.5`, routed the same `plugin/list` flow,
logged the same featured plugin `401 Unauthorized` warning, and stayed
connected. The warning is therefore a noisy last stderr line from an
unauthenticated featured-plugin fetch, while the local health gap was that
codex-switch did not verify the Desktop app-server startup window after an
internal backend auto-update.

The repair adds `codex-switch verify <profile> --app-server-smoke`. The smoke
starts the profile `codex_bin app-server --analytics-default-enabled` with the
target profile `CODEX_HOME`, sends `initialize`, `initialized`, and a
Desktop-like `plugin/list` request, then waits briefly for the process to stay
healthy. JSON-RPC auth errors from `plugin/list` are accepted as responses; a
non-zero app-server exit such as `241` fails verification with bounded
stdout/stderr context. One-key `codex-switch internal` now automatically adds
`--app-server-smoke` to post-switch verification when the internal update check
actually ran an auto-update. Users can also request it explicitly for manual
internal backend rebinding or upgrades.

Verification evidence is recorded in
`.planning/verification/20260703060556-internal-app-protocol-compat-startup-smoke.md`.
The focused red tests failed before implementation for the missing
`--app-server-smoke` flag and missing one-key auto-update forwarding. Focused
green tests passed for plugin-list auth error success, exit-code `241`
failure, and automatic one-key internal auto-update smoke. Neighbor verifier
smoke tests passed, the full profile-switch regression suite passed 104 tests,
Python and shell syntax checks passed, OpenSpec validated all 11 items, `git
diff --check` passed, and a direct real internal app-server smoke returned
`code=0` with `app-server smoke passed`. The release bundle was regenerated
and installed locally; installed `codex-switch --skip-self-update internal
--help` lists `--app-server-smoke`.

`scripts/validate_workflow_state.py` is still unavailable in this checkout, so
that gate is recorded as unavailable rather than executed. Archive remains
unavailable because the archive gate is closed. Do not archive until the gate
is explicitly opened.

On 2026-07-03, the internal Desktop settings sync gap after switching to
`internal` was diagnosed and repaired under OpenSpec change
`independent-profile-homes`. `config.toml` shared settings were already syncing;
the missing values were Desktop/Electron UI settings stored in
`.codex-global-state.json`. That file had been excluded wholesale from
cross-home sync with credentials and runtime state, which protected prompt
history and thread state but also prevented safe settings such as window bounds,
hotkeys, sidebar state, and composer preferences from following the internal
home.

The repair keeps `.codex-global-state.json` excluded from generic shared
support copy/link plans, then merges only a sanitized Desktop settings subset.
Top-level Desktop settings and allowlisted `electron-persisted-atom-state`
settings are copied; prompt history, thread permissions, prompt drafts, queued
follow-ups, remote thread summaries, unread-thread state, thread client IDs,
credentials, and remote routing identifiers remain profile-local. Independent
switch flows now run this merge in both directions, and the generated internal
Desktop wrapper runs the same helper on startup. README and the
`independent-profile-homes` design/spec/tasks were updated.

Verification evidence is recorded in
`.planning/verification/20260703174622-desktop-global-settings-state-sync.md`.
The new focused regressions failed before implementation for the missing merge
helper, missing switch-created state file, and stale wrapper state, then passed
after implementation. Adjacent shared-state/wrapper isolation regressions
passed, the full profile-switch suite passed 107 tests, Python compile and
shell syntax checks passed, OpenSpec strict validation passed all 11 items,
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`, and `git
diff --check` passed. The installed bundle was refreshed with `./install.sh`.

The current workstation internal home was repaired without changing the active
profile by merging the sanitized settings subset from `/Users/cY/.codex` into
`/Users/cY/.codex-switch/homes/internal/.codex-global-state.json`. A key-only
safety check showed no copied prompt-history, thread permission, draft,
unread-thread, remote-summary, or thread-client-id atom keys. Current
`codex-switch --skip-self-update status` still reports active profile
`openai-official`. Archive remains unavailable because the archive gate is
closed; do not archive until the gate is explicitly opened.

On 2026-07-03, the user clarified that the missing settings were the Codex
Desktop Settings sidebar categories: General, Appearance, Configuration,
Personalization, Pets, and Keyboard shortcuts. A follow-up audit showed
General/Appearance/Configuration/Personalization settings were covered by the
existing `config.toml` and sanitized `.codex-global-state.json` sync, but
`pets/` was still excluded from shared support despite backing the user-facing
Pets settings panel.

The repair keeps plugin caches, credentials, browser/process state, sqlite
state, sessions, histories, secrets, and model catalogs excluded, but removes
`pets` from the Python and generated-shell non-shareable lists so the existing
shared-support sync/link logic handles it. Regression tests were added for
switch-time `pets/` sync and generated internal Desktop wrapper startup sync.
README and the `independent-profile-homes` OpenSpec design/spec/tasks were
updated.

Plugins/Skills were audited at the same time. Official and internal
`config.toml` currently have matching plugin/marketplace/hook/MCP config
counts: 25 plugins, 5 marketplaces, 43 hooks, and 2 MCP entries. Internal
`skills` is a symlink to `/Users/cY/.codex/skills`. Internal `plugins` remains
a profile-local cache directory by design; `codex-switch --skip-self-update
repair-plugins internal --dry-run` reports no missing enabled plugins. DevFlow
plugin-project migration sync-only still reports `migration_pending` because
of legacy `.codex/skills` duplicates/conflicts with `.agents/skills`; no apply
was run.

Verification evidence is recorded in
`.planning/verification/20260703181220-settings-panel-pets-plugins-skills-sync.md`.
The focused `pets/` regressions failed before implementation and passed after
the fix. Adjacent settings/shared-support/wrapper/plugin regressions passed,
the full profile-switch suite passed 109 tests, Python compile and shell
syntax checks passed, OpenSpec strict validation passed all 11 items,
`scripts/package-release.sh` generated `dist/codex-switch.tar.gz`, and `git
diff --check` passed. The installed bundle was refreshed with `./install.sh`.
The current workstation internal home now has
`/Users/cY/.codex-switch/homes/internal/pets -> /Users/cY/.codex/pets`, and
the active profile remains `openai-official`.

On 2026-07-03, after the user reported that switching to `internal` still
showed `The requested item was created under a different Azure OpenAI resource`,
the live issue was rechecked. The installed `codex-switch` initially did not
show `--responses-tool-smoke` because `./install.sh` had been run without
`CODEX_SWITCH_SOURCE_DIR`, so it installed the latest GitHub release instead of
the current working-tree repair. On the 2026-07-03 20:00 CST recheck, installed
`codex-switch --skip-self-update verify internal --responses-tool-smoke
--report` again failed before verification with `unrecognized arguments:
--responses-tool-smoke`, confirming installed bundle drift. The working-tree
wrapper reproduced the backend failure and wrote
`/Users/cY/.codex-switch/verification/20260703T115956Z-internal.json`. The
current working tree was then installed explicitly with
`CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh`, and
installed `verify --help` now includes both `--responses-tool-smoke` and
`--app-server-smoke`.

`codex-switch --skip-self-update verify internal --responses-tool-smoke
--report` wrote
`/Users/cY/.codex-switch/verification/20260703T120052Z-internal.json` after
the install refresh. Because the active profile had already returned to
`openai-official`, the report also contains active-profile mismatch
diagnostics. The Responses smoke nevertheless reproduced and classified the
user-visible error as
`internal Responses resource-stickiness failure; Responses context follow-up
must stay on the same Azure OpenAI resource`. No account/deployment headers
were present in this repro, but the diagnostic kind is
`azure_responses_resource_mismatch`.

Verification evidence is recorded in
`.planning/verification/20260703110316-internal-responses-stickiness-live-repro.md`.
This is not the previous plugin/list app-server crash and not the
Settings/Plugins/Skills sync issue. The remaining durable repair belongs in
AIDP/internal backend routing: Responses context follow-up requests must stay
on the same Azure OpenAI resource, or the backend must expose a supported sticky
routing key. Archive remains unavailable because the archive gate is closed.

On 2026-07-03, the Lark internal Codex setup document
`OOYBdDO2MoSU7nxb8iLcQAWMnPf` was checked against the current
`codex-switch` internal profile. The document says internal mode must use the
script-installed internal Codex CLI, write Azure ModelHub provider config
(`https://aidp.bytedance.net/api/modelhub/online`, `wire_api = "responses"`,
AK query param), and force Codex Desktop to use the internal CLI via a
LaunchAgent `CODEX_CLI_PATH` override. The referenced LaunchAgent Wiki
`GfnEwy3u3ixJ9bk0bvxco8msnIb` describes the same
`~/Library/LaunchAgents/com.openai.codex-cli-path.plist` mechanism used by
`codex-switch`.

Verification evidence is recorded in
`.planning/verification/20260703201031-internal-profile-doc-procedure-check.md`.
Current live state remains `openai-official`: LaunchAgent and running
app-server point to `/Applications/Codex.app/Contents/Resources/codex`.
Stored internal profile state matches the document's contract with an extra
codex-switch Desktop wrapper layer:
`codex_bin=/Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex`,
`app_cli_path=/Users/cY/.codex-switch/bin/codex-internal-app`, and internal
config uses `model_provider = "azure"`, ModelHub base URL, Responses wire API,
and a present AK query param. Conclusion: the stored internal profile setup is
equivalent to the document's required local setup, but the current live machine
is intentionally back on official. The remaining Azure resource mismatch occurs
after local internal binary/provider selection, inside AIDP/internal backend
Responses follow-up routing.

On 2026-07-03, the internal profile was experimentally rolled back from the
latest internal Codex release `0.142.5` to the previous release `0.142.4`.
GitHub `SDGLBL/codex` releases show latest `internal-rust-v0.142.5` and
previous `internal-rust-v0.142.4`. Local `/Users/cY/.local/bin/codex` already
contained `codex-cli 0.142.4`, so the internal profile was rebound with
`codex-switch --skip-self-update set-bin --preserve-app-cli internal
/Users/cY/.local/bin/codex`, then activated with
`codex-switch --skip-self-update internal --skip-update-check --skip-doctor
--no-status` to avoid auto-updating back to 0.142.5. The internal manifest,
switch shim, and generated Desktop wrapper now delegate to
`/Users/cY/.local/bin/codex`.

Verification evidence is recorded in
`.planning/verification/20260703205658-internal-bin-rollback-01424-smoke.md`.
The working-tree verifier command
`./scripts/codex-switch --skip-self-update verify internal --app-server-smoke
--responses-tool-smoke --report` wrote
`/Users/cY/.codex-switch/verification/20260703T125615Z-internal.json`.
With 0.142.4, both `App-server smoke` and `Responses tool smoke` passed; the
report has no smoke diagnostics. The only remaining verification issues are
that the currently running Codex Desktop/app-server processes still use
`/Applications/Codex.app/Contents/Resources/codex` and must be fully quit and
reopened to inherit `/Users/cY/.codex-switch/bin/codex-internal-app`. Current
shell `PATH` still resolves bare `codex` first from the older internal
plugin-appserver path at 0.142.5, so profile-bound commands are corrected but
current-terminal bare `codex` resolution remains a separate shell environment
detail.

On 2026-07-03, the previous internal release `0.142.4` was reinstalled through
the real internal installer flow instead of reusing the existing local binary.
Preflight confirmed the internal install AK was present without printing it,
and dry-run confirmed the pinned install target
`codex-switch --skip-self-update update-internal --version 0.142.4
--install-dir /Users/cY/.local/bin`. A preinstall backup was written under
`/Users/cY/.codex-switch/backups/20260703T210044-pre-reinstall-internal-0.142.4`.
The real installer downloaded Codex CLI and bundled rg, resolved version
`0.142.4`, installed to `/Users/cY/.local/bin`, and configured internal Azure
provider settings. The preinstall and postinstall sha256 were both
`8bdbbf4b1a3b391425fcda4e86537805e51ddea97d896a563eaa1494c4eef6f1`, so the
previous local 0.142.4 binary was not corrupt, but the download/install flow
was fully re-run.

Verification evidence is recorded in
`.planning/verification/20260703210228-internal-bin-01424-reinstall.md`.
After reinstall, `codex-switch --skip-self-update set-bin --preserve-app-cli
internal /Users/cY/.local/bin/codex` and
`codex-switch --skip-self-update internal --skip-update-check --skip-verify
--skip-doctor --no-status` reactivated the profile without auto-upgrading back
to 0.142.5. Current internal manifest, switch shim, and Desktop wrapper all
delegate to `/Users/cY/.local/bin/codex`, which reports `codex-cli 0.142.4`.
`codex-switch --skip-self-update verify internal --app-server-smoke
--responses-tool-smoke --report` wrote
`/Users/cY/.codex-switch/verification/20260703T130213Z-internal.json`; both
smokes passed. The report remains `ok=false` only because the already-running
Desktop/app-server processes still use the official app bundle and need a full
Desktop quit/reopen to inherit `/Users/cY/.codex-switch/bin/codex-internal-app`.
The current terminal's bare `codex` still resolves first to the old
plugin-appserver 0.142.5 path, which is separate PATH-ordering drift from the
profile-bound shim/wrapper state.

On 2026-07-03, `internal-app-protocol-compat` was extended with a blocked
release policy for internal Codex CLI `0.142.5` and shell CLI alignment
diagnostics. The user confirmed that switching back to internal `0.142.4`
works, so `0.142.5` is now treated as a known-bad default update target.
`codex-switch internal` keeps or installs pinned fallback `0.142.4` while
GitHub latest remains `internal-rust-v0.142.5`; when latest advances to a
successor release, one-key internal switching resumes the ordinary unpinned
latest auto-update path. Direct `codex-switch update-internal` also pins to
`0.142.4` by default when latest is blocked, unless the caller explicitly
passes `--version`.

`codex-switch status` now reports whether bare command-line `codex` resolves
to the codex-switch shim. `codex-switch shim-env` prepends the shim directory
and clears the shell command cache with `hash -r`. Installed status currently
shows active profile `openai-official`; the current terminal's `PATH codex`
still points first to the old internal plugin-appserver binary, but status now
reports that as a mismatch and prints
`eval "$(codex-switch shim-env)"`. In a child shell after applying that command,
`which codex` resolves to `/Users/cY/.codex-switch/bin/codex` and status
reports `PATH codex alignment: ok`.

Verification evidence is recorded in
`.planning/verification/20260703212846-internal-01425-block-pin.md`. The new
focused regressions failed before implementation for missing blocked-release
handling and missing PATH alignment status, then passed after implementation.
The focused Slice 7 tests passed, the adjacent one-key auto-update app-server
smoke test passed, the full profile-switch regression suite passed 114 tests,
Python compile checks passed, shell syntax checks passed, `git diff --check`
passed, OpenSpec strict validation passed all 11 items, workflow validation
reported `ok=true`, the release package was regenerated, and the local
installed codex-switch was refreshed from this checkout. Installed
`codex-switch --skip-self-update check-update internal` now reports latest
`0.142.5` as blocked and skips updating `/Users/cY/.local/bin/codex` away from
`0.142.4`. Installed
`codex-switch --skip-self-update update-internal --dry-run` shows pinned
version `0.142.4`.

Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened.

On 2026-07-03, `always-check-self-update` was extended with version-ordered
self-update after `codex-switch internal` re-downloaded internal Codex
`0.142.5`. The root cause was that the installed local-source `codex-switch`
repair was overwritten by the published `0.1.12` bundle because wrapper
self-update replaced the implementation whenever bundle `VERSION` strings were
different. The correct contract is version ordering: a release bundle should
replace the installed implementation only when the release version is newer.

`sync_self_update` now compares current and staged bundle versions by ordering.
Same-version and older-release checks remove the staged bundle and report the
current implementation as already up to date; newer releases still sync and
re-exec. Prerelease ordering treats `0.1.13-dev` as newer than `0.1.12` but
older than formal `0.1.13`, so a future real release can still take over. The
temporary local-source marker path was removed from `install.sh` and
`scripts/codex-switch`. The local checkout `VERSION` is now `0.1.13-dev`.
Active profile was not switched and is expected to remain `openai-official`.

Verification evidence is recorded in
`.planning/verification/20260703221616-version-ordered-self-update.md`.
Focused RED tests failed before implementation and passed after the fix. The
full profile-switch regression suite passed 123 tests; Python compile checks,
shell syntax checks, `git diff --check`, `scripts/package-release.sh`,
`openspec validate always-check-self-update --strict --no-interactive`,
`openspec validate internal-app-protocol-compat --strict --no-interactive`, and
`openspec validate --all --strict --no-interactive` all passed. Installed
`codex-switch check-update internal` ran self-update without
`--skip-self-update`, reported local `0.1.13-dev` already up to date, and kept
internal Codex at `0.142.4` while blocking latest `0.142.5`. DevFlow
plugin-project-migration reported `ok=true` with control plane current, but
existing skill-layout duplicate/conflict migration findings remain and were
left untouched.

Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened.

On 2026-07-03, `internal-app-protocol-compat` was extended again so profile
switches automatically prepare command-line `codex` alignment instead of only
diagnosing PATH drift after the fact. When a switch updates the
`~/.codex-switch/bin/codex` shim, codex-switch now installs or refreshes a
marker-managed shell startup block. The block prepends the store `bin`
directory to PATH and runs `hash -r` when the shell supports it. Existing shell
profile content outside the managed block is preserved, repeated switches
replace the block instead of duplicating it, and
`CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP=1` skips the mutation for controlled
environments. The shell profile path is also included in independent switch
dry-run/backup plans when it will be mutated.

The implementation deliberately does not overwrite whichever `codex` binary is
currently first on PATH. That path may be a plugin cache binary or another
user-managed install, and replacing it would be unsafe. A child
`codex-switch` process also cannot mutate the already-running parent shell's
in-memory PATH, so current-shell drift remains visible through
`codex-switch status` and can still be repaired immediately with
`eval "$(codex-switch shim-env)"`; newly opened shells will inherit the managed
bootstrap after the next real switch.

Verification evidence is recorded in
`.planning/verification/20260703213928-switch-shell-bootstrap-alignment.md`.
The focused regressions failed before implementation for missing switch-time
bootstrap installation and missing managed-block replacement, then passed after
implementation. The Slice 8 focused tests passed, adjacent CLI alignment and
internal blocked-update tests passed, the full profile-switch regression suite
passed 117 tests, Python compile checks passed, shell syntax checks passed,
`git diff --check` passed, OpenSpec strict validation passed all 11 items, the
release package was regenerated, and the local installed codex-switch was
refreshed from this checkout. Installed dry-run evidence with
`CODEX_SWITCH_SHELL_PROFILE=/tmp/codex-switch-shell-bootstrap-check.zshrc`
shows the shell profile path in both backup and mutation plans. No real
workstation profile switch was run during this verification; active profile
remains `openai-official`.

Archive remains unavailable because the archive gate is closed. Do not archive
until the gate is explicitly opened.
