## 1. Contract and RED Tests

- [x] 1.1 Add transaction RED tests for the exact CLI-only manifest-plus-executable bundle, schema-v4 marker validation, rollback, and unchanged schema-v3 full bundles.
- [x] 1.2 Add promotion RED tests for digest/version-bound CLI generation commit, failed CLI postcondition rollback, and untouched Desktop/parity artifacts.
- [x] 1.3 Add wrapper RED tests proving `split` selects CLI-only promotion and runtime smoke while direct `update-internal` retains full parity promotion.
- [x] 1.4 Add runtime and switch RED tests for CLI-only shell execution, digest drift rejection, and internal-App pre-mutation readiness failure.
- [x] 1.5 Add verify, Doctor, and status RED tests proving internal parity is not applicable only for internal-CLI/official-App selection.

## 2. Atomic CLI-Only Promotion

- [x] 2.1 Extend the runtime-rebind transaction with a fail-closed CLI-only bundle scope and recoverable schema-v4 marker while preserving full-scope defaults.
- [x] 2.2 Implement CLI-only staged promotion with exact candidate validation, additive manifest generation/readiness metadata, prepared postcondition validation, rollback, and terminal output.
- [x] 2.3 Route only split auto-update through CLI-only promotion, replace forced App compatibility verification with bounded internal runtime smoke, and preserve `--keep-version` behavior.

## 3. Runtime and App Readiness

- [x] 3.1 Validate digest-bound CLI-only generations in the managed internal shell path without consuming stale App capability/parity evidence.
- [x] 3.2 Preserve shared Plugin/Skill preflight for functional CLI commands and existing informational command behavior.
- [x] 3.3 Add one internal-App readiness guard to both public switching and the deepest transaction boundary before backup or App mutation.
- [x] 3.4 Make the internal App generation validator reject CLI-only generations and make a successful full rebind clear CLI-only metadata atomically.

## 4. Surface-Specific Diagnostics

- [x] 4.1 Make verify collect and repair parity only when the resolved active App profile is internal, with a stable not-applicable diagnostic for split mode.
- [x] 4.2 Apply the same App-owner parity rule to Doctor and status without suppressing internal CLI or official App health checks.
- [x] 4.3 Freeze one active selection snapshot across verify and Doctor, bind parity repair to a locked exact-record CAS, and cover concurrent selection drift test-first.
- [x] 4.4 Run focused transaction, promotion, wrapper, runtime, switch, verify, Doctor, and status tests and close regressions test-first.

## 5. Documentation and Final Verification

- [x] 5.1 Update README and SKILL guidance for CLI-only split updates, App-running behavior, `--keep-version`, and deferred internal-App compatibility.
- [x] 5.2 Run the full source suite, Bash/Python/static checks, strict OpenSpec validation, and diff-integrity review.
- [x] 5.3 Record fresh verification evidence, update the Ledger and namespaced state, and make a source-only completion claim with live install/promotion explicitly unclaimed.

## 6. Live Acceptance Repair

- [x] 6.1 Reopen the completed claim and record the production-sized backend rejection, managed-smoke bypass, public TDD seams, compatibility decision, and conditional App guidance in the existing OpenSpec.
- [x] 6.2 Add managed-shell RED coverage for a valid backend larger than the text-artifact limit and an over-bound backend, then implement stable streaming executable hashing without changing CLI-generation schema v1.
- [x] 6.3 Add promotion RED coverage proving the prepared postcondition uses the true CLI-generation validator plus a freshly rendered managed-shim probe and atomically restores binary plus manifest on failure.
- [x] 6.4 Add verifier and wrapper RED coverage proving CLI-only runtime smoke uses the managed shim, `preserve` omits restart guidance while `rebind` retains it, and progress is visible before apply exits; then implement all behaviors without buffering the Python producer or stream filter.
- [x] 6.5 Update operator guidance and run focused plus broad source, static, strict OpenSpec, compatibility, and diff-integrity validation.
- [x] 6.6 Record fresh repair evidence, review the scoped diff, update the Ledger and namespaced state, and replace the invalidated completion claim without installing, updating, re-running split, or restarting App.
