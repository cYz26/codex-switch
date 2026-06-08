# Current System Baseline

## Why

Initialize a safe baseline for Codex-managed project work.

## What Changes

- Create workflow state, planning files, OpenSpec artifacts, and verification gates.

## Target State

- Complete the approved behavior for `current-system`.
- Keep required capabilities in the active change unless explicitly marked as non-goals.
- Use capability slices and validation evidence as the execution boundary.

## Scope

- Project mode: brownfield
- Change type: setup

## Capability Evidence

- authoritative/current: Record official docs, primary source, CLI help, schema, or version evidence when the change depends on current or external capability.
- local scan: Record relevant repo files, config, plugin manifests, hooks, installed cache, scripts, tests, or generated artifacts inspected.
- comparison: Record native capability, local availability, fallback options, assumptions, and the selected contract.

## Non-Goals

- Do not expand beyond the requested change without updating this proposal.

## Completion Contract

- [x] Target State is clear.
- [x] Acceptance Criteria are defined in specs.
- [x] Capability Slices and Validation Commands are defined in tasks.
- [x] Verification evidence is recorded before archive.

## Risks

- Compatibility and verification risks must be resolved before archive.
