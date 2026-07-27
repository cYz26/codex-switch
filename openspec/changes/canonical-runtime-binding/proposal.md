## Why

Shell CLI, Desktop launcher, backend binary, manifest, active record, and running-process expectations are derived independently today. After the official desktop consolidation into ChatGPT.app or an internal backend rebind, those sources can disagree while status, Doctor, or verify either false-pass or reject a valid managed proxy chain.

## What Changes

- Introduce one canonical runtime-binding interface that derives shell CLI, Desktop launcher, backend binary, app home, bundle ownership, and expected running process for each supported profile.
- Treat `/Applications/ChatGPT.app` as the current official Desktop bundle and ChatGPT's bundled `codex` as the official CLI. Treat `/Applications/Codex.app` only as a verified legacy migration adapter; never select ChatGPT Classic as a Codex backend.
- Make init/capture, switch, status, Doctor, and verify consume the same binding result and fail closed instead of falling back to a managed PATH shim as the official bundle CLI.
- Treat PATH or explicit symlinks as discovery aliases only for the internal product profile; persist and attest the resolved regular backend so capability receipts never bind to a symlink.
- Make internal rebinding transactional: validate the new backend, regenerate the managed launcher/proxy, attest launcher and child backend, run compatibility smoke, then persist the binding.
- Require app-server initialize success, derive verification expectations from the profile manifest/binding rather than stale `active.json`, and report observation drift separately.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: official Desktop discovery, internal managed launcher binding, process attestation, Doctor/status/verify alignment, and rebind compatibility requirements are changed.

## Impact

Primary impact is in constants/path/lifecycle/binding/running-app/status/Doctor/verify modules and isolated runtime-binding tests. Current evidence is ChatGPT bundle `com.openai.codex` version `26.715.70719`, bundled CLI `0.145.0-alpha.27`, internal CLI `0.142.4`, and no installed Codex.app. No real Desktop start/stop/rebind is required for implementation verification.
