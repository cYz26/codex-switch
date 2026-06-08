# Verification: isolate-desktop-session-state

## Metadata

- Change: `isolate-desktop-session-state`
- Phase: `01-foundation`
- Recorded at: 2026-06-08T11:20:25+08:00
- Result: passed with one process note

## Scope

Verified the internal Codex Desktop wrapper runtime-state isolation repair:

- stale profile app-home symlinks for response/session runtime state are removed when they point into live `CODEX_HOME`
- future wrapper launches do not create live symlinks for excluded runtime state
- generated internal Desktop wrapper still launches the configured profile Codex binary
- shared non-auth config overlay behavior remains covered by regression tests

## Commands

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state
```

Result: passed.

```text
.
----------------------------------------------------------------------
Ran 1 test in 1.336s

OK
```

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed.

```text
.....................
----------------------------------------------------------------------
Ran 21 tests in 7.761s

OK
```

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && git diff --check
```

Result: passed.

```bash
python3 -m json.tool evals/evals.json >/dev/null && python3 -m json.tool dist/codex-switch/evals/evals.json >/dev/null
```

Result: passed.

```bash
openspec validate isolate-desktop-session-state --strict --json
```

Result: passed. Summary: 1 item passed, 0 failed.

```bash
openspec validate --all --strict --json
```

Result: passed after normalizing `openspec/specs/current-system/spec.md` to the
required OpenSpec `Purpose` and `Requirements` structure. Summary: 3 items
passed, 0 failed.

```bash
node /Users/cY/.codex/plugins/cache/openai-curated/plugin-eval/3f0def1b/scripts/plugin-eval.js analyze dist/codex-switch --format markdown
```

Result: completed with score 77/100, grade C, risk high.

Plugin Eval findings:

- `deferred_cost_tokens-budget-high`: deferred, because the evaluated release
  target is an installable CLI bundle that must include the full `scripts/`
  implementation. Removing or hiding those scripts would break the release
  artifact. Residual risk: Plugin Eval overstates static deferred token cost for
  this hybrid skill+CLI package; actual skill invocation remains 1,620 tokens
  and the scripts are not loaded unless inspected or executed. Follow-up path:
  evaluate a future split release shape or add a plugin-eval package profile
  that distinguishes executable payloads from skill references.
- `extra-doc-files`: deferred, because `README.md` is required in the
  installable release package. Residual risk: minor static best-practice score
  loss. Follow-up path: only revisit if codex-switch gains a dedicated plugin
  bundle separate from the CLI release archive.
- `py-complexity-high`: deferred as out of scope for the runtime-state isolation
  repair. Residual risk: higher review cost in existing CLI modules. Follow-up
  path: plan a separate refactor with characterization tests.

## Process Note

The focused regression and full verification pass in the current working tree.
The red phase for the focused regression was not replayed in this session
because the implementation was already present in the dirty working tree before
this verification step began. No archive action was taken.

## Evidence Summary

- Focused regression: passed.
- Full regression suite: 21 tests passed.
- Python compile check: passed.
- Shell syntax checks: passed.
- Whitespace diff check: passed.
- Release package rebuilt.
- OpenSpec strict validation passed for the active change and all specs/changes.
- Plugin Eval release target score recorded with justified deferrals.
