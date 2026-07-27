# VER-001 Final Source Verification

Date: 2026-07-25
Outcome: complete

The current worktree passed the full post-integration source matrix:

- transaction 215/215;
- profile 195/195;
- update/release 108/108;
- Runtime Binding 55/55 on Python 3.12 and system Python 3.9;
- Protocol/SAP 37/37 on both runtimes;
- Config Document 24/24;
- Verifier 22/22 on both supported test routes;
- official advisory 6/6 on both runtimes;
- strict OpenSpec 17/17;
- Bash 5/5;
- AST 54/54 and production imports 46/46 on both runtimes;
- workflow YAML 2/2 and release static contracts 7/7;
- isolated package validation and `git diff --check`.

The isolated current-source package is version `0.1.13`, has 64 manifest
files, mode `0755`, archive size `381951`, and payload SHA-256
`d79769dff0241bf68c5e256bfcc2398a19d8dd6c1fb8c83678caef3199d31fd5`.

Full evidence:
`.planning/verification/20260725151329-final-source-verification.md`.

`ROLLOUT-001` is next and already authorized. It must install this exact source,
prove live official ownership and App task entry, restore internal, and prove
the internal managed launcher/backend chain. No commit, push, tag, release,
archive, destructive cleanup, dependency change, or parity implementation is
authorized.
