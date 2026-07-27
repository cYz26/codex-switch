# Fail-Safe Installer and Runner Adapters Verified Checkpoint

Date: 2026-07-24

## Outcome

`fail-safe-update-release` tasks 2.1-2.2 are complete, bringing the change to
8/38. Installer and remote-runner entrypoints now stage candidates, use trusted
bootstrap modules, validate complete bundles, promote immutable digest roots,
and preserve the stable `current/scripts/codex-switch` public path.

## Trust Boundary

- Piped stdin execution is safe when `BASH_SOURCE[0]` is unavailable.
- Explicit or real script-local module directories are trusted directly.
- Installed or archive module pairs must match embedded SHA-256 values.
- Verified modules are copied to temporary trusted staging and re-hashed.
- Missing profile, bundle, or promotion Python modules reject the candidate.
- Malicious bootstrap modules remain inert and cannot create test sentinels.

## Replay Contract

The promotion CLI passes the requested command into `promote_candidate` as
`scripts/codex-switch`. Replay occurs exactly once from the promoted
`releases/<digest>` root. A concurrent promotion may change `current` without
redirecting that command. Nonzero and signal-derived exit status are preserved.

## Verification

- Python 3.12.13 update/release suite: 47/47 passed.
- Python 3.9.6 installer/runner adapter class: 10/10 passed.
- Six adjacent profile adapter tests: passed on Python 3.9.6 and 3.12.13.
- Dual Python compile, Bash syntax, and strict FSR OpenSpec: passed.
- Embedded bundle digest: `21db34cf16c52c5c5e671205f95c19b0cb7a8de94199363db24f09f3a7cc6920`.
- Embedded promotion digest: `590994799860ef13b74f2b07e45ad249e81e9dcf1e984ac7408bef7743845544`.
- Isolated package: exact three public outputs, 60 manifest files, 67 archive
  members, payload SHA-256
  `75c79fb0608d55c780b9b27bfc8b07c918e1249e5ca2f836cf0eda5792e7ee46`.
- `git diff --check`: passed.

## Safety Boundary

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or archive action ran. Full profile-suite
verification remains deferred to task 7.3.

## Next Action

Execute task 2.3 by RED/GREEN for self-update invalid candidate, handshake,
timeout, concurrency, and exactly-once replay behavior.
