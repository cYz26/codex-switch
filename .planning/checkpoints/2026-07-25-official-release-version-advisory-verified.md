# Official Release Version Advisory Verified

Date: 2026-07-25

`official-release-version-advisory` is complete at 13/13 tasks.

The wrapper now prints a bounded, non-blocking latest-stable
`openai/codex` comparison for official/internal update checks and one-key
switches. Internal comparison runs after any auto-update and cannot select an
install target. Profile-store zero-write, zero-helper, failure, skip, packaging,
and dual-runtime contracts are covered.

Final results:

- policy 4/4 and focused wrapper 7/7 on Python 3.12.13 and Python 3.9.6;
- release missing-module regression 1/1 on both runtimes;
- full profile 171/171 and update/release 64/64 on Python 3.12.13;
- strict OpenSpec 17/17;
- AST 53/53 and production imports 46/46 on both runtimes;
- Bash syntax, isolated bundle validation, trusted hash binding, and
  `git diff --check` passed.

Full evidence:
`.planning/verification/20260725013044-official-release-version-advisory.md`.

No live switch/update/install/App restart/plugin/release/Git mutation ran.
The primary `fail-safe-update-release` implementation remains separate and
incomplete; resume it from its authoritative task list only when that work is
continued.
