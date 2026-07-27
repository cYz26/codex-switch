## Context

The current implementation derives official CLI paths, internal Desktop launchers, manifest fields, active observations, LaunchAgent expectations, and process identity in separate modules. The old default and process marker still name Codex.app, while the installed product is `/Applications/ChatGPT.app` with bundle identifier `com.openai.codex`. Internal capture persists a raw backend as the Desktop path, but normal switching uses a managed launcher. Internal `set-bin` can either bypass that launcher or leave it embedding the previous backend.

The live ChatGPT process also demonstrates two parser requirements: the main executable is `/Applications/ChatGPT.app/Contents/MacOS/ChatGPT`, and its app-server command places global `-c` options before the `app-server` subcommand. A fixed `codex app-server` regex omits this valid process and can make diagnostics false-pass.

## Skill Routing Ledger

- request kind: compatibility, integration, error-handling, and diagnostic repair
- workflow mode: Full OpenSpec
- capability-research: used; OpenAI's current ChatGPT desktop migration guidance, bundle identity/version, both CLI versions, generated schemas, and live read-only process shapes were checked
- decision-resolution: used; ChatGPT.app is canonical and Codex.app is legacy-only
- decision-grilling: skipped; no open product decision remains
- implementation-planning: used through DevFlow/OpenSpec and AI-native plan structure
- architecture-guidance: used; one Runtime Binding module is the interface for all consumers
- domain-language-modeling: skipped; existing shell/Desktop/backend terminology is sufficient
- openspec-routing: required and used
- Open Questions: none

## Goals / Non-Goals

**Goals:**

- Derive one complete effective binding per supported profile.
- Discover the current official ChatGPT bundle without accepting a managed PATH shim fallback.
- Keep internal Desktop on the managed launcher/proxy after capture and rebind.
- Make status, Doctor, verify, and switching share the same expectations.
- Attest both the launcher and actual child backend, including commands with global options before `app-server`.
- Require a successful app-server initialize result before smoke can pass.

**Non-Goals:**

- Treating ChatGPT Classic as a Codex backend target.
- Supporting arbitrary Desktop bundle locations or profile names.
- Starting, stopping, or switching the user's live ChatGPT process during automated verification.
- Removing protocol compatibility solely because current versions happen to match.

## Capability Evidence

- `authoritative_current`: OpenAI's current desktop migration guidance says the updated Codex app becomes ChatGPT with Chat, Work, and Codex; the previous app remains ChatGPT Classic.
- `local_scan`: ChatGPT.app bundle id is `com.openai.codex`, version `26.715.70719`; bundled CLI is `0.145.0-alpha.27`; internal CLI is `0.142.4`; Codex.app is absent. The live main executable and app-server command match ChatGPT paths and include a pre-subcommand `-c` option.
- `comparison`: adding ChatGPT constants to each caller would preserve contradictory ownership. A single binding result gives leverage across switch, status, Doctor, verify, and tests.
- `assumptions`: a legacy Codex.app may still exist on older installations; it is accepted only after the same bundle/executable validation and only when ChatGPT.app is absent.
- `contract`: delta scenarios cover canonical discovery, shim rejection, internal launcher derivation, rebind rollback, option-aware process parsing, stale backend detection, and initialize errors.

## Decisions

### Decision 1: Introduce a deep Runtime Binding module

Create `codex_switch_runtime_binding.py` with a frozen result:

```python
@dataclass(frozen=True)
class RuntimeBinding:
    profile: str
    shell_cli: Path
    desktop_cli: Path
    backend_cli: Path
    codex_home: Path
    desktop_host: DesktopHost | None
    requires_proxy: bool

def discover_desktop_hosts(roots: DesktopRoots = DEFAULT_DESKTOP_ROOTS) -> DesktopInventory: ...
def resolve_runtime_binding(context: RuntimeBindingContext, inventory: DesktopInventory) -> RuntimeBinding: ...
def attest_runtime_binding(binding: RuntimeBinding, observation: RuntimeObservation) -> RuntimeAttestation: ...
```

Switch, lifecycle/capture, set-bin, status, Doctor, and verify consume this result. The manifest remains persisted intent; `active.json`, launchctl, and process inventory are observations compared against it, never sources for expected values.

Alternative A was adding ChatGPT paths to existing constants and conditions. It was rejected because it keeps multiple truth sources. Alternative B was storing every effective path redundantly in `active.json`. It was rejected because redundant observations become stale and hide manifest drift.

### Decision 2: Use verified DesktopHost adapters

`ChatGPTDesktopHost` is the only adapter that can satisfy a new healthy official binding; it defines the canonical bundle root, main executable, bundled CLI, and bundle identity. `LegacyCodexDesktopHost` only observes an older Codex.app and emits migration evidence; because no current local bundle exists to verify its historical identity, it cannot certify a new healthy binding. Each current adapter requires a regular executable bundled CLI and the exact expected bundle identifier. ChatGPT Classic has no adapter; the locally installed Classic bundle uses `com.openai.chat` and has no bundled `codex`.

Official resolution fails closed with migration guidance if no verified current ChatGPT host exists, if only a legacy observation exists, or if the only CLI candidate is beneath the codex-switch managed store/shim. It does not use `PATH` as official Desktop evidence.

### Decision 3: Internal Desktop intent is the managed launcher plus backend

For `internal`, `desktop_cli` is always the deterministic managed launcher path, `backend_cli` is the validated manifest `codex_bin`, and `requires_proxy` is true. Fresh capture/init records that intent consistently. Rebinding stages a launcher generated with the new backend, validates and smokes the staged chain, atomically promotes launcher plus manifest, then rolls both back on failure.

PATH and explicit symlinks are discovery aliases, not persisted backend identity. Internal capture and rebind resolve them to the final regular executable before writing `codex_bin`. A normal internal switch that encounters a legacy symlink-valued manifest uses the same canonical backend for the shim, launcher, and capability receipt, then commits the canonical path with the refreshed launcher/receipt. The capability receipt keeps its no-follow regular-file check; weakening that check would make the receipt attest a mutable alias rather than the backend it describes.

### Decision 4: Process observation is option-aware and attests the full chain

Replace the fixed regex with token-aware parsing that locates the `app-server` subcommand after supported global options and their values. Desktop main-process recognition comes from the selected DesktopHost adapter. An internal observation is healthy only when environment intent equals the managed launcher, the proxy parent is present, and the child executable equals `backend_cli`. A stable launcher with a stale child is a mismatch.

Process inventory and launchctl/environment values become one immutable `RuntimeObservation` snapshot that status, Doctor, and verify can share inside a one-key invocation. `attest_runtime_binding` returns stable finding codes instead of letting each caller reconstruct comparisons.

### Decision 5: App-server smoke uses structured response outcomes

Initialize passes only on a matching JSON-RPC response containing `result` and no `error`. A later plugin-list response may use the explicitly documented non-fatal auth error, but cannot compensate for failed initialization. Prerequisite/mismatch/timeout outcomes are represented separately instead of inferred from message substrings.

## Critical Path

1. Add RED tests for ChatGPT discovery, managed-shim fallback rejection, fresh internal capture, option-aware process parsing, stale child backend, manifest/active drift, and initialize error.
2. Implement DesktopHost adapters and `RuntimeBinding` resolution.
3. Migrate lifecycle/switch/binding persistence to canonical results.
4. Migrate process inventory, status, Doctor, and verify expectations.
5. Make internal rebind staged and transactional, then run isolated chain smoke.

## Incidental Finding Budget

One bounded RED/GREEN guard is allowed for another caller that derives a binding inside the named modules. UI wording or performance work not required for correctness is `DEFER_AND_CONTINUE`; unsupported bundle/product selection or live Desktop mutation is `BLOCKED_AWAITING_HUMAN`.

## Risks / Trade-offs

- [Legacy installations may not have ChatGPT.app yet] → retain the verified legacy adapter without making it co-equal or default.
- [Process command quoting can be complex] → parse the `ps` command conservatively, fail closed on ambiguous shapes, and cover real observed forms.
- [Internal rebind smoke can be slow] → keep it bounded and injectable; no manifest promotion occurs before it succeeds.
- [Bundle identifiers may remain `com.openai.codex` despite the ChatGPT name] → validate both filesystem adapter and bundle identity rather than inferring from display name.

## Migration Plan

No eager live-state migration runs. Existing internal manifests whose `app_cli_path` is the raw backend or whose `codex_bin` is a symlink alias are interpreted through the canonical internal binding and corrected only on the next explicit capture/rebind/switch transaction. Existing ChatGPT bindings continue unchanged. A legacy Codex.app observation yields migration-required status until ChatGPT.app is installed; it is not auto-promoted to current ownership. Rollback restores the prior code, manifest, and managed launcher.

## Continuation Policy

- Execution policy: `auto-until-terminal`.
- Canonical execution source: this change's `tasks.md`.
- After each validated item, select the next dependency-ready runtime-binding item.
- Genuine Human Gates: unsupported bundle identity, public CLI compatibility expansion, destructive live Desktop mutation, or new external dependency.
- Live switch/install/release, Git effects, archive, and migrations remain separately unauthorized.

## Open Questions

None.
