---
checkpoint_id: 2026-07-27-parity-exact-source-install-verified
created_at: 2026-07-27T12:28:00+08:00
boundary: live_install_verified
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Execute task 8.3 same-backend parity preparation and rebind
---

# Checkpoint: Exact-Source Install Verified

Date: 2026-07-27 12:28:00 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Status: `VERIFIED`

## Result

Task 8.2 is complete at 70/79. One safe live RED exposed a historical
manifest-v1 compatibility defect. A single installer-level RED/GREEN fixed it
without a general migration framework or extra fault matrix.

```text
new focused regression:
  Python 3.12.13 1/1
  system Python 3.9.6 1/1
adjacent focused matrix:
  Python 3.12.13 5/5
  system Python 3.9.6 5/5
active strict OpenSpec: valid
```

## Installed Identity

```text
current payload:
  d55005d6d8b78a9e123aa4fe8d801da131df3d5020daf7d43b88f93828914392
rollback payload:
  ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab
manifest files/directories/required paths: 66/5/20
prebuilt versus installed tree: byte-exact
install staging residue: 0
bytecode directories: 0
restart output: absent
```

The installed release validates only through its resolved immutable path;
direct validation of the `current` symlink remains intentionally rejected.

## Boundary

ChatGPT/proxy/backend pids remain `95489`/`95838`/`95842`. No App restart,
same-backend rebind, provider task, dependency, commit, push, tag, release,
archive, or retained-evidence cleanup occurred.

## Next Action

Run task 8.3 through the supported same-backend parity preparation/rebind for
`/Users/cY/.local/bin/codex`. Record manifest, capability receipt, parity
receipt, overlay, profile/shared/runtime config digests, then require clean
status, Doctor, and `verify internal --repair=none` before task 8.4.
