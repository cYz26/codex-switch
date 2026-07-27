# DevFlow Refresh and Core Implementation Review

Date: 2026-07-22

Repository: `/Users/cY/dev/codex-switch`

Reviewed revision: `main@0a9400d` (`VERSION 0.1.13`)

## Completion Claim

- The targeted global `dev-flow@cy-codex-skills` installation is refreshed to
  `0.3.0+codex.20260529145038` and verified `matches-source`.
- Project-local DevFlow/OpenSpec skill activation is current. Six OpenSpec 1.6
  skills were regenerated in isolation and verified already present.
- Durable generated-template drift was merged into `AGENTS.md`: the Matt
  methodology contract and bounded-subagent execution contract.
- Workflow validation is healthy. The only remaining workflow warning is the
  explicitly deferred legacy root-state migration; twelve legacy
  `.codex/skills` duplicates remain migration inputs and were not removed.
- The current implementation does need optimization. The highest-priority work
  is correctness and state safety, not optional performance tuning.
- No production implementation, workstation profile switch, release, commit,
  push, provider migration, legacy skill cleanup, or root-state migration was
  performed.

## Live Ownership Evidence

- Shell `codex`: `/Users/cY/.codex-switch/bin/codex`.
- Desktop bundle CLI:
  `/Applications/ChatGPT.app/Contents/Resources/codex`, version
  `codex-cli 0.145.0-alpha.27`.
- Internal profile CLI: `/Users/cY/.local/bin/codex`, version
  `codex-cli 0.142.4`.
- `codex-switch status` reported active profile `openai-official`, the
  configured shell/App bundle paths, and PATH shim alignment.
- A running ChatGPT Desktop process and its bundled app-server were observed;
  no process was started, stopped, or rebound.

## Refresh Evidence

### Targeted global refresh

```text
env CODEX_HOME=/Users/cY/.codex \
  /Applications/ChatGPT.app/Contents/Resources/codex \
  plugin add dev-flow@cy-codex-skills --json

installed version: 0.3.0+codex.20260529145038
installed path: /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038
```

```text
python3.12 /Users/cY/dev/skills/cy-codex-skills/dev/scripts/
  codex_auto_update_plugins_skills.py --json

dev-flow@cy-codex-skills: matches-source
```

The full updater was not applied. Its unrelated release, plugin, and project
refresh candidates were outside this request.

### Project refresh

Pre-change diagnostics ran with Python 3.12:

- `plugin_project_migration.py --json`: `ok: true`; control plane current;
  no missing or stale project skills; root-state migration and legacy duplicate
  cleanup remain pending.
- `validate_workflow_state.py --json`: `ok: true`; generated-template drift was
  limited to the Matt methodology and bounded-subagent contracts.
- `doctor_workflow.py --check-cache-drift --json`: cache/current workflow
  healthy except the deferred legacy root-state migration.
- `scaffold_workflow.py --mode auto --dry-run --json`: brownfield scaffold
  candidate only; no scaffold output was applied.
- `git status --short`: the pre-existing hook-created
  `.planning/devflow/context-health/events.jsonl` was untracked and preserved.

Project dependency refresh ran first as dry-run and then apply:

```text
python3.12 .../activate_project_dependencies.py \
  --repo /Users/cY/dev/codex-switch \
  --codex-home /Users/cY/.codex \
  --refresh-project-skills --dry-run --json

python3.12 .../activate_project_dependencies.py \
  --repo /Users/cY/dev/codex-switch \
  --codex-home /Users/cY/.codex \
  --refresh-project-skills --apply --json
```

All required DevFlow links were already linked. The six OpenSpec skills were
verified present; no legacy layout cleanup or provider-state write occurred.

## Review Method

This was a current-codebase audit, not a diff review. The main agent mapped the
CLI, lifecycle/switching, config/state, Desktop proxy, plugin/update/release,
diagnostic/verification, and regression-test paths. Six bounded read-only
reviews were run with disjoint module scopes, then deduplicated and rechecked
against the current source and OpenSpec contracts.

Baseline verification was green:

```text
env PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
Ran 123 tests in 54.984s
OK

openspec validate --all --strict --no-interactive
11 passed, 0 failed

bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
passed

Python 3.12 AST parse of scripts/*.py
passed
```

The green baseline proves the existing suite is stable. It does not cover the
failure and compatibility branches below.

## Consolidated Findings

No P0 was found. After the user's product-scope clarification, ten P1 findings
and three P2 findings remain active. P1 denotes a concrete data-loss, security,
false-success, or core-contract failure reachable through an official/internal
product path. P2 denotes a durable correctness or compatibility issue with a
narrower trigger.

### Deferred review note — Arbitrary profile names can escape the profile store

`scripts/codex_switch_store.py:11-18,60-66` accepts exact `.` and `..` as
profile names. `Store.profile_dir("..")` resolves to the store root, so capture
or later profile operations can write outside `profiles/` and corrupt the store
layout.

Disposition: `DEFER_AND_CONTINUE`. The user confirmed that only
`openai-official`/`official` and `internal` are product profiles, so arbitrary
profile hardening is outside the approved repair and is not counted as an
active P1. Revisit containment only if custom profiles become product scope;
the unsupported legacy route retains residual risk.

### P1-02 — Snapshot mode breaks home isolation and produces unrestorable backups

`scripts/codex_switch_switching.py:67-77,91-149` sends snapshot mode through the
legacy live-home path instead of the independent target home. For internal this
can mutate official config/auth while running the internal binary. That path
uses `backup_live_files()` (`scripts/codex_switch_backup.py:12-40`), which writes
`files`; `restore_backup()` reads only `entries`
(`scripts/codex_switch_restore.py:167-196`) and can report success after
restoring nothing.

Disposition: keep home isolation independent of config strategy. Use one
versioned backup schema and one mutation plan for all supported switch modes;
reject or explicitly migrate unknown legacy manifests.

### P1-03 — Restore can overwrite changed directories and deletes before payload validation

`scripts/codex_switch_restore.py:124-132` treats any two directories as equal.
A non-force restore therefore does not detect added or edited contents before
`remove_existing()` recursively removes the directory. `restore_entry()` at
lines 142-162 removes the current target before proving the backup payload
exists or matches its recorded state.

Disposition: recursively attest kind, content, symlink target, and mode; preflight
every entry and payload before the first mutation; stage restored content and
commit atomically or roll back.

### P1-04 — Switch and capture are not failure-atomic

The independent switch mutates homes/config/shim before the late Desktop
binding step (`scripts/codex_switch_switching.py:365-485`). A launchctl failure
can leave mixed target state and an unfinalized backup. Capture overwrite writes
config before required-auth and TOML validation
(`scripts/codex_switch_capture.py:25-48`); a missing auth failure leaves a
partially changed profile, while `allow_missing_auth` retains stale destination
credentials.

Disposition: introduce one immutable, fully validated Profile transaction
module with versioned snapshot, atomic apply, rollback, and explicit managed-file
replacement semantics. Hold a store-scoped interprocess lock through commit.

### P1-05 — Runtime/App ownership has contradictory sources of truth

The default bundle constant recognizes only `Codex.app`
(`scripts/codex_switch_constants.py:9`); on this machine the real bundle is
`ChatGPT.app`, so `resolve_official_app_cli_path()` can fall back to the managed
PATH shim (`scripts/codex_switch_paths.py:36-41`). Process recognition likewise
hard-codes the old App executable (`scripts/codex_switch_running_app.py:13,97-108`).

Fresh `init --capture-current internal` stores the raw binary as `app_cli_path`
(`scripts/codex_switch_lifecycle.py:70-79`), while switching uses the generated
managed App launcher (`scripts/codex_switch_switching.py:424,472-485`). Doctor
then expects the raw manifest value (`scripts/codex_switch_doctor_active.py:36-57`)
and rejects the normal switch. An isolated temporary-store reproduction returned
`ACTION REQUIRED`; the three one-key internal tests skip Doctor.

Disposition: create one Runtime binding module that derives shell CLI, managed
App launcher, backend binary, bundle ownership, and running-process expectations.
Switch, status, doctor, and verify must consume the same result.
`/Applications/ChatGPT.app` with bundle id `com.openai.codex` is the only
current healthy host. Codex.app is migration observation only, ChatGPT Classic
is excluded, and managed-shim fallback fails closed.

### P1-06 — Internal rebind can bypass or stale the managed proxy

`scripts/codex_switch_bindings.py:76-106` either replaces internal
`app_cli_path` with the raw new backend or preserves a generated launcher that
still embeds the old backend. `scripts/codex_switch_running_app.py:128-137`
accepts a proxy-parented process based on the stable launcher marker without
proving its child backend matches the current manifest.

Disposition: make internal rebind atomic: validate the new binary, regenerate
the managed launcher, persist the intended binding, run compatibility smoke,
then commit. Compare both expected launcher and expected backend in diagnostics.

### P1-07 — Proxy transformations are schema-blind and config recovery can undo user writes

`scripts/codex_switch_app_proxy.py:147-166,283-295` does not recognize the real
`keyPath: "model"` config-write shape, but recursively rewrites matching field
names anywhere in arbitrary payloads. Capability handling also filters a
marketplace kind even when canonical dynamic tools are supported. Separately,
`scripts/codex_switch_config.py:283-285` restores array-of-table blocks by byte
identity, so changing `[[skills.config]] enabled=true` to false can append the
old true block and revive a disabled entry.

Disposition: route transformations by RPC method, direction, exact field path,
and explicit capability. Unknown payload data must remain unchanged. Remove
proxy-side post-response file recovery because it invalidates AppServer's
returned version. A temporary-home internal `0.142.4` probe proved versioned
writes preserve unrelated config; bind that behavior to a capability receipt
and fail before forwarding an unproven write. Give offline array-table merges
stable identity and add generated-launcher → proxy → fake-backend E2E tests.

### P1-08 — Install, self-update, packaging, and release promotion are not fail-safe

- `scripts/package-release.sh:6-11` can map `PACKAGE_DIR` to the repository when
  `CODEX_SWITCH_DIST_DIR` is its parent, then `rm -rf` the checkout.
- `install.sh:37-46,117-122,129-136` deletes the current destination before
  copy; Bash conditional-function semantics can mask copy failure and report
  success.
- `scripts/codex-switch:307-339,366-369` validates only that the staged launcher
  is executable, removes the previous copy before a successful re-exec, and has
  no post-promotion rollback handshake.
- `.github/workflows/auto-release.yml:61-81` pushes the version commit and tag
  before packaging assets; a packaging failure leaves a latest tag without a
  release asset and the next plan may not self-heal.

Disposition: stage into a validated version directory, verify structure/version,
syntax/import and command smoke, promote atomically, retain last-known-good until
a success handshake, and package/verify assets before pushing release refs.
Guard every destructive package path by canonical containment.

### P1-09 — Internal update failure can be reported as success; ordering can downgrade a healthy binary

The update call stack runs inside an `if` condition
(`scripts/codex-switch:633-642`), which disables Bash `errexit` in called
functions. `run_internal_auto_update()` does not test the helper status and then
sets `INTERNAL_AUTO_UPDATED=1` (`scripts/codex-switch:1091-1107`). Separately,
lines 991-1021 treat unequal versions as update-needed, so a healthy current
version newer than latest can be downgraded, including to a blocked-release
fallback.

Disposition: return a structured update result, check the helper explicitly,
verify the installed binary equals the intended target, then mark success. Use
ordered version comparison and downgrade only when the current version itself
is explicitly blocked.

### P1-10 — Unparseable plugin catalog can mass-disable enabled plugins

Plugin catalog commands merge stderr into stdout
(`scripts/codex_switch_plugins.py:267-274`). `available_plugin_selectors()`
maps empty or invalid JSON to an empty verified set at lines 317-325; the
`--disable-unavailable` path at lines 390-419 then treats every missing plugin
as proven unavailable and rewrites configs.

Disposition: separate stdout/stderr, validate the response schema, distinguish
verified-empty from unknown/invalid, and fail closed before any disable write.
Also validate installed cache markers rather than treating any child entry as a
complete materialization.

### P1-11 — Verification can both false-pass and expose secrets

`response_seen()` accepts any response with a matching ID
(`scripts/codex_switch_verify.py:322-330`), so an initialize error plus a later
not-initialized error can pass app-server smoke at lines 421-436. Generic smoke
failures embed raw command output and the raw exec prompt into printed and JSON
reports (`scripts/codex_switch_verify.py:529-540,585-603,656-659`), which can
persist Authorization headers, API keys, or signed URLs. Manifest drift can
also be hidden because App verification prefers stale `active.json` at lines
175-183.

Disposition: require a successful initialize result, model each smoke as a
structured outcome, derive expectations from the canonical binding module,
sanitize and cap all output, never persist the raw prompt, and apply explicit
timeouts/bounded capture to subprocess checks.

### P2-01 — TOML handling has incompatible partial parsers

On the currently selected system `python3` (3.9.6), the fallback in
`scripts/codex_switch_toml_validate.py:7-32` accepts malformed TOML such as
`foo = @bad`. `scripts/codex_switch_config.py:212-261` tracks only the first
line of an assignment, so a multiline overlay can retain stale continuation
lines.

Disposition: require a real TOML parser or fail closed, and put parsing,
value-span edits, entity identity, overlay, and deterministic render behind one
Config document module.

### P2-02 — Generated App launcher duplicates and weakens home-sync symlink policy

`scripts/codex_switch_app_wrapper.py:100-140` implements its own symlink cleanup
and share rules. It misses relative/cross-profile isolated links and can create
a loop that the canonical Python home-sync implementation rejects
(`scripts/codex_switch_home_sync.py:314-345`).

Disposition: remove the duplicate policy. Make the generated launcher call the
same canonical sync interface, then test relative, cross-profile, dangling, and
self/target-home links through the launched path.

### P2-03 — Concurrent switches are not serialized

`scripts/codex_switch_switching.py:325-502` performs the read, plan, backup,
mutation, binding, active-record write, and backup finalization without a
store-scoped lock. Concurrent switches can interleave into a hybrid state.

Disposition: add a store-scoped lock acquired before reading active/manifests
and held through finalization. A second caller should receive a precise busy
result; add a controlled concurrency regression.

## Architecture Deepening Opportunities

The architecture scan used the module/interface/depth/seam/adapter/leverage/
locality vocabulary. The strongest deepening candidates are:

1. **Profile transaction module — Strong.** One interface owns validated plan,
   versioned snapshot, atomic apply, rollback, and commit.
2. **Runtime binding module — Strong.** One ownership seam serves switch,
   status, doctor, and verify; ChatGPT.app is current and Codex.app is a
   migration-only observation adapter.
3. **App-server compatibility adapter — Strong.** Method- and schema-scoped
   transforms replace recursive field-name rewriting; the generated launcher
   and fake backend test the same interface.
4. **Release and update module — Strong.** One staged-promotion interface owns
   version ordering, validation, smoke, atomic promotion, handshake, and
   last-known-good retention.
5. **Config document module — Worth exploring.** One semantic document
   interface replaces the shallow validator/scanner/editor helpers.

The temporary visual report for this run was generated and opened at:

`/var/folders/3c/z9wcw8kx66lfmbr02yb5vxd80000gp/T/architecture-review-20260722T113526.html`

It is supplemental visualization, not the durable source of truth.

## Recommended Repair Route

Do not address these as isolated one-line fixes. The systemic route is:

1. `transactional-profile-state`: snapshot isolation, v2 backup, restore
   preflight, capture replacement, rollback, and locking.
2. `canonical-runtime-binding`: current ChatGPT ownership, canonical binding,
   atomic internal rebind, process and backend attestation.
3. `schema-scoped-app-proxy`: exact transforms, backend-owned config versions,
   semantic offline TOML, canonical launcher sync, and full chain coverage.
4. `fail-safe-update-release`: package containment, installer/self-update
   rollback, ordered updates, catalog fail-closed, bounded sanitized verify,
   and release reconciliation.

All four Full OpenSpec artifact sets were subsequently created and passed
strict validation after the user approved this route. Implementation evidence
belongs in their task lists and per-change verification records, not this
read-only baseline review.

Performance-only work, including splitting the 1,218-line shell orchestration
and 5,677-line test file, should follow the correctness seams above. Moving
policy into the deep Python modules will make that split mechanical rather than
cosmetic.

## Final Validation and Residual Risk

Fresh final validation after the evidence and control-plane updates:

- `env PYTHONDONTWRITEBYTECODE=1 python3.12
  scripts/test_codex_profile_switch.py`: 123 tests in 56.181 seconds, `OK`.
- `openspec validate --all --strict --no-interactive`: 11 passed, 0 failed.
- `bash -n scripts/codex-switch install.sh run.sh
  scripts/package-release.sh`: passed.
- Python 3.12 AST parse: 39 files passed.
- `codex_auto_update_plugins_skills.py --json`:
  `dev-flow@cy-codex-skills` remains `matches-source`; project migration remains
  `migration-pending`.
- `validate_workflow_state.py --json`: `ok: true`, no issues, one legacy
  root-state migration warning.
- `doctor_workflow.py --check-cache-drift --json`: diagnosis remains
  `needs repair` solely for that explicitly deferred legacy root-state
  migration; embedded workflow validation is `ok: true`.
- `git diff --check`: passed. `AGENTS.md.generated` is absent.
- Final repository writes are limited to `AGENTS.md`, `TASK_LEDGER.md`,
  `.planning/STATE.md`, and this verification record. The hook-created
  `.planning/devflow/context-health/events.jsonl` remains untracked and was
  preserved out of scope.

Residual risk until implementation: supported edge paths can lose or mix local
state, fail open or false-pass, and some release/update failures can remove the
last working copy or report success incorrectly. No failing path was invoked on
the user's workstation during this review.
