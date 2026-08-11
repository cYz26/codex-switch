# Agent Task Contract

## Goal
Close the final P1 SIGKILL race by ensuring every real subprocess used by the
shared Plugin materializer inherits the exact active store mutation lock, so a
surviving backend prevents recovery from retiring its durable intent until the
backend exits, then prove late-write recovery with a real subprocess test.

## Worker ID
`split-shared-backend-lease`

## Stable Input Snapshot
- `scripts/codex_switch_transaction.py`: `d33270d137b51a4d0e024bef27db99c8a3465401ad6be5f1e9645d581af60856`
- `scripts/codex_switch_shared_configuration.py`: `0083c321d08d0fb208f52d61e8f71a83b1b6e1b3e8e62ce112608eaecbbd016a`
- `scripts/codex_switch_plugins.py`: `287eb4916c571d7fea79a1bc52f2c2bca52b56ff968cdd5b9938defcd5a8f91a`
- `scripts/test_codex_shared_configuration.py`: `35d2d5f0d635e718a6ac76ab8a45381aa8c122d3ecde3a60be4916f2aed3db53`
- `scripts/test_codex_shared_materialization.py`: `8cbef96c486fd9310a1f8852c6a43bc6f18cf4f2d46055d7eeb7f61329f3358d`
- OpenSpec design: `f432f642dbbad8cb8641518dcec67417a1710b37010980e204f5736c296130bb`
- OpenSpec spec: `ded292550cacb5e626a9932fc589ef733e0576171fa7bc32f04628fff3297c45`
- OpenSpec tasks: `b0080fb60f8e2922e6b0b35a8068778cc51e3c21532be851947e90fffdd1da3f`

Stop before editing if any stable input differs. OpenSpec is a read-only input.
Main will not edit any allowed production or test file while this worker runs.

## Scope
Allowed write set for worker `split-shared-backend-lease` only:
- `scripts/codex_switch_transaction.py`
- `scripts/codex_switch_shared_configuration.py`
- `scripts/codex_switch_plugins.py`
- `scripts/test_codex_shared_configuration.py`
- `scripts/test_codex_shared_materialization.py` only for adjacent mock or
  signature compatibility required by the production lease parameter

Read adjacent store/IO/lock/runtime/process/release tests as needed. Forbidden:
every other write, live profile/cache/App/backend/network operations,
dependencies, cleanup, Git, release, archive, or deletion of retained Plugin
cache artifacts.

## Constraints
Read `.agents/skills/diagnosing-bugs/SKILL.md` and `.agents/skills/tdd/SKILL.md`
fully. Treat OpenSpec Decisions 14 and 15 and the independent reviewer repro as
canonical. Preserve strict receipt/cache/path/App attestation, exact
selector-only recovery, target CAS, independent caches, retained artifacts,
read-only report/plan behavior, and `state.json` as the only main commit point.

Implement systemically:

1. Expose the active exact store-root lock descriptor through the private
   `LockedStoreMutation` seam only while its lock is active. Validate identity
   against the current store root and fail closed for an absent/stale/wrong
   descriptor.
2. Thread that descriptor only through locked shared reconcile, the production
   materializer, and every external command it invokes. Use subprocess FD
   inheritance (`pass_fds` or an equivalent kernel lease) so parent SIGKILL
   leaves the lock held by the surviving backend. Do not weaken the existing
   nonblocking store-busy behavior.
3. Validate at the materializer boundary that the descriptor is a real
   directory FD matching the exact store root. Do not expose it in persisted
   state, config, logs, receipts, environment, or public CLI.
4. Preserve normal synchronous behavior: backend exit precedes main commit and
   lock release. Ordinary exceptions still recover Decision 14 intent. On
   parent SIGKILL, a new apply must fail closed while the backend lease is live,
   leave intent/config/state untouched, and plan nothing.
5. Add a real subprocess regression: external helper starts and blocks; kill
   the reconcile parent; prove helper survives and early apply is store-busy
   with intent retained and target unchanged; release helper; prove late
   selector write; after helper exit, prove next apply selectively recovers the
   intent before planning. Bound all waits and reap/terminate test helpers on
   failure without touching real processes.
6. Keep existing in-process SIGKILL and all 69 focused regressions green. The
   test must not invoke a real Codex backend, App, network, or workstation home.

## Verification
Run and report exact results for:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_shared_configuration.SharedConfigurationTests.test_sigkill_parent_keeps_backend_store_lease_until_late_write_recovery
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_shared_configuration
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_shared_materialization
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_transaction
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest \
  scripts.test_codex_shared_configuration \
  scripts.test_codex_shared_materialization \
  scripts.test_codex_shared_lifecycle
PYTHONPYCACHEPREFIX=/tmp/codex-switch-worker-pycache python3.12 -m py_compile \
  scripts/codex_switch_transaction.py \
  scripts/codex_switch_shared_configuration.py \
  scripts/codex_switch_plugins.py
openspec validate independent-app-cli-profiles --strict --no-interactive
git diff --check -- \
  scripts/codex_switch_transaction.py \
  scripts/codex_switch_shared_configuration.py \
  scripts/codex_switch_plugins.py \
  scripts/test_codex_shared_configuration.py \
  scripts/test_codex_shared_materialization.py
```

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` and report:
- changed files and final hashes;
- complete test logs and validation results, including initial RED and final
  GREEN commands/counts;
- exact lease ownership and descriptor-validation mapping;
- parent SIGKILL, surviving backend, store-busy early apply, retained intent,
  late write, backend exit, and final selective-recovery proof;
- complete adjacent results, unverified areas, risks, and incidental findings.

## Human Gate
The worker must stop and report `BLOCKED_AWAITING_HUMAN` before write-set
expansion, public API/persistence expansion, a new dependency, weakening any
existing strict guard, inability to prove bounded helper termination, shared
files outside this contract, ambiguous deletion, a failing production
contract, live/backend/network/App/workstation action, cache cleanup, Git,
install, release, or archive.
