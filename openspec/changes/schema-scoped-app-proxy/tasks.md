# Schema-Scoped App Proxy Implementation Plan

**Goal:** Make the internal Desktop chain schema-scoped, version-safe, and
testable end to end while consolidating TOML and launcher home-sync policy.

**Architecture:** `codex_switch_protocol_adapter.py` owns exact protocol
transforms and tri-state receipts. AppServer remains the only config-write
owner. `codex_switch_config_document.py` serves offline merges only. The shell
launcher delegates preparation to canonical Python home sync.

**Tech Stack:** Python 3.12 standard library, `tomllib`, `unittest`, JSONL,
existing shell entrypoints.

## Global Constraints

- Product profiles are official and internal only.
- Current host is `/Applications/ChatGPT.app`; Codex.app is migration-only.
- No live profile/backend mutation, install, release, commit, or push.
- No production dependency or unsafe Python 3.9 parser fallback.
- Every production change records RED before GREEN.
- Main owns OpenSpec, ledger, state, shared evidence, and final integration.

## Target State

Modern internal traffic remains canonical; legacy transforms occur only at
exact proven paths. Unknown payloads survive unchanged. Proven AppServer writes
retain backend versions without a local patch; unproven writes fail before
forwarding. Offline merges understand complete TOML spans and stable skill
identity. CLI and launcher share one home-sync policy.

## Completion Contract

- [x] Every delta scenario has a focused regression.
- [x] Internal `0.142.4` modern capabilities are not downgraded.
- [x] Unknown payload fixtures round-trip byte-semantically unchanged.
- [x] No post-response config write remains.
- [x] Unproven config-write requests reach neither backend nor filesystem.
- [x] Real launcher/proxy/fake-backend lifecycle tests pass without hangs or
  interpreter-shutdown aborts.
- [x] Focused/full tests, strict OpenSpec, syntax, and diff checks pass.

## Critical Path

Protocol tracker → schema capabilities → behavioral write receipt → proxy
migration → Config Document → canonical home sync → real-chain E2E.

## 1. Protocol Adapter and Tracking

- [x] 1.1 Add RED tests in `scripts/test_codex_protocol_config.py` for exact
  model paths (`config/value/write`, `config/batchWrite.edits`, documented
  thread/turn paths), arbitrary nested payload preservation, error payloads,
  orphan/same-direction IDs, and boolean ID rejection.
- [x] 1.2 Create `scripts/codex_switch_protocol_adapter.py` with immutable
  capabilities, direction-aware pending tracking, dispatch tables, and
  copy-on-write exact transforms; make 1.1 GREEN.
- [x] 1.3 Add RED tests for canonical/legacy/unknown dynamic-tools and remote
  marketplace capabilities as independent three-state inputs; implement schema
  receipt extraction/digest validation and make them GREEN.
- [x] 1.4 Migrate `scripts/codex_switch_app_proxy.py` off recursive model and
  namespace traversal; normalize only top-level IDs in
  `thread/resume.params.history` so Desktop memory resume matches disk resume;
  omit reasoning entries that contain no portable encrypted content, content,
  or summary; prove unchanged messages preserve their input JSONL line.

## 2. Version-Safe Config Writes

- [x] 2.1 Add RED tests for a digest-bound behavioral receipt: schema-valid
  response, canonical target path, semantic preservation of unrelated MCP,
  marketplace, plugin, and skill entries, stale digest, timeout, error, and
  malformed response.
- [x] 2.2 Implement an isolated temporary-home AppServer probe with bounded
  initialize/write handling; persist only the sanitized capability result and
  backend/schema digests; make 2.1 GREEN.
- [x] 2.3 Add RED proxy tests proving a valid receipt forwards a write exactly
  once and returns the backend version unchanged, while missing/stale/failed
  receipts return a stable compatibility error before backend/file mutation.
- [x] 2.4 Delete `remember_config_write_request()` and
  `restore_config_write_response()` plus their post-response `atomic_write`;
  implement write gating and make 2.3 GREEN.
- [x] 2.5 Add response-order and concurrent pending-write tests; ensure backend
  errors, invalid path/status/version, and old generations never trigger a
  compensating write.

## 3. Semantic Offline Config Document

- [x] 3.1 Add RED tests for valid/invalid TOML, missing parser, quoted/dotted
  keys, CRLF, comments, multiline strings/arrays/inline tables, and complete
  value spans.
- [x] 3.2 Create `scripts/codex_switch_config_document.py` using `tomllib` for
  semantics and a span-only scanner; replace values in reverse offset order,
  reparse results, and make 3.1 GREEN.
- [x] 3.3 Add RED identity tests for `[[skills.config]]`: current disabled wins,
  missing restored once, duplicate/missing/non-scalar identity skipped, no path
  normalization, protected ancestor/equal/descendant paths, exact plugin
  removal, bidirectional profile convergence, and stale snapshots that retain
  marketplace/hook support without reviving usage state.
- [x] 3.4 Implement explicit skill identity and `recover_missing_from()`; migrate
  offline merge/overlay callers in `codex_switch_config.py` and TOML helpers;
  make current runtime `[plugins.*]` and `[[skills.config]]` authoritative for
  restart/switch/snapshot paths; make 3.3 GREEN without using the document
  after AppServer responses.
- [x] 3.5 Remove malformed-TOML fallback acceptance from
  `codex_switch_toml_validate.py`; use the resolved Python 3.11+ interpreter and
  prove every caller preflights before its first write.

## 4. Canonical Launcher Preparation

- [x] 4.1 Add RED tests for relative, cross-profile, dangling, live-home,
  target-home, and self-referential symlinks through the launcher preparation
  entrypoint, plus equivalence with normal switch classification.
- [x] 4.2 Add `sync_profile_app_home_for_launch()` to
  `scripts/codex_switch_home_sync.py`, composing existing validated helpers and
  preflighting config/parser state before mutation; prove launcher restart and
  normal switch use the same authoritative plugin/skill state; make 4.1 GREEN.
- [x] 4.3 Make `scripts/codex_switch_app_wrapper.py` generate a thin launcher
  pinned to resolved `CODEX_SWITCH_PYTHON`/`sys.executable`; remove duplicate
  `find`, symlink, copy/link, and embedded TOML policy.
- [x] 4.4 Add static and subprocess tests proving app-server flags before/after
  the subcommand are preserved and non-app-server commands execute the backend
  directly once.

## 5. Real-Chain Integration and Cleanup

- [x] 5.1 Extend the fake backend and add generated-wrapper E2E tests for modern
  `0.142.4`, legacy `0.140`, unknown version, write gating, response masking,
  raw payload preservation, stderr, flush, EOF, timeout, and nonzero exit.
- [x] 5.2 Remove superseded recursive/line-only helpers only after `rg` proves no
  supported caller remains; retain explicit legacy rules and diagnostics.
- [x] 5.2a Add RED current-version fixtures for
  `PluginListMarketplaceKind` and rejection of historical
  `source_type = "github"` in the behavioral probe seed.
- [x] 5.2b Recognize both historical/current marketplace definition names,
  switch the probe to a network-free local marketplace fixture, and make the
  current-version regressions plus isolated real-binary receipts GREEN.
- [x] 5.3 Run `PYTHONDONTWRITEBYTECODE=1 python3.12
  scripts/test_codex_protocol_config.py -v` and require zero failures.
- [x] 5.4 Run the complete profile suite, strict OpenSpec, shell syntax, Python
  AST/import checks, and `git diff --check`.
- [x] 5.5 Record schema/probe digests, RED/GREEN commands, changed files, exact
  compatibility limits, and E2E outcomes in
  `.planning/devflow/verification/schema-scoped-app-proxy.md`.
- [x] 5.6 Replace the daemon buffered-stdin reader with a stoppable low-level
  client-input loop, signal it when the backend exits, and join client/stdout/
  stderr forwarding before returning the exact backend status.
- [x] 5.7 Re-run the early nonzero-exit, EOF, stderr, and complete proxy/profile
  regressions; append the final integration evidence before `VER-001`.

## Execution Ledger

| Slice | Owner | Write Set | Evidence | Human Gate | Outcome | Status |
|---|---|---|---|---|---|---|
| Adapter/tracker | main | adapter/proxy/test | exact-path RED/GREEN | new schema contract | CONTINUE_NEXT_ITEM | done; tasks 1.1-1.4 complete |
| Write receipt | delegated worker | adapter/proxy/test | isolated receipt and zero-write rejection | live backend | CONTINUE_NEXT_ITEM | done; tasks 2.1-2.5 complete |
| Config Document | delegated worker then main review | config/TOML/document/test | parser/span/identity log | new dependency | CONTINUE_NEXT_ITEM | done; tasks 3.1-3.5 complete, focused 24/24, profile 136/136, runtime 55/55, transaction 211/211 |
| Launcher/E2E | delegated worker then main | wrapper/home-sync/fake test | process-chain log | live switch | CONTINUE_NEXT_ITEM | done; stoppable low-level client input, bounded stream drain, exact backend exit status |
| Final verification | main | control plane/evidence | full commands | external effects | COMPLETE | done; protocol 37/37 on both runtimes, profile 195/195, strict/static/package gates green |

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate schema-scoped-app-proxy --strict --no-interactive
bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
git diff --check
```

## Risks / Rollback

- Unproven legacy config writes become explicit errors instead of unsafe best
  effort; rebind to a probed backend is the remediation.
- Rollback restores prior adapter/proxy/wrapper modules and receipt format; no
  test touches live profile state.
