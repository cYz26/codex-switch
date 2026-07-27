## Context

`repair-plugins` already refreshes marketplace snapshots and parses
`codex plugin list --available --json`, but it reduces that JSON to a selector
set. It then calls `plugin add` only for enabled selectors whose cache root is
empty. A local marketplace plugin can therefore change while retaining its
version and remain stale indefinitely.

The current Codex JSON contract exposes `pluginId`, `version`, and
`source: {"source": "local", "path": ...}` for installed and available
plugins. The existing runtime-binding module separately resolves the canonical
official ChatGPT bundled CLI, the internal backend CLI, and each profile's
actual `CODEX_HOME`. Those two existing contracts are sufficient for a
deterministic CLI-only refresh.

## Skill Routing Ledger

- artifact-status: final
- capability-research: used; current Codex plugin help/JSON, local marketplace
  metadata, cache layout, runtime binding, and process observation APIs were
  inspected
- decision-resolution: used; refresh only provable source/cache drift and
  defer active-runtime replacement
- decision-grilling: skipped; the user approved the target sequence and no
  product decision remains open
- implementation-planning: used through DevFlow and this OpenSpec change
- architecture-guidance: skipped; the change extends existing plugin repair,
  runtime-binding, and process-observation boundaries without a new subsystem
- domain-language-modeling: skipped; selector, source, version, cache, and
  profile runtime are already stable domain terms
- openspec-routing: required and used
- Open Questions: none

## Goals / Non-Goals

**Goals:**

- Run plugin maintenance through the target product profile's canonical CLI
  and explicit target `CODEX_HOME`, independent of whether ChatGPT has been
  restarted.
- Refresh marketplace/catalog state, detect inspectable enabled-plugin cache
  drift, and call `plugin add` only for missing or provably stale selectors.
- Preserve existing unavailable-plugin and dry-run truthfulness.
- Prevent same-version cache replacement underneath a target profile
  app-server that is already running.
- Keep one-key order as switch, plugin refresh, verify, Doctor, status.

**Non-Goals:**

- Refreshing project-local DevFlow/OpenSpec configuration or skill links.
- Reinstalling every enabled plugin.
- Comparing remote sources that Codex does not expose as a local snapshot.
- Stopping or restarting ChatGPT automatically.
- Removing old version directories or runtime residue from installed caches.

## Decisions

### Decision 1: Resolve one plugin-maintenance runtime

For `internal` and `openai-official`, `repair_profile_plugins` calls
`resolve_store_runtime_binding()`, executes `binding.backend_cli`, and sets
`CODEX_HOME=binding.codex_home`. It first runs `--version` through that same
environment and reports the resolved path/version before marketplace work.
Custom profiles retain their existing manifest `codex_bin` and profile-home
fallback because canonical product binding intentionally rejects arbitrary
profile names.

Using the shell `codex` or the currently running app-server was rejected:
neither proves ownership of the target profile. Requiring an App restart before
the maintenance command was also rejected because CLI process selection and
Desktop process lifetime are independent.

### Decision 2: Preserve structured catalog entries

Replace selector-only parsing with a frozen catalog entry containing selector,
version, and an optional local source path. Recursive parsing remains tolerant
of the current `installed`/`available` envelope and field aliases, but a cache
is inspectable only when:

- selector and version are non-empty and the version is a safe path segment;
- `source.source` is `local`;
- `source.path` is an absolute existing directory; and
- its `.codex-plugin/plugin.json` name/version match the catalog entry.

Selectors without this evidence remain available for existing missing-plugin
logic but are skipped for stale-cache comparison with a truthful diagnostic.
Guessing a path from marketplace configuration was rejected because the Codex
catalog already resolves local, bundled, git-snapshot, and curated layouts.

### Decision 3: Compare deterministic tree manifests

For the catalog version, compare the source tree with
`plugins/cache/<marketplace>/<plugin>/<version>`. The manifest records relative
path, entry type, file SHA-256, symlink target, and executable-bit state.
Ignore `.git`, `__pycache__`, Python bytecode, `.DS_Store`, and standard
tool-cache residue that is not plugin payload.

If the version directory is absent, or its manifest differs, classify the
selector as stale. If manifests match, perform no install. Timestamps,
ownership, and non-executable permission bits are excluded because Codex cache
materialization may legitimately normalize them.

### Decision 4: Keep missing, unavailable, and stale classifications separate

After catalog refresh:

- missing plus available: existing `plugin add` behavior;
- missing plus unavailable: existing skip/optional disable behavior;
- installed plus inspectable and equal: no-op;
- installed plus inspectable and different: stale refresh candidate;
- installed plus uninspectable: diagnostic-only skip.

Each selector is added at most once even if it appears in more than one
classification. Dry-run does not inspect the refreshed catalog and therefore
prints only conditional actions, never a concrete `plugin add` claim.

### Decision 5: Fail closed on active target app-server replacement

Process observation is collected only after stale candidates are known. A
candidate is blocked when an observed app-server matches the target binding's
Desktop CLI/proxy chain. `repair-plugins` exits with actionable remediation:
quit ChatGPT completely, rerun repair, then reopen it. Missing-plugin behavior
is unchanged.

Silently hot-replacing was rejected because open tasks can retain hooks and
skills from the old cache. Silently returning success after deferral was also
rejected because the one-key flow would otherwise claim a current cache that it
did not install.

### Decision 6: Reuse the existing one-key orchestration point

No new App callback or conversation-side action is introduced.
`scripts/codex-switch` already invokes `repair-plugins` after the switch and
before verification and Doctor, so extending that command automatically
extends normal CLI profile switches. Project-local workflow refresh remains a
separate, explicitly authorized operation.

## Completion Contract

- Stale inspectable enabled caches invoke one target-profile `plugin add`.
- Current inspectable caches invoke no `plugin add`.
- Missing and unavailable compatibility behavior remains covered.
- Canonical CLI path, `--version`, and explicit target `CODEX_HOME` are
  observed in tests.
- Uninspectable sources and dry-run output do not overclaim.
- A matching running target app-server blocks stale replacement with
  remediation.
- One-key output proves refresh occurs before verification and Doctor.
- Focused, full profile-suite, Python compatibility, OpenSpec, syntax, and diff
  checks pass.

## Critical Path

Structured catalog parsing -> tree manifest comparison -> stale classification
-> active-runtime gate -> one-key regression -> full verification.

## Incidental Finding Budget

One bounded RED/GREEN guard may cover an existing plugin JSON shape or
profile-home compatibility issue. Project migration, plugin removal, App
lifecycle control, public option expansion, or unrelated runtime-binding work
is `BLOCKED_AWAITING_HUMAN`.

## Risks / Trade-offs

- [Codex changes catalog JSON shape] -> keep recursive aliases and treat
  incomplete records as uninspectable rather than reinstalling.
- [Runtime residue causes false drift] -> exclude only named non-payload
  residue and retain file content, type, symlink, and executable-bit checks.
- [A source changes during comparison] -> `plugin add` remains the only writer;
  a later run re-evaluates source/cache parity.
- [A target app-server cannot be identified conclusively] -> only a positively
  matching target chain blocks; unrelated running profiles do not.
- [Official tests could execute the workstation CLI] -> use isolated internal
  CLI integration fixtures and injected binding tests for official resolution.

## Migration Plan

There is no eager cache migration. The next explicit `repair-plugins` or normal
one-key profile switch evaluates current state and refreshes only confirmed
drift. Rollback restores the previous plugin module and leaves caches/config
untouched; no new persisted format is introduced.

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_stale_local_plugin_cache
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_codex_profile_switch.py
python3.9 -m py_compile scripts/codex_switch_plugins.py
python3.12 -m py_compile scripts/codex_switch_plugins.py
openspec validate refresh-stale-profile-plugin-caches --strict
bash -n scripts/codex-switch
git diff --check
```

## Continuation Policy

- Execution policy: `auto-until-terminal`.
- Canonical execution source: this change's `tasks.md`.
- Continue through RED/GREEN, integration, documentation, and final
  verification without routine confirmation.
- Genuine Human Gates: a new dependency, App lifecycle automation, destructive
  cache cleanup, project migration, release, install, commit, push, or archive.

## Open Questions

None.
