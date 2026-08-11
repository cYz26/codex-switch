# Package Verification: SHARED-SWITCH-OPT-20260810T162102+0800

## Outcome

- Status: `VERIFIED_NOT_INSTALLED`.
- Generated-artifact disposition: `RETAIN`.
- Physical root:
  `/private/tmp/codex-switch-shared-opt-20260810T162102+0800`.
- Live profile/App/install effect: not performed.
- Cleanup: not authorized and not performed.

## Package Identity

```text
version: 0.1.13
archive SHA-256:
  1314f7c83de6d77c9487f69b44e5ccc1dec698feba572b3f959e2acfea630751
manifest SHA-256:
  2a41b93478d3f1489d574778e6e7f154aa8ffd479a0dc6e2ea0e7e33d364fa03
payload SHA-256:
  bb30440a284d6e120a48de19c42f3995795220085d2f8c7a1c6fd8b8bda829d3
required paths: 22
files: 71
directories: 5
```

The package builder exited zero and performed its built-in manifest, mode,
archive, required-path, and runtime-import validation. README, SKILL, Home
selector, transaction, complete transaction test, and complete profile test
are byte-exact between source and the package. Fresh package-local focused
results are transaction 8/8 and profile 4/4.

## Release-Counterpart Plugin Eval

The installed plugin-eval CLI was not on shell PATH, so the same installed
entrypoint was invoked directly with Node:

```text
node .../plugin-eval/0.1.2/scripts/plugin-eval.js analyze \
  /private/tmp/codex-switch-shared-opt-20260810T162102+0800/codex-switch \
  --format markdown
```

Final result: 58/100, grade D, high static risk, with 2 failures, 3 warnings,
and 2 informational checks. The final active budget is 3,810 tokens (43
trigger plus 3,767 invoke), reduced from this task's first 3,878-token report
after compressing the new operator guidance. Deferred support-tree cost is
1,032,389 tokens. Findings remain the existing classes recorded by INC-012:
invoke/deferred static budgets, top-level README, historical Python complexity,
seven long lines, and unavailable coverage artifacts. No new finding class was
introduced by this change.

Fixing those findings requires a separately planned benchmark-backed
Skill/package architecture change rather than expanding this transaction
repair. They remain `DEFER_AND_CONTINUE`; runtime behavior is covered by 541
source tests plus the fresh package-local focused matrix. No live benchmark,
provider call, rewrite, install, release, or cleanup was performed.
