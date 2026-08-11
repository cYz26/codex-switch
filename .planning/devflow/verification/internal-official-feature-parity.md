# Internal Official Feature Parity Verification

## 2026-07-26 Reference Policy RED

Timestamp: 2026-07-26 08:06:17 +0800
Tasks: 1.1-1.2
Result: expected RED captured

### Preflight

- OpenSpec apply state: ready, 0/79 complete before this slice.
- Test-first capability: ready through the trusted project-local `tdd` skill.
- ChatGPT bundled CLI: `codex-cli 0.146.0-alpha.3.1`,
  SHA-256 `6d8be49e49751554df16572369e636cbe02c84b208cad3dc35528c846eeca223`.
- Internal CLI: `codex-cli 0.144.6`,
  SHA-256 `410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6`.
- ChatGPT bundle id: `com.openai.codex`.
- Read-only status retained the internal managed launcher/proxy/backend chain.

### Changed Files

- `scripts/test_codex_parity.py`

### RED Evidence

Syntax parse:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 -c <AST parse>
exit 0
syntax-ok
```

Focused RED:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
exit 1
ModuleNotFoundError: No module named 'codex_switch_parity'
```

The failure is expected because task 1.3 has not created the production parity
module. No test reached an unrelated assertion or fixture failure.

### Boundaries

No production module, live profile/App state, provider traffic, retained probe,
dependency, release, archive, or Git history was modified.

### Next Item

Task 1.3: create the immutable parity foundation records and canonical
reference/internal fingerprint validation, then make the focused suite GREEN.

## 2026-07-26 Reference Foundation GREEN

Timestamp: 2026-07-26 10:07:41 +0800
Task: 1.3
Result: complete

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### GREEN Iteration

The first production attempt ran all seven tests. Four passed and the remaining
tests reported eight errors from one cause:

```text
TypeError: Object of type mappingproxy is not JSON serializable
```

The canonical JSON boundary now converts the top-level read-only mapping to a
plain dictionary before deterministic `json.dumps` encoding. No test or public
contract was weakened.

### Final Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 7 tests in 0.050s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 7 tests in 0.052s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
Ran 55 tests in 26.205s
OK
```

Python 3.12 and system Python 3.9 AST checks passed for the new module and
test. A system-Python import smoke printed policy version `1`. Focused
`git diff --check` passed.

### Review

- Runtime Binding still owns executable, launcher, and Desktop-host authority.
- Only `scripts/test_codex_parity.py` imports the new parity module.
- PATH observations cannot replace the bundled CLI.
- `network-latest` cannot be constructed as reference authority.
- The allowed-difference set is exactly binary, model, endpoint, provider, and
  auth.
- Official and internal fingerprint changes invalidate stored evidence.

### Boundaries and Residual Work

No feature-list execution, schema comparison, classification table, receipt,
overlay, config projection, probe, caller integration, live effect, dependency,
release, archive, or Git history mutation ran. Task 1.4 is dependency-ready.

## 2026-07-26 Feature Inventory RED

Tasks: 1.4
Result: expected RED captured

### Capability Evidence

- `authoritative_current`: both bundled `0.146.0-alpha.3.1` and internal
  `0.144.6` expose `codex features list` as "List known features with their
  stage and effective state".
- `local_scan`: the repository contains no existing feature-list parser or
  inventory owner. Existing bounded subprocess code is coupled to verifier or
  app-server ownership and cannot be imported without creating a future
  verify/parity cycle.
- `comparison`: isolated official/internal temporary homes produce the same
  three-column name/stage/effective format. An isolated internal override
  `-c features.multi_agent_v2=true` changes only that feature's effective
  boolean while retaining its stage.
- `contract`: parity will own a private strict parser and injected bounded
  feature-list runner. Tests supply fixture results and never read or write
  workstation config.
- `assumptions`: the command's current text format is version-bound by the CLI
  fingerprints. Unknown stages, malformed rows, duplicate names, timeout,
  truncation, or nonzero exit fail closed.

The isolated capability checks used new `/tmp/codex-parity-features-*`
directories and did not point either CLI at the live CODEX_HOME.

### RED Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 -c <AST parse>
exit 0
syntax-ok
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
exit 1
ImportError: cannot import name 'FeatureCommandRequest' from
'codex_switch_parity'
```

The missing public feature inventory seam is the expected failure. Task 1.5 is
next.

## 2026-07-26 Feature Inventory GREEN

Timestamp: 2026-07-26 10:17:46 +0800
Task: 1.5
Result: complete

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

The parity module now:

- runs `codex features list` with an exact injected request contract;
- supplies an isolated `CODEX_HOME` without reading or writing live config;
- bounds execution time and both output streams and terminates the process
  group on timeout;
- parses only the current fingerprint-bound three-column feature format;
- records isolated default and effective state separately;
- rejects malformed, duplicate, stage-changing, nonzero, timeout, or truncated
  evidence;
- retains official-only and internal-only features during comparison; and
- sorts records before canonical JSON encoding so identical input is
  byte-identical.

### Final Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 12 tests in 0.052s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 12 tests in 0.053s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
Ran 55 tests in 24.070s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v
Ran 55 tests in 24.793s
OK
```

Python 3.12.13 and system Python 3.9.6 both passed AST and import checks for
`codex_switch_parity.py`. The DevFlow dependency check reported
`test-first-execution` ready. Its existing legacy `.codex/skills` layout
recommendations are nonblocking and were not applied.

### Boundaries and Next Item

No live config, profile/App state, provider traffic, schema comparison,
classification, receipt, overlay, probe, caller integration, retained-probe
cleanup, dependency, release, archive, or Git history mutation ran. Task 1.6 is
dependency-ready.

## 2026-07-26 Protocol Inventory RED

Task: 1.6
Result: expected RED captured

### Changed Files

- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Test Contract

The new tests define one parity-owned protocol seam. They cover all four
generated protocol roots, method extraction, local transitive reference
closure, documentation-field removal, deterministic ordering, side-only method
retention, actual producer direction, additive optional compatibility,
required/enum incompatibility, reference cycles, and unsupported constructs.
They do not import or modify Protocol Adapter policy.

### RED Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 -c <AST parse>
exit 0
syntax-ok
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
exit 1
ImportError: cannot import name 'ProtocolInventory' from
'codex_switch_parity'
```

The failure is the intended missing production seam. Task 1.7 is next.

## 2026-07-26 Protocol Inventory GREEN

Task: 1.7
Result: GREEN and retained real-schema comparison passed

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

The parity module now:

- extracts every method from the four generated protocol roots;
- expands transitive local `#/definitions/...` references;
- removes documentation-only schema fields and canonicalizes ordering;
- retains official-only and internal-only methods;
- selects official as producer for client messages and internal as producer
  for server messages;
- evaluates additive fields, required fields, enums, types, arrays,
  constraints, unions, intersections, and explicit additional-property rules;
- preserves valid Draft-07 boolean schemas in properties, array items, and
  combinator branches; and
- rejects cycles, tuple-form array items, foreign references, and unsupported
  schema keywords with stable fail-closed codes.

Protocol Adapter remains unchanged and contains no parity policy.

### Follow-on RED Guards

The first retained real-schema replay failed before inventory completion:

```text
ParityValidationError:
Tuple-form protocol array items are unsupported.
```

Inspection proved the actual value was valid `items: true`, not tuple-form
items. The focused regression failed at the same boundary:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py \
  ParityProtocolInventoryTests.test_boolean_array_items_use_subset_semantics -v
exit 1
ParityValidationError: Tuple-form protocol array items are unsupported.
```

Three additional false-health guards were captured before their fixes:

```text
test_boolean_property_schemas_use_subset_semantics
AssertionError: True is not false

test_additional_properties_default_uses_subset_semantics
AssertionError: True is not false

test_boolean_combinator_branches_use_subset_semantics
AssertionError: True is not false
```

### Final Focused Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 25 tests in 0.047s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 25 tests in 0.050s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
Ran 55 tests in 24.674s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v
Ran 55 tests in 25.431s
OK
```

Python 3.12.13 and system Python 3.9.6 both passed AST parsing and production
import of `codex_switch_parity.py`. The source-owned DevFlow dependency check
reported `test-first-execution` ready with no failed required checks. The
authority scan found no protocol-inventory or parity finding implementation
outside `codex_switch_parity.py` and its focused test. `git diff --check`
passed.

### Retained Real-Schema Evidence

Both Python runtimes produced the same result from the retained generated
schema directories:

```text
official 347 208 323adadf709882fe18aba53c76e5fa4a2310ac1d87ce895ebb9b0fc6e28ca146
internal 337 202 880578b7724156225e5f3bff4268d92be3b980de842ba9e1223466056438a9c1
comparison 208 15 6
```

The 15 raw native incompatibilities contain seven enum, four array-item, four
missing-method, and four type reason-code occurrences. The six side-only
methods are `app/installed`, `app/read`, `environment/status`,
`thread/searchOccurrences`, `thread/environment/connected`, and
`thread/environment/disconnected`. This is inventory evidence only; policy
classification remains task 1.10-1.11.

### Boundaries and Next Item

No classification, receipt, overlay, config projection, probe, caller
integration, live profile/App/provider mutation, retained-schema cleanup,
dependency, release, archive, or Git history mutation ran. Task 1.8 is
dependency-ready.

## 2026-07-26 Protocol Adapter Rule-Set Digest RED

Task: 1.8
Result: expected RED captured

### Changed Files

- `scripts/test_codex_protocol_config.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Test Contract

Two `ProtocolAdapterEvidenceTests` require:

- one public `protocol_adapter_rule_set_digest()` seam;
- deterministic lowercase SHA-256 output;
- canonical digest stability when mapping insertion order changes;
- digest changes when any request, response, or notification model-path table,
  config-write method set, or remote-marketplace literal changes; and
- an AST-level guarantee that `codex_switch_protocol_adapter.py` does not
  import `codex_switch_parity`.

### Baseline and RED Evidence

Before the RED edit:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
Ran 37 tests in 23.561s
OK
```

After the RED edit:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 -c <AST parse>
exit 0
syntax-ok
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_protocol_config.py ProtocolAdapterEvidenceTests -v
Ran 2 tests in 0.001s
FAILED (failures=2)
AssertionError: Protocol Adapter rule-set digest seam is missing
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
Ran 39 tests in 20.334s
FAILED (failures=2)
```

The two new tests are the only failures; all 37 pre-existing Protocol Adapter
tests remain GREEN. `codex_switch_protocol_adapter.py` was not modified.

### Boundaries and Next Item

No production adapter/parity implementation, classification, receipt, overlay,
config projection, probe, caller integration, live profile/App/provider
mutation, retained evidence cleanup, dependency, release, archive, or Git
history mutation ran. Task 1.9 is dependency-ready.

## 2026-07-26 Protocol Adapter Rule-Set Digest Verified

Task: 1.9
Result: GREEN

### Changed Files

- `scripts/codex_switch_protocol_adapter.py`
- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

The task 1.8 test file `scripts/test_codex_protocol_config.py` remains the
adapter-owned acceptance seam and was not changed during GREEN.

### RED Evidence

The retained task 1.8 RED was reproduced after restart:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_protocol_config.py ProtocolAdapterEvidenceTests -v
Ran 2 tests in 0.001s
FAILED (failures=2)
AssertionError: Protocol Adapter rule-set digest seam is missing
```

After the adapter seam became GREEN, the parity-input RED was added:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_parity.py \
  ParityReferenceTests.test_candidate_binds_validated_adapter_rule_set_digest -v
Ran 1 test in 0.001s
FAILED (failures=1)
AssertionError: ParityCandidate adapter rule-set digest input is missing
```

### Implementation Contract

- `protocol_adapter_rule_set_digest()` reads the live module globals on each
  call and canonicalizes the three exact model-path mappings, sorted
  config-write method set, and remote-marketplace literal.
- Canonical JSON uses ASCII encoding, sorted object keys, and compact
  separators before lowercase SHA-256.
- `ParityCandidate.adapter_rule_set_sha256` is required caller-supplied
  evidence and is validated as a canonical lowercase SHA-256.
- Invalid evidence reports
  `parity.candidate.adapter_rule_set_digest_invalid`.
- Production Protocol Adapter does not import parity, and production parity
  does not import Protocol Adapter.

The resulting digest on both supported runtimes is:

```text
b9ac004f3801eaf094745e6e45754c7e5a058b33775746e49682aef7c240f849
```

### GREEN Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
Ran 39 tests in 23.632s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 \
  scripts/test_codex_protocol_config.py -v
Ran 39 tests in 23.515s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 26 tests in 0.053s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 26 tests in 0.049s
OK
```

Python 3.12.13 and system Python 3.9.6 each passed AST parsing of the four
affected Python files, imports of both production modules, and produced the
same digest. Strict active OpenSpec validation, authority scans, and
`git diff --check` passed.

### Boundaries and Next Item

No classification policy, receipt, overlay, config projection, probe, caller
integration, live profile/App/provider mutation, dependency change, retained
evidence cleanup, release, archive, or Git history mutation ran. Progress is
9/79; task 1.10 is dependency-ready.

## 2026-07-26 Parity Policy RED

Task: 1.10
Result: expected RED captured

### Changed Files

- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Test Contract

Eight `ParityPolicyTests` require:

- baseline initialize, config, model, collaboration, thread, turn, item, tool,
  approval, and completion protocol closures to be core and unhealthy when
  missing or incompatible;
- `multi_agent_v2` and active-model `multi_agent_version = "v2"` to be core;
- the six exact official-only methods to be optional-unless-observed;
- stable `skill_search` absence to be optional-unless-observed;
- four named under-development features and behavior-compatible stage/default
  drift for `enable_fanout`, `item_ids`, and `memories` to be optional;
- official-only `tool_mode` to be pending-provider optional evidence;
- observed optional protocol or feature surfaces to escalate to core;
- unknown feature drift to be unclassified and unhealthy; and
- stable finding codes, severities, policy version, health, and deterministic
  finding/queue order.

The intended public seam is one parity-owned
`evaluate_parity_policy(...)` call. The tests use existing comparison records
and do not add policy to Protocol Adapter, Runtime Binding, or callers.

### RED Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_parity.py ParityPolicyTests -v
Ran 8 tests in 0.002s
FAILED (failures=8)
AssertionError: Parity policy evaluation seam is missing
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 34 tests in 0.062s
FAILED (failures=8)
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 34 tests in 0.067s
FAILED (failures=8)
```

All 26 pre-existing parity tests remain GREEN on both Python 3.12.13 and
system Python 3.9.6. Test AST parsing on both runtimes and
`git diff --check` pass.

### Boundaries and Next Item

No production classification table, evaluation seam, caller integration,
receipt, overlay, config projection, probe, live state, dependency, retained
evidence cleanup, release, archive, or Git history mutation ran. Progress is
10/79; task 1.11 is dependency-ready.

## 2026-07-26 Parity Policy Verified

Task: 1.11
Result: GREEN

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

- `_PARITY_CLASSIFICATION_TABLES` is immutable and keyed by
  `PARITY_POLICY_VERSION`.
- The version-`1` table contains exact/prefix core protocol classification,
  the six direction-qualified optional-unless-observed protocol methods, core
  and optional feature sets, and metadata-only optional features.
- `evaluate_parity_policy(...)` consumes existing comparison records plus
  active-model metadata and observed sets.
- `ParityPolicyEvaluation` owns health, policy version, stable findings, and
  deterministic synchronization-queue ordering.
- Core, observed-core, and unclassified findings are errors; optional and
  pending-provider findings are warnings.
- Known optional labels apply only to official-reference drift. A review
  RED/GREEN guard proves internal-only drift remains unclassified and
  unhealthy.

### Focused and Full GREEN

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_parity.py ParityPolicyTests -v
Ran 9 tests in 0.000s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 \
  scripts/test_codex_parity.py ParityPolicyTests -v
Ran 9 tests in 0.001s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 35 tests in 0.062s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 35 tests in 0.062s
OK
```

Adjacent dual-runtime regressions:

```text
Protocol Adapter: 39/39 on Python 3.12.13 and system Python 3.9.6
Runtime Binding: 55/55 on Python 3.12.13 and system Python 3.9.6
```

Strict active OpenSpec validation, AI plan lint, dual-runtime AST/import,
classification-authority scan, and `git diff --check` passed.

### Retained Real-Schema Classification

Both Python runtimes produced the same policy result from the retained
347-document official and 337-document internal schema inventories:

```text
healthy False
findings 17
parity.protocol.core_incompatible 8
parity.protocol.optional_missing 6
parity.protocol.unclassified_drift 3
queue 6
```

The queue contains exactly:

```text
client_request:app/installed
client_request:app/read
client_request:environment/status
client_request:thread/searchOccurrences
server_notification:thread/environment/connected
server_notification:thread/environment/disconnected
```

The unclassified methods are:

```text
client_request:account/login/start
client_request:externalAgentConfig/import
client_request:plugin/share/updateTargets
```

This retained result is intentionally unhealthy and is not a final parity
health claim; adapter coverage, behavior evidence, and later receipt/probe
tasks have not yet been applied.

### Boundaries and Next Item

No receipt serialization, overlay, config projection, probe, caller
integration, live profile/App/provider mutation, dependency change, retained
evidence cleanup, release, archive, or Git history mutation ran. Progress is
11/79; task 1.12 is dependency-ready.

## 2026-07-26 Parity Serialization Verified

Task: 1.12
Result: GREEN

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED/GREEN Evidence

Initial focused result:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_parity.py ParitySerializationTests -v
Ran 3 tests in 0.004s
FAILED (failures=2)
```

The existing feature/protocol inventory exclusion contract passed immediately.
The two failures were the expected missing receipt-facing
`ParityPolicyEvaluation.canonical_bytes` seam.

Final focused results:

```text
Python 3.12.13: 3/3
system Python 3.9.6: 3/3
```

Final complete parity results:

```text
Python 3.12.13: 38/38 in 0.055s
system Python 3.9.6: 38/38 in 0.058s
```

Strict active OpenSpec validation, AI plan lint, dual-runtime AST/import, and
`git diff --check` passed.

### Persistence Contract

The tests inject all of the following into runner stderr, schema documentation,
or free-text finding fields:

- credential value;
- 64-character credential digest;
- Authorization bearer header;
- query API secret;
- raw provider config;
- raw prompt;
- raw model output;
- absolute temporary probe path; and
- 128 KiB process output.

None enters feature/protocol inventory bytes or receipt-facing policy bytes.
The policy payload stores only:

```text
healthy
policy_version
findings[].category
findings[].code
findings[].severity
synchronization_queue[].category
synchronization_queue[].identifier
synchronization_queue[].finding_code
```

Finding free text is omitted. Queue categories, codes, lengths, and
feature/model/protocol identifier grammars are checked before serialization;
unsafe identity raises `parity.policy.serialization_invalid`.

### Boundaries and Next Item

No parity receipt file, overlay, probe, caller integration, live profile/App/
provider mutation, dependency change, retained evidence cleanup, release,
archive, or Git history mutation ran. Progress is 12/79; task 1.13 is
dependency-ready.

## 2026-07-26 Parity Reference/Inventory Slice Verified

Task: 1.13
Result: GREEN

### Fresh Dual-Runtime Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 38 tests in 0.066s
OK
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 38 tests in 0.071s
OK
```

The restart preserved the active Goal, `HEAD == origin/main == 0a9400d`, the
dirty worktree, and every completed parity source/test edit. Tasks 1.1-1.13
close the Reference/inventory slice with deterministic bundled-reference,
feature, protocol, adapter-digest, classification, synchronization-queue, and
sanitized policy serialization evidence.

### Boundaries and Next Item

No receipt or overlay file, probe, caller integration, live profile/App/
provider mutation, dependency change, retained evidence cleanup, release,
archive, or Git history mutation ran. Progress is 13/79; create the durable
slice checkpoint and execute task 2.1 by RED.

## 2026-07-26 Parity Receipt RED

Task: 2.1
Result: RED

### Changed Files

- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Evidence

Focused results on Python 3.12.13 and system Python 3.9.6:

```text
PYTHONDONTWRITEBYTECODE=1 <python> \
  scripts/test_codex_parity.py ParityReceiptTests -v
Ran 8 tests
FAILED (failures=12)
```

Complete results on each runtime:

```text
PYTHONDONTWRITEBYTECODE=1 <python> scripts/test_codex_parity.py
Ran 46 tests
FAILED (failures=12)
```

All 38 pre-existing tests pass. The eight new test methods fail only at the
shared assertion that these approved seams are absent:

```text
PARITY_RECEIPT_SCHEMA_VERSION
ParityReceipt
ParityReceiptArtifact
resolve_parity_artifact_paths
write_parity_receipt_artifact
load_parity_receipt_artifact
```

The 12 failure reports are the eight methods plus expanded malformed/unsafe
subtests; there are zero errors. Test compilation passes on both runtimes, and
the focused `git diff --check` passes.

### Contract

The RED group covers canonical bytes, current policy/schema version, complete
fingerprints/digests, profile-local paths and modes, exact manifest metadata,
optional-only queue health, missing/symlink/non-regular/wrong-mode/oversized/
malformed/unsupported receipts, digest drift, and official/provider/runtime
staleness.

No production receipt, overlay, caller, live profile/App/provider mutation,
dependency change, retained evidence cleanup, release, archive, or Git history
mutation ran. Progress is 14/79; task 2.2 is dependency-ready.

## 2026-07-26 Parity Receipt Verified

Task: 2.2
Result: GREEN

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### GREEN Evidence

Focused receipt tests:

```text
Python 3.12.13: 8/8 in 0.043s
system Python 3.9.6: 8/8 in 0.040s
```

Complete parity suites:

```text
Python 3.12.13: 46/46 in 0.104s
system Python 3.9.6: 46/46 in 0.105s
```

Adjacent dual-runtime regressions:

```text
Protocol Adapter: 39/39 in 30.650s and 30.440s
Runtime Binding: 55/55 in 29.504s and 30.785s
```

Strict active OpenSpec validation, AI-native plan lint, dual-runtime AST,
receipt-authority/import scans, and `git diff --check` passed.

### Receipt Contract

- Schema version is `1`; policy version is the current parity policy.
- Canonical JSON is bounded to 256 KiB, duplicate-key-free, and byte-stable.
- Official/internal fingerprints and every approved evidence digest are bound.
- Profile-local paths are exact; the parity directory is `0700` and receipt is
  a regular non-symlink `0600` file.
- Writes are temporary-file, fsync, descriptor-relative rename operations.
- Loads are no-follow, descriptor-relative, inode/mode/size/digest checked, and
  canonical-round-trip checked.
- Optional-only queue evidence remains healthy.
- Missing, unsafe, mode-invalid, oversized, malformed, unsupported,
  digest-mismatched, and stale states use stable receipt codes.

No caller prepares or promotes the receipt, no overlay is generated, and no
live profile/App/provider mutation, dependency change, retained evidence
cleanup, release, archive, or Git history mutation ran. Progress is 15/79; task
2.3 is dependency-ready.

## 2026-07-26 Parity Overlay RED

Task: 2.3
Result: RED

### Changed Files

- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Evidence

Complete results on Python 3.12.13 and system Python 3.9.6:

```text
PYTHONDONTWRITEBYTECODE=1 <python> scripts/test_codex_parity.py -v
Ran 54 tests
FAILED (failures=17)
```

All 46 pre-existing tests pass. The eight new test methods fail only at the
shared assertion that these approved seams are absent:

```text
ParityOverlayArtifact
prepare_parity_overlay
validate_parity_overlay
```

The 17 reports are the eight methods plus expanded missing/duplicate,
unsafe-source, invalid-root, and tool-mode subtests; there are zero errors.
Test compilation passes on both runtimes, and the focused
`git diff --check -- scripts/test_codex_parity.py` passes.

### Contract

The RED group covers unique active-model selection, exact absent-to-v2
addition, already-v2 zero semantic diff, canonical payload/digests, deep
preservation, source byte/mode preservation, missing/duplicate slug,
unsupported root and unsafe source rejection, `tool_mode` and every broader
mutation rejection, and source digest/identity race rejection.

No production overlay implementation, caller, manifest promotion, live
profile/App/provider mutation, dependency change, retained evidence cleanup,
release, archive, or Git history mutation ran. Progress is 16/79; task 2.4 is
dependency-ready.

## 2026-07-26 Parity Overlay Verified

Task: 2.4
Result: GREEN

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED/GREEN Evidence

The eight task-2.3 contracts became GREEN on both runtimes:

```text
Python 3.12.13: 8/8 in 0.044s
system Python 3.9.6: 8/8 in 0.046s
```

Main review added one bounded guard inside the approved overlay contract.
Before the fix, Python 3.12.13 reported two focused failures:

```text
non-canonical ParityOverlayArtifact payload was accepted
explicit-null multi_agent_version returned mutation_forbidden
```

After the guard fix:

```text
Parity: 54/54 in 0.126s on Python 3.12.13
Parity: 54/54 in 0.134s on system Python 3.9.6
Protocol Adapter: 39/39 in 22.226s and 20.614s
Runtime Binding: 55/55 in 25.311s and 26.195s
```

The first concurrent dual-runtime Protocol Adapter attempt produced differing
fixture failures because those probe tests share cross-process test state.
Both required serial runs passed 39/39; only the serial evidence is counted.

Strict active OpenSpec validation, AI-native plan lint, dual-runtime AST,
parity ownership scans, and focused `git diff --check` passed.

### Overlay Contract

- Source reading is no-follow, regular-file-only, bounded to 16 MiB, and
  validates lstat/open/post-read identity, size, mode, mtime, ctime, and the
  candidate-bound expected digest.
- JSON parsing rejects duplicate keys, malformed UTF-8/JSON, non-finite
  constants, unsupported roots, invalid entries, missing/duplicate active
  slugs, and source metadata other than absent or exact `v2`.
- The overlay is a structured deep copy with either zero semantic diff or one
  exact add at `/models/<active-index>/multi_agent_version`.
- Recursive JSON Pointer comparison rejects every broader mutation, including
  `tool_mode`.
- `ParityOverlayArtifact` binds canonical payload bytes, source/overlay
  digests, source mode, active slug/index, and only empty or single-add change
  evidence.

### Read-Only Real Catalog Evidence

```text
source: /Users/cY/.codex/model-catalogs/azure-models.json
source SHA-256: 75c9e8d4dadbe3f612f1b6fbabfe6785c312460bd6b5bedfe1565acdedd41f9a
source mode: 0600
active model index: 0
change: /models/0/multi_agent_version = v2
overlay SHA-256: 2437757759c89c96dbee4204d716ad77f3b7a24bb1b96d6fef9dfc9ad290d85f
source bytes unchanged: true
source mode unchanged: true
```

No overlay file was written or promoted, no caller imports the overlay seam,
and no live profile/App/provider mutation, dependency change, retained
evidence cleanup, release, archive, or Git history mutation ran. Progress is
17/79; task 2.5 is dependency-ready.

## 2026-07-26 Parity Manifest Candidate RED

Timestamp: 2026-07-26 11:52:58 +0800
Task: 2.5
Result: RED

### Changed Files

- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Evidence

Focused results on Python 3.12.13 and system Python 3.9.6:

```text
PYTHONDONTWRITEBYTECODE=1 <python> \
  scripts/test_codex_parity.py ParityBundleManifestTests -v
Ran 4 tests
FAILED (failures=4)
```

Complete results on each runtime:

```text
PYTHONDONTWRITEBYTECODE=1 <python> scripts/test_codex_parity.py -v
Ran 58 tests
FAILED (failures=4)
```

All 54 pre-existing tests pass. The four new methods fail only at the shared
assertion that these approved seams are absent:

```text
ParityBundle
prepare_parity_bundle_artifacts
```

There are zero errors and no unrelated assertion failure. The focused
`git diff --check` passes.

### Contract

The RED group requires:

- an exact manifest candidate containing receipt/overlay final paths and
  payload digests, parity policy version, official-reference digest,
  source-catalog path/digest, Protocol Adapter digest, capability-receipt
  digest, and internal-fingerprint digest;
- stable rejection of every missing or mismatched manifest field;
- generated receipt and overlay files held only in one private mode-`0700`
  staging root as regular non-symlink mode-`0600` files; and
- final profile parity paths absent and source catalog bytes/mode unchanged
  before the schema-v3 transaction task.

No production bundle seam, profile artifact, caller integration, live
profile/App/provider mutation, dependency change, retained evidence cleanup,
release, archive, or Git history mutation ran. Progress is 18/79; task 2.6 is
dependency-ready.

## 2026-07-26 Parity Bundle and Slice Verified

Timestamp: 2026-07-26 12:00:48 +0800
Tasks: 2.6-2.7
Result: GREEN

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

The parity module now:

- creates immutable `ParityBundle` records from one canonical receipt and
  source-preserving overlay artifact;
- cross-checks final overlay path, overlay digest/change set, source path and
  digest, and active model before accepting one bundle generation;
- derives and validates an exact 12-key manifest candidate containing every
  required path, payload digest, policy/schema version, official/internal
  fingerprint, source-catalog, Protocol Adapter, and capability-receipt field;
- rejects every missing, extra, or mismatched manifest field with stable bundle
  codes;
- writes only canonical receipt/overlay payloads into a new private mode-`0700`
  child of the supplied work root as no-follow, exclusive, fsynced regular
  mode-`0600` files; and
- never creates or writes the final profile parity directory.

Main review expanded tamper coverage to every path, digest, schema/policy, and
internal-fingerprint manifest value, added receipt/overlay source-model-change
cross-evidence guards, and made staging-directory fsync no-follow.

### Fresh Verification

```text
ParityBundleManifestTests
Python 3.12.13: 4/4 in 0.041s
system Python 3.9.6: 4/4 in 0.041s
```

```text
Parity
Python 3.12.13: 58/58 in 0.160s
system Python 3.9.6: 58/58 in 0.174s
```

```text
Protocol Adapter
Python 3.12.13: 39/39 in 23.930s
system Python 3.9.6: 39/39 in 20.991s
```

```text
Runtime Binding
Python 3.12.13: 55/55 in 25.254s
system Python 3.9.6: 55/55 in 25.205s
```

The explicit structural source-preservation selection passed 3/3 in 0.024s on
Python 3.12.13 and 3/3 in 0.021s on system Python 3.9.6. It proves the source
fixture bytes and mode remain identical, the parsed overlay equals the source
after removing the one approved v2 addition, and bundle staging leaves the
source and final profile paths unchanged.

Strict active OpenSpec validation, AI-native plan lint, Python 3.12/3.9 AST and
import checks, no-caller authority scan, and `git diff --check` passed.

No caller, transaction, rebind, update, live profile/App/provider mutation,
dependency change, retained evidence cleanup, release, archive, or Git history
mutation ran. Progress is 20/79; task 3.1 is dependency-ready.

## 2026-07-26 Parity Config Projection RED

Timestamp: 2026-07-26 12:07:49 +0800
Task: 3.1
Result: RED

### Changed Files

- `scripts/test_codex_parity.py`
- `scripts/test_codex_config_document.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Contract

The two parity tests define `ConfigInputs`, `ConfigProjection`,
`ConfigProjection.payload_for`, and `prepare_parity_config_projection` as the
parity-owned preparation seam. They require:

- only the internal profile payload points `model_catalog_json` at the managed
  overlay and sets `features.multi_agent_v2 = true`;
- shared input does not receive either internal-only setting;
- profile model/provider/auth and unrelated feature/provider settings remain;
- one shared scalar `[agents].max_threads` assignment is removed while sibling
  agent and TUI settings remain;
- `changed_paths` and `max_threads_source` identify the exact projected
  artifacts;
- preparation never writes either source file; and
- already-clean sources return byte-identical payloads, an empty changed set,
  no max-threads source, and deterministic equality across repeated calls.

The two Config Document tests define one
`remove_exact_scalar_assignment(path, table_path, label)` seam. They require
removal of only the assignment statement, preservation of the table, leading
comment, sibling keys, later sections, and semantic reparsing, plus object- and
byte-identical no-op behavior when the assignment is absent.

### Focused RED Evidence

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_parity.py ParityConfigProjectionTests -v
Ran 2 tests
FAILED (failures=2)
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 \
  scripts/test_codex_parity.py ParityConfigProjectionTests -v
Ran 2 tests
FAILED (failures=2)
```

Both parity methods fail only at the shared assertion that these seams are
absent:

```text
ConfigInputs
ConfigProjection
prepare_parity_config_projection
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_config_document.py \
  ConfigDocumentTests.test_remove_exact_scalar_assignment_preserves_section_and_siblings \
  ConfigDocumentTests.test_remove_exact_scalar_assignment_is_idempotent_when_absent \
  -v
Ran 2 tests
FAILED (failures=2)
```

Both Config Document methods fail only because
`ConfigDocument.remove_exact_scalar_assignment` is absent.

### Complete RED Evidence

```text
Parity Python 3.12.13
Ran 60 tests
FAILED (failures=2)
58 prior tests passed
```

```text
Parity system Python 3.9.6
Ran 60 tests
FAILED (failures=2)
58 prior tests passed
```

```text
Config Document Python 3.12.13
Ran 26 tests
FAILED (failures=2)
24 prior tests passed
```

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 -m py_compile \
  scripts/test_codex_parity.py scripts/test_codex_config_document.py
exit 0

git diff --check -- \
  scripts/test_codex_parity.py scripts/test_codex_config_document.py
exit 0
```

There are zero test errors and no unrelated assertion failures. No production
code, source config, caller, transaction, rebind, update, live
profile/App/provider mutation, dependency change, retained evidence cleanup,
release, archive, or Git history mutation ran. Progress is 21/79; task 3.2 is
dependency-ready.

## 2026-07-26 Parity Config Ambiguity/TOCTOU RED

Timestamp: 2026-07-26 12:10:29 +0800
Task: 3.2
Result: RED

### Changed Files

- `scripts/test_codex_parity.py`
- `scripts/test_codex_config_document.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Added Contracts

Parity preparation must return an unhealthy `ConfigProjection` with one stable
error finding, empty `changed_paths`, and no `max_threads_source` for:

- duplicate exact assignments;
- dotted `agents.max_threads`;
- non-scalar values;
- invalid TOML;
- exact assignments in more than one source;
- symlinked config sources; and
- a source whose identity changes after its bounded read.

The finding codes are:

```text
parity.config.max_threads_ambiguous
parity.config.source_invalid
parity.config.source_unsafe
parity.config.source_stale
```

Every fixture asserts zero preparation writes. The concurrent replacement uses
the same bytes at a new inode so final byte equality cannot conceal the
identity race.

Config Document directly rejects dotted and non-scalar target assignments with
the stable `config_exact_assignment_ambiguous` diagnostic.

### Focused RED Evidence

```text
ParityConfigProjectionTests
Python 3.12.13: 9 tests, 9 expected failures
system Python 3.9.6: 9 tests, 9 expected failures
```

All methods fail only because these seams are absent:

```text
ConfigInputs
ConfigProjection
prepare_parity_config_projection
```

```text
Config Document dotted/non-scalar selection
Python 3.12.13: 2 tests, 2 expected failures
```

Both methods fail only because
`ConfigDocument.remove_exact_scalar_assignment` is absent.

### Complete RED Evidence

```text
Parity Python 3.12.13
Ran 67 tests
FAILED (failures=9)
58 prior tests passed
```

```text
Parity system Python 3.9.6
Ran 67 tests
FAILED (failures=9)
58 prior tests passed
```

```text
Config Document Python 3.12.13
Ran 28 tests
FAILED (failures=4)
24 prior tests passed
```

Test compile and focused `git diff --check` passed. There are zero test errors
and no unrelated assertion failures. No production code, source config, caller,
transaction, rebind, update, live profile/App/provider mutation, dependency
change, retained evidence cleanup, release, archive, or Git history mutation
ran. Progress is 22/79; task 3.3 is dependency-ready.

## 2026-07-26 Parity Config Projection GREEN

Timestamp: 2026-07-26 12:23:53 +0800
Task: 3.3
Result: GREEN

### Changed Files

- `scripts/codex_switch_config_document.py`
- `scripts/codex_switch_parity.py`
- `scripts/test_codex_config_document.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

- Added `ConfigDocument.remove_exact_scalar_assignment()` for one exact scalar
  table assignment, preserving the section, comments outside the statement,
  sibling keys, and unrelated sections.
- Added immutable `ConfigInputs` and `ConfigProjection` records.
- Added bounded no-follow config reads with size, digest, inode, mode, mtime,
  and ctime checks.
- Added internal-only `model_catalog_json` and
  `features.multi_agent_v2 = true` projection plus exact
  `agents.max_threads` removal.
- Reparsed every successful payload and returned zero promotable payloads for
  stable ambiguity, invalid, unsafe, oversized, or stale findings.
- Added no production caller, home-sync integration, or write path.

### Main Review Finding and TDD Closure

The interrupted implementation checked each source at the end of its own read,
but did not revalidate earlier sources after later sources were read. The new
test
`test_previously_read_source_replacement_is_unhealthy_and_writes_nothing`
replaced the already-read profile source with the same bytes and a new inode
while the shared source was read.

```text
Python 3.12.13 RED
Ran 1 test
FAILED
Expected projection.healthy is False; observed True
```

Final all-source identity/digest revalidation was added before the projection
can return payloads.

```text
Python 3.12.13 GREEN: 1/1
system Python 3.9.6 GREEN: 1/1
```

### Fresh Verification

```text
Parity Python 3.12.13: 69/69
Parity system Python 3.9.6: 69/69
Config Document Python 3.12.13: 29/29
Protocol Adapter Python 3.12.13: 39/39
Protocol Adapter system Python 3.9.6: 39/39
Runtime Binding Python 3.12.13: 55/55
Runtime Binding system Python 3.9.6: 55/55
```

```text
AI-native plan lint: passed
strict active OpenSpec: passed
strict all OpenSpec: 18/18
Python 3.12 and 3.9 production imports: passed
Python 3.12 and 3.9 affected-file AST parse: passed
affected-file py_compile: passed
projection caller/authority scans: no production caller
git diff --check: passed
```

No source config, canonical home-sync, transaction, rebind, update, live
profile/App/provider state, dependency, release, archive, retained evidence,
cleanup, or Git history changed. Progress is 23/79; task 3.4 is
dependency-ready.

## 2026-07-26 Parity Home Sync RED

Timestamp: 2026-07-26
Task: 3.4
Result: RED

### Changed Files

- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Contracts

- An internal profile and shared config derive managed-home text with the
  profile-local parity overlay and `features.multi_agent_v2 = true`.
- Shared features and unrelated profile/provider, agent sibling, and TUI
  settings remain present.
- Only stale `agents.max_threads` is absent.
- A materialized stale runtime cannot override projected profile/shared values.
- Derivation returns staged text and does not write profile, shared, or runtime
  inputs.

### RED Evidence

```text
Python 3.12.13
Ran 2 tests
FAILED (failures=2)
Errors: 0
```

```text
system Python 3.9.6
Ran 2 tests
FAILED (failures=2)
Errors: 0
```

The unmaterialized case observes missing `model_catalog_json`. The materialized
case observes `stale-model` instead of `gpt-5.6-sol`. Both failures are direct
behavior assertions, not interface or parser errors.

### Adjacent Verification

```text
Python 3.12.13 adjacent home-sync/profile regressions: 6/6
test file py_compile: passed
focused git diff --check: passed
```

The same six older adjacent tests cannot run directly under system Python 3.9
because their existing production paths require Python 3.11+ `tomllib`; the two
new focused tests install a bounded parser fixture and run on both required
runtimes.

No production code, source/runtime config, caller, transaction, rebind, update,
live profile/App/provider state, dependency, release, archive, cleanup, retained
evidence, or Git history changed. Progress is 24/79; task 3.5 is
dependency-ready.

## 2026-07-26 Parity Home Sync GREEN

Timestamp: 2026-07-26
Task: 3.5
Result: GREEN

### Changed Files

- `scripts/codex_switch_home_sync.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

- Added one optional `ConfigProjection` input to canonical internal home
  derivation.
- Required a healthy projection bound to the same internal profile and
  canonical shared source.
- Used projected profile text as the only profile seed and merged its shared
  v2 feature state into projected shared text.
- Ignored materialized runtime text as an authority while projection is active,
  preventing stale model, feature, and `agents.max_threads` recovery.
- Returned staged managed-home text without writing profile, shared, or runtime
  inputs.
- Preserved the legacy home-sync path when no projection is supplied.

### GREEN Evidence

```text
Focused home-sync projection
Python 3.12.13: 2/2
system Python 3.9.6: 2/2
```

```text
Python 3.12.13 adjacent home-sync/profile: 6/6
Python 3.12.13 full profile: 200/200
Python 3.12.13 full transaction: 219/219
```

```text
Parity Python 3.12.13: 69/69
Parity system Python 3.9.6: 69/69
Config Document Python 3.12.13: 29/29
Dual-runtime home-sync import/compile: passed
Focused git diff --check: passed
```

The attempted direct full Config Document suite under system Python 3.9
reproduced its established unsupported Python-3.11+-`tomllib` baseline
(`3 failures, 22 errors`). This is not a changed-path regression: the new
focused home-sync and parity paths install the bounded parser fixture and pass
on system Python 3.9.

No live profile/App/provider mutation, source/runtime config write,
transaction promotion, dependency, release, archive, cleanup, retained
evidence, or Git history change occurred. Progress is 25/79; task 3.6 is
dependency-ready.

## 2026-07-26 Parity Probe RED

Timestamp: 2026-07-26
Task: 3.6
Result: RED

### Changed Files

- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Contracts

- Probe requests use only the exact candidate backend and isolated candidate
  home/config/overlay/capability artifacts.
- Core requests are ordered initialize, initialized,
  `collaborationMode/list`, then `thread/start`.
- Success requires v2, `agentRole=explorer`, `source=thread_spawn`, child
  `parity-subagent-ok`, and parent `parity-parent-ok`.
- V1/nickname-only, timeout, malformed, missing, early-exit, and oversized
  outcomes fail with distinct stable result codes.
- Timeout terminates the complete process group.
- Candidate artifacts are revalidated after each probe.
- Persistable evidence contains only bounded result codes and sanitized
  evidence digests; secret changes do not change the digest, safe routing
  changes do.

### RED Evidence

```text
Parity Python 3.12.13
Ran 79 tests
69 passed
10 expected failures
Errors: 0
```

```text
Parity system Python 3.9.6
Ran 79 tests
69 passed
10 expected failures
Errors: 0
```

All failures name only missing `ParityProbeInputs`, `ParityProbeRequest`,
`ParityProbeCommandResult`, `ParityProbeResult`, `ParityProbeReport`, and
`run_parity_probes`. Test compile and focused diff checks passed.

No production probe, provider traffic, source/runtime write, live
profile/App/provider mutation, dependency, release, archive, cleanup, retained
evidence change, or Git history change occurred. Progress is 26/79; task 3.7 is
dependency-ready.

## 2026-07-26 Parity Probe GREEN

Timestamp: 2026-07-26
Task: 3.7
Result: GREEN

### Changed Files

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

- Added immutable `ParityProbeInputs`, `ParityProbeRequest`,
  `ParityProbeCommandResult`, `ParityProbeResult`, and `ParityProbeReport`.
- Added no-follow candidate backend/config/overlay/capability snapshots with
  identity and digest revalidation after every probe.
- Added bounded stdout/stderr capture, timeout handling, and full process-group
  `SIGTERM`/`SIGKILL` termination.
- Added exact initialize/core response ordering and typed explorer v2
  spawn/child/parent completion validation with no v1 fallback.
- Persisted only stable result/finding codes and bounded sanitized evidence
  digests.

### Review RED/GREEN

The initial process-group test failed on both runtimes because its Python
fixture had not created the descendant within a 0.2-second startup window. The
fixture now uses a deterministic shell process group whose parent and child
ignore `SIGTERM`; the default runner proves group-wide termination.

Main review added three failing boundaries before the final implementation:

- mixed v1 then v2 output incorrectly passed because the last spawn won;
- repeated v2 spawns incorrectly passed;
- child-before-spawn or parent-before-child output incorrectly passed.

The evaluator now scans all spawn events, rejects any v1, requires exactly one
v2 explorer `thread_spawn`, and requires strict
`spawn < child completion < parent completion` ordering.

The sanitizer review also reproduced secret-dependent evidence digests for URL
userinfo and extended signed-query variants. Probe sanitization now matches the
existing verifier's header, assignment, URL, bearer, and signed-query coverage.

### Fresh Verification

```text
Focused ParityProbeTests
Python 3.12.13: 12/12
system Python 3.9.6: 12/12
```

```text
Complete parity
Python 3.12.13: 81/81
system Python 3.9.6: 81/81
```

```text
Dual-runtime AST/import/export checks: passed
Focused git diff --check: passed
Probe process-residue inspection: passed
```

The TDD methodology is ready. The broader dependency diagnostic remains
`missing_required` only because of the established unrelated DevFlow
skill-layout source conflicts; no activation, migration, or legacy cleanup was
authorized.

No caller integration, retained probe fixture, provider traffic,
source/runtime write, live profile/App mutation, dependency, release, archive,
cleanup, or Git history change occurred. Progress is 27/79; task 3.8 is
dependency-ready.

## 2026-07-26 Retained Probe Fixture

Timestamp: 2026-07-26
Task: 3.8
Result: GREEN

### Changed Files

- `scripts/test_codex_parity.py`
- `testdata/parity/retained-v2-probe-redacted.json`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Fixture Contract

- The checked-in fixture retains synthetic provider id/name, Azure-style base
  URL, Responses wire API, auth-source key name, API-version query structure,
  safe route evidence, and exact core/typed-v2 event shapes.
- Every credential-bearing value is `[REDACTED]`.
- No real home/temp path, bearer value, raw credential, or credential digest is
  present.
- The fixture is under `testdata/`, outside the current release allowlist.

### RED/GREEN Evidence

The focused test first failed with one assertion:

```text
redacted retained parity probe fixture is missing
```

After adding the synthetic fixture:

```text
Python 3.12.13 focused retained fixture: 1/1
system Python 3.9.6 focused retained fixture: 1/1
```

For each runtime, the test substitutes two different transient API-key values
into isolated temporary configs. It proves:

- report canonical bytes and receipt results are identical across secrets;
- neither secret, raw config bytes, nor config path appears in the report;
- the complete candidate file tree is byte-identical before and after probing.

### Fresh Verification

```text
Complete parity Python 3.12.13: 82/82
Complete parity system Python 3.9.6: 82/82
Dual-runtime fixture JSON/AST/secret scan: passed
Focused git diff --check: passed
```

The old retained v2 probe directory was inspected only for filenames and
permissions. Its credential-bearing config was not read, copied, rewritten, or
deleted.

No provider traffic, live profile/App mutation, source/runtime write,
dependency, release, archive, cleanup, or Git history change occurred. Progress
is 28/79; task 3.9 is dependency-ready.

## 2026-07-26 Config and Probe Slice Verification

Timestamp: 2026-07-26
Task: 3.9
Result: GREEN

### Changed Files

- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-config-probes-verified.md`

No production source or test file changed for task 3.9.

### Fresh Verification

```text
Complete parity
Python 3.12.13: 82/82 in 2.049s
system Python 3.9.6: 82/82 in 7.633s
```

```text
Config Document
Python 3.12.13: 29/29 in 3.314s
system Python 3.9.6 direct baseline: 29 tests, 3 failures, 22 errors
```

The system-Python result exactly reproduces the established unsupported
Python-3.11+-`tomllib` boundary. It is not a changed-path regression.

```text
Focused home-sync parity projection
Python 3.12.13: 2/2 in 0.016s
system Python 3.9.6: 2/2 in 4.880s
```

Those tests install the bounded parser fixture and prove staged projection,
source preservation, stale-runtime rejection, and zero writes on both required
runtimes.

```text
Verifier
Python 3.12.13 full suite: 22/22 in 14.798s
system Python 3.9.6 native sanitizer focus: 2/2 in 0.004s
system Python 3.9.6 full supported route: 22/22 in 11.033s
```

The supported system-Python command supplies
`CODEX_SWITCH_PYTHON=/opt/homebrew/bin/python3.12` so wrapper fixtures use a
validated Python 3.11+ interpreter. An initial unpinned full run produced eight
wrapper-generation errors because `sys.executable` was Python 3.9; no sanitizer
or parity assertion failed.

```text
Strict active OpenSpec: passed
Python 3.12.13 AST: 56/56 scripts
system Python 3.9.6 AST: 56/56 scripts
Python 3.12.13 production imports: passed
system Python 3.9.6 production imports: passed
git diff --check: passed
generated bytecode cleanup: passed
```

The DevFlow dependency check reports Full OpenSpec and TDD ready. Its
nonblocking legacy skill-layout recommendations remain untouched.

No live provider call, profile/App mutation, source/runtime write, dependency,
release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, or Git history effect occurred. Progress is 29/79; the
Config/probes slice is complete and task 4.1 is dependency-ready.

## 2026-07-26 Runtime Bundle Target-Set RED

Timestamp: 2026-07-26
Task: 4.1
Result: RED

### Changed Files

- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Contract

The new tests require:

- `RuntimeBindingTextArtifact` typed entries;
- `commit_runtime_binding_bundle()` under the existing store lock;
- schema-v3 marker state `prepared`;
- exact required roles and paths for manifest, launcher, capability receipt,
  parity receipt, parity overlay, and profile config;
- explicit shared-config and active-runtime-config optional roles across all
  four presence combinations;
- mode `0755` only for the launcher and `0600` for every other text artifact;
  and
- an `after_marker` hard interruption before any target write.

The caller supplies artifacts in reverse role order. The marker must derive its
exact role/path authority rather than accepting input order as policy.

### Expected Failure Evidence

```text
Python 3.12.13
Ran 2 tests in 0.111s
FAILED (failures=5)
Errors: 0
```

```text
system Python 3.9.6
Ran 2 tests in 0.086s
FAILED (failures=5)
Errors: 0
```

Every failure is:

```text
Runtime binding bundle seams are missing:
RuntimeBindingTextArtifact, commit_runtime_binding_bundle
```

The five reports are one required-target test plus four explicit optional
subtests. No failure is caused by syntax, fixture setup, parser support, path
creation, or an existing behavior assertion.

### Adjacent Verification

```text
Existing runtime-rebind v1/v2 tests
Python 3.12.13: 4/4
system Python 3.9.6: 4/4
```

```text
Strict active OpenSpec: passed
Python 3.12.13 test compile: passed
system Python 3.9.6 test compile: passed
Trailing-whitespace scan: passed
git diff --check: passed
Generated bytecode cleanup: passed
```

No production code, runtime marker, target file, live profile/App/provider
state, dependency, release, archive, provider/root-state migration, legacy
skill cleanup, destructive cleanup, or Git history effect occurred. Progress
is 30/79; task 4.2 is dependency-ready.

## 2026-07-26 Runtime Bundle Target-Safety RED

Timestamp: 2026-07-26
Task: 4.2
Result: RED

### Changed Files

- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Contract

The new tests require commit-time validation to reject, before marker creation
or target writes:

- duplicate entries;
- unexpected role/path entries;
- parent/child-overlapping paths;
- a missing required role;
- symlink and directory targets;
- any non-launcher mode other than `0600`;
- any launcher mode other than `0755`; and
- a payload larger than `MAX_PARITY_CATALOG_BYTES`.

Recovery validation must also:

- reject digest-invalid schema-v3 old and new embedded states;
- preflight every target against both recorded states before rollback or
  roll-forward writes;
- retain a prepared or committed marker when a foreign target is present; and
- leave every other old/new target byte and mode unchanged on that failure.

The prepared foreign-state fixture deliberately places the overlay in its valid
new state while the manifest is foreign. The committed fixture leaves
write-eligible old targets while the manifest is foreign. Both require a full
preflight rather than partial convergence before foreign-state detection.

### Expected Failure Evidence

```text
Task 4.2, Python 3.12.13
Ran 5 tests
FAILED (failures=13)
Errors: 0
```

```text
Task 4.2, system Python 3.9.6
Ran 5 tests
FAILED (failures=13)
Errors: 0
```

```text
Combined tasks 4.1-4.2, each runtime
Ran 7 tests
FAILED (failures=18)
Errors: 0
```

Every failure is:

```text
Runtime binding bundle seams are missing:
RuntimeBindingTextArtifact, commit_runtime_binding_bundle
```

No failure is caused by syntax, fixture setup, parser support, path mutation, or
an existing behavior assertion.

### Adjacent Verification

```text
Existing runtime-rebind schema-v1/v2 tests
Python 3.12.13: 4/4
system Python 3.9.6: 4/4
```

```text
Python 3.12.13 test AST: passed
system Python 3.9.6 test AST: passed
Trailing-whitespace scan: passed
Post-edit strict OpenSpec: passed
Post-edit git diff --check: passed
Generated bytecode cleanup: passed
```

No production code, runtime marker, target file, live profile/App/provider
state, dependency, release, archive, provider/root-state migration, legacy
skill cleanup, destructive cleanup, or Git history effect occurred. Progress
is 31/79; task 4.3 is dependency-ready.

## 2026-07-26 Runtime Bundle Schema-v3 GREEN

Timestamp: 2026-07-26
Task: 4.3
Result: GREEN

### Changed Files

- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Implementation

The transaction module now provides:

- `RuntimeBindingTextArtifact(role, path, payload, mode)`;
- `commit_runtime_binding_bundle(..., artifacts=..., fault_hook=...)`;
- exact required and optional role/path authority derived from the locked
  `Store`;
- a 16 MiB per-text-artifact old/new journal bound;
- deterministic activation order: parity overlay, capability receipt, parity
  receipt, optional shared config, profile config, optional active runtime
  config, launcher, and manifest;
- schema-v3 prepared/committed markers with embedded old/new state;
- complete old/new preflight before any recovery write;
- immediate target-level old/new revalidation before each recovery write; and
- unchanged schema-v1/v2 validation, recovery, and pair-commit behavior.

The existing pair function remains the compatibility entry point until its
callers migrate in later approved tasks.

### Review Finding

Main-agent review found that an external target could become foreign after the
initial recovery preflight but before its own convergence write. The first
implementation could then overwrite those late foreign bytes. The recovery
loop now rechecks the target against both recorded states immediately before
writing. A bounded regression mutates the manifest after preflight and proves
the foreign payload and marker remain.

### GREEN Evidence

```text
Schema-v3 focused
Python 3.12.13: 9/9 in 0.356s
system Python 3.9.6: 9/9 in 0.356s
```

The focused set includes exact target/optional matrices, invalid target sets
and types, modes and size, old/new digest rejection, prepared/committed foreign
preflight, successful eight-role manifest-last promotion, and the late-foreign
no-overwrite guard.

```text
Complete transaction
Python 3.12.13: 228/228 in 18.522s
system Python 3.9.6: 228/228 in 120.548s
```

```text
Runtime Binding
Python 3.12.13: 55/55 in 24.446s
system Python 3.9.6: 55/55 in 25.182s
```

### Remaining Boundary

Task 4.4 still owns fault injection after marker publication, each ordered
artifact class, committed marker publication, and marker retirement. Task 4.5
still owns explicit legacy marker fixtures. No caller consumes the new bundle
until the later internal rebind integration task.

No live profile/App/provider state, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred. Progress is 32/79; task 4.4 is dependency-ready.

## 2026-07-26 Runtime Bundle Fault Matrix Verified

Timestamp: 2026-07-26
Task: 4.4
Result: GREEN

### Changed Files

- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Evidence

The tests define eleven hard-interruption phases:

```text
after_marker
after_parity_overlay
after_capability_receipt
after_parity_receipt
after_shared_config
after_profile_config
after_active_runtime_config
after_launcher
after_manifest
after_committed_marker
after_marker_retirement
```

Before implementation, `after_marker` already passed and the other ten phase
subtests failed only because `HardInterruption` was not raised:

```text
Python 3.12.13: 2 methods, 10 expected failures, 0 errors
system Python 3.9.6: 2 methods, 10 expected failures, 0 errors
```

### GREEN Contract

- Prepared interruption records the exact promoted prefix and untouched suffix.
- The next locked mutation restores every target's old bytes and mode.
- Committed-marker interruption retains a committed marker and complete new
  target set until lock-entry roll-forward retires the marker.
- Marker-retirement interruption has no marker and retains the complete new
  target set.
- Legacy schema-v1/v2 commit and recovery code is unchanged.

### Fresh Verification

```text
Schema-v3 focused
Python 3.12.13: 11/11 in 0.604s
system Python 3.9.6: 11/11 in 0.623s
```

```text
Complete transaction
Python 3.12.13: 230/230 in 18.725s
system Python 3.9.6: 230/230 in 119.192s
```

```text
Dual-runtime AST/import: passed
Strict active OpenSpec: passed
Trailing-whitespace and git diff --check: passed
Generated bytecode cleanup: passed
```

No live profile/App/provider state, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred. Progress is 33/79; task 4.5 is dependency-ready.

## 2026-07-26 Legacy Runtime Rebind Fixtures Verified

Timestamp: 2026-07-26
Task: 4.5
Result: GREEN

### Changed Files

- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Characterization Contract

One fixture method executes four subtests:

```text
schema v1 + prepared
schema v1 + committed
schema v2 + prepared
schema v2 + committed
```

For each fixture:

- the marker field set is exact and has no schema-v3 `artifacts` field;
- embedded old/new bytes, modes, and SHA-256 values use the legacy layout;
- recovery begins from a mixed valid old/new target set;
- prepared converges to old and committed converges to new;
- schema v1 preserves an unrelated receipt's bytes and `0640` mode;
- schema v2 converges its owned receipt bytes and `0600` mode; and
- a fail-fast patch proves the schema-v3 marker validator is never invoked.

### Fresh Verification

```text
Legacy schema-v1/v2 fixture method
Python 3.12.13: 1 method, 4/4 subtests
system Python 3.9.6: 1 method, 4/4 subtests
```

```text
Complete transaction
Python 3.12.13: 231/231 in 18.636s
system Python 3.9.6: 231/231 in 121.778s
```

Strict active OpenSpec, dual-runtime AST, trailing-whitespace and
`git diff --check`, and generated-bytecode cleanup pass.

No production source, live profile/App/provider state, dependency, release,
archive, provider/root-state migration, legacy skill cleanup, destructive
cleanup, or Git history effect occurred. Progress is 34/79; task 4.6 is
dependency-ready.

## 2026-07-26 Internal Rebind Parity Integration RED

Timestamp: 2026-07-26
Task: 4.6
Result: RED

### Changed Files

- `scripts/test_codex_runtime_binding.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### RED Contract

Two runtime-binding methods require:

- parity preparation before launcher smoke;
- schema-v3 bundle commit after smoke and child-backend attestation;
- no legacy `commit_runtime_binding_pair()` call;
- the exact eight roles `manifest`, `launcher`, `capability_receipt`,
  `parity_receipt`, `parity_overlay`, `profile_config`, `shared_config`, and
  `active_runtime_config`;
- exact final target paths, `0600` text modes and `0755` launcher mode;
- parity manifest metadata and staged receipt/overlay/config payloads; and
- unchanged source-catalog bytes and `0640` mode.

One profile method executes four subtests:

```text
failed preparation
unknown evidence
core incompatibility
unclassified drift
```

Every subtest requires `SwitchError`, zero schema-v3 commit calls, no target
change, and source-catalog byte/mode preservation.

### Expected Failure Evidence

```text
Runtime Binding, Python 3.12.13
Ran 2 tests in 5.516s
FAILED (failures=2)
Errors: 0
```

```text
Runtime Binding, system Python 3.9.6
Ran 2 tests in 5.143s
FAILED (failures=2)
Errors: 0
```

The first method observes:

```text
events = ["smoke"]
legacy_pair_calls = 1
```

instead of:

```text
events = ["parity", "smoke", "commit"]
legacy_pair_calls = 0
```

The second method receives no schema-v3 artifacts because the current caller
does not invoke `commit_runtime_binding_bundle()`.

```text
Profile unhealthy evidence, Python 3.12.13
Ran 1 test in 10.725s
FAILED (failures=4)
Errors: 0
```

```text
Profile unhealthy evidence, system Python 3.9.6
Ran 1 test in 10.172s
FAILED (failures=4)
Errors: 0
```

All four profile failures show no `SwitchError` and changed legacy promotion
targets. The source catalog remains byte- and mode-unchanged, so the failures
are specifically the absent parity gate and schema-v3 integration rather than
fixture corruption.

### Adjacent Verification

```text
Established internal rebind tests
Python 3.12.13: 4/4 in 9.162s
system Python 3.9.6: 4/4 in 8.502s
```

```text
Python 3.12.13 test AST: passed
system Python 3.9.6 test AST: passed
Trailing-whitespace scan: passed
Tracked test diff check: passed
```

No production source, runtime marker/target outside temporary fixtures, live
profile/App/provider state, dependency, release, archive, provider/root-state
migration, legacy skill cleanup, destructive cleanup, or Git history effect
occurred. Progress is 35/79; task 4.7 is dependency-ready.

## 2026-07-26 Internal Runtime Parity Rebind GREEN

Timestamp: 2026-07-26
Task: 4.7
Result: GREEN

### Changed Files

- `scripts/codex_switch_bindings.py`
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_runtime_binding.py`
- `scripts/test_codex_transaction.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### GREEN Contract

Internal `set-bin` now:

- prepares parity before launcher smoke and rejects unhealthy or incomplete
  evidence before any promotion;
- preserves configured source-catalog bytes and mode;
- projects the managed overlay, profile config, authoritative shared config, and
  active runtime config from one parity generation;
- writes the staged launcher and manifest with the matching capability receipt,
  parity receipt, overlay, config, and Protocol Adapter metadata;
- verifies the smoke child backend, typed receipt generation, config-write
  proof, and Runtime Binding attestation; and
- commits exactly the eight approved roles through
  `commit_runtime_binding_bundle()` with manifest last.

Review hardening also requires stable no-follow bounded `active.json` reads,
exact-integer marker schema values, bounded marker reads, marker-generation
checks before every write, and identity-bound marker retirement. The existing
schema-v1/v2 fixtures remain byte-compatible.

### Fresh Verification

```text
Parity
Python 3.12.13: 83/83 in 2.085s
system Python 3.9.6: 83/83 in 38.698s
```

```text
Runtime Binding
Python 3.12.13: 60/60 in 40.776s
system Python 3.9.6: 60/60 in 41.847s
```

```text
Transaction
Python 3.12.13: 238/238 in 20.765s
system Python 3.9.6: 238/238 in 127.774s
```

```text
Unhealthy parity promotion guard
Python 3.12.13: 1/1 method, four subtests, in 3.845s
system Python 3.9.6: 1/1 method, four subtests, in 3.991s
```

The source-owned DevFlow dependency check reports
`ready_with_recommendations`, with Full OpenSpec and TDD ready. The installed
cache comparison reports the known source-link mismatch; no activation,
migration, or legacy skill cleanup was authorized or performed.

No live profile/App/provider state, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred. Progress is 36/79; task 4.8 is dependency-ready.

### Post-Edit Control-Plane Verification

```text
openspec validate internal-official-feature-parity --strict --no-interactive
Change 'internal-official-feature-parity' is valid
```

```text
openspec validate --all --strict --no-interactive
18 passed, 0 failed
```

```text
OpenSpec apply progress: 36/79, state ready
First pending item: 4.8
Python 3.12.13 AST: 56/56
system Python 3.9.6 AST: 56/56
git diff --check: passed
generated bytecode/process residue: none
```

## 2026-07-26 Launcher and Shell Generation Equivalence RED

Timestamp: 2026-07-26
Task: 4.8
Result: RED

### Changed Files

- `scripts/test_codex_runtime_binding.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Confirmed Test Seams

- active internal shell execution through the generated store shim;
- active internal Desktop execution through the generated managed launcher and
  app proxy;
- backend-observed managed-home config, overlay, v2, and capability-receipt
  generation; and
- backend-start markers proving mixed generations were or were not rejected
  before child execution.

### RED Contract

The equivalence method requires shell and Desktop to observe the same:

- promoted backend generation;
- managed-home path and config digest;
- managed overlay path and digest;
- `multi_agent_v2 = true`;
- capability receipt path; and
- expected capability receipt digest.

The mixed-generation method executes two subtests:

```text
old launcher + new manifest/capability receipt
new launcher + old parity overlay
```

Each subtest requires a nonzero launch result, a bounded
generation/digest/launcher/overlay/receipt error, and no backend-start marker.

### Expected Failure Evidence

```text
Python 3.12.13
Ran 2 tests in 10.229s
FAILED (failures=3)
Errors: 0
```

```text
system Python 3.9.6
Ran 2 tests in 10.005s
FAILED (failures=3)
Errors: 0
```

The equivalence failure shows the Desktop contract on the promoted `new`
backend and receipt generation while the shell contract remains on `old` with
empty capability receipt path/digest. Both mixed-generation subtests exit zero,
emit runtime-contract output, and write their backend-start markers.

### Adjacent Verification

```text
Established internal rebind set
Python 3.12.13: 10/10 in 26.398s
system Python 3.9.6: 10/10 in 25.733s
```

```text
Unhealthy parity promotion guard
Python 3.12.13: 1/1 method, four subtests, in 2.751s
system Python 3.9.6: 1/1 method, four subtests, in 2.682s
```

```text
Python 3.12.13 test compile: passed
system Python 3.9.6 test compile: passed
```

No production source, live profile/App/provider state, dependency, release,
archive, provider/root-state migration, legacy skill cleanup, destructive
cleanup, or Git history effect occurred. Progress is 37/79; task 4.9 is
dependency-ready.

## 2026-07-26 Runtime Rebind Adapter Retirement GREEN

Timestamp: 2026-07-26
Task: 4.9
Result: GREEN

### Changed Files

- `scripts/codex_switch_runtime_binding.py`
- `scripts/codex_switch_app_wrapper.py`
- `scripts/codex_switch_shim.py`
- `scripts/codex_switch_bindings.py`
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_runtime_binding.py`
- `scripts/test_codex_transaction.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`

### Adapter and Generation Contract

- `commit_runtime_binding_pair()` and all production/test imports and callers
  are removed.
- `commit_runtime_binding_bundle()` is the sole current runtime-rebind commit
  interface.
- Schema-v1/v2 marker validation and recovery remain independent of schema v3.
- The internal shell shim dynamically resolves the active manifest instead of
  retaining the pre-rebind backend/receipt generation.
- Shell and parity-aware Desktop launchers invoke one shared Runtime Binding
  validator before backend execution.
- Zero parity fields preserve the established legacy launch boundary.
- Any parity field requires the complete launcher, backend, capability receipt,
  parity receipt, overlay, projected config, and v2 generation.

### Bounded Review Guard

Review found that missing parity receipt `overlay` or
`internal_fingerprint.capability_receipt_sha256` bindings were conditionally
skipped.

```text
RED: Python 3.12.13
Ran 1 method with two subtests in 3.741s
FAILED (failures=2, errors=0)
Both malformed receipts reached the backend and wrote the marker.
```

```text
GREEN: Python 3.12.13
Ran 1 method with two subtests in 3.204s
OK
Both malformed receipts are rejected before backend execution.
```

The final validator also requires the manifest parity capability digest,
receipt internal fingerprint digest, and active capability receipt digest to
match.

### Fresh Verification

```text
Runtime Binding after the final test-isolation edit
Python 3.12.13: 63/63 in 52.956s
system Python 3.9.6: 63/63 in 52.226s
```

```text
Transaction
Python 3.12.13: 234/234 in 22.220s
system Python 3.9.6: 234/234 in 119.539s
```

```text
Complete profile
Python 3.12.13: 201/201 in 281.569s
```

```text
rg commit_runtime_binding_pair scripts: no matches
active strict OpenSpec: valid
all strict OpenSpec: 18 passed, 0 failed
Python 3.12.13 AST: passed
system Python 3.9.6 AST: passed
git diff --check: passed
generated bytecode: none
```

### Test Isolation Incident and Repair

The first Runtime Binding full run did not provide
`CODEX_SWITCH_SHELL_PROFILE`, so
`test_canonical_official_switch_repairs_manifest_drift` temporarily wrote its
deleted temporary store path into the managed `~/.zshrc` block. The block was
immediately restored to `/Users/cY/.codex-switch/bin`. Read-only
`codex-switch --skip-self-update status` then confirmed:

```text
Active profile: internal
PATH codex alignment: ok
GUI CODEX_CLI_PATH: /Users/cY/.codex-switch/bin/codex-internal-app
LaunchAgent CODEX_CLI_PATH: /Users/cY/.codex-switch/bin/codex-internal-app
Running backend: /Users/cY/.local/bin/codex via the app proxy
```

The test now patches `CODEX_SWITCH_SHELL_PROFILE` to its temporary directory
and asserts that local file contains the temporary store bin. Focused runs on
both runtimes and the final full Runtime Binding runs preserve the repaired
real shell profile:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mtime: 1785055828
ctime: 1785055828
```

No profile, App, provider, install, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect remains. Progress is 38/79; task 4.10 is dependency-ready.

## 2026-07-26 Runtime Bundle/Rebind Slice Verification

Timestamp: 2026-07-26T17:56:32+08:00
Task: 4.10
Result: GREEN

### Changed Files

- `scripts/codex_switch_runtime_binding.py`
- `scripts/test_codex_runtime_binding.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-runtime-bundle-verified.md`

### Integrated Review Finding

The generation trigger recognized only five parity manifest fields. A manifest
retaining `parity_adapter_rule_set_sha256` without the primary receipt/overlay
fields was therefore treated as a zero-parity legacy manifest by both the
generated Desktop wrapper and the dynamic shell shim.

Disposition: `CONTINUE_WITH_MINIMAL_GUARD`. This is required behavior inside
the approved shell/Desktop generation contract and existing write set.

```text
RED: Python 3.12.13
Ran 1 method in 1.799s
FAILED (failures=2, errors=0)
Desktop and shell both returned zero and wrote the legacy backend marker.
```

```text
RED: system Python 3.9.6
Ran 1 method in 1.459s
FAILED (failures=2, errors=0)
Desktop and shell both returned zero and wrote the legacy backend marker.
```

The minimal GREEN reserves the `parity_` manifest namespace. Any parity field
now invokes `validate_internal_runtime_generation()`; incomplete evidence
fails before backend execution, while a manifest with zero parity fields keeps
the established legacy path.

```text
GREEN focused guard
Python 3.12.13: 1/1 in 1.274s
system Python 3.9.6: 1/1 in 1.235s
```

### Fresh Final Serial Verification

```text
Parity
Python 3.12.13: 83/83 in 2.148s
system Python 3.9.6: 83/83 in 28.050s
```

```text
Protocol Adapter
Python 3.12.13: 39/39 in 23.968s
system Python 3.9.6: 39/39 in 21.133s
```

```text
Runtime Binding
Python 3.12.13: 65/65 in 57.578s
system Python 3.9.6: 65/65 in 110.328s
```

```text
Transaction
Python 3.12.13: 234/234 in 21.881s
system Python 3.9.6: 234/234 in 119.746s
```

```text
Profile
Python 3.12.13 complete: 201/201 in 281.464s
system Python 3.9.6 supported projection routes: 2/2 in 4.282s
```

Direct system-Python profile CLI evidence:

```text
exit: 2
message: codex-profile-switch: Python 3.11+ with tomllib is required before any profile state mutation
temporary store created: no
```

### Static and Authority Gates

```text
active strict OpenSpec: valid
all strict OpenSpec: 18 passed, 0 failed
Python 3.12.13 AST: 56/56
system Python 3.9.6 AST: 56/56
commit_runtime_binding_pair matches under scripts/: 0
commit_runtime_binding_bundle production owners:
  scripts/codex_switch_bindings.py
  scripts/codex_switch_transaction.py
shared runtime generation production owners:
  scripts/codex_switch_runtime_binding.py
  scripts/codex_switch_app_wrapper.py
  scripts/codex_switch_shim.py
Protocol Adapter rule-set digest definitions: 1
capability receipt path definitions: 1
git diff --check: passed
generated bytecode residue: none
```

The integrated review found no remaining blocking correctness, compatibility,
false-health, crash-recovery, or scope findings in the Runtime bundle/rebind
slice.

### Shell Profile Isolation

Every dynamic suite used:

```text
CODEX_SWITCH_SHELL_PROFILE=/private/tmp/codex-switch-validation.ZLjc15/.zshrc
```

The real shell profile remains unchanged:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mtime: 1785055828
ctime: 1785055828
```

No live profile, App, provider, install, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred. Progress is 39/79; task 5.1 is dependency-ready.

### Next Action

Add task 5.1 tests-only RED for the staged internal update contract. Do not run
a real installer, binary swap, profile mutation, or Human Gate 8.1 action.

## 2026-07-26 Staged Internal Update RED

Timestamp: 2026-07-26T18:12:36+08:00
Task: 5.1
Result: expected RED captured

### Capability and Seam

- OpenSpec apply state: ready, 39/79 complete before this task.
- Test-first capability: ready through the trusted project-local `tdd` skill.
- Confirmed public seams: `scripts/codex_env_setup update-internal` and
  `scripts/codex-switch update-internal`.
- External boundaries: the team installer, `codesign`, and `curl` are replaced
  only by temporary deterministic test scripts.
- Real installer, profile, App, provider, and installation paths are excluded.

### Changed Files

- `scripts/test_codex_update_release.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-internal-update-red.md`

### Test Contract

Seven `CodexStagedInternalUpdateTests` require:

- an explicit candidate install directory that is a mode-`0700` private
  sibling of the bound `codex` binary;
- byte- and mode-identical bound state while the installer and candidate
  executable are probed;
- exact requested-versus-observed semantic version enforcement;
- code-sign before validation of the final candidate bytes;
- propagation of installer exit `17` as exit `17`;
- dry-run output for target version, candidate path class, parity checks,
  artifact set, and promotion order with zero writes; and
- no bound replacement or success wording when candidate
  parity/compatibility fails.

The valid installer fixture also proves that model, Azure endpoint, auth input,
and intended version reach the trusted installer unchanged.

### RED Evidence

Syntax and diff checks:

```text
Python 3.12 AST: syntax-ok
system Python 3.9 AST: python39-syntax-ok
git diff --check -- scripts/test_codex_update_release.py: exit 0
```

Focused Python 3.12:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_update_release.py CodexStagedInternalUpdateTests -v
Ran 7 tests in 5.270s
FAILED (failures=12, errors=0)
```

Focused system Python 3.9:

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 \
  scripts/test_codex_update_release.py CodexStagedInternalUpdateTests -v
Ran 7 tests in 3.738s
FAILED (failures=12, errors=0)
```

Complete Python 3.12 update/release:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py
Ran 120 tests in 228.528s
FAILED (failures=12, errors=0)
```

All 113 pre-existing methods remained green. The failures are confined to the
seven new methods; the count is 12 because the dry-run method records five
missing report labels and the prohibited in-place move text as independent
subtest assertions.

### Expected Failure Map

- Non-sibling candidate: current helper installs successfully instead of
  rejecting before `curl`.
- Private mode: current helper creates the candidate directory as `0755` under
  controlled `umask 022`.
- Intended version: requested `2.0.0` accepts observed `2.0.1`.
- Code-sign order: candidate `--version` runs before the fake `codesign`, so a
  candidate requiring final signed bytes exits nonzero.
- Failure propagation: installer exit `17` is converted to helper exit `1`.
- Dry-run: output advertises moving the existing bound binary, omits the five
  required staged parity/promotion fields, and otherwise leaves the temporary
  fixture unchanged.
- Parity-before-replacement: a helper-installed candidate that fails
  app-server compatibility replaces the bound binary before the failure.

No failure is an import, fixture, syntax, or unrelated baseline regression.

### Boundary Evidence

The real `~/.zshrc` remains byte- and metadata-identical:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mtime: 1785055828
ctime: 1785055828
```

No production source, live profile, App, provider, install, dependency,
release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, or Git history effect occurred.

### Next Item

Task 5.2: refactor `scripts/codex_env_setup` to install only into an explicit
validated private sibling candidate directory, keep the bound binary unchanged,
preserve model/endpoint/auth inputs, enforce exact candidate version and
code-sign ordering, and propagate installer failures. Binary swap, parity
promotion, and the complete wrapper dry-run remain later tasks.

## 2026-07-26 Staged Installer Candidate GREEN

Timestamp: 2026-07-26T18:29:44+08:00
Task: 5.2
Result: GREEN

### Capability and Scope

- OpenSpec apply state: ready, 40/79 complete before this task.
- Test-first and change-review capabilities: ready through the trusted
  project-local `tdd` and `code-review` skills.
- Write set: `scripts/codex_env_setup`, the existing staged update test class,
  and main-owned control-plane/evidence files.
- Explicit exclusions: executable swap journal, wrapper parity preparation,
  full dry-run plan, post-promotion handshake, live install/update, profile/App
  mutation, and Human Gate 8.1.

### Changed Files

- `scripts/codex_env_setup`
- `scripts/test_codex_update_release.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-installer-verified.md`

### RED Evidence

The bounded mutation guard was added before the identity implementation:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 \
  scripts/test_codex_update_release.py \
  CodexStagedInternalUpdateTests.test_env_setup_detects_bound_mutation_by_installer -v
Ran 1 test in 1.621s
FAILED (failures=1)
```

```text
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 \
  scripts/test_codex_update_release.py \
  CodexStagedInternalUpdateTests.test_env_setup_detects_bound_mutation_by_installer -v
Ran 1 test in 1.445s
FAILED (failures=1)
```

Both failures were the expected false success: the installer changed the bound
bytes, while the helper returned zero and printed `Bound internal Codex remains
unchanged`.

### GREEN Contract

`scripts/codex_env_setup` now:

- requires an explicit, absent `.codex-internal-update-*` directory whose
  resolved parent is the bound binary's parent;
- creates and revalidates that directory as a regular mode-`0700` directory;
- passes model, Azure endpoint, auth input, and exact intended version to the
  trusted installer without changing them;
- never moves, backs up, replaces, or deletes the bound binary;
- captures the bound binary through an `O_NOFOLLOW` descriptor and binds
  dev, inode, mode, size, nanosecond mtime/ctime, and SHA-256;
- rechecks that identity after installer, code-sign, and candidate `--version`
  execution;
- code-signs before parsing and enforcing the final exact semantic version; and
- propagates installer, code-sign, and candidate-probe nonzero statuses without
  converting them to generic success.

### Focused GREEN Evidence

Python 3.12:

```text
six installer/helper methods
Ran 6 tests in 4.143s
OK
```

Native system Python 3.9 helper path:

```text
PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 \
  scripts/test_codex_update_release.py <six helper methods> -v
Ran 6 tests in 6.894s
OK
```

The single mutation guard passes on both test runners after implementation.

### Planned Remaining RED

The complete staged class intentionally remains nonzero:

```text
Ran 8 tests
FAILED (failures=2)
```

The only failing methods are:

- `test_update_internal_dry_run_reports_complete_zero_mutation_plan`
- `test_candidate_probe_failure_preserves_bound_before_parity_promotion`

They are wrapper/promotion work reserved for tasks 5.5-5.6 and are not
implemented by task 5.2.

### Broader Regression and Review

The corrected pre-existing-suite selector reported:

```text
selected pre-existing tests: 113
Ran 113 tests in 222.367s
OK
```

An initial ad hoc selector omitted the `scripts/` import path and produced 42
`ModuleNotFoundError` results; it was a harness error, not a product result, and
the corrected identical 113-test selection passed.

```text
bash -n scripts/codex_env_setup: passed
Python 3.12 test AST: passed
system Python 3.9 test AST: passed
git diff --check -- scripts/codex_env_setup scripts/test_codex_update_release.py: passed
main review: no blocking scope, correctness, exit-status, or false-success finding
```

### Boundary Evidence

`HEAD`, `origin/main`, and branch remain:

```text
0a9400dca86ff94dcbc2b6868057e088781cc49f
main
```

The real shell profile remains unchanged:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785055828
```

No live profile, App, provider, install, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup, or
Git history effect occurred.

### Next Item

Task 5.3: add tests-only executable-swap journal RED coverage for exact
bound/candidate/backup siblings, no embedded binary bytes, mode/digest checks,
prepared rollback, committed roll-forward, rename interruption points, and
foreign binary preservation. Do not implement the swap journal in task 5.3.

## 2026-07-26 Executable-Swap Journal RED

Timestamp: 2026-07-26T18:48:44+08:00
Task: 5.3
Result: RED contract verified

### Capability and Scope

- OpenSpec apply state: ready, 41/79 complete before this task.
- `test-first-execution` and `architecture-guidance`: ready through the trusted
  project-local `tdd` and `codebase-design` skills.
- Approved seam: a typed `RuntimeBindingExecutableSwap` value passed as the
  optional `executable_swap` argument to `commit_runtime_binding_bundle()`.
- Marker contract: top-level `executable_swap` stores only exact paths,
  old/new modes, and old/new SHA-256 digests; binary payload bytes are never
  embedded.
- Explicit exclusions: production implementation, wrapper integration,
  handshake/backup retirement, live install/update, profile/App mutation, and
  Human Gate 8.1.

### Changed Files

- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-executable-swap-red.md`

### RED Evidence

Python 3.12.13:

```text
five executable-swap methods
Ran 5 tests in 0.334s
FAILED (failures=23, errors=0)
```

System Python 3.9.6:

```text
five executable-swap methods
Ran 5 tests in 0.284s
FAILED (failures=23, errors=0)
```

Every assertion fails at the same intended missing seam:

```text
Runtime binding executable-swap seams are missing:
RuntimeBindingExecutableSwap
```

There are no import, fixture, syntax, or unexpected production failures.

### Contract Coverage

The five methods require:

- exact bound path and direct sibling backup path;
- a candidate executable inside a private sibling staging directory;
- pairwise-distinct paths and rejection before marker publication;
- regular non-symlinked old/new executables with exact mode and SHA-256;
- no existing or foreign backup before commit;
- prepared rollback after `before_bound_to_backup`,
  `after_bound_to_backup`, `before_candidate_to_bound`,
  `after_candidate_to_bound`, and `after_manifest`;
- committed roll-forward after committed-marker publication and after marker
  retirement;
- retained old backup after committed promotion for the later handshake; and
- fail-closed preservation of foreign bound, candidate, or backup bytes in
  both prepared and committed recovery.

### Existing Baseline

The pre-existing 234 transaction methods were selected by AST and run through
the real test script path so multiprocessing spawn retained a valid main
module:

```text
Python 3.12.13: Ran 234 tests in 22.044s, OK
system Python 3.9.6: Ran 234 tests in 119.804s, OK
```

Both accepted runs set `CODEX_SWITCH_SHELL_PROFILE` to a private temporary
file. Two discarded harness attempts are not counted:

- an import selector omitted `scripts/` from `sys.path`;
- a `<stdin>` selector broke macOS multiprocessing spawn and caused four
  lock-holder readiness failures.

### Shell-Profile Boundary Incident

Before the isolation correction, one otherwise passing unisolated baseline
run used the real shell bootstrap path and atomically rewrote `~/.zshrc` with
byte-identical content. The semantic state stayed unchanged:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
size: 1959
mode: 600
mtime: 1785055828
```

The filesystem identity changed once:

```text
previous inode: 48028504
current inode: 48362010
current ctime: 1785062545
```

The accepted isolated Python 3.12 and system Python 3.9 runs each asserted the
real file's hash and full current stat tuple before and after the suite; both
were stable. All later transaction-suite commands must keep the shell-profile
override.

No live profile, App, provider, internal install/update, dependency, release,
archive, provider/root-state migration, legacy skill cleanup, destructive
cleanup, or Git history effect occurred.

### Next Item

Task 5.4: implement the smallest typed executable-swap extension to the
schema-v3 bundle journal, use exact sibling rename/digest recovery, preserve
schema-v1/v2 behavior, and make all five task-5.3 methods GREEN.

## 2026-07-26 Executable-Swap Journal GREEN

Timestamp: 2026-07-26T19:04:23+08:00
Task: 5.4
Result: GREEN

### Capability and Scope

- OpenSpec apply state: ready, 42/79 complete before this task.
- `test-first-execution` and `architecture-guidance`: ready.
- Production write set:
  `scripts/codex_switch_transaction.py`.
- Existing RED test set:
  `scripts/test_codex_transaction.py`.
- Explicit exclusions: update wrapper integration, candidate parity
  preparation, post-promotion handshake, backup retirement, live install or
  update, and Human Gate 8.1.

### Implemented Contract

The transaction module now exposes:

```text
RuntimeBindingExecutableSwap(
  bound_path,
  candidate_path,
  backup_path,
  old_mode,
  old_sha256,
  new_mode,
  new_sha256,
)
```

`commit_runtime_binding_bundle()` accepts it through one optional
`executable_swap` argument. When absent, the existing schema-v3 marker shape
and behavior are unchanged.

When present:

- bound and backup are direct siblings;
- candidate is the same executable basename inside a mode-0700
  `.codex-internal-update-*` sibling stage;
- all paths are absolute, normalized, distinct, no-follow routed, and
  non-overlapping with text bundle targets;
- old/new mode and lowercase SHA-256 evidence must match the current regular
  executable files before marker publication;
- the marker stores paths, modes, and digests only;
- old bound is durably renamed to backup, then candidate to bound;
- text artifacts retain their existing activation order with manifest last;
- prepared recovery restores old bound, restores the candidate, removes the
  backup, and rolls the text bundle back;
- committed recovery retains old backup, keeps candidate absent, and rolls the
  binary plus text bundle forward; and
- any bound/candidate/backup triple outside the three known phases is reported
  as foreign binary state without overwrite or deletion.

Main review replaced the stage-directory `lstat` check with a no-follow opened
parent descriptor and revalidates the private-stage path contract whenever a
binary phase is classified.

### RED to GREEN

Recorded RED from task 5.3:

```text
Python 3.12.13: 5 methods, 23 expected failures, 0 errors
system Python 3.9.6: 5 methods, 23 expected failures, 0 errors
cause: missing RuntimeBindingExecutableSwap
```

Fresh focused GREEN after the final review edit:

```text
Python 3.12.13: Ran 5 tests in 0.708s, OK
system Python 3.9.6: Ran 5 tests in 0.726s, OK
```

### Complete Transaction Regression

All runs set `CODEX_SWITCH_SHELL_PROFILE` to a private temporary file and
asserted the real shell profile hash and full current stat tuple before and
after:

```text
Python 3.12.13:
Ran 239 tests in 22.863s
OK

system Python 3.9.6:
Ran 239 tests in 120.646s
OK
```

The full suite includes schema-v1/v2 fixture recovery, schema-v3 markers
without executable swaps, all existing text-bundle fault phases, and the five
new swap methods.

### Static, Interface, and Review Evidence

```text
strict OpenSpec: valid
Python 3.12 AST/import: passed
system Python 3.9 AST/import: passed
commit interface includes one optional executable_swap argument
typed fields are exactly the seven approved path/mode/digest fields
authority scan: production swap ownership only in codex_switch_transaction.py
git diff --check: passed
generated __pycache__ under scripts: none
main review: no blocking correctness, compatibility, scope, or foreign-state finding
```

The real shell profile remains at:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

This is the stable post-incident identity recorded in task 5.3; task 5.4
caused no further change.

No new live profile, App, provider, internal install/update, dependency,
release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, or Git history effect occurred.

### Next Item

Task 5.5: add wrapper-level RED tests proving `update-internal` prepares
capability, parity, config, and overlay artifacts against the staged candidate,
revalidates all fingerprints under the store lock, and never probes the bound
path first.

## 2026-07-26 Staged Update Wrapper RED

Timestamp: 2026-07-26T19:24:06+08:00
Task: 5.5
Result: expected RED captured

### Capability and Scope

- OpenSpec apply state: ready, 43/79 complete before this task.
- `test-first-execution`: ready through the trusted project-local `tdd`
  capability.
- Confirmed public seam: `scripts/codex-switch update-internal`.
- Test-only write set: `scripts/test_codex_update_release.py` plus main-owned
  OpenSpec/control-plane/evidence files.
- Explicit exclusions: wrapper production integration, successful promotion,
  post-promotion handshake, backup retirement, live internal update, profile or
  App mutation, dependency changes, and Human Gate 8.1.

### RED Contract

The staged update class now requires:

- a zero-mutation dry-run that names staged capability/parity receipts, the
  model-catalog overlay, projected profile/shared/active-runtime configs,
  managed launcher/manifest, complete locked fingerprint set, and
  post-promotion-only bound app-server smoke;
- staged candidate capability generation through
  `app-server generate-json-schema` before any bound executable invocation;
- exact bound, candidate, and backup paths at one internal
  `promote-internal-update` adapter boundary;
- complete capability/parity/overlay/config/runtime artifact roles; and
- lock-held revalidation of bound/candidate binaries, internal manifest,
  official reference, source catalog, capability receipt, and profile/shared/
  active-runtime config inputs.

The promotion-driver fixture exits 73 after preparation and lock-held
revalidation, before any binary or runtime-bundle promotion. All files and
processes are temporary.

### Expected Failure Evidence

Python 3.12.13:

```text
Ran 4 tests in 1.946s
FAILED (failures=4)
Errors: 0
```

System Python 3.9.6:

```text
Ran 4 tests in 2.014s
FAILED (failures=4)
Errors: 0
```

The four failures are direct behavior assertions:

- dry-run still passes the bound install directory and exits before reporting
  candidate artifacts or lock revalidation;
- the legacy helper path still overwrites the bound binary before candidate
  parity failure;
- candidate capability generation never reaches the staged binary; and
- the wrapper never invokes the locked promotion boundary, so helper exit 92
  is returned instead of the fixture's deliberate exit 73.

No failure is a syntax, import, fixture, or unrelated baseline error.

### Preserved GREEN and Broader Regression

```text
Task-5.2 installer methods:
Python 3.12.13: 6/6
system Python 3.9.6: 6/6

Pre-existing update/release tests:
Python 3.12.13: 113/113 in 225.396s
```

Static and hygiene evidence:

```text
Python 3.12 test syntax: passed
system Python 3.9 test AST: passed
focused git diff --check: passed
generated test bytecode residue: none
main review: no blocking scope, fixture, or false-positive finding
```

Every accepted command set `CODEX_SWITCH_SHELL_PROFILE` to a temporary file and
asserted the real `~/.zshrc` identity before and after:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

No production implementation, live profile, App, provider, install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Item

Task 5.6: integrate private sibling candidate staging, candidate capability and
parity preparation, exact executable swap, and runtime-bundle promotion into
`run_update_internal_env_setup`. Do not report success before version,
canonical binding, app-server, capability-receipt, and parity-receipt
postconditions pass.

## 2026-07-26 Staged Internal Update Promotion Verified

Timestamp: 2026-07-26T21:02:46+08:00
Task: 5.6
Result: GREEN verified

### Capability and Scope

- OpenSpec apply state before control-plane closure: ready, 44/79 complete.
- `test-first-execution`: ready through the trusted project-local `tdd`
  capability; dependency diagnosis returned `ready_with_recommendations`.
- Production path reviewed:
  `run_update_internal_env_setup` -> `promote-internal-update` ->
  `cmd_promote_internal_update` -> internal parity-aware rebind and
  schema-v3 bundle commit.
- Task write set: `scripts/codex-switch`,
  `scripts/codex_switch_bindings.py`,
  `scripts/test_codex_profile_switch.py`, plus main-owned OpenSpec,
  control-plane, verification, and checkpoint files.
- Explicit exclusions: task-5.7 handshake rollback, task-5.8 backup retirement
  and restart output, live internal update, profile/App mutation, dependency
  changes, and Human Gate 8.1.

### Implemented Contract

- Public `--install-dir` and `CODEX_INSTALL_DIR` values continue to identify
  and validate the internal profile's bound binary directory.
- The trusted helper always receives a fresh private mode-0700
  `.codex-internal-update-*` sibling and the exact bound binary path.
- Candidate version/capability/parity/config/overlay/runtime preparation occurs
  before bound-path replacement.
- Promotion delegates exact bound, candidate, backup, and target-version
  values to one hidden production command.
- The store mutation lock revalidates the bound/candidate binaries, manifest,
  official reference, source catalog, capability receipt, and relevant config
  inputs before the typed executable swap and schema-v3 runtime bundle commit.
- Success output follows the installed-version, canonical Runtime Binding,
  app-server child attestation, capability-receipt, and parity-receipt
  postconditions.
- A post-promotion handshake failure is intentionally not closed by this item;
  task 5.7 adds RED rollback coverage and task 5.8 makes it GREEN before backup
  retirement.

### Fresh GREEN Evidence

All commands used
`CODEX_SWITCH_SHELL_PROFILE=/private/tmp/codex-switch-task-5.6.IkqQzy/.zshrc`
and `PYTHONDONTWRITEBYTECODE=1`.

```text
CodexStagedInternalUpdateTests
Python 3.12.13: 10/10 in 10.114s
system Python 3.9.6: 10/10 in 8.040s

Complete update/release
Python 3.12.13: 123/123 in 226.745s

Profile internal-update selector
Selection: test names beginning with update_internal, internal_update,
one_key_internal, blocked_current, internal_auto_update, the successful
auto-update comparison, or the wrapper internal-update-check guard
Python 3.12.13: 30/30 in 93.772s
system Python 3.9.6: 30/30 in 86.036s

Complete profile
Python 3.12.13: 201/201 in 272.950s

Parity
Python 3.12.13: 83/83 in 2.157s
system Python 3.9.6: 83/83 in 34.837s

Runtime Binding
Python 3.12.13: 65/65 in 56.647s
system Python 3.9.6: 65/65 in 120.601s

Executable-swap transaction selector
Python 3.12.13: 5/5 in 0.740s
system Python 3.9.6: 5/5 in 0.702s
```

Both mismatched CLI `--install-dir` and mismatched `CODEX_INSTALL_DIR` routes
reject before helper invocation. Main review found no blocking correctness,
compatibility, scope, false-success, or live-mutation issue inside task 5.6.

### Boundary and Hygiene

The real `~/.zshrc` remained unchanged before and after every accepted run:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

Generated `scripts/__pycache__` residue: none.

No live profile, App, provider, internal install/update, dependency, release,
archive, provider/root-state migration, legacy skill cleanup, destructive
cleanup, or Git history effect occurred.

### Post-Control-Plane Checks

```text
openspec validate internal-official-feature-parity --strict --no-interactive
Change 'internal-official-feature-parity' is valid

openspec validate --all --strict --no-interactive
18 passed, 0 failed

openspec instructions apply --change internal-official-feature-parity --json
45/79 complete; task 5.7 is the first unchecked item

bash -n scripts/codex-switch scripts/codex_env_setup
passed

Python 3.12 AST: 56/56 files
system Python 3.9 AST: 56/56 files
git diff --check: passed
```

### Next Item

Task 5.7: add tests-only RED coverage proving any failed post-promotion version,
canonical binding, app-server, capability receipt, overlay, config, or parity
handshake restores the old binary backup and complete old runtime bundle.

## 2026-07-26 Post-Promotion Handshake Rollback RED

Timestamp: 2026-07-26T21:20:52+08:00
Task: 5.7
Result: expected RED captured

### Capability and Scope

- OpenSpec apply state before control-plane closure: ready, 45/79 complete.
- `test-first-execution`: ready through the trusted project-local `tdd`
  capability; dependency diagnosis returned `ready_with_recommendations`.
- Approved public seam: hidden production command
  `promote-internal-update`.
- Test-only write set: `scripts/test_codex_runtime_binding.py` plus main-owned
  OpenSpec/control-plane/evidence files.
- Explicit exclusions: rollback implementation, backup retirement,
  restart-required output, live internal update, profile/App mutation,
  dependency changes, and Human Gate 8.1.

### RED Contract

Seven methods now require complete old-generation restoration after independent
post-promotion failure of:

- installed version;
- canonical Runtime Binding;
- app-server smoke;
- capability receipt;
- managed overlay;
- projected profile config; and
- parity receipt verification.

Every fixture first installs a complete old generation, then prepares a
byte-distinct new generation containing:

- the bound binary;
- manifest;
- managed launcher;
- capability receipt;
- parity receipt;
- model-catalog overlay;
- internal profile config;
- authoritative shared config; and
- active derived runtime config.

The command must raise the expected handshake `SwitchError`, print no verified
update success, and restore all nine targets to the old bytes and modes.
Failure injection targets the real underlying checks and does not replace
`_verify_internal_update_promotion`.

### Expected Failure Evidence

```text
Python 3.12.13:
Ran 7 tests in 37.428s
FAILED (failures=7)
Errors: 0

system Python 3.9.6:
Ran 7 tests in 89.100s
FAILED (failures=7)
Errors: 0
```

Every method reaches its intended handshake failure. The final assertion then
reports the same nine unrestored targets:

```text
active_runtime_config
bound_binary
capability_receipt
launcher
manifest
parity_overlay
parity_receipt
profile_config
shared_config
```

This is the missing task-5.8 rollback, not a syntax, import, fixture, candidate
preparation, or unrelated baseline error.

### Preserved GREEN

```text
Complete-bundle/rebind adjacency:
Python 3.12.13: 3/3 in 7.788s
system Python 3.9.6: 3/3 in 17.189s

Executable-swap transaction selector:
Python 3.12.13: 5/5 in 0.744s
system Python 3.9.6: 5/5 in 0.766s
```

Main review found and closed one test-quality gap before checkpointing: the
first fixture reused identical overlay/config payloads across generations.
The final fixture now makes every runtime target byte-distinct, so a partial
rollback cannot false-pass.

### Boundary and Hygiene

The real `~/.zshrc` remains at the stable post-task-5.3 identity:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

Generated `scripts/__pycache__` residue: none.

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Post-Control-Plane Checks

```text
openspec validate internal-official-feature-parity --strict --no-interactive
Change 'internal-official-feature-parity' is valid

openspec validate --all --strict --no-interactive
18 passed, 0 failed

openspec instructions apply --change internal-official-feature-parity --json
46/79 complete; task 5.8 is the first unchecked item

Python 3.12 AST: 56/56 files
system Python 3.9 AST: 56/56 files
tracked and touched-untracked whitespace checks: passed
generated bytecode residue: none
HEAD and origin/main: 0a9400d
```

### Next Item

Task 5.8: retain rollback authority through the complete post-promotion
handshake, restore the old binary and complete old runtime bundle on any
failure, retire the old backup only after durable success, add
restart-required output only then, and make the seven 5.7 methods GREEN.

## 2026-07-26 Post-Promotion Handshake Rollback GREEN

Timestamp: 2026-07-26T22:04:44+08:00
Task: 5.8
Result: complete

### Capability and Scope

- OpenSpec apply state before closure: ready, 46/79 complete.
- `test-first-execution`: ready through the trusted project-local `tdd`
  capability; source dependency diagnosis returned
  `ready_with_recommendations`.
- Production write set:
  `scripts/codex_switch_transaction.py`,
  `scripts/codex_switch_bindings.py`, and
  `scripts/test_codex_runtime_binding.py`.
- Bounded incidental safety guard:
  `scripts/test_codex_transaction.py`.
- Explicit exclusions remained live internal update/rebind, profile/App
  mutation, provider/model/API/auth changes, dependency changes, release,
  archive, Git effects, destructive cleanup, and Human Gate 8.1.

### Implementation

`commit_runtime_binding_bundle()` keeps the schema-v3 marker prepared through
an optional `prepared_validator`. A validator failure therefore executes the
existing prepared recovery path and restores:

- the old bound binary;
- manifest;
- managed launcher;
- capability receipt;
- parity receipt;
- model-catalog overlay;
- profile config;
- authoritative shared config; and
- active derived runtime config.

After the validator returns, the transaction revalidates the complete promoted
generation, publishes `committed`, converges committed recovery, and only then
retires the exact mode/digest-checked backup when requested.

`cmd_promote_internal_update()` passes the full version, canonical binding,
app-server child, capability-receipt, artifact, parity-receipt, and immutable
input handshake as the prepared validator. It requests backup retirement only
for the staged executable swap and suppresses ordinary rebind output. Verified
success and restart-required output occur only after the transaction returns.

### Fresh GREEN Evidence

```text
Python 3.12.13 Runtime Binding:
Ran 74 tests in 109.873s
OK

system Python 3.9.6 Runtime Binding:
Ran 74 tests in 244.134s
OK

Python 3.12.13 transaction after the safety guard:
Ran 239 tests in 24.153s
OK

system Python 3.9.6 transaction after the safety guard:
Ran 239 tests in 140.002s
OK
```

The Runtime Binding suites include all seven task-5.7 failure cases, successful
backup retirement, restart output ordering, adjacent complete-bundle/rebind
coverage, and executable-swap integration. Failure paths print neither
verified success nor restart-required output, leave no backup or marker, and
restore the candidate plus all nine old-generation targets.

### Validation Isolation Incident

The first fresh Python 3.12 transaction run did not set
`CODEX_SWITCH_SHELL_PROFILE`. It passed 239/239 in 24.947s but atomically
rewrote the real `~/.zshrc` with byte-identical content. The immediately
started system-Python run was stopped.

Before:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

After:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

The bounded repair moves shell-profile isolation into
`TransactionTests.setUp`, assigning each test its own temporary
`CODEX_SWITCH_SHELL_PROFILE`. Both final full suites intentionally ran without
an external isolation variable and preserved the complete new stable tuple.
The canonical validation command blocks now also establish a private shell
profile before dynamic suites.

### Post-Control-Plane Checks

```text
openspec validate internal-official-feature-parity --strict --no-interactive
Change 'internal-official-feature-parity' is valid

openspec validate --all --strict --no-interactive
18 passed, 0 failed

Python 3.12 AST: 56/56 files
system Python 3.9 AST: 56/56 files
tracked and touched-untracked whitespace checks: passed
generated bytecode residue: none
HEAD and origin/main: 0a9400d
```

Main review found no blocking spec, rollback-authority, foreign-state,
backup-retirement, output-order, or scope issue.

No shell content, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Item

Task 5.9: prove `set-bin internal <external-path>` commits the same parity
bundle without moving, copying, deleting, or journal-owning the external
backend.

## 2026-07-26 External Backend Ownership Proof

Timestamp: 2026-07-26T22:11:08+08:00
Task: 5.9
Result: complete

### Scope

- Production behavior: unchanged.
- Test write set: `scripts/test_codex_runtime_binding.py`.
- Control-plane write set: active OpenSpec tasks, ledger, state, verification,
  and checkpoint.
- Explicit exclusions: executable-swap behavior changes, external binary
  writes, live internal rebind/update, profile/App/provider changes,
  dependencies, release/archive, Git effects, and Human Gate 8.1.

### Ownership Contract

The test executes the real `cmd_set_bin()` internal path with a backend under
an external directory and captures the schema-v3 marker immediately after
durable prepared publication.

It proves the marker contains all eight parity/runtime roles:

```text
active_runtime_config
capability_receipt
launcher
manifest
parity_overlay
parity_receipt
profile_config
shared_config
```

It also proves:

- the marker contains no `executable_swap`;
- no artifact path targets the external backend;
- device, inode, full mode, link count, size, mtime, ctime, and bytes remain
  exact across the command;
- the external parent directory entry set remains exact;
- no regular file under the profile store contains a same-byte backend copy;
- the final manifest and Runtime Binding reference the original external path;
  and
- no runtime-rebind marker remains after success.

### Evidence

The first run produced one test-only error on each runtime:

```text
NameError: name 'stat' is not defined
```

The error occurred in the final managed-copy scan after the external identity
and marker checks had executed. Adding the missing test import required no
production change.

Fresh accepted results:

```text
Focused ownership proof:
Python 3.12.13: Ran 1 test in 2.669s, OK
system Python 3.9.6: Ran 1 test in 5.989s, OK

Adjacent ownership/bundle/rollback selector:
Python 3.12.13: Ran 3 tests in 7.752s, OK
system Python 3.9.6: Ran 3 tests in 17.639s, OK
```

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Item

Task 5.10: run the complete dual-runtime update/release, transaction, Runtime
Binding, parity, and supported profile verification matrix before selecting
task 6.1.

## 2026-07-26 Staged Update Slice Closure

Timestamp: 2026-07-26T22:47:22+08:00
Task: 5.10
Result: complete

### Scope

- Production source: unchanged.
- Control-plane write set: active tasks, ledger, state, verification, and
  checkpoint.
- Explicit exclusions: live update/rebind, App/profile/provider mutation,
  dependency changes, commit, push, release, archive, cleanup, and Human Gate
  8.1.

### Fresh Serial Matrix

```text
Python 3.12.13
update/release: 123/123 in 221.574s
transaction: 239/239 in 24.524s
Runtime Binding: 75/75 in 111.688s
parity: 83/83 in 2.096s
complete profile: 201/201 in 280.376s

system Python 3.9.6
update/release: 123/123 in 252.430s
transaction: 239/239 in 139.227s
Runtime Binding: 75/75 in 253.637s
parity: 83/83 in 34.185s
supported profile projection routes: 2/2 in 4.924s
```

The direct system-Python complete profile attempt ran 201 tests in 196.500s
and reported one failure plus 83 errors. Every reported path resolves to the
existing explicit Python 3.11+ `tomllib` requirement. The supported projection
tests install their bounded parser fixture and pass. A direct CLI boundary
check returned:

```text
exit: 2
store created: no
message: codex-profile-switch: Python 3.11+ with tomllib is required before any profile state mutation
```

The first system-Python transaction invocation accidentally received a PTY,
reached the expected interactive home selector, and was interrupted before a
write. The accepted non-interactive rerun is the 239/239 result above.

### Static and Workflow Gates

```text
active strict OpenSpec: valid
all strict OpenSpec: 18 passed, 0 failed
OpenSpec apply: 49/79, task 6.1 first
workflow validator: ok=true, issues=0
Bash syntax: 5/5
Python 3.12.13 AST: 56/56
system Python 3.9.6 AST: 56/56
git diff --check: passed
changed-file trailing whitespace: 0
generated bytecode residue: 0
```

The workflow validator retains two non-blocking existing warnings: legacy root
state migration before the 1.0.0 sunset and the intentionally pending compact
recommendation at this checkpoint.

### Validation Budget and Complexity Gate

- task-local validation: focused regression only;
- slice closure: complete required dual-runtime matrix for that slice;
- integrated/final gates: full-project verification only at tasks 7.x/9.x;
- no adjacent complete-suite repetition unless related code changed, a result
  was not collected, or a real failure requires a rerun; and
- no shared abstraction, extra fault axis, or non-contract edge test without a
  named failing acceptance criterion. Otherwise record
  `DEFER_AND_CONTINUE`.

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Item

Task 6.1: add verifier tests-only RED for parity evidence loading/evaluation,
stable findings, sanitized reports, deterministic optional queue, and
`--repair=none` zero writes.

## 2026-07-26 Parity Verifier RED

Timestamp: 2026-07-26T22:57:25+08:00
Task: 6.1
Result: expected RED captured

### Scope

- Test write set: `scripts/test_codex_verify.py`.
- Production source: unchanged.
- Public behavior seams: `collect_verification_problems()`,
  `write_verification_report()`, and `cmd_verify()` with `repair=none`.
- Explicit exclusions: task 6.2 implementation, status/Doctor integration,
  public CLI expansion, live repair, dependency changes, and Human Gate 8.1.

### RED Contract

Five tests require:

1. Missing, malformed, stale reference/runtime/provider/config/overlay/adapter
   evidence to preserve stable `parity.*` finding codes.
2. Core protocol, unclassified feature, and typed-role probe failures to make
   verification unhealthy.
3. Optional-only findings to remain healthy and expose a sorted synchronization
   queue.
4. One collected `ParityReport` to flow into a structured report with secret
   sanitization and intact codes/queue entries.
5. `--repair=none` to collect parity once, return nonzero for unhealthy
   evidence, and leave every pre-existing store file byte- and mode-exact.

### Expected Failures

```text
Python 3.12.13
Ran 5 tests in 0.021s
FAILED (failures=5, errors=0)

system Python 3.9.6
Ran 5 tests in 0.017s
FAILED (failures=5, errors=0)
```

Three failures identify the missing `parity_report` collection parameter, one
identifies the missing structured-report parameter, and one proves
`cmd_verify()` currently prints success instead of observing the injected
missing-receipt report. No test failed from fixture setup, imports, syntax, or
runtime variance.

### Focused Static Evidence

```text
Python 3.12 compile: passed
system Python 3.9 compile: passed
active strict OpenSpec: valid
git diff --check: passed
untracked test whitespace: clean
generated bytecode residue: none
```

The explicit compile command created one
`scripts/__pycache__/test_codex_verify.cpython-312.pyc`; it was removed
exactly, and the now-empty generated directory was removed.

The DevFlow dependency check reports the project-local `tdd` methodology
resource ready. Its overall `workflowReady=false` comes from pre-existing
unrelated DevFlow source conflicts and legacy skill-layout recommendations.
Those require separate migration/cleanup authority and were not changed.

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Item

Task 6.2: implement the smallest read-only parity load/evaluation path in the
verifier and reuse one result for collection and report generation. Run only
the five task-6.1 tests to GREEN before selecting adjacent verification.

## 2026-07-26 Parity Verifier Integration

Timestamp: 2026-07-26T23:10:41+08:00
Task: 6.2
Result: focused GREEN

### Scope

- Production write set: `scripts/codex_switch_verify.py`.
- Focused test addition: one loader-contract method in
  `scripts/test_codex_verify.py`.
- Existing seams: `collect_verification_problems()`,
  `write_verification_report()`, and `cmd_verify()`.
- Explicit exclusions: status/Doctor production integration, public CLI
  expansion, repair routing, live profile/App/provider mutation, dependency
  changes, and Human Gate 8.1.

### Implementation

`collect_parity_report()` now:

- reports an old manifest with no receipt as `parity.receipt.missing`;
- reads only the existing bounded mode-0600 profile-local receipt;
- validates receipt and manifest ownership through
  `load_parity_receipt_artifact()`;
- checks the current Protocol Adapter digest and canonical runtime generation;
- checks official/internal binary, source catalog, and projected config
  fingerprints without regenerating schema, features, probes, or artifacts;
  and
- returns one `ParityReport` reused by collection, structured reporting, and
  `cmd_verify`.

Only error findings become verification problems. Optional-only findings keep
the report healthy and expose the receipt's deterministically sorted
synchronization queue. Structured output preserves codes and queue structure
while the existing sanitizer removes sensitive message content.

### TDD Evidence

The added loader contract first failed on both runtimes with:

```text
AttributeError: module 'codex_switch_verify' has no attribute
'collect_parity_report'
```

Fresh focused GREEN:

```text
Python 3.12.13
Ran 6 ParityVerificationTests in 0.026s
OK

system Python 3.9.6
Ran 6 ParityVerificationTests in 0.036s
OK
```

Four adjacent regressions covering canonical runtime-smoke selection, binding
failure containment, structured smoke reporting, and unique report allocation
also pass 4/4 in 0.878s and 0.561s respectively. Both interpreters parse the
two touched Python files.

Per the layered validation budget, task 6.2 did not repeat the unchanged full
verifier, diagnostics-slice, staged-update, or project-wide matrices.

### Control-Plane Verification

```text
active strict OpenSpec: valid
all strict OpenSpec: 18/18
OpenSpec apply: 51/79, task 6.3 first
workflow validator: ok=true, issues=0
workflow warning: existing legacy root-state migration reminder
git diff --check: passed
touched untracked trailing whitespace: none
Python 3.12 AST: 2/2 touched files
system Python 3.9 AST: 2/2 touched files
generated scripts bytecode residue: none
HEAD == origin/main: 0a9400d
```

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

### Boundary

`verify --repair=none` performs zero store writes in the focused contract. No
receipt, overlay, config, profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

### Next Item

Task 6.3: add tests-only RED for shared parity health codes and deterministic
optional queue ordering across status, Doctor, and profile verification. Do not
implement task 6.4 in the same item.

## 2026-07-26 Parity Diagnostics RED

Timestamp: 2026-07-26T23:20:59+08:00
Task: 6.3
Result: expected RED captured

### Scope

- Test write set: `scripts/test_codex_profile_switch.py`.
- Production source: unchanged.
- Existing seams: `codex_switch_status.cmd_status`,
  `codex_switch_doctor.cmd_doctor`, and `codex_switch_verify.cmd_verify`.
- Explicit exclusions: task 6.4 production integration, repair routing, public
  CLI expansion, live profile/App/provider mutation, dependency changes, and
  Human Gate 8.1.

### RED Contract

The two tests require all three commands to:

1. collect the same injected `ParityReport` exactly once;
2. print `Parity health: healthy|unhealthy`;
3. print identical stable `Parity finding: <code>` lines;
4. keep warning-only optional drift healthy; and
5. print the deterministic synchronization queue in category/identifier/code
   order.

The first run reached the expected status/Doctor assertions but verify errored
before parity collection because the temporary store had no internal manifest.
The test seam now supplies an empty read-only manifest, allowing verify to
reach the already mocked collector without changing production behavior.

Fresh expected RED:

```text
Python 3.12.13
Ran 2 tests in 0.027s
FAILED (failures=6, errors=0)

system Python 3.9.6
Ran 2 tests in 0.026s
FAILED (failures=6, errors=0)
```

Status and Doctor fail because parity collection is absent. Verify collects
exactly once, then fails because it prints only the existing verification
summary and not the shared health/finding/queue diagnostics.

Per the layered validation budget, task 6.3 did not repeat the unchanged
complete profile, verifier, diagnostics-slice, staged-update, or project-wide
matrices.

### Control-Plane Verification

```text
active strict OpenSpec: valid
all strict OpenSpec: 18/18
OpenSpec apply: 52/79, task 6.4 first
workflow validator: ok=true, issues=0
workflow warning: existing legacy root-state migration reminder
Python 3.12 AST: passed
system Python 3.9 AST: passed
git diff --check: passed
touched trailing whitespace: none
generated scripts bytecode residue: none
HEAD == origin/main: 0a9400d
```

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, Git history, or Human Gate 8.1 effect occurred.

### Next Item

Task 6.4: integrate parity reporting through the existing verifier-owned
collection/presentation seam into narrow status and Doctor callers, then make
only the two task-6.3 tests GREEN. Do not add a second policy implementation or
start task 6.5 repair routing.

## 2026-07-26 Parity Diagnostics Integration

Timestamp: 2026-07-26T23:30:34+08:00
Task: 6.4
Result: focused GREEN

### Scope

- Production write set:
  `scripts/codex_switch_verify.py`,
  `scripts/codex_switch_status.py`, and
  `scripts/codex_switch_doctor.py`.
- Focused test seam: `scripts/test_codex_profile_switch.py`.
- Explicit exclusions: repair routing, new public CLI, parity
  preparation/reclassification, package/docs work, live effects, dependency
  changes, and Human Gate 8.1.

### Implementation

- `print_parity_diagnostics()` derives health from the existing structured
  parity result, prints stable finding codes, and sorts synchronization rows by
  their canonical queue key.
- `parity_problem_messages()` reuses the same error findings and sanitizes
  messages before Doctor or verify displays them.
- `cmd_verify()` prints the one report it already collected.
- `cmd_status()` reports parity only when the active profile is internal.
- `cmd_doctor()` reuses its active Runtime Binding, reports parity only for
  active internal, and includes parity error findings in its existing failure
  result.
- A collector invoked without a binding resolves internal Runtime Binding only
  after the receipt itself is healthy and full generation validation is
  required.

No caller implements classification, finding severity, receipt loading, or
queue policy.

### TDD Evidence

Fresh focused GREEN:

```text
Python 3.12.13: shared diagnostics 2/2 in 0.017s
system Python 3.9.6: shared diagnostics 2/2 in 0.016s
Python 3.12.13: ParityVerificationTests 6/6 in 0.026s
system Python 3.9.6: ParityVerificationTests 6/6 in 0.039s
Python 3.12.13: adjacent status/Doctor regressions 3/3 in 4.762s
Python 3.12 AST: 4/4 touched files
system Python 3.9 AST: 4/4 touched files
```

Two direct system-Python adjacent subprocess cases stop during init at the
established Python 3.11+ `tomllib` boundary; the adjacent Doctor case that
explicitly selects the supported interpreter passes. This is not a task-6.4
production failure.

### Incidental Finding

`DEFER_AND_CONTINUE`: the existing one-key internal fixture contains a legacy
manifest with no parity receipt, so verification now stops with
`parity.receipt.missing`. The current acceptance criterion is diagnostics
consistency, not repair. Tasks 6.5/6.6 already own the explicit staged rebind
repair contract; no fallback, in-place patch, fixture-only production hook, or
public CLI was added here.

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No live profile, App, provider, internal install/update, receipt, overlay,
config, dependency, release, archive, provider/root-state migration, legacy
skill cleanup, destructive cleanup, Git history, or Human Gate 8.1 effect
occurred.

### Next Item

Task 6.5: add tests-only RED for explicit parity repair routing through staged
internal rebind and for zero in-place mutation from ordinary status, Doctor,
and `verify --repair=none`. Do not implement task 6.6 in the same item.

## 2026-07-26 Parity Repair Routing RED

Timestamp: 2026-07-26T23:36:01+08:00
Task: 6.5
Result: expected RED captured

### Scope

- Test write set:
  `scripts/test_codex_verify.py` and
  `scripts/test_codex_profile_switch.py`.
- Production source: unchanged.
- Existing production route under contract:
  `codex_switch_bindings.cmd_set_bin`.
- Explicit exclusions: task 6.6 implementation, new public CLI, in-place
  artifact repair, live effects, dependency changes, and Human Gate 8.1.

### RED Contract

Explicit parity repair must:

1. receive the current verified `RuntimeBinding`;
2. delegate to `cmd_set_bin` with `name=internal`,
   `codex_bin=<current backend>`, and `preserve_app_cli=False`;
3. use the existing staged parity preparation and schema-v3 runtime-bundle
   promotion path; and
4. recollect parity after rebind and base command success on the fresh report.

Fresh expected RED:

```text
Python 3.12.13
Ran 2 tests in 0.015s
FAILED (failures=2, errors=0)

system Python 3.9.6
Ran 2 tests in 0.014s
FAILED (failures=2, errors=0)
```

The failures are exactly:

- `repair_internal_parity` does not exist; and
- `verify --repair=safe` performs no staged rebind or second parity
  collection, so it prints the original missing-receipt report and exits 1.

### Read-Only Characterization

```text
Python 3.12.13: 1/1 in 0.018s
system Python 3.9.6: 1/1 in 0.020s
```

Normal status, active-internal Doctor, and `verify --repair=none` preserve the
exact inode, mode, size, mtime, ctime, and bytes of:

- internal manifest;
- parity receipt;
- managed model overlay;
- internal profile config; and
- managed internal launcher.

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, public CLI, live profile, App, provider, internal
install/update, dependency, release, archive, provider/root-state migration,
legacy skill cleanup, destructive cleanup, Git history, or Human Gate 8.1
effect occurred.

### Next Item

Task 6.6: implement the smallest current-backend staged rebind route and
recollect parity after explicit safe repair. Do not add a new public command or
modify parity artifacts in place.

## 2026-07-26 Parity Repair Routing Integration

Timestamp: 2026-07-26T23:44:05+08:00
Task: 6.6
Result: focused GREEN

### Scope

- Production write set: `scripts/codex_switch_verify.py`.
- Existing test contract:
  `scripts/test_codex_verify.py` and
  `scripts/test_codex_profile_switch.py`.
- Explicit exclusions: public CLI changes, direct receipt/overlay/config/
  launcher/manifest patching, package/docs work, live effects, dependency
  changes, and Human Gate 8.1.

### Implementation

- `repair_internal_parity(args, binding)` locally imports
  `codex_switch_bindings.cmd_set_bin` to avoid a module cycle.
- The delegated namespace fixes `name=internal`,
  `codex_bin=<binding.backend_cli>`, and `preserve_app_cli=False`.
- `cmd_verify` calls the route only for explicit safe repair when the current
  internal parity result is unhealthy.
- After repair, verify reloads manifest/active state, resolves Runtime Binding
  again, recollects parity, and prints/evaluates only the fresh result.

### TDD Evidence

Fresh RED before implementation:

```text
Python 3.12.13: 2 tests in 0.014s, 2 failures, 0 errors
system Python 3.9.6: 2 tests in 0.018s, 2 failures, 0 errors
```

Fresh GREEN:

```text
Python 3.12.13: focused repair 2/2 in 0.108s
system Python 3.9.6: focused repair 2/2 in 0.068s
Python 3.12.13: ParityVerificationTests 8/8 in 0.146s
system Python 3.9.6: ParityVerificationTests 8/8 in 0.098s
Python 3.12.13: read-only artifact characterization 1/1 in 0.015s
system Python 3.9.6: read-only artifact characterization 1/1 in 0.015s
Python 3.12 and system Python 3.9 compile: passed
targeted `git diff --check`: passed
```

The explicit compile command produced one ignored Python 3.12 bytecode file;
that exact file was removed without touching other cache content.

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No live profile, App, provider, internal install/update, public CLI, direct
parity artifact mutation, dependency, release, archive, provider/root-state
migration, legacy skill cleanup, destructive cleanup, Git history, or Human
Gate 8.1 effect occurred.

### Next Item

Task 6.7: add package/release RED tests for the parity module, transitive
imports, generated launcher references, immutable payload file set, and
absence of retained probe/config evidence, then make them GREEN without
starting docs task 6.8.

## 2026-07-26 Parity Package Integration

Timestamp: 2026-07-26T23:53:25+08:00
Task: 6.7
Result: focused GREEN

### Scope

- Production write set:
  `scripts/codex_switch_release_bundle.py`,
  `scripts/package-release.sh`, and
  `scripts/codex_switch_promotion.py`.
- Test seams:
  `scripts/test_codex_update_release.py` and
  `scripts/test_codex_profile_switch.py`.
- Explicit exclusions: docs task 6.8, authority scan task 6.9, complete
  diagnostics matrix 6.10, live effects, dependency changes, release
  publication, and Human Gate 8.1.

### RED Contract

Fresh dual-runtime RED had five methods and eight failures:

- four newly required parity/launcher modules were not source-required;
- missing transitive runtime imports did not block packaging;
- import-time payload mutation did not block packaging;
- unresolved generated `$SWITCH_SCRIPTS` targets did not block packaging; and
- the real package manifest omitted the four runtime-required paths.

```text
Python 3.12.13: 5 methods, 8 failures, 0 errors in 2.010s
system Python 3.9.6: 5 methods, 8 failures, 0 errors in 2.032s
```

### Implementation

- Added `codex_switch_parity.py`, `codex_switch_runtime_binding.py`,
  `codex_switch_app_proxy.py`, and `codex_switch_home_sync.py` to the package
  required-module/required-path contract.
- Release staging scans generated `$SCRIPT_DIR`/`$SWITCH_SCRIPTS` Python
  references and rejects any target missing from the payload.
- Every packaged non-test Python module imports under `-I -B` in an isolated
  copied payload; the exact file/directory/mode/digest snapshot must remain
  unchanged.
- Packaging resolves Python 3.11+ with `tomllib`, including when the outer test
  process is system Python 3.9.
- Historical immutable canonicalization adds inert placeholders for the same
  newly required modules without changing the original legacy tree.

### GREEN Evidence

```text
Python 3.12.13: focused package 5/5 in 2.618s
system Python 3.9.6: focused package 5/5 in 2.683s
Python 3.12.13: adjacent release/promotion 4/4 in 10.687s
system Python 3.9.6: adjacent release/promotion 4/4 in 12.311s
Python 3.12.13: profile package adapter 1/1 in 1.364s
system Python 3.9.6: profile package adapter 1/1 in 1.472s
post-review reference/manifest selector: 2/2 on both runtimes
Bash syntax: passed
dual-runtime AST: 4/4 Python files
targeted `git diff --check`: passed
```

Isolated actual `scripts/package-release.sh`:

```text
manifest files: 66
manifest directories: 5
required paths: 20
archive members: 73
archive size: 522880 bytes
payload SHA-256: bbd79beaf00d33a48009630284ac84bb8547e215f2122e2fb1781d59c8428ae5
parity module present: true
retained probe present: false
config/auth evidence present: false
bytecode present: false
```

### Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No live profile, App, provider, internal install/update, dependency, release
publication, archive, provider/root-state migration, legacy skill cleanup,
retained-evidence cleanup, Git history, or Human Gate 8.1 effect occurred.

### Next Item

Task 6.8: update only `README.md` and `SKILL.md` with the approved
official-reference boundary, core/optional findings, no-v1-fallback
remediation, staged update semantics, and explicit live Desktop acceptance
gate.

## 2026-07-26 Parity Operator Contract

Timestamp: 2026-07-26T23:57:47+08:00
Task: 6.8
Result: docs/static GREEN

### Scope

- Updated only `README.md` and `SKILL.md` for the task contract.
- Preserved all existing unrelated documentation and dirty-worktree changes.
- Explicit exclusions: authority scans task 6.9, diagnostics slice closure
  6.10, production code, complete-suite reruns, and every live/Human Gate 8.1
  effect.

### Documented Contract

- The canonical Runtime Binding's current verified ChatGPT Desktop bundled CLI
  is the official parity reference. PATH, network latest, cached release
  metadata, and the stable advisory are observations only.
- Internal binary, model, endpoint, provider, and auth remain the complete
  allowed identity differences.
- Core, unclassified, missing, stale, malformed, and failed-probe evidence is
  unhealthy with stable codes. Known optional drift remains a deterministic
  synchronization queue unless policy escalates it.
- Missing or failed multi-agent v2 evidence never silently selects v1.
  Explicit `verify internal --repair=safe` routes through staged
  current-backend rebind and does not patch parity artifacts in place.
- `update-internal` prepares a private sibling candidate, proves parity before
  replacement, retains last-known-good through the complete handshake, restores
  or preserves it on failure without success/restart output, and prints one
  restart notice only after durable success and backup retirement.
- Source tests, update success, and rebind success do not satisfy live
  acceptance. ChatGPT quit/reopen, a provider-backed typed `explorer` task, and
  runtime ownership attestation remain behind explicit Human Gate 8.1
  authorization.

### Focused Evidence

```text
git diff --check -- README.md SKILL.md: passed
README parity-contract scan: all required terms found
SKILL parity-contract scan: all required terms found
obsolete `Codex.app` scan in README.md/SKILL.md: zero matches
active strict OpenSpec: passed
```

No complete Python, profile, transaction, update/release, package, or
project-wide suite was repeated because related production code did not change.

### Boundary

No production code, live profile, App, provider, internal install/update,
dependency, commit, push, release, archive, provider/root-state migration,
legacy skill cleanup, destructive cleanup, retained-evidence cleanup, or Human
Gate 8.1 effect occurred.

### Next Item

Task 6.9: run only the planned `rg` authority scans for Runtime Binding,
Protocol Adapter, Capability Receipt, and the single production parity
implementation. Do not start slice-closure task 6.10 or any live effect.

## 2026-07-27 Parity Authority Closure

Timestamp: 2026-07-27T00:07:37+08:00
Task: 6.9
Result: focused GREEN

### Scope

- Scanned Runtime Binding for parity classification ownership.
- Scanned Protocol Adapter and its Capability Receipt definitions for
  provider/overlay and official-reference policy.
- Scanned all production callers for parity finding, queue, policy evaluation,
  and overlay construction.
- Fixed only the one confirmed violation in
  `scripts/codex_switch_verify.py`.
- Explicit exclusions: task 6.10 full diagnostics slice matrix, integrated
  task 7, live effects, dependencies, Git effects, release/archive, cleanup,
  and Human Gate 8.1.

### TDD Evidence

Fresh RED before the production edit:

```text
Python 3.12.13: 1 test in 0.001s, 1 failure, 0 errors
system Python 3.9.6: 1 test in 0.001s, 1 failure, 0 errors
failure: Parity must own evidence-error finding classification.
```

The minimal implementation adds `parity_error_report()` to the parity module.
It owns unresolved official/internal fingerprints, stable error severity, and
code-to-category mapping. Verifier imports that entry point and supplies only
the evidence code/message, profile directory, and optional current backend.

Fresh GREEN:

```text
Python 3.12.13: focused ownership 1/1 in 0.003s
system Python 3.9.6: focused ownership 1/1 in 0.002s
Python 3.12.13: ParityVerificationTests 8/8 in 0.158s
system Python 3.9.6: ParityVerificationTests 8/8 in 0.128s
dual-runtime compile for parity/verifier: passed
```

The explicit compile check created two ignored Python 3.12 bytecode files;
those exact generated files were removed, and no other cache content was
touched.

### Authority Evidence

```text
Runtime Binding parity-classification scan: zero hits
Protocol Adapter provider/overlay-policy scan: zero hits
Capability Receipt official-reference-policy scan: zero hits
production caller construction scan: zero hits
```

The single production implementation locations are all in
`scripts/codex_switch_parity.py`:

```text
ParityFinding: line 2176
ParityQueueItem: line 2212
ParityPolicyEvaluation: line 2242
prepare_parity_overlay: line 4966
evaluate_parity_policy: line 7687
parity_error_report: line 8103
```

### Control-Plane Checks

```text
active strict OpenSpec: valid
all strict OpenSpec: 18 passed, 0 failed
OpenSpec apply: 58/79 complete, task 6.10 next
DevFlow workflow validator: ok=true, 0 issues
workflow warning: legacy root state migration before the 1.0.0 sunset
Python 3.12 AST: 3/3 touched files
system Python 3.9 AST: 3/3 touched files
git diff/trailing-whitespace checks: passed
production caller authority scan: zero hits outside parity
generated bytecode residue: zero
```

### Boundary

No complete adjacent suite was repeated under the layered validation budget.
No live profile, App, provider, internal install/update, dependency, commit,
push, release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, retained-evidence cleanup, or Human Gate 8.1 effect
occurred.

### Next Item

Task 6.10: run the recorded focused verifier, Doctor/status, package, parity,
profile, and update/release slice-closure suites on Python 3.12 and system
Python 3.9 before selecting task 7.

## 2026-07-27 Diagnostics and Package Slice Closure

Timestamp: 2026-07-27T00:15:14+08:00
Task: 6.10
Result: dual-runtime focused GREEN

### Scope

The slice-closure matrix covers:

- parity reference and error-classification ownership;
- all verifier parity evidence, reporting, repair, and zero-write contracts;
- shared status/Doctor/verify health, queue ordering, and read-only artifacts;
- packaged docs and immutable package runtime imports;
- release-bundle containment, manifest, historical, and generated-reference
  contracts;
- staged internal update candidate/parity ordering; and
- immutable package status, release workflow ordering, and historical
  installer/runner migration.

It intentionally does not run the complete file-level integrated suites owned
by tasks 7.1 and 7.2.

### Python 3.12.13

Validation root:
`/private/tmp/codex-switch-parity-610-py312.oPgVL2`

```text
ParityReferenceTests: 9/9 in 0.073s
ParityVerificationTests: 8/8 in 0.155s
profile diagnostics/package seams: 4/4 in 1.529s
CodexUpdateReleaseTests: 37/37 in 22.639s
CodexStagedInternalUpdateTests: 10/10 in 9.721s
package/promotion/workflow adjacency: 3/3 in 9.260s
total: 71/71, zero failures/errors
```

### System Python 3.9.6

Validation root:
`/private/tmp/codex-switch-parity-610-py39.Bdl7GL`

```text
ParityReferenceTests: 9/9 in 0.078s
ParityVerificationTests: 8/8 in 0.123s
profile diagnostics/package seams: 4/4 in 1.400s
CodexUpdateReleaseTests: 37/37 in 24.581s
CodexStagedInternalUpdateTests: 10/10 in 7.626s
package/promotion/workflow adjacency: 3/3 in 10.123s
total: 71/71, zero failures/errors
```

### Mutation Boundary

The real `~/.zshrc` remains:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production code changed during task 6.10. No acceptance failure, generated
bytecode residue, live profile/App/provider/internal update, dependency,
commit, push, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, retained-evidence cleanup, or Human Gate 8.1
effect occurred.

### Next Item

Task 7.1: run the complete parity suite on Python 3.12 and system Python 3.9
as the first integrated verification gate.

## 2026-07-27 Integrated Parity Verification

Timestamp: 2026-07-27T00:18:32+08:00
Task: 7.1
Result: dual-runtime complete GREEN

### Commands and Results

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
Ran 84 tests in 2.151s
OK

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
Ran 84 tests in 32.688s
OK
```

Both runs cover the complete parity module and retained fixtures, including
the task-6.9 ownership regression. No test was filtered or skipped.

### Boundary

No production or test source changed. The real `~/.zshrc` retained SHA-256
`8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4`,
inode `48897140`, size `1959`, mode `600`, mtime `1785055828`, and ctime
`1785074064`. No bytecode residue, live profile/App/provider/internal update,
dependency, commit, push, release, archive, cleanup, or Human Gate 8.1 effect
occurred.

### Next Item

Task 7.2: run the complete cross-module integrated suites serially on Python
3.12, then repeat the project-required dual-runtime routes on system Python
3.9.

## 2026-07-27 Integrated Cross-Module Verification

Timestamp: 2026-07-27T01:12:15+08:00
Task: 7.2
Result: dual-runtime integrated GREEN

### Python 3.12.13

Validation root:
`/private/tmp/codex-switch-parity-72-py312.iIn50R`

```text
Protocol Adapter: 39/39 in 23.720s
Runtime focused regression: 1/1 in 2.042s
Runtime Binding: 75/75 in 112.316s
transaction: 239/239 in 23.888s
verifier: 30/30 in 10.958s
update/release: 126/126 in 253.292s
complete profile: 204/204 in 273.063s
```

The 15 profile methods affected by the new parity gate pass 15/15 in 54.376s.
One lookup-only fixture initially reached the correct
`parity.receipt.missing` failure; adding its existing `--skip-verify`
isolation made the focused method and then all 15 pass without changing
production behavior.

### System Python 3.9.6

Validation root:
`/private/tmp/codex-switch-parity-72-py39.I5Wg11`

```text
Protocol Adapter: 39/39 in 22.916s
Runtime Binding: 75/75 in 249.496s
transaction: 239/239 in 137.982s
verifier: 30/30 in 10.847s
update/release: 126/126 in 300.648s
supported profile projection routes: 2/2 in 5.063s
direct profile CLI: exit 2 before store creation
```

The first verifier run reported eight fixture errors because generated managed
wrappers inherited the Python 3.9 test runner. The fixture now uses the same
installed Python 3.12/3.11 selection already used by Runtime Binding and
transaction tests. The three affected methods pass 3/3 in 5.908s; the full
verifier then passes on Python 3.9 and was refreshed on Python 3.12.

### Integrated Corrections

- `install.sh` and `run.sh` trust the current verified release-bundle module
  hash `dd121b4c...baac13` and promotion module hash
  `561f6720...ad199c`.
- Intentionally invalid Python release candidates are mutated only after valid
  bundle construction, then their manifest/archive are rebuilt.
- Fresh internal profiles without parity receipts remain unhealthy with
  `parity.receipt.missing`; no implicit repair or broad success path was added.
- Unrelated lookup/plugin tests skip verification explicitly rather than
  weakening the default one-key verification contract.

### Boundary and Hygiene

```text
dual-runtime AST for final touched tests: passed
targeted git diff --check: passed
generated bytecode residue: zero
~/.zshrc SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No live profile, App, provider, internal install/update, dependency, commit,
push, release, OpenSpec archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, retained-evidence cleanup, or Human Gate 8.1
effect occurred.

### Next Item

Task 7.3: run active and all strict OpenSpec validation.

## 2026-07-27 Strict OpenSpec Verification

Timestamp: 2026-07-27T01:14:12+08:00
Task: 7.3
Result: GREEN

```text
openspec validate internal-official-feature-parity --strict --no-interactive
Change 'internal-official-feature-parity' is valid

openspec validate --all --strict --no-interactive
Totals: 18 passed, 0 failed (18 items)
```

No source, test, live profile, App, provider, internal install/update,
dependency, commit, push, release, archive, cleanup, or Human Gate 8.1 effect
occurred.

### Next Item

Task 7.4: run the pinned DevFlow workflow validator and record all results
without editing generated guidance.

## 2026-07-27 Workflow State Verification

Timestamp: 2026-07-27T01:15:18+08:00
Task: 7.4
Result: GREEN_WITH_WARNING

```text
ok: true
issues: []
warning: Legacy DevFlow root state is read-only; migrate to
         .planning/devflow/STATE.md before the 1.0.0 sunset
```

The warning is pre-existing and outside the approved write/migration boundary.
No generated guidance, provider selection, dependency, root-state migration,
legacy skill cleanup, live state, Git, release, archive, or Human Gate 8.1
effect occurred.

### Next Item

Task 7.5: run Bash syntax, dual-runtime AST, and production-import scans.

## 2026-07-27 Static and Import Verification

Timestamp: 2026-07-27T01:16:22+08:00
Task: 7.5
Result: GREEN

```text
/bin/bash syntax: 5/5
Python 3.12.13 AST: 56/56
Python 3.12.13 production imports: 47/47
system Python 3.9.6 AST: 56/56
system Python 3.9.6 production imports: 47/47
generated bytecode residue: zero
```

The first PATH-relative `bash` command returned 127 before reading any file
because Bash is not on the tool shell PATH. The accepted `/bin/bash` command
passes every required entrypoint. No source or live state changed.

### Next Item

Task 7.6: build and validate an isolated release package.

## 2026-07-27 Isolated Package Verification

Timestamp: 2026-07-27T01:19:39+08:00
Task: 7.6
Result: GREEN

Validation root:
`/private/tmp/codex-switch-parity-76.tX4jAq`

```text
manifest files: 66
manifest directories: 5
required paths: 20
production imports: 47
archive members: 73
archive size: 525008 bytes
archive SHA-256: b9d21c9f4e5e880ca5858d7111f1728084a72cf656b54db384a5be922afe598a
manifest payload SHA-256:
  5cb103bb9f454b2767a9ae3f2e7dbd7cd9ed6a291b53cbeddc99b4a14746758d
```

The release validator and an independent structured audit verified:

- exact manifest versus actual file and directory sets;
- every file/directory mode, size, and SHA-256;
- all required paths and executable expectations;
- immutable import of all 47 packaged production modules under `-I -B`;
- exact tar member set, modes, sizes, and bytes; and
- absence of retained probe files, `.planning`, OpenSpec, testdata,
  `config.toml`, `auth.json`, symlinks, special files, and bytecode.

No repository output directory, live state, dependency, publication, Git
history, archive, cleanup, or Human Gate 8.1 effect occurred.

### Next Item

Task 7.7: run diff/write-set, ownership, and 66-scenario coverage audits.

## 2026-07-27 Diff, Write-Set, Authority, and Coverage Audit

Timestamp: 2026-07-27T01:32:26+08:00
Task: 7.7
Result: GREEN

### Diff and Dirty-Worktree Classification

```text
git diff --check
exit 0
```

A deterministic `git status --porcelain=v1 -uall` classifier attributes 71
dirty paths to `internal-official-feature-parity` and leaves 130 paths as
pre-existing or unrelated work. No path was reverted, staged, deleted, or
cleaned.

The exact active-change non-checkpoint set is:

```text
.planning/STATE.md
.planning/devflow/verification/internal-official-feature-parity.md
README.md
SKILL.md
TASK_LEDGER.md
install.sh
run.sh
openspec/changes/internal-official-feature-parity/.openspec.yaml
openspec/changes/internal-official-feature-parity/design.md
openspec/changes/internal-official-feature-parity/proposal.md
openspec/changes/internal-official-feature-parity/specs/codex-switch/spec.md
openspec/changes/internal-official-feature-parity/tasks.md
scripts/codex-switch
scripts/codex_env_setup
scripts/codex_switch_app_wrapper.py
scripts/codex_switch_bindings.py
scripts/codex_switch_config_document.py
scripts/codex_switch_doctor.py
scripts/codex_switch_home_sync.py
scripts/codex_switch_parity.py
scripts/codex_switch_promotion.py
scripts/codex_switch_protocol_adapter.py
scripts/codex_switch_release_bundle.py
scripts/codex_switch_runtime_binding.py
scripts/codex_switch_shim.py
scripts/codex_switch_status.py
scripts/codex_switch_transaction.py
scripts/codex_switch_verify.py
scripts/package-release.sh
scripts/test_codex_config_document.py
scripts/test_codex_parity.py
scripts/test_codex_profile_switch.py
scripts/test_codex_protocol_config.py
scripts/test_codex_runtime_binding.py
scripts/test_codex_transaction.py
scripts/test_codex_update_release.py
scripts/test_codex_verify.py
testdata/parity/retained-v2-probe-redacted.json
```

The remaining 33 active-change paths are the planned checkpoint plus every
`2026-07-26-parity-*` and `2026-07-27-parity-*` checkpoint. All other dirty
paths are the classifier complement and remain attributed to earlier changes,
existing project control-plane material, or unrelated work. Shared files such
as `TASK_LEDGER.md`, `.planning/STATE.md`, `README.md`, `SKILL.md`, shell
entrypoints, and common runtime modules contain earlier work as well; this
audit attributes only the task-recorded parity edits, not their complete
HEAD-relative diffs.

The canonical File Structure was corrected to include every actual parity
write seam omitted from its initial summary: the retained fixture,
`codex_switch_runtime_binding.py`, `codex_switch_shim.py`,
`codex_switch_release_bundle.py`, `codex_switch_promotion.py`, `install.sh`,
and `run.sh`.

`install.sh` and `run.sh` are necessary task-7.2 trust-anchor updates, not a
new update-framework expansion. Their parity-change ownership is limited to
binding these exact verified module bytes:

```text
scripts/codex_switch_release_bundle.py
  dd121b4cb32755f7e6a72f34f680acd2298541c03bf2be1dba637c2e5fbaac13
scripts/codex_switch_promotion.py
  561f6720f0b41e2fa19faad49d8738caef749f6b9a215a525a187bfda7ad199c
```

Both entrypoints contain the same two lowercase SHA-256 constants.

### Authority Scans

The exact fresh scans were:

```text
rg -n \
  'ParityFinding|ParityQueueItem|ParityPolicyEvaluation|evaluate_parity_policy|prepare_parity_overlay|parity_error_report|_PARITY_CLASSIFICATION_TABLES|PARITY_POLICY_VERSION' \
  scripts/codex_switch_runtime_binding.py
result: zero hits

rg -n \
  'OfficialReference|prepare_parity_overlay|ParityOverlay|model_catalog_json|multi_agent_version|tool_mode|_PARITY_CLASSIFICATION_TABLES|evaluate_parity_policy|PARITY_POLICY_VERSION' \
  scripts/codex_switch_protocol_adapter.py
result: zero hits

rg -n \
  'OfficialReference|official_reference|chatgpt-bundle|CURRENT_CHATGPT_BUNDLE_ID|parity_official_reference' \
  scripts/codex_switch_protocol_adapter.py
result: zero hits in the Capability Receipt owner

find scripts -maxdepth 1 -type f -name 'codex_switch_*.py' \
  ! -name 'codex_switch_parity.py' -print0 |
  xargs -0 rg -n \
  'ParityFinding\(|ParityQueueItem\(|ParityPolicyEvaluation\(|evaluate_parity_policy\(|prepare_parity_overlay\('
result: zero caller-owned policy constructions
```

The single production definitions remain in
`scripts/codex_switch_parity.py`:

```text
ParityFinding: 2176
ParityQueueItem: 2212
ParityPolicyEvaluation: 2242
prepare_parity_overlay: 4966
evaluate_parity_policy: 7687
parity_error_report: 8103
```

Verifier has four `parity_error_report()` delegation call sites and no local
finding/category construction. Runtime Binding retains executable, launcher,
Desktop-host, and attestation authority; Protocol Adapter retains exact
transform and capability-receipt authority; parity remains the only
classification, queue, overlay, and official-reference policy owner.

### Scenario-to-Evidence Audit

Aliases below name exact test classes:

```text
PR=ParityReferenceTests             FI=ParityFeatureInventoryTests
PI=ParityProtocolInventoryTests     PP=ParityPolicyTests
PS=ParitySerializationTests         RC=ParityReceiptTests
OV=ParityOverlayTests               BM=ParityBundleManifestTests
PREP=ParityPreparationTests         PROBE=ParityProbeTests
CP=ParityConfigProjectionTests      AE=ProtocolAdapterEvidenceTests
AT=ProtocolAdapterTests             CD=ConfigDocumentTests
RB=RuntimeBindingTests              TX=TransactionTests
UR=CodexUpdateReleaseTests          SU=CodexStagedInternalUpdateTests
VV=ParityVerificationTests          PF=CodexProfileSwitchTests
```

The first 60 scenarios map to named automated tests already covered by tasks
7.1-7.2. The final six are deliberately live-only and remain mapped to
unexecuted tasks 8.1-8.7.

| # | Scenario | Named regression or live task |
|---:|---|---|
| 1 | Current ChatGPT bundle is authoritative | `PR.test_verified_chatgpt_bundle_is_the_reference_authority`; `RB.test_official_resolution_uses_bundled_cli_for_full_chain` |
| 2 | PATH and network latest are not reference authority | `PR.test_path_observation_cannot_override_the_bundled_reference`; `PR.test_network_latest_cannot_be_constructed_as_reference_authority` |
| 3 | Official reference change invalidates prior evidence | `PR.test_reference_fingerprint_change_is_stale`; `RC.test_official_provider_and_runtime_drift_make_receipt_stale` |
| 4 | Non-whitelisted identity difference is classified | `PR.test_allowed_identity_difference_whitelist_is_exact_and_immutable`; `PP.test_known_optional_labels_do_not_whitelist_internal_only_drift` |
| 5 | Feature inventory separates default and effective state | `FI.test_isolated_defaults_are_distinct_from_effective_state` |
| 6 | Protocol inventory includes direction and transitive shape | `PI.test_all_four_directions_and_transitive_local_refs_are_recorded`; `PI.test_documentation_and_input_order_do_not_change_canonical_bytes` |
| 7 | Identical inputs produce identical inventory bytes | `FI.test_feature_order_and_canonical_bytes_are_deterministic`; `PI.test_documentation_and_input_order_do_not_change_canonical_bytes`; `PS.test_policy_receipt_payload_is_deterministic_and_rejects_unsafe_identity` |
| 8 | Unsupported schema construct fails closed | `PI.test_unsupported_schema_constructs_fail_closed`; `VV.test_core_unclassified_and_probe_failures_are_unhealthy` |
| 9 | Inventory persistence excludes sensitive material | `PS.test_inventory_payloads_exclude_external_context`; `PS.test_policy_receipt_payload_excludes_free_text_and_is_bounded`; `PROBE.test_sanitized_evidence_is_bounded_and_secret_stable` |
| 10 | Official core request must be accepted internally | `PI.test_compatibility_uses_the_actual_producer_direction`; `PP.test_baseline_protocol_closures_are_core_and_unhealthy` |
| 11 | Internal core response must satisfy Desktop | `PI.test_compatibility_uses_the_actual_producer_direction`; `PP.test_baseline_protocol_closures_are_core_and_unhealthy` |
| 12 | Proven adapter covers native drift | `AE.test_rule_set_digest_is_deterministic_and_policy_free`; `AE.test_rule_set_digest_covers_exact_tables_canonically`; `PR.test_candidate_binds_validated_adapter_rule_set_digest`; `AT.test_proxy_rejects_every_unproven_receipt_before_backend_or_file_mutation` |
| 13 | Additive optional field is not an automatic core failure | `PI.test_additive_optional_properties_are_compatible` |
| 14 | Known official-only extensions enter the queue | `PP.test_six_known_official_only_methods_are_optional_unless_observed` |
| 15 | Observed optional extension escalates to core | `PP.test_observed_optional_protocol_method_escalates_to_core` |
| 16 | Multi-agent v2 is core | `PP.test_multi_agent_v2_feature_and_model_metadata_are_core`; `PROBE.test_v1_or_nickname_only_subagent_never_passes` |
| 17 | Known metadata-only drift remains visible | `PP.test_known_development_and_stage_default_drift_are_optional` |
| 18 | Skill search absence is queued | `PP.test_skill_search_is_optional_unless_observed` |
| 19 | Official-only under-development features are queued | `PP.test_known_development_and_stage_default_drift_are_optional` |
| 20 | Tool mode is not inferred | `PP.test_tool_mode_is_pending_provider_optional_evidence`; `OV.test_tool_mode_addition_or_change_is_rejected` |
| 21 | New feature drift fails closed | `PP.test_unknown_feature_drift_is_unclassified_and_unhealthy` |
| 22 | Healthy receipt binds complete evidence | `RC.test_receipt_payload_is_canonical_and_binds_complete_evidence`; `BM.test_manifest_candidate_binds_every_required_parity_digest` |
| 23 | Receipt is profile-local and manifest-owned | `RC.test_profile_local_paths_modes_and_manifest_metadata_are_exact` |
| 24 | Missing or malformed receipt is unhealthy | `RC.test_missing_receipt_fails_with_stable_code`; `RC.test_symlink_non_regular_and_wrong_mode_receipts_are_rejected`; `RC.test_oversized_malformed_and_unsupported_receipts_are_rejected`; `VV.test_collect_parity_report_marks_missing_receipt_unhealthy` |
| 25 | Provider or runtime change makes receipt stale | `RC.test_official_provider_and_runtime_drift_make_receipt_stale`; `VV.test_evidence_failures_preserve_stable_finding_codes` |
| 26 | Optional queue is deterministic | `RC.test_optional_queue_round_trip_remains_healthy`; `VV.test_optional_only_queue_is_healthy_and_deterministic` |
| 27 | Missing v2 field is the only overlay change | `OV.test_unique_active_model_missing_field_adds_only_v2_path` |
| 28 | Existing v2 field requires no semantic change | `OV.test_existing_v2_has_zero_semantic_diff` |
| 29 | Source catalog remains byte-unchanged | `OV.test_deep_structure_and_source_bytes_and_mode_are_preserved`; `PREP.test_prepare_parity_bundle_orchestrates_complete_staged_candidate` |
| 30 | Ambiguous active model blocks overlay | `OV.test_missing_and_duplicate_active_model_slugs_are_rejected`; `OV.test_unsupported_roots_and_unsafe_sources_are_rejected`; `PF.test_set_bin_internal_unhealthy_parity_evidence_promotes_nothing` |
| 31 | Broader overlay mutation is rejected | `OV.test_tool_mode_addition_or_change_is_rejected`; `OV.test_every_broader_overlay_mutation_is_rejected` |
| 32 | Source changes during preparation | `OV.test_source_digest_and_identity_races_are_rejected`; `PREP.test_prepare_parity_bundle_orchestrates_complete_staged_candidate` |
| 33 | Internal profile selects overlay and v2 | `CP.test_internal_profile_projects_overlay_and_v2_only`; `PF.test_internal_home_config_uses_parity_projection_without_mutating_sources` |
| 34 | Exact stale assignment is removed | `CD.test_remove_exact_scalar_assignment_preserves_section_and_siblings`; `CP.test_already_clean_projection_is_byte_identical_and_idempotent` |
| 35 | Ambiguous max-threads config blocks promotion | `CP.test_duplicate_max_threads_is_unhealthy_and_writes_nothing`; `CP.test_dotted_max_threads_is_unhealthy_and_writes_nothing`; `CP.test_non_scalar_max_threads_is_unhealthy_and_writes_nothing`; `CP.test_inline_parent_max_threads_is_unhealthy_and_writes_nothing`; `CP.test_invalid_toml_is_unhealthy_and_writes_nothing`; `CP.test_multiply_sourced_max_threads_is_unhealthy_and_writes_nothing`; `CP.test_symlinked_config_source_is_unhealthy_and_writes_nothing`; `CP.test_concurrent_source_replacement_is_unhealthy_and_writes_nothing`; `CP.test_previously_read_source_replacement_is_unhealthy_and_writes_nothing` |
| 36 | Active managed home is updated in the same bundle | `RB.test_successful_internal_rebind_supplies_complete_schema_v3_bundle`; `RB.test_internal_rebind_only_promotes_materialized_active_internal_config`; `TX.test_runtime_rebind_bundle_schema_v3_optional_config_targets_are_explicit` |
| 37 | Failed v2 evidence has no v1 fallback | `PROBE.test_v1_or_nickname_only_subagent_never_passes`; `PF.test_set_bin_internal_unhealthy_parity_evidence_promotes_nothing`; `VV.test_core_unclassified_and_probe_failures_are_unhealthy` |
| 38 | Probe uses candidate artifacts | `PROBE.test_candidate_artifacts_and_core_method_order_are_exact` |
| 39 | Typed-role subagent probe completes | `PROBE.test_typed_explorer_v2_markers_are_required_for_success`; `PROBE.test_typed_subagent_completion_order_is_required` |
| 40 | Probe output is bounded and sanitized | `PROBE.test_sanitized_evidence_is_bounded_and_secret_stable`; `PROBE.test_retained_redacted_provider_fixture_never_copies_transient_config` |
| 41 | Probe timeout or malformed output fails | `PROBE.test_timeout_stops_before_later_probe`; `PROBE.test_malformed_or_missing_core_responses_fail_closed`; `PROBE.test_early_exit_is_distinct_from_missing_response`; `PROBE.test_oversized_output_is_rejected`; `PROBE.test_default_runner_terminates_the_complete_process_group` |
| 42 | Candidate changes during probe | `PROBE.test_candidate_input_change_during_probe_is_stale`; `PREP.test_prepare_parity_bundle_orchestrates_complete_staged_candidate` |
| 43 | Complete bundle is promoted together | `TX.test_runtime_rebind_bundle_promotes_in_deterministic_manifest_last_order`; `RB.test_successful_internal_rebind_supplies_complete_schema_v3_bundle` |
| 44 | Prepared interruption rolls back | `TX.test_runtime_rebind_bundle_prepared_fault_matrix_rolls_back_every_target` |
| 45 | Committed interruption rolls forward | `TX.test_runtime_rebind_bundle_committed_fault_matrix_rolls_forward_every_target` |
| 46 | Foreign target state fails closed | `TX.test_runtime_rebind_bundle_recovery_rejects_foreign_old_and_new_states_before_target_write`; `TX.test_runtime_rebind_bundle_recovery_does_not_overwrite_foreign_state_after_preflight` |
| 47 | Bundle target set is exact | `TX.test_runtime_rebind_bundle_schema_v3_has_exact_required_target_set`; `TX.test_runtime_rebind_bundle_rejects_invalid_target_sets_before_marker`; `TX.test_runtime_rebind_bundle_rejects_unsafe_target_types_before_marker` |
| 48 | Legacy rebind markers remain recoverable | `TX.test_runtime_rebind_legacy_schema_v1_v2_marker_fixtures_remain_byte_compatible` |
| 49 | Installer targets a sibling candidate | `SU.test_env_setup_stages_private_sibling_and_preserves_bound_inputs`; `SU.test_env_setup_rejects_non_sibling_candidate_before_installer` |
| 50 | Candidate parity precedes bound replacement | `SU.test_candidate_probe_failure_preserves_bound_before_parity_promotion`; `SU.test_candidate_capability_failure_never_probes_bound_path`; `SU.test_wrapper_delegates_complete_candidate_bundle_with_locked_revalidation` |
| 51 | Candidate failure preserves last-known-good | `SU.test_env_setup_propagates_installer_failure_status`; `SU.test_candidate_probe_failure_preserves_bound_before_parity_promotion`; `PF.test_set_bin_internal_unhealthy_parity_evidence_promotes_nothing` |
| 52 | Binary and runtime bundle recover together | `TX.test_runtime_rebind_executable_swap_prepared_fault_matrix_rolls_back_binary_and_runtime_bundle`; `TX.test_runtime_rebind_executable_swap_committed_fault_matrix_rolls_forward_binary_and_runtime_bundle` |
| 53 | Foreign binary state fails closed | `TX.test_runtime_rebind_executable_swap_recovery_preserves_foreign_bound_candidate_and_backup_states` |
| 54 | Backup survives until final handshake | `RB.test_promote_internal_update_rolls_back_failed_version_handshake`; `RB.test_promote_internal_update_rolls_back_failed_binding_handshake`; `RB.test_promote_internal_update_rolls_back_failed_app_server_handshake`; `RB.test_promote_internal_update_rolls_back_failed_receipt_handshake`; `RB.test_promote_internal_update_rolls_back_failed_overlay_handshake`; `RB.test_promote_internal_update_rolls_back_failed_config_handshake`; `RB.test_promote_internal_update_rolls_back_failed_parity_handshake`; `RB.test_promote_internal_update_retires_backup_after_success`; `RB.test_promote_internal_update_reports_restart_only_after_durable_success` |
| 55 | Internal update dry-run has zero mutation | `SU.test_update_internal_dry_run_reports_complete_zero_mutation_plan` |
| 56 | Read-only diagnostics do not repair | `VV.test_repair_none_parity_verification_has_zero_writes`; `PF.test_parity_diagnostics_share_unhealthy_core_code`; `PF.test_read_only_parity_diagnostics_preserve_owned_artifacts` |
| 57 | Optional drift is reported as a queue | `VV.test_optional_only_queue_is_healthy_and_deterministic`; `PF.test_parity_diagnostics_share_optional_queue_order` |
| 58 | Explicit repair uses staged rebind | `VV.test_explicit_parity_repair_uses_current_backend_set_bin`; `VV.test_safe_repair_rechecks_parity_after_staged_rebind` |
| 59 | Packaged runtime contains parity implementation | `UR.test_release_bundle_rejects_missing_required_python_modules`; `UR.test_release_bundle_rejects_missing_transitive_runtime_import`; `UR.test_release_bundle_rejects_runtime_import_payload_mutation`; `UR.test_release_bundle_rejects_unresolved_generated_script_reference`; `UR.test_successful_bundle_has_manifest_modes_digests_and_archive` |
| 60 | Official release advisory remains separate | `PF.test_internal_check_compares_with_official_stable_without_helper`; `PF.test_official_check_compares_bundled_prerelease_with_stable`; `PF.test_official_stable_lookup_failure_is_nonblocking`; `PR.test_verified_chatgpt_bundle_is_the_reference_authority` |
| 61 | Live acceptance requires Human Gate | live tasks `8.1-8.2`; not executed |
| 62 | Runtime ownership is attested before task | live tasks `8.2-8.4` and `8.6`; not executed |
| 63 | Explicit explorer child is observable | live task `8.5`; not executed |
| 64 | Desktop shows task-oriented child metadata | live tasks `8.5-8.6`; not executed |
| 65 | Child and parent complete under same ownership | live tasks `8.5-8.6`; not executed |
| 66 | Partial smoke cannot pass | live tasks `8.5-8.7`; not executed |

Coverage count:

```text
delta requirements: 12
delta scenarios: 66
automated mapped scenarios: 60
Human-Gated live scenarios: 6
unmapped scenarios: 0
```

### Boundary and Next Item

No production code, test behavior, live profile, App, provider, internal
install/update, dependency, commit, push, release, archive, cleanup, or Human
Gate 8.1 effect occurred. No integrated suite was repeated because task 7.2
already recorded fresh results and related code has not changed.

Task 7.8 is next: perform the read-only main-agent code review and resolve only
findings that correspond to a failing acceptance criterion inside the approved
write set.

## 2026-07-27 Read-Only Main-Agent Review

Timestamp: 2026-07-27T01:42:06+08:00
Task: 7.8
Result: GREEN

### Review Scope

The review used the canonical OpenSpec requirements, 66-scenario mapping, and
active-change write set rather than treating the mixed dirty-worktree diff as
one change. It inspected:

- receipt candidate parsing, canonical digest-bound loading, and
  `collect_parity_report()` false-health paths;
- source-catalog and config projection read/revalidation/write boundaries;
- schema-v3 prepared/committed recovery and executable-swap ordering;
- post-promotion handshake, rollback, backup retirement, and restart output;
- persisted probe/report/receipt sanitization and credential boundaries; and
- Protocol Adapter transform scope and policy ownership.

### Findings

```text
acceptance-criterion failures: 0
in-scope source fixes required: 0
new tests required: 0
full suites repeated: 0
```

Receipt health remains fail-closed. `_read_parity_receipt_candidate()` is only
a bounded preliminary parse used to compare manifest metadata. The authoritative
load is `load_parity_receipt_artifact()`, which reopens the canonical
profile-local artifact through directory descriptors, validates mode/identity,
requires the manifest payload digest, rejects duplicate keys and noncanonical
JSON, and compares official/internal fingerprints plus the current Protocol
Adapter digest. `collect_parity_report()` then validates the active
manifest/launcher/backend/capability receipt/parity receipt/overlay/runtime
config generation and current official binary, internal binary, source catalog,
and projected config digests before returning healthy.

Source and config boundaries remain narrow. Catalog and config readers reject
symlinks/non-regular files, bind identity and digest across reads, produce only
deep-copy or in-memory projected payloads, and revalidate source identity before
promotion. Before marker publication all mutable config inputs are rechecked;
after marker publication the journal validates exact old/new target states.
Only the approved profile/shared/active-runtime config targets can enter the
bundle, and the configured source catalog is never a transaction target.

Executable promotion retains last-known-good through the complete handshake.
The seven version/binding/app-server/capability-receipt/overlay/config/parity
failure tests each require the old binary and complete runtime bundle to be
restored, remove marker/backup state, retain the candidate, and emit neither
success nor restart output. Success coverage requires backup retirement and a
single restart notice only after the receipt handshake and durable cleanup.

Persisted parity data contains endpoint digests and auth-source kind, not
credential values. Probe output and verification reports are bounded and
sanitized. The Protocol Adapter remains an exact transform owner with no
provider, overlay, or parity-classification policy.

### Incidental Finding

`DEFER_AND_CONTINUE`: a real process crash after the committed marker has been
retired but before executable-backup retirement completes could leave a stale
old-binary backup without a recovery marker. At that point the promoted
generation and complete handshake are already durable, so this is cleanup
residue rather than false health, rollback loss, or mixed-generation recovery.
No approved acceptance criterion names this post-commit cleanup window.
Residual risk is an unexpected sibling backup requiring manual inspection; a
future dedicated cleanup/recovery contract can address it if product scope
requires automatic retirement.

### Boundary and Next Item

No production/test behavior, live profile/App/provider state, internal
install/update, dependency, commit, push, release, archive, cleanup, or Human
Gate 8.1 effect occurred. Related code has not changed since task 7.2, so the
layered validation budget forbids repeating the adjacent full matrix.

Progress is 67/79. Task 7.9 evidence consolidation is next.

## 2026-07-27 Pre-Human-Gate Evidence Consolidation

Timestamp: 2026-07-27T01:48:00+08:00
Task: 7.9
Result: GREEN

### Integrated Commands and Counts

Task 7.1 ran the exact required commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
84/84 in 2.151s

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
84/84 in 32.688s
```

Task 7.2 ran the cross-module suites serially:

```text
Python 3.12.13
Protocol Adapter: 39/39 in 23.720s
Runtime focused regression: 1/1 in 2.042s
Runtime Binding: 75/75 in 112.316s
transaction: 239/239 in 23.888s
verifier: 30/30 in 10.958s
update/release: 126/126 in 253.292s
complete profile: 204/204 in 273.063s

system Python 3.9.6
Protocol Adapter: 39/39 in 22.916s
Runtime Binding: 75/75 in 249.496s
transaction: 239/239 in 137.982s
verifier: 30/30 in 10.847s
update/release: 126/126 in 300.648s
supported profile projection routes: 2/2 in 5.063s
direct profile CLI: exit 2 before store creation at the established
                    Python 3.11+ tomllib boundary
```

The remaining integrated gates are:

```text
active strict OpenSpec: valid
all strict OpenSpec: 18 passed, 0 failed
DevFlow workflow validator: ok=true, issues=[]
Bash syntax: 5/5
Python 3.12 AST/import: 56/56 and 47/47
system Python 3.9 AST/import: 56/56 and 47/47
isolated package: 66 files, 5 directories, 20 required paths,
                  47 imports, 73 archive members
git diff --check: passed
scenario mapping: 60 automated + 6 Human-Gated, 0 unmapped
main review acceptance-criterion failures: 0
```

### RED/GREEN Index

This verification record contains 23 named RED sections. Each records the
focused command, expected failure count, zero unrelated errors, and the exact
missing or failing contract before implementation. The corresponding GREEN
sections record the focused dual-runtime result and required adjacent checks.
No expected RED remains in the integrated task-7 results.

Slice-closure evidence is:

```text
reference/inventory/classification: tasks 1.1-1.13 complete
receipt/overlay: tasks 2.1-2.7 complete; final parity 58/58 per runtime
config/probes: tasks 3.1-3.9 complete; parity 82/82 per runtime
runtime bundle/rebind: parity 83/83, adapter 39/39, runtime 65/65,
                       transaction 234/234 per runtime;
                       complete profile 201/201 on Python 3.12
staged update: update/release 123/123, transaction 239/239,
               Runtime Binding 75/75, parity 83/83 per runtime;
               complete profile 201/201 on Python 3.12 and supported
               profile routes 2/2 on system Python 3.9
diagnostics/package: focused matrix 71/71 per runtime
integrated: task 7.1 and 7.2 counts above
```

### Stable Finding Codes

Read-only diagnostics preserve these public evidence codes:

```text
parity.receipt.missing
parity.receipt.malformed
parity.receipt.stale
parity.reference.stale
parity.overlay.source_stale
parity.config.source_stale
parity.preparation.adapter_stale
```

Classification findings are:

```text
parity.protocol.core_missing
parity.protocol.core_incompatible
parity.protocol.observed_core_missing
parity.protocol.observed_core_incompatible
parity.protocol.optional_missing
parity.protocol.unclassified_drift

parity.feature.core_drift
parity.feature.observed_core_missing
parity.feature.observed_core_drift
parity.feature.optional_missing
parity.feature.optional_drift
parity.feature.unclassified_drift

parity.model.multi_agent_version_core
parity.model.tool_mode_pending_provider
parity.model.unclassified_drift
```

Bounded probe failures use `parity.probe.<stable-result-code>` for
`timeout`, `output_oversized`, `early_exit`, `malformed_output`,
`missing_response`, `protocol_order`, `response_error`, `v1_fallback`, and
`typed_subagent_missing`; candidate input drift is
`parity.probe.candidate_stale`.

### Fixture and Package Digests

```text
verified ChatGPT bundled CLI:
  6d8be49e49751554df16572369e636cbe02c84b208cad3dc35528c846eeca223
verified internal CLI:
  410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6
Protocol Adapter rule set:
  b9ac004f3801eaf094745e6e45754c7e5a058b33775746e49682aef7c240f849
read-only source catalog:
  75c9e8d4dadbe3f612f1b6fbabfe6785c312460bd6b5bedfe1565acdedd41f9a
read-only managed overlay:
  2437757759c89c96dbee4204d716ad77f3b7a24bb1b96d6fef9dfc9ad290d85f
synthetic canonical receipt fixture:
  root: /private/tmp/codex-switch-parity-receipt-fixture
  bytes: 3051
  SHA-256:
  a098a6a96a498aca17d4b14997dd1e6e229f9706d0178b2b5babdcd4a42e3860
retained redacted provider-shaped probe fixture:
  b1184a34d528e083b2dd12c6a71f82cf704097b152a550e0856549260ec985eb
isolated package archive:
  b9d21c9f4e5e880ca5858d7111f1728084a72cf656b54db384a5be922afe598a
isolated package manifest payload:
  5cb103bb9f454b2767a9ae3f2e7dbd7cd9ed6a291b53cbeddc99b4a14746758d
```

The receipt digest is a deterministic synthetic fixture at the recorded fixed
root. The overlay digest is read-only preparation evidence. Neither is a claim
about a promoted live profile; live receipt/overlay/config digests do not exist
until the explicitly authorized task 8.3 rebind succeeds.

### Changed Files

The task-7.7 exact non-checkpoint list remains authoritative at 38 paths. With
the planned checkpoint plus every `2026-07-26-parity-*` and
`2026-07-27-parity-*` checkpoint, task 7.9 completion will attribute 73 dirty
paths to this active change: 38 non-checkpoint paths and 35 checkpoints. The
130 pre-existing/unrelated dirty paths remain outside this change, for 203
total dirty paths. Shared files are attributed only to their recorded parity
edits; no unrelated bytes are claimed or reverted.

### Residual Optional Queue

No promoted receipt exists yet, so there is no live synchronization queue to
claim. Retained real-schema evidence deterministically queues these six
reference-only protocol methods:

```text
client_request:app/installed
client_request:app/read
client_request:environment/status
client_request:thread/searchOccurrences
server_notification:thread/environment/connected
server_notification:thread/environment/disconnected
```

The policy also queues these only when the corresponding drift is observed:

```text
optional-unless-observed feature: skill_search
optional features: code_mode_buffered_exec, executor_capability_discovery,
                   external_agent_memory_import, mcp_2026_07_28
metadata-only optional drift: enable_fanout, item_ids, memories
pending-provider model metadata: tool_mode
```

Observed use escalates the applicable optional-unless-observed surface to core;
unknown drift remains unhealthy and never enters the optional queue by default.

### Human Gate 8.1 Prerequisites

Before any live effect, the user must explicitly authorize all of:

1. installing the exact verified source through the supported
   `CODEX_SWITCH_SOURCE_DIR`/Python 3.12 command;
2. same-backend parity preparation/rebind for
   `/Users/cY/.local/bin/codex`;
3. resulting local profile/App/runtime mutations;
4. fully quitting and reopening ChatGPT; and
5. one real provider-backed typed `explorer` Subagent task.

After authorization, live execution must re-attest the current source, bundle,
App/PATH/profile/backend ownership before mutation; capture promoted manifest,
capability receipt, parity receipt, overlay, and config digests; prove one new
ChatGPT process and the managed launcher/proxy/exact backend chain; require the
child `thread_spawn`, `agentRole=explorer`, task-oriented metadata,
`parity-subagent-ok`, and parent completion; then re-attest ownership and run
final installed status/Doctor/verify/package identity/no-op update checks.

Generic turns, untyped or nickname-only children, parent-only markers, v1
fallback, unattested runtime ownership, or partial smoke evidence cannot pass.
Commit, push, tag, release, OpenSpec archive, retained-evidence cleanup,
dependency changes, provider/model/API/auth migration, and unrelated profile
or App mutation remain unauthorized.

### Control-Plane Validation and Stop

```text
scoped git diff --check: passed
active strict OpenSpec validation:
  Change 'internal-official-feature-parity' is valid
named RED sections: 23
parity checkpoints after task 7.9: 35
active-change dirty paths: 73
pre-existing/unrelated dirty paths: 130
total dirty paths: 203
OpenSpec progress: 68/79
```

No unchanged full suite was repeated. No production/test behavior, live
profile/App/provider state, internal install/update, dependency, commit, push,
tag, release, archive, cleanup, or Human Gate 8.1 effect occurred.

Task 8.1 is next and must not execute without explicit user authorization.

## 2026-07-27 Human Gate Authorization

Timestamp: 2026-07-27T12:08:47+08:00
Task: 8.1
Result: AUTHORIZED

The user explicitly replied `授权，继续` after the immediately preceding gate
request enumerated all five required live effects. Authorization therefore
covers:

1. installing the exact verified source through the task-8.2 command;
2. same-backend parity preparation/rebind for
   `/Users/cY/.local/bin/codex`;
3. resulting local profile/App/runtime mutations;
4. fully quitting and reopening ChatGPT through a bounded one-shot controller;
   and
5. one real provider-backed typed `explorer` Subagent task.

Mutation-preflight re-attestation:

```text
OpenSpec progress before update: 68/79
active profile: internal
active configured CLI: /Users/cY/.local/bin/codex
GUI/App CLI: /Users/cY/.codex-switch/bin/codex-internal-app
running ChatGPT pid: 95489
running App Proxy/backend pids: 95838/95842
bundled reference: codex-cli 0.146.0-alpha.3.1
bundled reference SHA-256:
  6d8be49e49751554df16572369e636cbe02c84b208cad3dc35528c846eeca223
internal backend: codex-cli 0.144.6
internal backend SHA-256:
  410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6
current installed release:
  /Users/cY/.local/share/codex-switch/releases/
  ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab
installed version: 0.1.13
installed parity module: absent
status/Doctor/verify --repair=none:
  parity.receipt.missing
```

Current source trust anchors match `install.sh`:

```text
codex_switch_release_bundle.py:
  dd121b4cb32755f7e6a72f34f680acd2298541c03bf2be1dba637c2e5fbaac13
codex_switch_promotion.py:
  561f6720f0b41e2fa19faad49d8738caef749f6b9a215a525a187bfda7ad199c
```

The required DevFlow capability check reports the pre-existing project/legacy
skill-layout conflicts while confirming OpenSpec `1.6.0` and project-local Matt
`tdd` readiness. Task 8 performs live acceptance rather than production-code
implementation. Legacy skill migration or cleanup requires separate approval,
so this is `DEFER_AND_CONTINUE` and does not expand the task.

No install, rebind, App restart, provider task, dependency, Git effect, release,
archive, or cleanup had occurred at the moment authorization was recorded.
Task 8.2 exact-source installation is next.

## 2026-07-27 Exact-Source Install RED

Timestamp: 2026-07-27T12:10:23+08:00
Task: 8.2
Result: RED_SAFE

The exact authorized command ran once:

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch \
CODEX_SWITCH_PYTHON="$(command -v python3.12)" \
/Users/cY/dev/codex-switch/install.sh
```

It exited 2 after 11.948 seconds:

```json
{"message":"Promotion candidate failed bundle validation: Release manifest required paths mismatch","outcome":"failed","reason":"candidate_invalid"}
```

The current source candidate was then built and validated independently under
`/private/tmp/codex-switch-parity-install-Qs1oOd`:

```text
payload SHA-256:
  5cb103bb9f454b2767a9ae3f2e7dbd7cd9ed6a291b53cbeddc99b4a14746758d
current required paths: 20
fresh isolated installer promotion: passed
```

Root cause: promotion validates both the new candidate and an existing
immutable `current` reference through the same current-version required-path
equality. Installed 0.1.13 has a valid schema-v1 manifest with the historical
16-path set. The four later required modules are
`codex_switch_parity.py`, `codex_switch_runtime_binding.py`,
`codex_switch_app_proxy.py`, and `codex_switch_home_sync.py`. The existing
release therefore fails before candidate publication even though it remains a
valid rollback generation.

Post-failure live attestation:

```text
current: releases/ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab
rollback: releases/9eb07bbc327b5f02a4f91d75d2aad902e58d9682e3d09802d898850cc4053f33
promotion-state SHA-256:
  ad51285c922e8ce03943c4a2e26297c1cbc7da20c0f186112d3a0b50d5abc85e
candidate release in live layout: absent
ChatGPT/proxy/backend pids: 95489/95838/95842
```

No reference, state, release, profile, App, provider, backend, dependency, Git,
release/archive, or cleanup mutation occurred. Task 8.2 remains unchecked and
progress remains 69/79.

Next RED: at the existing installer adapter seam, construct an immutable
manifest-v1 `current` release with the exact historical 16-path requirement,
install a current candidate, and require the new release to become `current`
while the historical release becomes byte-exact `rollback`. Do not add a
general manifest-migration framework, extra fault axes, or another live install
attempt before this regression is GREEN.

## 2026-07-27 Exact-Source Install GREEN

Task: 8.2
Result: VERIFIED
Progress: 70/79

### RED and GREEN

The focused installer regression
`test_installer_upgrades_supported_historical_manifest_v1_current` failed
before implementation on both runtimes with the exact live error:

```text
Python 3.12.13: 1 test, 1 failure in 5.244s
system Python 3.9.6: 1 test, 1 failure in 5.449s
reason: candidate_invalid
message: Release manifest required paths mismatch
```

The minimal implementation keeps current candidates strict while allowing the
fixed historical 16-path set only when promotion reads an existing immutable
reference. Final focused results:

```text
Python 3.12.13: new regression 1/1 in 6.223s
system Python 3.9.6: new regression 1/1 in 7.161s
Python 3.12.13 adjacent matrix: 5/5 in 18.941s
system Python 3.9.6 adjacent matrix: 5/5 in 22.780s
Python 3.12.13 AST: 3/3
system Python 3.9.6 AST: 3/3
Bash syntax: 2/2
active strict OpenSpec: valid
focused diff check: passed
```

The adjacent matrix covered current strict bundle evidence, ordinary second
promotion, piped hash-bound installer/runner bootstrap, historical
unmanifested migration, and the new historical manifest-v1 upgrade. No full
unchanged suite was repeated.

### Installed Identity

The exact authorized command succeeded:

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch \
CODEX_SWITCH_PYTHON="$(command -v python3.12)" \
/Users/cY/dev/codex-switch/install.sh
```

```text
current:
  releases/d55005d6d8b78a9e123aa4fe8d801da131df3d5020daf7d43b88f93828914392
rollback:
  releases/ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab
version: 0.1.13
manifest files/directories/required paths: 66/5/20
prebuilt package versus installed current: byte-exact
release-bundle module:
  3772b5bab9e4d3eeea95e52569d3d78da5b3a96145c64d9164ce2853f0da0437
promotion module:
  fe516e541a93a6b11f6065e354885b52f634c2941c00476f6a6fa287b9e47f70
promotion-state:
  4925d86749da7c05cdd55780599c3c15cf0059665af7bbe0caa98ff37b72f12b
install staging residue: 0
bytecode directories: 0
restart output: absent
```

An initial read-only validator probe correctly rejected the `current` symlink;
the accepted rerun used its resolved immutable release and passed. One zsh
no-match residue probe was replaced by a `find`-based check and reported zero.

ChatGPT/proxy/backend pids remain `95489`/`95838`/`95842`; the proxy still runs
from the prior immutable release until the later authorized restart. Task 8.3
same-backend parity preparation/rebind is next.

## 2026-07-27 Same-Backend Rebind RED

Timestamp: 2026-07-27T12:28:41+08:00
Task: 8.3
Result: RED_SAFE
Progress: 70/79

The supported command ran exactly once:

```bash
/Users/cY/.local/bin/codex-switch --skip-self-update \
  set-bin internal /Users/cY/.local/bin/codex
```

```text
exit: 2
duration: 2.3416s
parity.feature.core_drift: 2
parity.protocol.core_incompatible: 8
parity.protocol.unclassified_drift: 3
```

The exact CLI message was:

```text
codex-profile-switch: Parity preparation is unhealthy:
parity.feature.core_drift, parity.feature.core_drift,
parity.protocol.core_incompatible (8),
parity.protocol.unclassified_drift (3)
```

The health gate rejected the prepared bundle before the runtime transaction.
Immediate post-failure proof at 12:29:10 matched the preflight:

```text
internal manifest:
  a7e339e7e988bb70609f2777b94c3ceae02877fb984b9e4111b01d0c96047a0a
managed launcher:
  bdb8bad418104ae8e09062bdd56baae53ac4698d6006eea5949e2500cbd2620b
capability receipt:
  cd8a9fe5c6dd8ff6c47b118dbaaae66ab0fd6888bc9348bf6638d824bb6620e2
profile config:
  0dd1af1d166dd19a05f96cb7fd0d541ed2b7fd66745b3278e93600ba24207ee1
official config:
  66d894bc32362fedcddafdf271ff4f476e4570740929a225835f4d9409e3649f
managed-home config at exact post-failure snapshot:
  7207e3cec6ef4a9011f84cfbdbe702f58bdadb811a910b4a9d65484bedbdedbc
active record:
  8d007d9ab0f99ee55922d7c1f064f34f5ad87581b39ddd79542c18239a072a32
backend:
  inode 43110921
  SHA-256 410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6
ChatGPT/proxy/backend pids:
  95489/95838/95842
parity directory:
  absent
.runtime-rebind-*:
  absent
.runtime-binding-rebind.json:
  absent
```

At 12:30 the running Codex session independently rewrote the managed-home
config from 15,457 bytes and digest `7207e3ce...dcbc` to 15,458 bytes and
digest `da41933f...e618`. Manifest, launcher, capability receipt, profile config,
official config, active record, backend, and process ownership remained
unchanged. This later concurrent write occurred after the exact 8.3
no-mutation snapshot, is not attributed to a transaction, and means any future
preparation must capture current config inputs again.

Task 8.3 remains unchecked. The only next operation is a read-only in-process
diagnostic that invokes the same preparation path, intercepts the bundle at the
health gate, emits only sanitized finding category/code/severity/message
details, and raises before smoke or transaction code. Do not retry rebind,
bypass unhealthy evidence into commit, edit production behavior, or start
task 8.4.

## 2026-07-27 Same-Backend Finding Diagnostic

Recorded: 2026-07-27T12:47:57+08:00
Task: 8.3
Result: DIAGNOSTIC_COMPLETE_BLOCKED
Progress: 70/79
Diagnostic duration: 1.9558s

The one permitted read-only in-process diagnostic completed after bundle
preparation and raised at the health boundary. It did not invoke launcher
smoke, publish a transaction marker, or call runtime commit code.

### Error Findings

```text
feature:
  parity.feature.core_drift
    item_ids
    multi_agent_v2

client_request:
  parity.protocol.core_incompatible
    thread/realtime/start
    thread/resume
    turn/start
    turn/steer

server_request:
  parity.protocol.core_incompatible
    item/commandExecution/requestApproval
    item/permissions/requestApproval

server_notification:
  parity.protocol.core_incompatible
    item/autoApprovalReview/completed
    item/autoApprovalReview/started

client_request:
  parity.protocol.unclassified_drift
    account/login/start
    externalAgentConfig/import
    plugin/share/updateTargets

error total: 13
```

The saved generated-schema comparison attributes the protocol incompatibilities
to these bounded reason families:

```text
account/login/start:
  parity.protocol.enum_incompatible
externalAgentConfig/import:
  parity.protocol.enum_incompatible
  parity.protocol.items_incompatible
plugin/share/updateTargets:
  parity.protocol.enum_incompatible
thread/realtime/start:
  parity.protocol.enum_incompatible
thread/resume:
  parity.protocol.enum_incompatible
  parity.protocol.items_incompatible
turn/start:
  parity.protocol.enum_incompatible
  parity.protocol.items_incompatible
turn/steer:
  parity.protocol.enum_incompatible
  parity.protocol.items_incompatible
item/commandExecution/requestApproval:
  parity.protocol.type_incompatible
item/permissions/requestApproval:
  parity.protocol.type_incompatible
item/autoApprovalReview/completed:
  parity.protocol.type_incompatible
item/autoApprovalReview/started:
  parity.protocol.type_incompatible
```

### Optional Queue

Fourteen warning findings match the already planned synchronization queue:

```text
optional protocol:
  client_request:app/installed
  client_request:app/read
  client_request:environment/status
  client_request:thread/searchOccurrences
  server_notification:thread/environment/connected
  server_notification:thread/environment/disconnected

optional-unless-observed feature:
  skill_search

optional feature:
  code_mode_buffered_exec
  executor_capability_discovery
  external_agent_memory_import
  mcp_2026_07_28

metadata-only optional feature:
  enable_fanout
  memories

pending-provider model metadata:
  tool_mode

warning total: 14
```

`item_ids` is not in the warning set because its effective-state mismatch made
the metadata-only policy escalate it to core for this candidate.

### Blocking Diagnosis

The eight core methods are not new task-8.3 policy discoveries. Task 1.11
already classifies all `thread/`, `turn/`, and `item/` methods as core.
However, `prepare_parity_bundle()` evaluates policy before running either
parity probe. An unhealthy policy result therefore prevents probes from
supplying later evidence.

The parity candidate and receipt bind
`protocol_adapter_rule_set_digest()`, but that digest is one global hash over
selected adapter tables. It does not state which exact rule covers a given
direction/method/reason tuple, and current receipt validation consumes no
method-scoped adapter coverage. The core app-server probe exercises only:

```text
initialize
initialized
collaborationMode/list
thread/start
```

The typed-subagent probe proves the v2 child behavior but does not prove that
the official schema shapes for the eight failing methods are natively accepted
or exactly transformed. The Completion Contract therefore cannot treat the
global digest or existing probes as proof that any of the eight native
incompatibilities is safely adapted.

The three unclassified methods also cannot be silently reclassified: unknown
drift is explicitly unhealthy, and the diagnostic supplied no acceptance-trace
or adapter evidence that would justify a new policy entry. Suppressing only
those three findings, only the feature findings, or only the eight core
findings would leave the same task-8.3 acceptance criterion failing.

### No-Mutation Proof

Before and after the diagnostic, all persistent target hashes/stat tuples,
parity paths, runtime-rebind marker paths, diagnostic temporary-directory
identities, and process ownership matched. ChatGPT/proxy/backend pids remained
`95489`/`95838`/`95842`. No smoke, transaction, rebind retry, restart,
provider-backed Desktop task, dependency, Git effect, release, archive, or
cleanup occurred.

### Outcome

Task 8.3 remains unchecked and progress remains 70/79. Task 8.4 is not
dependency-ready. A future repair is eligible only if its plan first names this
exact acceptance failure and one focused RED/GREEN proves the complete
13-error blocker can be resolved without broadening the fixed
binary/model/provider/API/auth boundary. Partial finding suppression,
additional unrelated fault axes, general adapter abstractions, and adjacent
full-suite repetition remain prohibited.

### Control-Plane Validation

```text
active strict OpenSpec: valid
OpenSpec apply progress: 70/79
task 8.3 checkbox: unchecked
AI-native plan lint: passed
DevFlow workflow state: ok=true, issues=[]
DevFlow warning: existing legacy root-state migration only
targeted git diff --check: passed
```

No Python test suite or live command was repeated after the diagnostic because
no production or test code changed.

## 2026-07-27 Task 8.3 Method-Coverage Repair Planning

Recorded: 2026-07-27T18:00:37+08:00
Task: 8.3 planning revision
Result: PLANNED_AWAITING_IMPLEMENTATION_GATE
Progress: 70/79

The planning-only authorization was consumed without changing production,
tests, fixtures, operator docs, installed files, runtime state, dependencies,
Git history, release/archive state, or retained evidence. The revision updates
only the active OpenSpec/control plane and creates one planning checkpoint.

### Current Ownership Re-attestation

The live ownership observed during planning differs from the retained RED:

```text
active profile:
  openai-official
configured CLI / App CLI:
  /Applications/ChatGPT.app/Contents/Resources/codex
bundled CLI version:
  codex-cli 0.146.0-alpha.3.1
running ChatGPT:
  pid 86658
running official app-server:
  pid 86992
PATH codex:
  /Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex
PATH status:
  mismatched with the expected switch shim
```

No switch, repair, restart, or PATH mutation was attempted. The earlier
internal pids `95489`/`95838`/`95842` and their config hashes remain historical
RED evidence only. Every future implementation/live boundary must regenerate
binary, schema, profile, process, and mutable-config evidence.

### Exact Saved Method Pairs

The retained generated-schema comparison supplies these exact pre-repair
normalized method-schema identities:

| Direction/method | Official SHA-256 | Internal SHA-256 | Current reasons |
|---|---|---|---|
| `client_request:thread/realtime/start` | `e1d4742bc1fede7aa522dad547ebc86e655a77bc5a305fb7a1d65c6f8228cdee` | `cc1e41a2dc2e3199ce5ddb002110f4aba7bd474f474d2f0f0ccfdd11c2739206` | enum |
| `client_request:thread/resume` | `c757c1b83790de16ab05fb06972dd72fa834c271edca72857fc3d49908fe5067` | `5cdfe4d5e82e4883bd34e51e4d648110f4cb2bbffc6843b7da51f98a9a10d4fd` | enum, items |
| `client_request:turn/start` | `cc050a440131cf50e45858727b6888a6a8569091a560e22fc6da9b52dbb17d29` | `3df948965f5ff576f76d423fabb6ece4828575fc54b5b0179e7e277918e11cb2` | enum, items |
| `client_request:turn/steer` | `97fcf150a9e85f0d99ef0df1c86139d0f29d48d7bf3e2ad1b16437f8c7c871dd` | `4106041861e355b3aee80bcffa88377d2c1b8a6dbd0d4f10a03157a397563c65` | enum, items |
| `server_request:item/commandExecution/requestApproval` | `fb980ddcd7d4c87793e9a6e6c0094ef044f15ae73b0247f7e53b7c8303abd893` | `381a00a145682ae9f2b4946b488d2999e017a63093438d7f078f845fdcb9ac1f` | type |
| `server_request:item/permissions/requestApproval` | `637044439a0587ac76e3d426f29020896eac7838c706f81b80a15cd5c97835f5` | `2abc1ddc068a466da9451547b04a0e2e52f3d4bc2a867adc25ded37f02b6830c` | type |
| `server_notification:item/autoApprovalReview/completed` | `d9ef2e2f60e6820d43670ab241c0c5e99ac6226edfa713275d28e1332a91f9ef` | `52242502854ecb5f34a73ade84e9760c064a2c45bafd18e10a3d1d67c76a9dd2` | type |
| `server_notification:item/autoApprovalReview/started` | `709c52ae763e76c97a6eab6dbb4f9290714df1ea82ea5b19e9001c9a0906b564` | `07eaa1f218c3f06a5698494150dc991808407806d8fd1e3f4482387c5fe4409a` | type |
| `client_request:account/login/start` | `9ee1c1845c95aead79d8576ad148dae40812ef7504c01f3e9dbab0db06e76e94` | `c7bb889ffce831bda9988b0ff8cd21d26307a0640ce232f3cd88c2aad0780350` | enum |
| `client_request:externalAgentConfig/import` | `fefc184359f5e62b08965f02947e01289c10f22547d7caf1f29ec07ff032fb04` | `fed545a509c5373f6b20d637e6fecc4e0159ba593a4c41dcc2861e2b522da983` | enum, items |
| `client_request:plugin/share/updateTargets` | `ed52c627514626c94a30ce7a8150d39344dd5bb7be64dcc45417134e2e2248a1` | `62854e4d78b8b1650b57f5a5d5bd02b8b45019267d9e8638e34107aee229e85e` | enum |

The method hashes are evidence inputs, not unconditional allowlist keys.
Implementation regenerates hashes after semantic normalization and binds each
accepted pair to a typed disposition and proof.

### Complete Thirteen-Error Closure

```text
semantic native equivalence:
  item/commandExecution/requestApproval
  item/permissions/requestApproval
  item/autoApprovalReview/completed
  item/autoApprovalReview/started

exact adapter plus optional extension:
  thread/resume
    adapter: top-level history ID removal and non-portable opaque reasoning
    optional-unless-observed: input_audio

exact optional-unless-observed extensions:
  thread/realtime/start: v3, response-handoff, initial-items
  turn/start: localAudio, audio
  turn/steer: localAudio, audio
  account/login/start: amazonBedrock
  externalAgentConfig/import: MEMORY, memory, migrationSource, providerId
  plugin/share/updateTargets: LISTED

core feature evidence:
  item_ids: exact observed resume-path adapter coverage; any other observed
            dependency remains unhealthy
  multi_agent_v2: overlay + config + final typed_subagent_v2 probe under the
                  same revalidated fingerprints
```

All entries flow through one final policy result. A global adapter digest,
method prefix, reason-only match, schema-pair-only allowlist, passed example,
or subset of the thirteen cannot make the candidate healthy.

### Planned Receipt and Evaluation Contract

- Protocol Adapter owns a structured manifest only for actual transforms.
  Production transform routing and the rule-set digest consume that same
  structured rule definition.
- Parity owns exact schema-pair dispositions and optional queue identifiers.
- Pre-probe eligibility stops unknown/uncovered drift and permits only named
  provisional evidence.
- Final policy consumes method coverage and probe results before receipt bytes
  exist.
- Receipt schema v2 contains sorted exact coverage records and final
  post-probe evidence. Receipt v1 is stale/unsupported and is regenerated
  through staged repair rather than modified in place.

### Added Scenario-to-Test Map

| Added scenario | Named regression |
|---|---|
| Equivalent nullable schema spellings normalize identically | `ParityProtocolInventoryTests.test_nullable_union_spellings_are_semantically_equal` |
| Method coverage is exact and receipt-bound | `ParityMethodCoverageTests.test_global_method_reason_and_schema_pair_only_evidence_fail_closed` |
| Adapter evidence names only actual transforms | `ProtocolAdapterEvidenceTests.test_rule_manifest_binds_every_actual_transform`; `test_thread_resume_transform_and_manifest_share_one_rule` |
| Exact optional extension remains fail-closed | `ParityMethodCoverageTests.test_exact_optional_extensions_escalate_when_observed_or_changed` |
| Saved task-8.3 failure closes atomically | `ParityMethodCoverageTests.test_retained_thirteen_error_fixture_closes_only_as_one_final_policy` |
| Multi-agent v2 requires final post-probe evaluation | `ParityMethodCoverageTests.test_multi_agent_v2_requires_final_typed_probe` |
| Item IDs require exact observed-path coverage | `ParityMethodCoverageTests.test_item_ids_requires_exact_resume_rule_and_no_other_dependency` |
| Legacy receipt cannot imply method coverage | `ParityReceiptTests.test_receipt_v1_cannot_imply_coverage`; `test_receipt_v2_round_trip_binds_sorted_method_coverage` |
| Eligibility and final policy are separate | `ParityBundleTests.test_uncovered_drift_stops_before_probe_and_final_policy_precedes_receipt` |

### Exact Planning Write Set

```text
openspec/changes/internal-official-feature-parity/proposal.md
openspec/changes/internal-official-feature-parity/design.md
openspec/changes/internal-official-feature-parity/tasks.md
openspec/changes/internal-official-feature-parity/specs/codex-switch/spec.md
TASK_LEDGER.md
.planning/STATE.md
.planning/devflow/verification/internal-official-feature-parity.md
.planning/checkpoints/2026-07-27-parity-method-coverage-repair-planned.md
```

The future implementation write set and both Human Gates are recorded in task
8.3. No path outside the planning list was changed by this revision.

### Planning Validation

```text
scenario count:
  12 requirements, 75 scenarios
active strict OpenSpec:
  passed
AI-native plan lint:
  passed
all strict OpenSpec:
  18 passed, 0 failed
DevFlow workflow validation:
  ok=true, issues=[]
DevFlow warning:
  legacy root state is read-only; migration remains unauthorized
targeted/full git diff hygiene:
  passed for tracked worktree and all six untracked planning artifacts
```

### Next Gate

Stop at `PARITY-8.3-IMPLEMENT`. That gate may authorize only the exact
production/test/fixture/operator-doc write set and isolated tests named in
task 8.3. After reviewed GREEN/package evidence, stop again at
`PARITY-8.3-LIVE-RETRY`. Neither gate is implied by the consumed planning
authorization or the old task-8.1 rollout approval.

## 2026-07-27 Task 8.3 Source/Package Milestone

Timestamp: 2026-07-27T19:23:50+08:00
Task: 8.3 source implementation
Result: `OFFICIAL_FIRST_PAUSE_READY`
Progress: 70/79
Next gate: `PARITY-8.3-LIVE-RETRY`

### Scope and Outcome

The user consumed `PARITY-8.3-IMPLEMENT` for the exact recorded write set.
The saved thirteen-error preparation blocker now closes atomically through
exact method coverage, nullable semantic equivalence, structured adapter
evidence, exact optional-extension records, versioned acceptance-trace
binding, and final post-probe evidence.

Receipt schema v2 requires sorted coverage records, the canonical
`official-desktop-core-v1` trace, and exactly one passed `core_protocol` plus
one passed `typed_subagent_v2` result. Preparation runs coverage, eligibility,
bounded probes, complete mutable-fingerprint revalidation, final policy, then
receipt construction. Unknown or uncovered drift stops before probes.

The user will primarily use the official profile, so live switching is
deprioritized. This section records a durable source/package milestone without
claiming task 8.3, the live acceptance slice, or the active change complete.

### RED to GREEN

The retained RED and fixture are in
`.planning/checkpoints/2026-07-27-parity-method-coverage-repair-red.md`.
All 11 named task-8.3 tests now pass on Python 3.12 and system Python 3.9.
Fresh complete producer/consumer results are:

```text
Protocol Adapter:
  Python 3.12: 41/41
  system Python 3.9: 41/41
Parity:
  Python 3.12: 93/93
  system Python 3.9: 93/93
Verifier:
  Python 3.12: 30/30
  system Python 3.9: 30/30
Runtime Binding:
  Python 3.12: 75/75
  system Python 3.9: 75/75
```

The behavioral preparation regression mutates the source catalog during the
typed probe and proves `parity.preparation.candidate_stale` before staging.
Receipt negatives reject schema v1, incomplete or failed required probes,
healthy `uncovered` coverage, a changed acceptance trace, a changed rule
digest, a missing resume rule ID, another item-ID dependency, and observed
optional extensions.

### Review

Read-only specification and engineering-discipline reviews report no blocker.
The earlier acceptance-trace data clump was removed by passing one immutable
trace object through both policy passes. Two non-blocking maintenance notes
remain outside this task: non-resume transforms still partially duplicate
manifest metadata, and the explicit preparation-order test uses source marker
ordering.

The required legacy-layout migration preflight was dry-run only. The
hook-provided nested `.pyz/activate_project_dependencies.py` path failed before
execution because it is not a Python package with `__main__`; the supported
sibling launcher then reported the known 16 DevFlow source conflicts and
`blocked_by_dependency_preflight` without writes. OpenSpec 1.6 and methodology
provenance remain ready. This is the pre-existing `DEFER_AND_CONTINUE`
dependency finding; no project link migration or legacy cleanup was applied.

### Evidence Digests

```text
retained fixture:
  529f746ef6370413cf1f18299f93a089f74076939242edd9579827ede65b1b5f
adapter source:
  8d1d45d762eeb7b4a3ffba2681e2691815f773341bd234aeb3bd6a10792ef4ed
parity source:
  e1a2e934d2374d421cc89cf7943571c57661d5035112f5f9d437025c3a16bfd5
adapter test:
  8ac80bbaa4502ad2599555d1a7e9d7e17d0a4292a10d9475c1616adb2687e5ef
parity test:
  0a8422171ca2f1ba29c9ada9a2e3b189e55a461a522048730fa9bc27cd5aa658
adapter rule set:
  1332cb0f29d32c0c5d3dc17b1cfe30ac7fb33bbe2d1fff7c9580fe2249ac9308
acceptance trace:
  official-desktop-core-v1
  1c8a577e2847e604f9e80f7b55452058250f7ca449adf7d5b65ca82ef41e2c26
```

### Isolated Package

The exact package command wrote only beneath
`/private/tmp/codex-switch-parity-83.HLiOjw`.

```text
package payload sha256:
  12c60c7e74a24b7e6b6b32f3b68443bdae6e0467666f5a400b897604d2a967fb
archive file sha256:
  2bbcb66b4f100c87686abdbc4fd4ba4e7d77250524f19ca6d3aaeff5c887c270
validate_release_outputs:
  passed
task source/package identity:
  README.md, SKILL.md, two production files, and two tests are byte-exact
retained fixture packaged:
  false
```

Package creation validated its manifest, generated references, immutable
runtime imports, top-level runner, and archive payload. The package is not
installed and is not standing authority after any source/runtime drift.

### Mutation Boundary and Pause

No installed release, live receipt, overlay, config, manifest, launcher,
active record, profile, App, process, provider, dependency, Git state, public
release, OpenSpec archive, or retained evidence was mutated. No ChatGPT
restart or provider-backed task ran.

Task 8.3 remains unchecked at 70/79. The durable checkpoints are:

- `.planning/checkpoints/2026-07-27-parity-method-coverage-repair-verified.md`
- `.planning/checkpoints/2026-07-27-parity-method-coverage-live-retry.md`

Stop at `PARITY-8.3-LIVE-RETRY`. Resume only with fresh explicit
authorization and current ownership/fingerprint attestation; task 8.4 remains
unavailable.

## 2026-07-28 Scheme A Installer Isolation Plan

Timestamp: 2026-07-28
Result: `APPROVED_PENDING_PLANNING_VALIDATION`
Progress: 70/84
Next item: 8.3A.1

### Root-Cause Evidence

The public staged-update helper invokes the current trusted installer with the
live process `HOME`, `CODEX_HOME`, and `PATH`. The installer always generates
`$CODEX_HOME/config.toml` and appends `# Added by Codex installer` plus its
install directory to `$HOME/.zshrc` when that directory is not already in the
child PATH. Three failed sibling installs consequently narrowed the live
official config and placed retained candidates ahead of the canonical
codex-switch shim.

This is upstream of switch publication. Current direct evidence rules out the
adjacent but incorrect repair paths:

- official/internal `plugin list --json`: 24 identical IDs/enabled states;
- synchronized common safe config values: identical;
- internal manifest `codex_bin`: `/Users/cY/.local/bin/codex`;
- internal generated Desktop wrapper `CODEX_BIN`:
  `/Users/cY/.local/bin/codex`;
- direct internal runtime and app-server smoke: pass;
- installed release key sources: byte-identical to repository `HEAD`.

### Approved Completion Contract

1. A harmful fake installer proves the current mutation and then sees only
   private `HOME`/`CODEX_HOME` plus candidate-first child PATH.
2. Live shell/config/profile/runtime sentinels remain byte/mode-stable during
   installer success and failure.
3. The exact private scratch root is mode 0700 and absent after success,
   failure, `HUP`, `INT`, or `TERM`; generated config and credential-bearing
   bytes are not retained or logged.
4. Existing candidate-retention behavior remains compatible, but no candidate
   is written to live PATH.
5. The three confirmed shell blocks and candidate directories are backed up and
   repaired precisely, with no deletion.
6. Exact-source install plus one controlled update/rebind/switch and bounded
   ChatGPT restart prove complete config/plugins and internal binary ownership.

### Exact Write and Live-Effect Boundary

```text
production:
  scripts/codex_env_setup
tests:
  scripts/test_codex_update_release.py
conditional only after recorded wrapper RED:
  scripts/codex-switch
canonical:
  openspec/changes/internal-official-feature-parity/**
  TASK_LEDGER.md
  .planning/STATE.md
  .planning/devflow/verification/internal-official-feature-parity.md
  .planning/checkpoints/2026-07-28-internal-installer-isolation-approved.md
live, recoverable:
  /Users/cY/.zshrc exact backup and three confirmed blocks
  /Users/cY/.local/bin/.codex-internal-update-cb601999175c954128459e72
  /Users/cY/.local/bin/.codex-internal-update-8c8e097f976e26a0ed76655a
  /Users/cY/.local/bin/.codex-internal-update-a17a48054bfaf3fedbae231a
  supported exact-source install/profile/runtime artifacts and one restart
```

No proxy, plugin refresh, global-state allowlist, credential/identity,
dependency, legacy layout, destructive deletion, provider-backed Desktop task,
Git, release, or archive action is authorized.

### Planning Preflight

The supported DevFlow dependency activation wrapper ran with
`--migrate-official-skill-layout --dry-run`. OpenSpec 1.6 and methodology
provenance are ready; the existing DevFlow source conflicts block migration.
No link, plugin, dependency, or legacy-layout write occurred. This remains a
separate deferred finding.

### Next Action

Run strict active/all OpenSpec, AI-native plan lint, workflow validation, and
diff hygiene. If they pass, execute task 8.3A.1 RED only.

### Task 8.3A.1 RED

```text
command:
  PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest \
    scripts.test_codex_update_release.CodexStagedInternalUpdateTests.\
test_env_setup_isolates_installer_config_and_shell_side_effects -v
result:
  1 test, 1 failure, 0 errors
failure:
  expected b'live-config-sentinel = true\n'
  observed b'installer-default-config\n'
```

The command itself exited successfully and installed the sibling candidate.
The single failure is the live config mutation required by the incident
reproduction. The fake installer also implements the real shell-append
condition. No production source or workstation state changed.

### Task 8.3A.2 GREEN

The production change is confined to `scripts/codex_env_setup`. It creates one
private scratch root under `/tmp`, captures its device/inode, supplies private
`HOME` and `CODEX_HOME` plus candidate-first child PATH, and removes only the
captured directory on exit. `scripts/codex-switch` remains unchanged.

```text
incident tests:
  Python 3.12: 3/3
  system Python 3.9: 3/3
supported paths:
  success
  installer exit 17 with exact status propagation
  HUP, INT, TERM
live config/shell sentinels:
  unchanged
installer root/home/codex-home modes:
  0700 / 0700 / 0700
scratch after return:
  absent
complete CodexStagedInternalUpdateTests:
  Python 3.12: 13/13
  system Python 3.9: 13/13
Bash syntax:
  passed
```

No source path outside the approved production/test/canonical set and no live
workstation state changed.

### Task 8.3A.3 Source and Package Verification

Final verification was serialized because two concurrent full suites
temporarily exceeded existing one-second candidate-smoke limits in unrelated
promotion setup. No timeout or unrelated test was changed; both serial reruns
passed.

```text
final complete update/release:
  Python 3.12: 132/132 in 290.800s
  system Python 3.9: 132/132 in 362.115s
  failures/errors: zero
focused signal/installer matrix:
  Python 3.12: 7/7
  system Python 3.9: 7/7
complete staged-update class:
  Python 3.12: 15/15
  system Python 3.9: 15/15
strict OpenSpec:
  active: valid
  all: 18/18
AI-native plan lint:
  passed
pinned workflow validation:
  ok: true
  issues: []
  warning: known read-only legacy DevFlow state migration input
static:
  Bash syntax: passed
  Python 3.12 AST: passed
  system Python 3.9 AST: passed
  git diff --check: passed
isolated package:
  root: /private/tmp/codex-switch-installer-isolation.rZHFJ2
  schema: codex-switch.release-bundle v1
  files: 66
  source/package env-helper SHA-256:
    0e7334481204785517ac68ac4a9086b77cc9b1136718fbc15234459b25c61bd9
residue:
  codex-switch-internal-installer scratch: absent
  packaged config/auth/credential/shell/bytecode paths: absent
  new source-tree bytecode dated 2026-07-28: absent
live preflight:
  .zshrc SHA-256:
    7caecab6b6bd2bc1ccc358e5071a40fa8fcb244ba065f3140dba0d1e24fc1807
  .zshrc mode: 0600
```

The only unrelated dirty path remains
`.planning/devflow/context-health/events.jsonl`; it was not read as authority,
modified, or removed.

### Next Action

Execute task 8.3A.4 only. Re-attest exact text, inode/type/mode/owner and
candidate contents before mutation; create a private recoverable backup first;
remove only the three named installer blocks and move only the three named
candidate directories. Stop on drift and delete nothing.

### Task 8.3A.4 Exact Recoverable Live Repair

Every target was re-attested immediately before mutation.

```text
original .zshrc:
  type/mode/owner: regular / 0600 / uid 502
  inode/device: 56884565 / 16777233
  SHA-256:
    7caecab6b6bd2bc1ccc358e5071a40fa8fcb244ba065f3140dba0d1e24fc1807
target block counts:
  cb601999175c954128459e72: 1
  8c8e097f976e26a0ed76655a: 1
  a17a48054bfaf3fedbae231a: 1
candidate directories:
  type: non-symlink directories
  mode/owner: 0700 / uid 502
  files: codex, codex-code-mode-host, rg
  version: codex-cli 0.145.0
recovery root:
  /Users/cY/.codex-switch/backups/
    20260728T161949+0800-installer-side-effect-recovery
  mode: 0700
backup .zshrc:
  mode: 0600
  SHA-256:
    7caecab6b6bd2bc1ccc358e5071a40fa8fcb244ba065f3140dba0d1e24fc1807
repaired .zshrc:
  mode: 0600
  inode/device preserved: 56884565 / 16777233
  SHA-256:
    8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
  diff: only the three confirmed two-line installer blocks and separators
fresh clean-environment zsh:
  command -v codex: /Users/cY/.codex-switch/bin/codex
  codex --version: codex-cli 0.146.0-alpha.3.1
```

The three candidate directories were moved into the recovery root without
changing their inodes or modes. Their former live paths are absent. The
existing plugin app-server PATH and canonical codex-switch shell block remain.
Nothing was deleted.

### Next Action

Execute task 8.3A.5 only: exact-source install, immutable installed identity,
one supported internal update/rebind/switch, one bounded ChatGPT restart, and
complete config/plugin/manifest/wrapper/App/proxy/backend/status/Doctor/verify
proof. Stop before the provider-backed Desktop task and every excluded effect.

### Task 8.3A.5 Safe Internal-0.145 Compatibility RED

Exact-source installation succeeded:

```text
current immutable payload:
  275ad2e2fda95c0d2591fe95aa4d9e7075988da286851f6584e51c3bad771dab
rollback:
  d55005d6d8b78a9e123aa4fe8d801da131df3d5020daf7d43b88f93828914392
manifest:
  codex-switch.release-bundle v1
  66 files
installed/source env-helper SHA-256:
  0e7334481204785517ac68ac4a9086b77cc9b1136718fbc15234459b25c61bd9
bytecode/staging residue:
  absent
```

The supported update dry-run selected internal 0.145.0. The one real update
installed and signed private candidate
`/Users/cY/.local/bin/.codex-internal-update-6efc91d3f6359549077f8a00/codex`,
then stopped before promotion:

```text
exit: 2
finding: parity.feature.core_drift
bound /Users/cY/.local/bin/codex: codex-cli 0.144.6, unchanged
candidate: codex-cli 0.145.0, mode-0700 private sibling
installer scratch: absent
.zshrc SHA-256:
  8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
official config SHA-256:
  ca02832ff0a2b8829f976e3dcb13a18b725fd61be8eeffd0a1f0d10ee52d2ca3
internal config SHA-256:
  59a14e0e108e17b3488871d8880255bae78c85d9cad1a05778093ba638db31f1
```

The three live hashes and modes match pre-update evidence. A read-only
diagnostic patched only in-process health-boundary callbacks and forced a stop
before smoke/commit even if preparation became healthy. It reported:

```text
evaluation stage: eligibility
item_ids official: stage=removed isolated_default=true effective=true
item_ids internal: stage=under development isolated_default=false effective=false
client_request:thread/resume: compatible=true reasons=none
thread/resume coverage record count: 0
item_ids observed dependencies: thread/resume.params.history
error:
  item_ids / parity.feature.core_drift /
  expected exact-resume-dependency-only / observed drift
warnings:
  mcp_2026_07_28 / parity.feature.optional_missing
  tool_mode / parity.model.tool_mode_pending_provider
```

The root cause is an exact policy asymmetry: adapter-covered resume is accepted
but natively compatible resume is not. No coverage record exists for a
compatible method by design. The proposed correction accepts only the exact
current native-compatible comparison or the existing exact adapter proof;
absence of coverage alone, missing/incompatible resume, stale coverage, or an
extra dependency remains unhealthy.

### Human Gate

Implementation requires adding the existing task-8.3-owned paths
`scripts/codex_switch_parity.py` and `scripts/test_codex_parity.py` to the
narrower Scheme A write set. Until explicitly approved, do not implement, rerun
promotion, switch internal, restart ChatGPT, download another candidate, or
claim task 8.3A.5 complete.

### Native-Resume Implementation Approval

At 2026-07-28T17:41:14+08:00 the user explicitly approved
`PARITY-0.145-NATIVE-RESUME-IMPLEMENT`. The production/test write set is
limited to `scripts/codex_switch_parity.py` and
`scripts/test_codex_parity.py`; canonical evidence remains main-owned. The
next evidence must be the named Python 3.12 RED before any production edit.
Only after dual-runtime GREEN, source/package validation, and fresh live
attestation may execution reuse the already retained candidate. No second
candidate download or excluded live effect is authorized.

### Native-Resume RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py \
  ParityMethodCoverageTests.test_item_ids_accepts_exact_native_resume_compatibility_without_adapter_coverage \
  -v
```

Result: exit 1; 1 test ran in 0.002 seconds with the single expected assertion
failure because `healthy` remained false. The comparison contained both exact
`client_request:thread/resume` method schemas, `compatible=true`, no reasons,
no adapter coverage, and only `thread/resume.params.history`. Production was
unchanged at RED.

### Native-Resume Focused and Full GREEN

The smallest production change accepts current native resume compatibility
only when the exact `client_request:thread/resume` comparison has both sides
and `compatible=true`; the existing exact adapter path remains unchanged.

```text
Python 3.12 named regression: 1/1
system Python 3.9 named regression: 1/1
Python 3.12 ParityMethodCoverageTests: 6/6
system Python 3.9 ParityMethodCoverageTests: 6/6
Python 3.12 complete parity: 94/94 in 2.283s
system Python 3.9 complete parity: 94/94 in 45.244s
```

The named test includes the required missing-side, incompatible-without-exact-
coverage, extra-dependency, and absent-exact-comparison negative matrix.

### Read-Only Review Guard RED

Standards review found that `ProtocolInventoryComparisonEntry` allows
contradictory `compatible=true` with non-empty reason codes; current native
proof accepted it. Spec review required missing-side checks that preserve
`compatible=true` and exact wrong-direction/wrong-method negatives.

After correcting a tests-only assertion-field mistake, the focused Python 3.12
test reached the production seam and produced exactly one expected failure:

```text
ParityMethodCoverageTests.
  test_item_ids_native_resume_compatibility_proof_is_exact_and_consistent
Ran 1 test in 0.005s
FAILED (failures=1)
```

The failure is the contradictory compatible/reason-coded entry remaining
healthy. No production edit followed the review before this RED was recorded.

### Native-Resume Final Source and Package Verification

The final production guard additionally requires empty reason codes. Missing
schema sides retain `compatible=true` in the test and must still produce the
feature-level `item_ids` core finding; compatible wrong-direction and
wrong-method comparisons also fail. Both read-only review axes report no
remaining actionable finding.

```text
Python 3.12 method coverage: 7/7
system Python 3.9 method coverage: 7/7
Python 3.12 full parity: 95/95 in 2.217s
system Python 3.9 full parity: 95/95 in 37.239s
Python 3.12 final update/release: 132/132 in 284.472s
system Python 3.9 final update/release: 132/132 in 348.351s
dual-runtime AST/import: passed
active strict OpenSpec: valid
all strict OpenSpec: 18/18
AI-native plan lint: passed
workflow: ok=true, issues=[]
workflow warning: legacy DevFlow root state is read-only
git diff checks: passed
new bytecode after approval: none
```

The first static harness used an incomplete module import path and a reserved
zsh variable; corrected diagnostic commands passed and are the accepted
results.

Final package root:
`/private/tmp/codex-switch-native-resume-final.P5dgvY`

```text
files/directories/required: 66/5/20
parity source/package SHA-256:
  f1d5928c7e6f9f2dbdb40018c6a06a108d64003d6ca142f7a3df04dd467f027e
test source/package SHA-256:
  1fc2abf1b40eddbeaf209e49d01de218396b1862f99f4998e93ba0aab121271c
archive SHA-256:
  2fe6ec94004a39f5815dba880b139063bf49d4db5a7fbb0b91e792d4908b4558
manifest SHA-256:
  c54123584f25c6f0adeeab6107d4f993a226c84abb6bd6bbe9abcc3eb0505cd3
```

The next live action must install this exact source, validate the new immutable
payload, then freshly re-attest and reuse only the already retained candidate.

### Exact-Source Reinstall and Retained-Candidate Preflight

The supported install promoted immutable payload
`6a23d04f8408681c26ed116583b208699f4b8fba4357162717befe7af8c1f132`;
strict candidate validation passed for version 0.1.13 and the 66-file bundle.

Fresh preflight proves candidate 0.145.0 SHA-256
`a34c872ccaaa02b6823bdf75138826a17177b91117a1920cedec9834772197b8`
is a signed non-symlink executable under the original mode-0700 retained root.
Bound 0.144.6 remains SHA-256
`410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6`;
the fixed backup and runtime marker are absent. The official bundle and all
recorded `.zshrc`/live-config hashes still match the safe gate. Full evidence
is in
`.planning/checkpoints/2026-07-28-internal-0145-retained-candidate-preflight.md`.

Promotion must call the installed immutable hidden seam directly. No
`update-internal`, installer, download, or second candidate is permitted.

### Retained-Candidate Core-Probe EOF RED

The exact installed hidden promotion seam reused the retained candidate and
returned 2 in 5.009 seconds:

```text
Parity preparation is unhealthy: parity.probe.missing_response
```

No transaction began. Bound 0.144.6 and candidate 0.145.0 retain their exact
inodes/hashes; backup and runtime marker are absent; runtime/installer scratch
counts are zero; shell/config/manifest/launcher/active hashes match preflight.

A minimal credential-free immediate-EOF differential produced only initialize
for official 0.146, bound 0.144.6, and candidate 0.145. A response-paced
candidate session returned initialize, collaboration, and thread response IDs
in order and exited 0. The fault is the probe runner closing stdin before the
stateful app-server drains later requests, not a candidate method gap.

Detailed hypotheses, alternatives, completion contract, and stop boundary are
recorded in
`.planning/checkpoints/2026-07-28-internal-0145-core-probe-eof-gate.md`.
Implementation stops at `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT`.
