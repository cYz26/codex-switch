# ROLLOUT-001 Official Restart Gate

Date: 2026-07-25
State: historical gate; internal restored, self-update repair pending

## Superseding Update

The official restart and internal restoration occurred after this checkpoint.
The current single ChatGPT process uses the managed Python 3.12 proxy and
internal backend. Rollout completion is now blocked only by the same-version
self-update defect recorded as FSR task 2.7.

Do not use `launchctl submit` for App restarts. macOS documents that submitted
jobs are kept alive after failure; the temporary rollout job repeatedly
relaunched ChatGPT until it was removed. Any future restart must be a bounded
one-shot action with explicit timeout, process verification, and cleanup.

The final current-source install is active at immutable release digest
`db85a38c2bc18fcb7d63f9bbca4dcbef898d5fcb0857646690075dd4418a2550`.
Installed `status` did not create bytecode residue, and strict candidate
validation passed afterward.

The real `codex-switch --skip-self-update official` transaction committed:

- active profile `openai-official`;
- official CLI/App binding
  `/Applications/ChatGPT.app/Contents/Resources/codex`;
- backup
  `/Users/cY/.codex-switch/backups/20260725T074950Z-switch-internal-to-openai-official`;
- clean official `gpt-5.5` config with no internal provider.

The pre-existing ChatGPT process still owns the internal launcher/backend, so
verification correctly reports GUI and app-server mismatch until a full App
restart.

Next:

1. Quit ChatGPT completely and reopen it.
2. Verify the new ChatGPT pid and bundle-owned official app-server.
3. Run official status/doctor/verify and prove a real task entry.
4. Run the read-only latest-stable and internal-update checks.
5. Restore internal with `--skip-update-check`, restart again, and prove the
   managed wrapper/proxy/backend chain plus a real task entry.

Durable evidence:
`.planning/verification/20260725151858-live-official-internal-rollout.md`.
