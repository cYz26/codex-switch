# Task 8.3 Method-Coverage Repair RED

Recorded: 2026-07-27T18:41:29+08:00
Change: `internal-official-feature-parity`
Task: 8.3
Progress: 70/79
Status: `RED_VERIFIED`
Next action: implement the smallest complete GREEN in the two approved
production files.

## Scope

The user explicitly authorized `PARITY-8.3-IMPLEMENT`. The RED write set is
limited to:

- `scripts/test_codex_protocol_config.py`
- `scripts/test_codex_parity.py`
- `testdata/parity/current-method-coverage-redacted.json`
- this checkpoint

No production, operator-doc, installed, profile, App, process, provider,
dependency, Git, release, archive, cleanup, or live runtime write occurred.

## Unmodified Baseline

Before the RED edits:

```text
Python 3.12 Protocol Adapter:
  39 tests, exit 0
Python 3.12 parity:
  84 tests, exit 0
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -q
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -q
```

## Retained Fixture

`testdata/parity/current-method-coverage-redacted.json` records only:

- the two saved core-feature facts;
- eleven direction/method identifiers;
- saved pre-repair and regenerated nullable-normalized method SHA-256 pairs;
- stable incompatibility reason codes;
- exact planned adapter/optional/native dispositions; and
- the expected deterministic optional queue.

It contains no raw schema, config, prompt, credential, provider output, or
process text.

Fixture SHA-256:

```text
529f746ef6370413cf1f18299f93a089f74076939242edd9579827ede65b1b5f
```

The four nullable pairs were regenerated read-only from the retained official
and internal schema directories. Their post-normalization hashes are equal;
the seven adapter/optional pairs retain their saved identities.

## RED Commands and Results

Protocol Adapter:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py \
  ProtocolAdapterEvidenceTests.test_rule_manifest_binds_every_actual_transform \
  ProtocolAdapterEvidenceTests.test_thread_resume_transform_and_manifest_share_one_rule \
  -v
```

Result: exit 1, 2 tests, 2 expected failures. Both fail because
`protocol_adapter_rule_manifest` and the shared named resume rule do not yet
exist.

Parity:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py \
  ParityProtocolInventoryTests.test_nullable_union_spellings_are_semantically_equal \
  ParityMethodCoverageTests.test_retained_thirteen_error_fixture_closes_only_as_one_final_policy \
  ParityMethodCoverageTests.test_global_method_reason_and_schema_pair_only_evidence_fail_closed \
  ParityMethodCoverageTests.test_exact_optional_extensions_escalate_when_observed_or_changed \
  ParityMethodCoverageTests.test_item_ids_requires_exact_resume_rule_and_no_other_dependency \
  ParityMethodCoverageTests.test_multi_agent_v2_requires_final_typed_probe \
  ParityReceiptTests.test_receipt_v2_round_trip_binds_sorted_method_coverage \
  ParityReceiptTests.test_receipt_v1_cannot_imply_coverage \
  ParityBundleTests.test_uncovered_drift_stops_before_probe_and_final_policy_precedes_receipt \
  -v
```

Result: exit 1, 9 tests, 12 expected assertion failures and zero errors.
Failures prove:

- four nullable-union spellings are not yet canonicalized;
- method coverage and typed-v2 two-pass inputs are absent;
- exact extension/item-ID evidence is absent;
- receipt schema remains v1 with no method coverage; and
- preparation has no coverage/eligibility/final-policy ordering.

Test/fixture syntax validation exited 0 before RED:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 -c \
  'import ast, json, pathlib; [ast.parse(pathlib.Path(path).read_text(), filename=path) for path in ("scripts/test_codex_protocol_config.py", "scripts/test_codex_parity.py")]; json.loads(pathlib.Path("testdata/parity/current-method-coverage-redacted.json").read_text())'
```

## Dependency Finding

The installed DevFlow dependency check confirms project-local Matt `tdd` and
OpenSpec 1.6.0 are ready, while pre-existing DevFlow source/layout conflicts
still make the aggregate check return `missing_required`. This is the already
approved `DEFER_AND_CONTINUE` finding. No dependency activation, migration, or
legacy cleanup was performed.

## Stop Conditions

Production GREEN remains limited to
`scripts/codex_switch_protocol_adapter.py` and
`scripts/codex_switch_parity.py`. Any additional production/test/doc path,
dependency, public contract expansion, changed schema pair outside the
retained fixture, or live effect is `BLOCKED_AWAITING_HUMAN`.
