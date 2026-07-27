# Live Official/Internal Rollout

Date started: 2026-07-25 15:18:58 +0800
Task: `ROLLOUT-001`
Status: complete; internal restored and self-update repair verified

## Claim

This record will prove that the current verified worktree was installed through
the supported local-source path, a real `official` switch and Desktop task entry
worked with official ownership, and the workstation was then restored to a
healthy managed `internal` Desktop binding.

It does not authorize commit, push, tag, release, archive, destructive cleanup,
dependency changes, internal backend mutation, or `PARITY-001` implementation.

## Verified Source Receipt

- Version: `0.1.13`
- Manifest files: `64`
- Package root mode: `0755`
- Archive bytes: `381951`
- Payload SHA-256:
  `d79769dff0241bf68c5e256bfcc2398a19d8dd6c1fb8c83678caef3199d31fd5`
- Source evidence:
  `.planning/verification/20260725151329-final-source-verification.md`

## Live Pre-Rollout Snapshot

### Commands

```bash
command -v codex-switch
type -a codex-switch
command -v codex
type -a codex
codex-switch --version
codex --version
/Applications/ChatGPT.app/Contents/Resources/codex --version
/Users/cY/.local/bin/codex --version
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch \
  CODEX_SWITCH_PYTHON="$(command -v python3.12)" \
  ./scripts/codex-switch --skip-self-update status
ps -axo pid=,ppid=,etime=,command= |
  rg '[C]hatGPT|[c]odex( |$).*app-server|codex_switch_app_proxy|codex-internal-app'
launchctl getenv CODEX_CLI_PATH
shasum -a 256 \
  scripts/codex-switch \
  /Users/cY/.local/share/codex-switch/current/scripts/codex-switch \
  /Users/cY/.local/bin/codex-switch
```

### Observed Ownership

- Active profile: `internal`, timestamp `20260725T022041Z`.
- Shell `codex-switch`:
  `/Users/cY/.local/bin/codex-switch`.
- Shell `codex`:
  `/Users/cY/.codex-switch/bin/codex`.
- Shell/internal backend version: `codex-cli 0.144.6`.
- ChatGPT App version: `26.721.41059` (`CFBundleVersion=5848`).
- ChatGPT bundle CLI:
  `/Applications/ChatGPT.app/Contents/Resources/codex`,
  `codex-cli 0.146.0-alpha.3.1`.
- Internal manifest backend:
  `/Users/cY/.local/bin/codex`.
- Internal manifest/Desktop launcher and `launchctl` binding:
  `/Users/cY/.codex-switch/bin/codex-internal-app`.
- Official manifest backend/Desktop CLI:
  `/Applications/ChatGPT.app/Contents/Resources/codex`.
- Running ChatGPT pid before rollout: `78706`.
- Running Desktop app-server before rollout: pid `79038`,
  `/Users/cY/.local/bin/codex -c features.code_mode_host=true app-server
  --analytics-default-enabled`.

### Pre-Rollout Findings

- Source wrapper SHA-256:
  `2306924949f9006d9d65918fdab15e61697b7b545d2ec282a76f573d7f431b66`.
- Installed release/PATH wrapper SHA-256:
  `08bb941ca3b93a16cf28c8fbca8b29fd98982502143029bd6e1dc1a546e81d5d`.
- The installed release therefore did not contain the verified current source,
  despite both reporting version `0.1.13`.
- Source status reported
  `attestation.internal.proxy_bypass` because the running Desktop app-server
  directly owned the internal backend.
- Source status reported
  `attestation.internal.launcher_fingerprint_mismatch` because the generated
  launcher bytes did not match the current binding contract.
- This snapshot is the live failure baseline. Installation alone is not
  sufficient; both findings must be closed after the official cycle and
  internal restoration.

## Rollout Ledger

- [ ] Install the exact verified current source through `install.sh`.
- [ ] Prove immutable installed-release identity and PATH wrapper identity.
- [ ] Run real `codex-switch --skip-self-update official`.
- [ ] Fully restart ChatGPT and prove official App/runtime ownership.
- [ ] Prove a real official Desktop task can be entered.
- [ ] Record the latest stable `openai/codex` advisory.
- [ ] Run a read-only internal update check without mutating the backend.
- [ ] Restore internal with `--skip-update-check`.
- [ ] Fully restart ChatGPT and prove wrapper/proxy/backend ownership.
- [ ] Prove a real internal Desktop task can be entered.
- [ ] Run final status, doctor/verify, control-plane, and diff checks.

## Risks / Gaps

- The historical official restart gate below has been consumed and internal is
  restored. Final rollout completion now waits for FSR task 2.7 and a clean
  normal `codex-switch status`.
- No further ChatGPT restart is required for the self-update repair.

## Same-Version Self-Update Incident

After internal restoration, a normal installed `codex-switch status`
reproduced:

```text
codex-switch self-update: checking latest release...
{"message": "Required release Python module is missing or invalid: .../codex_switch_release_bundle.py", "outcome": "failed", "reason": "source_invalid"}
codex-switch self-update: warning: sync failed; continuing with current implementation
```

The installed current version is `0.1.13`, and the trusted GitHub latest
release resolves to `v0.1.13`. The published asset is a historical layout that
predates the strict release modules. The wrapper currently downloads,
canonicalizes, and validates that asset before comparing versions. FSR task 2.7
moves trusted version comparison ahead of workdir creation and candidate
materialization. Same-version and older releases become clean no-ops; newer
releases still require strict validation and immutable promotion.

The earlier Python traceback was a Python 3.9/tomllib compatibility path.
Current source resolves Python 3.11+ before dispatch, generated Desktop wrappers
pin the validated absolute interpreter, and the active proxy runs Python
3.12.13 with `-B`. Existing regressions prove explicit old Python is rejected
before the switch script or store path can mutate.

## Restart Incident And Guard

An ad hoc rollout command submitted a temporary ChatGPT restart script with
`launchctl submit`. The local macOS manual states that this mechanism keeps the
program alive after failure. When the script exited unsuccessfully, launchd
reran it and ChatGPT repeatedly restarted. The submitted job is no longer
loaded; current launchd state contains only the normal ChatGPT application job
and `com.openai.codex-cli-path`.

Future rollout automation must not use `launchctl submit` for one-shot App
restarts. Use a bounded one-shot controller, wait for the old pid to exit,
launch once, verify one new pid and expected app-server ownership, and always
remove temporary state.

## Live Findings And Repairs

### Historical Current Migration

The first supported install attempt failed:

```text
Legacy current canonicalization failed: Required release Python module is
missing or invalid:
/Users/cY/.local/share/codex-switch/current/scripts/codex_switch_release_bundle.py
```

The installed directory-based `current` predated four strict-bundle release
modules. The fix:

- adds inert placeholders only in a private canonical rollback copy;
- preserves the original legacy directory during migration;
- rejects a symlinked legacy `scripts/` directory before any external write;
- keeps strict validation unchanged for the new candidate.

RED/GREEN:

- historical installer/runner migration failed at the exact live error, then
  passed for both entrypoints;
- a symlinked `scripts/` fixture wrote four files outside staging before the
  guard, then passed with zero external writes.

### Immutable Runtime Bytecode

After the first successful promotion, running installed `status` created 39
`scripts/__pycache__/*.pyc` files and strict manifest revalidation failed. The
fix invokes every shell-entrypoint and generated Desktop Python helper with
interpreter-scoped `-B`. It does not export bytecode controls into the Codex
backend or user task environment.

The 39 generated files were preserved, not deleted, at:

```text
/Users/cY/.codex-switch/backups/20260725T074830Z-immutable-release-bytecode-residue/__pycache__
```

After the fix, an isolated real packaged `status` preserved the release on
Python 3.12 and system Python 3.9, and the installed release remained strictly
valid after a real installed `status`.

### Revision-Named Curated Plugin Cache

After internal restoration, the running App materialized the eight enabled
`openai-curated` plugins under cache key `11c74d6b`, but installed Doctor still
reported every plugin missing. The cache trees and markers were complete.

The live catalog proved that `11c74d6b` is the curated Git snapshot/cache key,
while each `.codex-plugin/plugin.json` retains its semantic plugin version.
The source repair separates those identities while preserving marker,
wrong-name, symlink, ordinary semantic-version, and source/cache mismatch
guards.

RED/GREEN:

- Doctor returned nonzero and repair repeated `plugin add` for the real layout.
- Dual-Python focused regressions passed 5/5.
- Full profile passed 198/198; update/release passed 110/110; SAP passed 37/37.
- Current-source Doctor and `verify internal` pass against the real restored
  home without another plugin mutation.

At this checkpoint the installed immutable release predated this repair. The
final FSR-002 closure below supersedes this pending statement.

## Post-Repair Verification

| Command | Result |
|---|---|
| `python3.12 scripts/test_codex_update_release.py -v` | 113/113 passed, final serial rerun |
| `python3.12 scripts/test_codex_profile_switch.py` | 198/198 passed |
| `python3.12 scripts/test_codex_protocol_config.py -v` | 37/37 passed, serial |
| system Python focused historical migration, external-write, and immutable-status regressions | passed |
| `openspec validate --all --strict --no-interactive` | 17/17 passed |
| Bash syntax, hash-bound bootstrap, and `git diff --check` | passed |

The one SAP probe failure seen during parallel full-suite execution passed
alone and in the serial 37/37 suite; final evidence uses serial results.

## Final Installed Source Receipt

- Supported command:

  ```bash
  CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch \
  CODEX_SWITCH_PYTHON="$(command -v python3.12)" \
  /Users/cY/dev/codex-switch/install.sh
  ```

- Version: `0.1.13`
- Manifest files: `64`
- Package root mode: `0755`
- Archive bytes: `383092`
- Archive SHA-256:
  `8f8de2692389c2e8526f122a7558eca5abc26072f7690a477996a972d857cd64`
- Payload/current release digest:
  `db85a38c2bc18fcb7d63f9bbca4dcbef898d5fcb0857646690075dd4418a2550`
- `current`:
  `releases/db85a38c2bc18fcb7d63f9bbca4dcbef898d5fcb0857646690075dd4418a2550`
- `rollback`:
  `releases/fa4993ce38009f9691a8b3610b8c667e02504e8ff1980c30488be36382b1e059`
- PATH wrapper SHA-256 equals source wrapper SHA-256:
  `07c675792aed80990c2dd8bf688ca0903309a42e2786fdb080a150e6934c9c0d`.
- Installed `status` followed by strict candidate validation passed with
  `pycache_present=false`.

## Official Switch Before Restart

Command:

```bash
/Users/cY/.local/bin/codex-switch --skip-self-update official
```

Transaction result:

- switch committed to `openai-official`;
- backup:
  `/Users/cY/.codex-switch/backups/20260725T074950Z-switch-internal-to-openai-official`;
- shell shim, official manifest, LaunchAgent, and `launchctl` all bind
  `/Applications/ChatGPT.app/Contents/Resources/codex`;
- official runtime and profile config use `model = "gpt-5.5"`,
  `cli_auth_credentials_store = "file"`, no `model_provider`, and no
  `[model_providers]`;
- official plugin repair installed the configured missing `figma`, `github`,
  `superpowers`, `build-ios-apps`, `build-web-apps`, `test-android-apps`,
  `plugin-eval`, and `openai-developers` caches;
- bundled CLI `0.146.0-alpha.3.1` was reported ahead of upstream stable
  `0.145.0` (`rust-v0.145.0`), with ChatGPT.app retaining update ownership.

The command returned action-required because the already-running ChatGPT pid
`78706` still had the old internal launcher and app-server pid `79038` still
ran `/Users/cY/.local/bin/codex`. This is the explicit restart gate, not a
transaction rollback.

## FSR-002 Final Closure

Date: 2026-07-25 20:39:32 +0800

The rollout subsequently restored `internal`, removed the failed temporary
restart job, and remained stable. The same-version self-update ordering defect
was repaired and verified before a final supported local-source install.

- Installed/current payload:
  `releases/9e9c9cd4bce6fd0efcc8dacd8a04e75221f7e64b4a7a3a2864423ea24fcecbd3`
- Rollback payload:
  `releases/db85a38c2bc18fcb7d63f9bbca4dcbef898d5fcb0857646690075dd4418a2550`
- Normal `codex-switch status` returned zero and printed
  `already up to date 0.1.13`.
- No `source_invalid` or `sync failed` text was emitted.
- Active profile and Desktop ownership remained `internal`.
- ChatGPT pid 4983, proxy pid 5332, and backend app-server pid 5346 retained
  their existing uptime; no additional App restart ran.
- Launchd contained only the normal ChatGPT application job and
  `com.openai.codex-cli-path`; no temporary restart/relaunch job remained.
- Final source verification passed update/release 113/113, profile 198/198,
  strict OpenSpec 17/17, Bash 5/5, dual-runtime AST 54/54 and production
  imports 46/46, workflow YAML 2/2, release static contracts 7/7, isolated
  package validation, and `git diff --check`.

This closes `FSR-002`, `INC-011`, and `ROLLOUT-001`. Commit, push, tag, release,
OpenSpec archive, dependency changes, destructive cleanup, parity
implementation, and any additional App restart remain outside this rollout.

## TPS Desktop No-Op Recovery Acceptance

Date closed: 2026-07-26 01:42:33 +0800

The later TPS recovery acceptance supersedes the earlier provisional official
cycle for the Desktop global-state no-op incident.

- Exact installed/current payload:
  `ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab`.
- Supported official command:
  `/Users/cY/.local/bin/codex-switch official --skip-update-check
  --skip-plugin-repair`.
- Retained failed backup
  `20260725T123636Z-switch-internal-to-openai-official` recovered through the
  supported transaction gate as `rolled_back/recovered`.
- Only strictly evidenced byte-identical no-op effects 22-30 released
  ownership; the regression suite proves a real `config_write` is not released.
- Fresh official backup:
  `20260725T171620Z-switch-internal-to-openai-official`, committed.
- Official App pid `92488` spawned app-server pid `92903` from
  `/Applications/ChatGPT.app/Contents/Resources/codex`, reported
  `0.146.0-alpha.3.1`, completed initialize, mounted routes, and served config,
  model, thread, plugin, skill, and MCP requests.
- Official App log:
  `/Users/cY/Library/Logs/com.openai.codex/2026/07/25/codex-desktop-2655f576-738d-439a-b6b0-8cac444bbf1d-92488-t0-i1-172041-0.log`.
- Internal restoration backup:
  `20260725T172136Z-switch-openai-official-to-internal`, committed.
- Current ownership: ChatGPT `95489`, proxy `95838` from the exact installed
  payload, backend app-server `95842` at `/Users/cY/.local/bin/codex`,
  launcher `/Users/cY/.codex-switch/bin/codex-internal-app`.
- Fresh repository-source `status`, `verify internal --repair=none`, and
  `doctor` passed.

Fresh source closure is 4/4 focused incident tests, 219/219 transaction,
198/198 profile, strict OpenSpec 17/17, Bash 5/5, dual-runtime AST 54/54 and
imports 46/46, isolated package payload `ed5d74c1...28ab`, and
`git diff --check`.

No commit, push, tag, release, OpenSpec archive, dependency change, provider
migration, or destructive cleanup was performed.
