# Verification: remote-script-runner

## Metadata

- Change: `remote-script-runner`
- Recorded at: 2026-06-08T11:51:59+08:00
- Result: passed with documented Plugin Eval deferrals

## Commands

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_remote_runner_downloads_release_and_execs_command
```

Result: passed.

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.803s

OK
```

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed.

```text
......................
----------------------------------------------------------------------
Ran 22 tests in 8.763s

OK
```

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh && git diff --check
```

Result: passed.

```bash
scripts/package-release.sh
```

Result: passed. Output: `dist/codex-switch.tar.gz`.

```bash
python3 -m json.tool evals/evals.json >/dev/null && python3 -m json.tool dist/codex-switch/evals/evals.json >/dev/null
```

Result: passed.

```bash
test -x dist/run.sh && test -x dist/codex-switch/run.sh && tar -tzf dist/codex-switch.tar.gz | rg '(^codex-switch/run.sh$|^codex-switch/scripts/codex-switch$)'
```

Result: passed.

```text
codex-switch/run.sh
codex-switch/scripts/codex-switch
```

```bash
openspec validate remote-script-runner --strict --json
```

Result: passed. Summary: 1 item passed, 0 failed.

```bash
openspec validate --all --strict --json
```

Result: passed. Summary: 3 items passed, 0 failed.

```bash
node /Users/cY/.codex/plugins/cache/openai-curated/plugin-eval/3f0def1b/scripts/plugin-eval.js analyze dist/codex-switch --format markdown
```

Result: completed with score 77/100, grade C, risk high.

Deferred Plugin Eval findings:

- `deferred_cost_tokens-budget-high`: deferred, because the evaluated release
  target is an installable CLI bundle that must include the full `scripts/`
  implementation. Removing or hiding those scripts would break the release
  artifact. Residual risk: Plugin Eval overstates static deferred token cost for
  this hybrid skill+CLI package; actual skill invocation remains good and the
  scripts are not loaded unless inspected or executed. Follow-up path: evaluate
  a future split package shape or a Plugin Eval profile that distinguishes
  executable payloads from skill references.
- `extra-doc-files`: deferred, because `README.md` is intentionally included in
  the installable release package. Residual risk: minor static best-practice
  score loss. Follow-up path: revisit only if codex-switch gains a dedicated
  plugin bundle separate from the CLI release archive.
- `py-complexity-high`: deferred as out of scope for this remote-runner change.
  Residual risk: higher review cost in existing CLI modules. Follow-up path:
  plan a separate refactor with characterization tests.

## Evidence Summary

- Focused remote-runner regression: passed.
- Full regression suite: 22 tests passed.
- Shell syntax, Python compile, JSON, package, tarball, and OpenSpec checks:
  passed.
- Release output includes `dist/run.sh` and `codex-switch/run.sh` in the tarball.
