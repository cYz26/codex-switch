# Final Source Verification

Date: 2026-07-25 15:13:29 +0800
Task: `VER-001`
Status: passed

## Completion Claim

The current worktree source passed the complete post-integration verification
matrix. This evidence authorizes the already approved `ROLLOUT-001`; it does
not itself claim that the installed PATH wrapper or running Desktop App has
been updated.

## Fresh Commands and Results

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v` | 55/55 passed |
| `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v` | 55/55 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v` | 37/37 passed |
| `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v` | 37/37 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v` | 215/215 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` | 195/195 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v` | 108/108 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_config_document.py -v` | 24/24 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_verify.py -v` | 22/22 passed |
| `CODEX_SWITCH_PYTHON="$(command -v python3.12)" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_verify.py -v` | 22/22 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_official_release.py -v` | 6/6 passed |
| `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_official_release.py -v` | 6/6 passed |
| `openspec validate --all --strict --no-interactive` | 17/17 passed |
| `bash -n scripts/codex-switch scripts/codex_env_setup install.sh run.sh scripts/package-release.sh` | 5/5 passed |
| dual-runtime AST/import harness | AST 54/54 and production imports 46/46 on Python 3.12 and system Python 3.9 |
| Ruby YAML parse | 2/2 release workflows parsed |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest scripts.test_codex_update_release.CodexReleaseWorkflowTests -v` | 7/7 passed |
| isolated `scripts/package-release.sh` plus `validate_release_outputs` | passed |
| `git diff --check` | passed |

The first raw system-Python verifier invocation intentionally failed during
fixture setup because system Python 3.9 cannot be embedded in the managed
Desktop wrapper. The supported dual-runtime route supplies
`CODEX_SWITCH_PYTHON=python3.12`; that exact command passed 22/22. No production
contract was relaxed.

## Isolated Package Receipt

- Version: `0.1.13`
- Manifest files: `64`
- Package root mode: `0755`
- Archive bytes: `381951`
- Payload SHA-256:
  `d79769dff0241bf68c5e256bfcc2398a19d8dd6c1fb8c83678caef3199d31fd5`
- Exact outputs: `codex-switch/`, `codex-switch.tar.gz`, `run.sh`
- Source: the current worktree through the supported package adapter
- Residual temporary output: none; the temporary directory was automatically
  removed after validation

## Review Closure

- Missing or empty internal `codex_bin` fails closed; symlink aliases resolve
  to the strict executable target before manifest, launcher, transaction, or
  capability-receipt use.
- Capture regressions use real temporary executables instead of string-only
  fixtures.
- Transaction binding drift is injected at the canonical resolver boundary.
- The minimal release fixture includes the required official-release module,
  so release verification cannot fail through missing-fixture cascades.
- The proxy client-input loop is stoppable after backend exit and preserves
  final stdout/stderr plus the exact backend status without thread traceback.

## Remaining Authorized Work

`ROLLOUT-001` remains: install this exact current source through the supported
local-source installer path, run live `codex-switch official` acceptance,
verify shell/App/profile/wrapper/running app-server ownership and real App task
entry, then restore and attest `internal`.

Commit, push, tag, release, OpenSpec archive, destructive cleanup, dependency
changes, and parity implementation remain outside this authorization.

`PARITY-001` stays queued for a subsequent independent Full OpenSpec after the
current Goal is complete and stable.
