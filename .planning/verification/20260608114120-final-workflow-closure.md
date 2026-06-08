# Verification: final workflow closure

## Metadata

- Recorded at: 2026-06-08T11:41:20+08:00
- Scope: final closure for `isolate-desktop-session-state` and baseline
  `current-system`
- Result: passed with documented Plugin Eval deferrals

## Commands

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed.

```text
.....................
----------------------------------------------------------------------
Ran 21 tests in 7.313s

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
openspec validate --all --strict --json
```

Result: passed. Summary after `isolate-desktop-session-state` archive: 3 items
passed, 0 failed.

```bash
node /Users/cY/.codex/plugins/cache/openai-curated/plugin-eval/3f0def1b/scripts/plugin-eval.js analyze dist/codex-switch --format markdown
```

Result: completed with score 77/100, grade C, risk high.

Deferred findings:

- `deferred_cost_tokens-budget-high`: release package necessarily includes the
  CLI implementation under `scripts/`; removing it would break installation and
  runtime behavior.
- `extra-doc-files`: `README.md` is intentionally included in the installable
  release package.
- `py-complexity-high`: existing CLI complexity is out of scope for this
  runtime-state isolation repair and should be handled in a separate refactor.

## Archive Evidence

- `openspec archive isolate-desktop-session-state -y`: passed.
- The change was archived as
  `openspec/changes/archive/2026-06-08-isolate-desktop-session-state/`.
- `openspec/specs/codex-switch/spec.md` was created and validated.
