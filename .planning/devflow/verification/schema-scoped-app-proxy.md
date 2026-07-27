# Schema-Scoped App Proxy Verification

## Completion Claim

Status: `COMPLETE`.

All SAP implementation tasks and Completion Contract rows are verified.
Protocol tasks 1.1-1.4, behavioral config-write receipt tasks 2.1-2.5,
semantic Config Document tasks 3.1-3.5, canonical launcher tasks 4.1-4.4, and
integration/cleanup/final-verification tasks 5.1-5.5 are complete. No live
profile switch, App restart, install/update, plugin mutation, release, commit,
push, or rollout edit was used as completion evidence.

## Final Verification and Current-Version Closure

Completion-time isolated receipts found and repaired two current-version fixture
drifts. Installed internal `0.144.6` and bundled official
`0.146.0-alpha.3` renamed the marketplace enum from
`PluginMarketplaceKind` to `PluginListMarketplaceKind`; both still advertise
`created-by-me-remote`. They also reject historical marketplace
`source_type = "github"` in favor of `git` or `local`. The stale probe fixture
therefore produced `UNKNOWN` despite the backend still supporting safe writes.
The adapter now recognizes both schema names, and the probe uses a network-free
local marketplace fixture.

### Current Real-Binary Receipts

| Binary | Version | Backend SHA-256 | Schema SHA-256 | Receipt SHA-256 | Capabilities |
|---|---|---|---|---|---|
| internal backend | `0.144.6` | `410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6` | `7e729a107d4516c75963131f6895c41f30d03539ccc9bfb2023161a8d918acfb` | `cd8a9fe5c6dd8ff6c47b118dbaaae66ab0fd6888bc9348bf6638d824bb6620e2` | dynamic tools, remote marketplace, config-write preservation all `true` |
| ChatGPT bundled official CLI | `0.146.0-alpha.3` | `01b89e3cb5b6759c64bc7b47f3f659100e74d743750106ea586b041981f03519` | `e79fdc7ddfb838ce0d536dafe71b4260c558f615bee63948c953a64b45437a10` | `2266001bdf754a41f8dd622f26e5ed2d273ba1392129dd607f046e838e7d874e` | dynamic tools, remote marketplace, config-write preservation all `true` |

Both receipts were generated with temporary `CODEX_HOME` directories. Each
probe initialized AppServer, performed two versioned `config/value/write`
requests, received canonical `filePath/status/version`, and preserved unrelated
MCP, marketplace, plugin, and Skill config.

### Final RED / GREEN and Regression Evidence

| Gate | Result |
|---|---|
| Current-version RED | schema-name fixture returned marketplace `None`; current-config validation backend made the stale probe return `None` |
| Current-version GREEN | both focused tests passed 2/2 after dual-name extraction and the local marketplace fixture |
| Real-binary GREEN | internal `0.144.6` and official `0.146.0-alpha.3` isolated receipts returned all three capabilities `true` |
| Protocol Python 3.12 | 35/35 passed |
| Protocol Python 3.9.6 | 35/35 passed |
| Config Document Python 3.12 | 24/24 passed |
| Runtime binding Python 3.12 | 55/55 passed |
| Transaction Python 3.12 | 211/211 passed |
| Full profile Python 3.12 | 139/139 passed |
| Generated-wrapper E2E | 7/7 modern/legacy/unknown/write/lifecycle cases passed inside the protocol suite |
| Strict OpenSpec | 16/16 repository items passed; SAP strict validation passed separately |
| Python static | 47/47 AST and 42/42 production imports passed on Python 3.9.6 and 3.12 |
| Shell/static | named Bash entrypoints, removed-helper caller scan, tracked/untracked whitespace checks passed |

### SAP Changed Files

Production and entrypoints:

- `scripts/codex-switch`
- `scripts/codex_profile_switch.py`
- `scripts/codex_switch_app_proxy.py`
- `scripts/codex_switch_app_wrapper.py`
- `scripts/codex_switch_bindings.py`
- `scripts/codex_switch_config.py`
- `scripts/codex_switch_config_document.py`
- `scripts/codex_switch_home_sync.py`
- `scripts/codex_switch_protocol_adapter.py`
- `scripts/codex_switch_toml_scan.py`
- `scripts/codex_switch_toml_validate.py`
- `scripts/codex_switch_transaction.py`

Regression tests:

- `scripts/test_codex_config_document.py`
- `scripts/test_codex_profile_switch.py`
- `scripts/test_codex_protocol_config.py`
- `scripts/test_codex_runtime_binding.py`
- `scripts/test_codex_transaction.py`

Planning/evidence:

- `openspec/changes/schema-scoped-app-proxy/{proposal,design,tasks}.md`
- `openspec/changes/schema-scoped-app-proxy/specs/codex-switch/spec.md`
- `.planning/devflow/verification/schema-scoped-app-proxy.md`
- `.planning/checkpoints/2026-07-24-sap-final-verified.md`
- `.planning/STATE.md`
- `TASK_LEDGER.md`

### Final Source SHA-256

```text
c8d5e88f154fba2ee351ce8908101a6cce74c53dab65775bf7da68a10aa676c1  scripts/codex-switch
953099df79e900abad777a1ee249860cbc5ee2d0cbb46c29c2c609a07d82eae6  scripts/codex_profile_switch.py
976e340f7ab3c5112fc7a29d081e495dcf4e8fda26f8061a48c54f21682b213d  scripts/codex_switch_app_proxy.py
27916f9bbcff4be54fd663ea7975e5e841cfd8276150fab8da05ffb68f2b5a47  scripts/codex_switch_app_wrapper.py
7b6105af61c28b355b5c57672b08e5a2417e329c5d04561a6da5513e858ce600  scripts/codex_switch_bindings.py
1c6ad3eb5c7350e137e7269895bdf1d2c3d1647652a78fbbf7976fa97166aa4b  scripts/codex_switch_config.py
a28cc3e27373a9a5374cd5513eac4b59bcaa61d3074b8b4853115b0f2e9b6a41  scripts/codex_switch_config_document.py
d6ecaf359d73915fb7fb38924ffa89c5af7663f8fb5f47f561324fdc10b85137  scripts/codex_switch_home_sync.py
73085554bdaf0afd143a9615b666048f478f6e99c3aabe9d8e928e69a65bd1fd  scripts/codex_switch_protocol_adapter.py
ebc28db586d1862cbe98482a4095e482ec122d57380ad36bc889248ebbe51447  scripts/codex_switch_toml_scan.py
1e046b157294d5378f8496529b2f5a6cdb7c38ea881650ffb68b47e1a217cca1  scripts/codex_switch_toml_validate.py
9591ee92d8e8f9b8bb3d5e5a5a3e0fa0ca5b1cc42e445ed95955425f313f00f9  scripts/codex_switch_transaction.py
78bf70683a455f644667787e3b2c4534f842fb0c7dae38f1c9c82d92bf617476  scripts/test_codex_config_document.py
6e75ff589201a4fb19f0e5de491b5dbdf0f3ae44e7a7cdc71395ec37d3722d78  scripts/test_codex_profile_switch.py
cc2189b80f4e749fdd9bcd6333453c0636f17f60cd9ff0ff906fc18f7ff3e9f9  scripts/test_codex_protocol_config.py
c87e1013fa2fb48e845c294c68b810ad43ced679d50a1d72a496618861b5b8db  scripts/test_codex_runtime_binding.py
c59981f8b855a1e146a1e3db6c7f9b24f889c85fa12912098cc06cb5a8a53b64  scripts/test_codex_transaction.py
```

### Exact Compatibility Limits

- `0.140` retains only the explicit exact-path legacy dynamic-tools and remote
  marketplace conversions. It has no unsafe config-write fallback.
- Modern `0.142.4` behavior remains covered by generated-wrapper E2E and prior
  isolated receipt evidence. Current installed `0.144.6` and bundled
  `0.146.0-alpha.3` are additionally proven by fresh isolated receipts.
- Historical `PluginMarketplaceKind` and current
  `PluginListMarketplaceKind` are recognized. Missing or conflicting evidence
  remains `UNKNOWN`, preserving canonical payloads instead of deleting data.
- Config-write safety remains digest-bound and fail-closed. The real behavioral
  probe directly proves `config/value/write`; batch-write gating shares the
  same receipt and has isolated schema/proxy regression coverage.
- Receipt generation is isolated and network-free for its config fixture. Any
  unrelated backend startup network warning is not used as capability evidence.
- Source completion does not activate the worktree. The installed launcher and
  running App remain unchanged until a separately authorized rebind/restart.

## Slice 7 - Superseded Helper Cleanup

Tasks 5.2-5.3 plus current-version guards 5.2a-5.2b are complete. Caller proof
covered these removed symbols:
`matching_toml_table_blocks`, `remove_matching_toml_table_blocks`,
`top_level_assignments`, `is_array_toml_table_block`,
`table_assignment_lines`, `merge_missing_table_assignments`,
`merge_table_assignments_overlay`, `has_toml_table`,
`scan_line_structure`, `table_name_from_header`, and
`validate_toml_text_basic`. An `rg` over production and test Python sources
returned no definitions or callers after cleanup. Explicit legacy handling
remains in `codex_switch_protocol_adapter.py`, including exact `0.140`
dynamic-tools flattening and independent marketplace filtering.

### Fresh Verification

| Gate | Command | Result |
|---|---|---|
| Caller map | `rg` for all eleven removed symbols under `scripts/*.py` | no matches |
| Config Document | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_config_document.py -v` | 24/24 passed |
| Protocol Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v` | 35/35 passed |
| Protocol Python 3.9.6 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v` | 35/35 passed |
| Profile Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` | 139/139 passed |
| Static | Python 3.9.6 and 3.12 compile of the three cleanup modules plus `git diff --check` | passed |

## Slice 6 - Generated Wrapper Real-Chain E2E

Task 5.1 is complete. The fake backend now records argv, `CODEX_HOME`, restored
`PYTHONPATH`, parsed and raw JSONL, EOF, stderr, and exit behavior. Generated
wrappers run canonical `prepare-launch` before the proxy and backend. The matrix
proves modern `0.142.4` pass-through, exact `0.140` legacy transforms, unknown
capability preservation, proven write forwarding, unproven write rejection,
response masking, byte-preserved unknown CRLF payloads, pre-EOF flush, bounded
stream drain, and backend exit-code authority.

The process review found three lifecycle defects. A 20 MB final JSONL response
was lost when the proxy returned immediately after `backend.wait()`. Waiting
without a bound then hung when a backend descendant retained stdout/stderr.
Finally, an early nonzero backend exit leaked a `BrokenPipeError` thread
traceback. The proxy now drains backend stdout/stderr against one two-second
deadline, emits one stable timeout diagnostic if inherited pipes remain open,
returns the backend status, and suppresses only expected closed-pipe exceptions
on the client-to-backend thread.

### RED / GREEN Evidence

| Stage | Command | Result |
|---|---|---|
| EOF RED | focused generated-wrapper lifecycle test with a 20 MB final response and backend exit 23 | failed: client received only the initialize response |
| Drain-timeout RED | focused inherited-pipe test with backend exit 19 | failed with `TimeoutExpired` after 5 seconds |
| Early-exit RED | focused backend-exit-before-read test with exit 29 | failed because stderr contained `Exception in thread` and `BrokenPipeError` |
| E2E GREEN | seven `test_generated_wrapper_proxy_chain_*` tests | 7/7 passed |
| Protocol Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v` | 34/34 passed |
| Protocol Python 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v` | 34/34 passed |
| Static | dual-runtime source compile, strict SAP OpenSpec, and `git diff --check` | passed |

Current SHA-256: proxy
`976e340f7ab3c5112fc7a29d081e495dcf4e8fda26f8061a48c54f21682b213d`;
protocol test
`cc2189b80f4e749fdd9bcd6333453c0636f17f60cd9ff0ff906fc18f7ff3e9f9`.
No live profile, App, install/update, plugin, release, or Git publication action
ran. The subsequent cleanup evidence is recorded above.

## Slice 5 - Canonical Launcher Preparation

Tasks 4.1-4.4 are complete. The managed launcher now calls
`codex_switch_home_sync.py prepare-launch` through its generation-time validated
Python 3.11+ interpreter. It contains no independent `find`, runtime/non-shared
classifier, copy/link loop, embedded TOML program, or direct auth deletion.
Non-app-server commands still reach the backend exactly once through proxy
`execve`; app-server argv before and after the subcommand remains unchanged,
and the backend receives the caller's original `PYTHONPATH`.

`sync_profile_app_home_for_launch()` parses the canonical profile, shared live,
and existing target configs and computes target config, Plugin/Skill snapshots,
and bidirectional Desktop settings before the first managed mutation. It then
removes every isolated runtime/non-shareable symlink, synchronizes only safe
shareable entries, writes authoritative usage state, refreshes snapshots, and
applies the existing no-auth internal policy. Shareable source symlinks fail
closed when relative, dangling, self-referential, or resolved within source or
target profile homes; absolute external links remain allowed. Normal switch
planning and `FilesystemAdapter.sync_shared_entry()` use the same classifier.

### RED / GREEN Evidence

| Stage | Command | Result |
|---|---|---|
| Initial RED | four focused launcher/switch tests in `scripts/test_codex_profile_switch.py` | 4/4 failed: wrapper policy remained embedded, five isolated links survived normal switch, three unsafe source links propagated, and malformed live TOML mutated a stale link first |
| Initial GREEN | same four focused tests | 4/4 passed |
| Review RED | unsafe-shareable plus preflight tests after adding a target-home symlink alias and malformed canonical profile config | 2/2 failed on the newly asserted boundary |
| Review GREEN | same two focused tests | 2/2 passed after resolved-target classification and explicit profile-config preflight |
| Launcher regression | ten `internal_switch_refreshes_desktop_wrapper` / `internal_desktop_wrapper*` tests | 10/10 passed |
| Shared sync regression | three `shared_support_*` tests | 3/3 passed |
| Full profile | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` | 139/139 passed |
| Transaction | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py` | 211/211 passed |
| Config Document | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_config_document.py -v` | 24/24 passed |
| Runtime binding | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py` | 55/55 passed |
| Protocol | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v` | 27/27 passed |
| Static | `/usr/bin/python3` 3.9.6 and Python 3.12 `py_compile` of the four launcher-slice files, strict SAP OpenSpec, Bash syntax, and `git diff --check` | passed |

Main review found and repaired the lexical-only target-home check and the
canonical profile-config preflight gap. No actionable task 4.x finding remains.
Task 5.1 is dependency-ready.

## Slice 4 - Semantic Config Document and Caller Migration

Tasks 3.1-3.5 are complete. `codex_switch_config_document.py` uses `tomllib`
for all TOML semantics and a source scanner only for complete assignment/table
spans. It decodes quoted and dotted keys semantically, preserves comments and
CRLF, replaces complete multiline string/array/inline-table values in reverse
offset order, reparses changed output, and returns the original document for a
semantic no-op. Python without `tomllib` fails closed with Python 3.11+
guidance. `[[skills.config]]` recovery uses the parsed scalar `path` as its
lexical identity, skips ambiguous or unknown array entities with stable
diagnostic codes, and honors protected ancestor/equal/descendant paths.

Offline merge/overlay callers now use the Config Document seam. Current
`[plugins.*]` and `[[skills.config]]` usage state is authoritative across
switch, restart, and snapshot paths; stale fallbacks recover only marketplace
and hook support metadata. The shell wrapper resolves Python 3.11+ with
`tomllib`, generated app wrappers pin a validated interpreter, and direct
Python 3.9 entry fails before profile state mutation. The legacy basic TOML
scanner is no longer an accepted validation fallback.

### RED / GREEN Evidence

| Stage | Command | Result |
|---|---|---|
| RED | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_config_document.py -v` before the module existed | 8/8 failed because `ConfigDocument` was absent |
| Table-span RED | same focused command after assignment-span GREEN | 1/9 failed because complete table spans were absent |
| Foundation GREEN | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_config_document.py -q` | 9/9 passed |
| Identity/caller RED | focused Config Document and profile selections before identity/caller migration | duplicate/current-disabled Skill and stale usage-state cases failed as recorded in Slice 2 |
| Complete GREEN | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_config_document.py -v` | 24/24 passed |
| Python 3.9 parser smoke | import module and parse one valid document | failed closed with Python 3.11+ guidance |
| Runtime binding | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -q` | 55/55 passed |
| Transaction first run | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -q` | 209/211; two adopted-home cases exposed an old non-TOML sentinel fixture |
| Transaction regression | focused adopted-home authority test after replacing the sentinel with valid TOML | 1/1 passed with byte-exact restore and mode assertions retained |
| Transaction full rerun | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -q` | 211/211 passed |
| Full profile | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py -q` | 136/136 passed |
| Protocol Python 3.12 / 3.9 | `scripts/test_codex_protocol_config.py -q` under each interpreter | 27/27 passed on each |
| Static | Python 3.9 and 3.12 syntax compile of 7 affected files, strict OpenSpec, Bash syntax, and `git diff --check` | passed |

Main review found no remaining task 3.x blocker. `rg` proves the superseded
line-only table helpers have no supported caller; their definitions remain
temporarily for the explicit task 5.2 cleanup gate.

## Slice 3 - Version-Safe Config-Write Receipt

Tasks 2.1-2.5 are complete in the worktree:

- schema generation and the behavioral write probe run in isolated temporary
  homes with bounded subprocess handling;
- the persisted schema-v2 receipt contains only backend/schema digests and
  tri-state capability results;
- the managed launcher supplies the receipt path and expected schema digest;
- the proxy accepts only a regular, parseable receipt whose backend and schema
  digests match;
- proven config writes reach the backend exactly once and preserve its response
  and version;
- missing, unsafe, malformed, stale, or old-generation receipts produce the
  stable compatibility error before backend or config-file mutation;
- response reordering, same-ID server requests, backend errors, invalid
  responses, and concurrent pending writes never trigger a compensating file
  write;
- the former post-response snapshot/restore config repair path has been
  removed; the remaining proxy `atomic_write` records only the optional child
  process diagnostic receipt and never writes `config.toml`.

### Fresh Verification

| Gate | Command | Result |
|---|---|---|
| Python 3.12 focused | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v` | 27/27 passed |
| Python 3.9 focused | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v` | 27/27 passed |
| Runtime binding Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -q` | 55/55 passed |
| Runtime binding Python 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -q` | 55/55 passed |
| Transaction Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -q` | 211/211 passed |
| Transaction Python 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_transaction.py -q` | 211/211 passed |
| Strict OpenSpec | `openspec validate schema-scoped-app-proxy --strict --no-interactive` | valid |
| Static | Python 3.9 and 3.12 `py_compile` of 9 affected files plus `git diff --check` | passed |
| Integrity | SHA-256 of adapter, proxy, wrapper, bindings, transaction, and three test files | unchanged from review baseline |

### Review Closure

Main review found and repaired the missing `stat` import, schema/probe child
process cleanup, unbounded schema stdout buffering, receipt symlink TOCTOU, and
dangling rebind-marker recovery bypass. The final review confirmed bounded
probe cleanup, digest and launcher authority, request ordering, fail-closed
diagnostics, and absence of a post-response config write. Two protocol failures
seen only while six heavy suites ran concurrently did not reproduce in isolated
runs; both Python versions passed 27/27 before the adjacent suites and static
gates were rerun.

## Slice 2 - Authoritative Plugin/Skill Usage State

The reproduced uninstall/restart defect is repaired in source. Current runtime
`[plugins.*]` and `[[skills.config]]` blocks are authoritative usage state:

- official/internal switches replace destination usage state exactly;
- internal Desktop restart copies the current internal usage state to the
  shared base before rebuilding the app home;
- stale target runtimes, profile layers, and snapshots recover only non-usage
  marketplace/hook support metadata;
- snapshot refresh copies runtime usage exactly and cannot revive removed
  plugins or duplicate an older enabled Skill over `enabled = false`.

### RED / GREEN Evidence

| Stage | Command | Result |
|---|---|---|
| RED | focused 8-test profile command for legacy layer, target runtime, source/target snapshot, bidirectional removal, disabled Skill, snapshot refresh, and wrapper restart | 8/8 failed on stale usage restoration; disabled Skill path appeared twice |
| GREEN focused | same Python 3.12 focused command | 8/8 passed |
| Full profile Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12 scripts/test_codex_profile_switch.py` | 129/129 passed |
| Full profile Python 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_profile_switch.py` | 129/129 passed |
| Protocol regression | `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12 scripts/test_codex_protocol_config.py -v` | 17/17 passed |
| Focused transaction | shared internal switch, shared official switch, and plugin-snapshot drift tests | 3/3 passed |
| Full transaction | `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12 scripts/test_codex_transaction.py` | 205/207; two existing store-mode assertions expect `0755` while the current process umask creates `0700` |
| Strict OpenSpec | `openspec validate schema-scoped-app-proxy --strict --no-interactive` | valid |
| Static | Python 3.12 compile and `git diff --check` | passed |

### Changed Behavior

- `codex_switch_config.py` classifies Plugin/Skill usage separately from
  recoverable support metadata and provides exact usage replacement.
- `codex_switch_home_sync.py` excludes usage state from target runtime,
  profile-layer, and snapshot fallback merges.
- `codex_switch_app_wrapper.py` propagates the internal runtime's exact usage
  state before rebuilding the managed app home.
- `codex_switch_transaction.py` no longer unions older usage blocks into the
  snapshot planned for commit.
- Profile regression coverage now encodes removal in both switch directions,
  disabled Skill identity, stale snapshot non-revival, and restart behavior.

No live profile, App, plugin, install, release, network publication, commit, or
push ran. This slice does not complete the broader Config Document or canonical
launcher tasks.

## Slice 1 - Pure Protocol Adapter Foundation

Tasks 1.1-1.4 are complete. The production proxy now uses only the exact
adapter and direction-aware tracker for JSONL traffic.

### RED / GREEN Evidence

| Stage | Command | Result |
|---|---|---|
| RED | `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -q` | missing `codex_switch_protocol_adapter` failed as expected |
| GREEN Python 3.9 | `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -q` | 14/14 passed |
| GREEN Python 3.12 | `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12 scripts/test_codex_protocol_config.py -q` | 14/14 passed |
| Strict OpenSpec | `openspec validate schema-scoped-app-proxy --strict --no-interactive` | valid |
| Static | dual-runtime AST/import and `git diff --check` | passed |
| Resume RED | focused adapter and proxy tests | local UUID remained in `thread/resume.params.history` |
| Resume GREEN Python 3.9 | protocol 16/16 plus proxy 8/8 | passed |
| Resume GREEN Python 3.12 | protocol 16/16 plus proxy 8/8 | passed |
| Real rollout fixture | 78-item history from thread `019f8dfb-ab5e-7f51-a8ba-86c5653a891c` | 78/78 top-level IDs removed; source unchanged |
| JSONL migration RED | focused proxy import/tests | `adapt_client_json_line` and `adapt_backend_json_line` were absent |
| JSONL migration GREEN Python 3.9 | protocol 17/17, app-proxy 12/12 | passed |
| JSONL migration GREEN Python 3.12 | protocol 17/17, app-proxy 12/12 | passed |
| Launcher routing RED | generated wrapper with `-c features.code_mode_host=true app-server --analytics-default-enabled` | backend ran directly and no proxy-child receipt was created |
| Launcher routing GREEN Python 3.9 / 3.12 | generated-wrapper subprocess test | proxy child received all four arguments in order; `--version` executed the backend once |
| Runtime suite Python 3.9 / 3.12 | `scripts/test_codex_runtime_binding.py -q` | 53/53 passed on each |
| Profile suite Python 3.9 / 3.12 | `scripts/test_codex_profile_switch.py -q` | 127/127 passed on each |
| Current affected rollout | thread `019f8e16-477d-79d3-b968-cf41d15446b4` | 56 source items, 13 opaque reasoning entries removed, 43 forwarded; source SHA-256 remained `fc30a6a0710038add99920dedf9a4850187de24562bfa7e30a3621d6522f7800` |
| Independent review closure | direction-aware config restore, binary JSONL, legacy marketplace/model-list compatibility, non-Codex rejection, backend environment isolation | all actionable findings fixed; complete dual-runtime suites rerun |
| Strict/static | both affected OpenSpec changes, `py_compile`, imports, `git diff --check` | passed |

### Implemented, Isolated Behavior

- Exact model translation for documented config/value, batch-edit,
  thread/start, turn/start, and realtime/start request paths.
- Exact model masking for model-list, config-read, and documented thread
  response/notification paths; error, tool-schema, metadata, writes, unknown
  methods, and arbitrary nested payloads remain unchanged.
- Copy-on-write result identity so an unchanged parsed message can retain its
  original JSONL line when proxy migration is completed.
- Direction-aware pending request tracking; server requests, orphan responses,
  and boolean IDs cannot consume a client request.
- Independent `true | false | unknown` capabilities for canonical dynamic
  tools, the remote marketplace kind, and behavioral config-write safety.
- Backend and generated-schema SHA-256 receipt binding with strict receipt
  schema validation.
- Exact `thread/resume.params.history[*].id` removal so Desktop memory-history
  resume matches disk-resume request construction while preserving order,
  content, `call_id`, nested metadata, and the source message.
- Opaque reasoning omission only when `encrypted_content`, `content`, and
  `summary` are all empty.
- Token-aware launcher routing for global options before `app-server`; the
  original argv is preserved, while non-app-server commands `exec` the backend
  exactly once.
- Binary stdio preserves unchanged JSONL bytes, including CRLF; changed JSON
  is emitted as canonical UTF-8 JSONL.
- Config-write restoration runs only for the matching backend response, not a
  same-ID server request. Backend processes receive the caller's original
  `PYTHONPATH`, not the proxy import path.

## Active Safety Boundary

Recursive client/server model and namespace traversal has been removed from the
production proxy. Digest-bound behavioral receipts now gate config writes
before forwarding, the old post-response config patch is gone, and launcher
home preparation now uses the canonical Python seam. Full SAP completion
remains open on final verification and evidence tasks 5.4-5.5.

The installed `0.1.13` release still has neither the protocol adapter nor the
new argv dispatcher. The authorized scoped rebind instead committed a managed
launcher with `SWITCH_SCRIPTS=/Users/cY/dev/codex-switch/scripts`; it did not
install the unfinished worktree. The existing ChatGPT process still runs
`/Users/cY/.local/bin/codex -c features.code_mode_host=true app-server
--analytics-default-enabled` directly, so the source fix is configured but will
not become active until ChatGPT is fully restarted.

## Scoped Live Rebind Evidence

- Backup:
  `/Users/cY/.codex-switch/backups/manual-20260723T103336Z-resume-proxy-rebind`.
- Command:
  `./scripts/codex-switch set-bin internal /Users/cY/.local/bin/codex`.
- Backend: `codex-cli 0.144.6`.
- Committed manifest SHA-256:
  `a60648ce4819ff7ba28fb825fa725ac62388fc44f089dcbe565440dea41aaeaf`.
- Committed launcher SHA-256:
  `f3854fe0b509b09cdccd79722c5b1c35e904812ef0310e14afbe511642920f6d`.
- Committed-launcher smoke: passed; child receipt recorded backend
  `/Users/cY/.local/bin/codex` and argv
  `["app-server", "--analytics-default-enabled"]`.
- Restart state: pending; no ChatGPT exit/reopen or rollout mutation ran.

## Exact Resume Point

1. Run task 5.4 complete profile/adjacent regression, strict OpenSpec, shell,
   dual-runtime Python compile/import, and diff gates.
2. Complete task 5.5 by reconciling final digests, commands, changed files,
   compatibility limits, and E2E outcomes in this record.
3. Obtain explicit authorization before any additional install/rebind or live
   rollout modification.

## Verified Baseline Available for Internal Continuation

- TPS: 207/207 transaction tests under Python 3.9 and 3.12.
- CRB: 53/53 runtime binding tests under Python 3.9 and 3.12.
- Legacy CLI: 127/127 under Python 3.9 and 3.12 after the incident regressions.
- CRB strict OpenSpec, Shell, dual-runtime AST/import, and diff gates passed.

A scoped live internal manifest/launcher rebind was performed after explicit
authorization. No app restart, launchctl change, installed-release update,
rollout mutation, release, network publication, commit, or push ran.

## Backend Early-Exit Integration Closure

The reopened lifecycle work is complete. The proxy no longer leaves a daemon
thread blocked in Python's buffered `sys.stdin` reader when the backend exits
first. Client input uses `select` plus `os.read`, observes a stop event, closes
the backend pipe on EOF or exit, and participates in the bounded client/stdout/
stderr drain before the exact backend status is returned. Early nonzero exit,
large final EOF output, stderr forwarding, inherited-pipe timeout, and
response-before-client-EOF regressions all pass without `BrokenPipeError`,
thread traceback, or interpreter-shutdown abort.

Fresh final-source evidence:

- Protocol adapter/proxy: 37/37 on Python 3.12 and 37/37 on system Python 3.9.
- Runtime Binding: 55/55 on both runtimes.
- Config Document: 24/24 on Python 3.12.
- Verifier: 22/22 on Python 3.12 and 22/22 under system Python 3.9 with the
  required Python 3.12 Desktop-wrapper runtime.
- Transaction: 215/215 on Python 3.12.
- Complete profile suite: 195/195 on Python 3.12.
- Strict OpenSpec, Bash syntax, dual-runtime AST/import, workflow, isolated
  package, and `git diff --check` gates passed.

This closes completion rows 6-7 and tasks 5.6-5.7. Live App startup and task
entry remain rollout evidence, not source-test evidence.
