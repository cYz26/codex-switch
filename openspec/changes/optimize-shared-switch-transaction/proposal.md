## Why

The first real `codex-switch split --keep-version` activation spent many
minutes under `Applying switch mutations...` because generic Home support
selection admitted 39 unrelated top-level entries and the journal repeatedly
re-hashed every frozen directory before and after each effect. Starting the App
during that window correctly triggered CAS rollback, but the excessive window,
misclassified Desktop temporary files, and missing progress made a healthy
safety mechanism operationally unusable.

## What Changes

- **BREAKING**: replace implicit denylist-based generic Home sharing with a
  versioned allowlist for supported user-authored support surfaces. Unknown,
  runtime-owned, backup, log, generated, and Desktop atomic-write artifacts are
  ignored and never propagated; existing unknown targets are preserved rather
  than deleted.
- Keep Plugin selectors, marketplace descriptors, configured Skills, personal
  Skills, and profile-local plugin caches under the existing shared-capability
  ownership model; do not reintroduce physical plugin-cache sharing.
- Preserve recoverable transaction semantics while removing validation work
  that grows as `all frozen trees × every effect`: attest selected sources once,
  guard the current effect and cheap continuously mutable inputs during apply,
  and retain one complete compare-and-swap proof before commit.
- Derive Desktop effects from the actual target state. When the live App is
  already provably healthy on the official binding, preserve that App surface
  and apply only the internal CLI side while the App remains running. Require a
  stopped App only when LaunchAgent, GUI environment, App wrapper, or another
  App-owned surface actually needs mutation; a late App launch during that
  rebind remains protected by transaction CAS and rollback.
- Keep Desktop global-state projection out of the supported split path. The
  split consumes only generic support and the existing generationed
  Plugin/Skill desired-state contract needed by the internal CLI; synchronized
  profile switches retain their existing Desktop settings behavior.
- Report deterministic shared-sync progress with item counts so an operator can
  distinguish forward progress from a stalled transaction.
- Add public transaction/CLI regressions, performance-work bounds, docs, and
  verification evidence for selection, progress, fast preflight, late drift,
  rollback, and unchanged supported sharing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: generic Home support selection, effect-derived split
  preflight, App-preserving CLI-only activation, mutation progress, and
  frozen-input validation become bounded, explicit, and observable without
  weakening final transaction safety.

## Impact

- Public behavior: a supported split preserves an already healthy official App
  while it runs; only a split that actually needs App mutation requires
  stopped-App proof. Preview identifies whether the App action is `preserve` or
  `rebind`, and mutation output includes counted shared-sync progress.
- Compatibility: only the documented support allowlist is newly projected;
  previously auto-shared unknown entries stop receiving updates but are not
  removed from either Home.
- Runtime code: Home support classification, transaction planning/journaling,
  frozen-input validation, Desktop-effect selection, and conditional process
  preflight.
- Verification and distribution: focused transaction/profile tests, README and
  Skill guidance, strict OpenSpec/workflow/static checks, release-counterpart
  Plugin Eval, and package/source parity.
- No dependency, live App/profile mutation, internal binary update, install,
  release, archive, Git effect, migration apply, cleanup, credential change, or
  destructive action is authorized.
