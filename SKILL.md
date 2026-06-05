---
name: codex-switch
description: Use when the user wants Codex to initialize, inspect, log in to, or switch local Codex profiles, official/internal auth, CODEX_HOME snapshots, profile-specific codex CLI binaries, or Codex Desktop CODEX_CLI_PATH bindings without manually running codex-switch commands.
metadata:
  short-description: Manage Codex profile switching
---

# Codex Switch

## Overview

Use this skill to operate the project-agnostic Codex workstation switcher. The
deterministic implementation is bundled with this repository under `scripts/`
and installed as a single public CLI: `codex-switch`.

`codex-switch` manages:

- profile files such as `~/.codex/internal.config.toml`
- optional file-backed `auth.json` profile stores
- profile-specific Codex CLI binary bindings
- a PATH-friendly `~/.codex-switch/bin/codex` shim
- Codex Desktop `CODEX_CLI_PATH` through a user LaunchAgent

It also owns internal Codex CLI checks and updates. The `internal` one-key
command automatically runs `codex-switch update-internal` when it detects that
the internal profile's bound CLI is older than the latest internal release.

## When to Use

Use for requests like:

- "initialize Codex profile switching"
- "switch to OpenAI official profile"
- "switch back to internal profile"
- "check which Codex profile, CLI, and app binary I am using"
- "bind openai-official to this codex binary"
- "run codex login in the official profile"
- "make Codex Desktop use the official app bundled CLI"

Do not use this skill for configuring project MCPs, app-specific hooks, Figma,
Bits, Aiden, or OpenSpec assets.

## Command Map

Prefer the wrapper:

```bash
scripts/codex-switch status
scripts/codex-switch internal --dry-run
scripts/codex-switch official
scripts/codex-switch check-update
scripts/codex-switch update-internal --dry-run
```

If the skill has been installed into `$CODEX_HOME/skills` and the wrapper has
been installed into PATH, use:

```bash
codex-switch status
codex-switch internal
codex-switch official
codex-switch update-internal
```

Advanced commands can call the Python switcher directly:

```bash
python3 scripts/codex_profile_switch.py doctor
python3 scripts/codex_profile_switch.py switch openai-official --dry-run
```

## Workflow

1. For first-time setup, run `scripts/codex-switch status` or `list`; if the
   store is missing, run `scripts/codex-switch init --capture-current internal`.
2. For one-key switching, run `scripts/codex-switch internal` or `official`.
   The wrapper always runs a dry-run plan, checks the target profile for CLI
   updates, automatically installs detected internal updates, performs the real
   switch, then runs `doctor` and `status`. When switching to `official`, the
   wrapper automatically runs `login openai-official` first if the profile uses
   file auth and no stored `auth.json` exists yet. The login runs in a clean
   temporary `CODEX_HOME` and copies only the resulting `auth.json` back to the
   stored profile, so legacy profile config does not break newer Codex login.
   Use `--skip-login` for non-interactive scripts. Use `--skip-update-check`
   when the update probe and auto-update should be omitted.
3. For login, run `scripts/codex-switch login-official` or
   `scripts/codex-switch login-internal`.
4. For CLI binding, run `scripts/codex-switch set-bin <profile> <absolute-path>`.
5. For Codex Desktop binding, run
   `scripts/codex-switch set-app-bin <profile> <absolute-path>`.
6. For standalone install/update checks, run `scripts/codex-switch check-update`.
   This remains read-only and prints `codex-switch update-internal` when an
   internal update is needed.

## Safety

- Treat `auth.json` as a secret. Never print its contents.
- Do not modify `/Applications/Codex.app`; bind to its bundled CLI path instead.
- Do not clear live auth when the target profile lacks `auth.json` unless the
  user explicitly asks for `--clear-missing-auth`.
- For `official`, prefer the one-key command's first-run auto-login; use
  `scripts/codex-switch login-official` only when you want to log in without
  switching or need to repair the stored official auth explicitly.
- Do not embed profile-specific model/provider/auth keys into live
  `~/.codex/config.toml`. Switching writes the selected profile layer to
  `<profile>.config.toml` and keeps live `config.toml` as a shared base.
- Do not reintroduce `[profiles.<name>]` or top-level `profile = "<name>"`.
- Already-running Codex Desktop processes may need a restart after App CLI
  binding changes.

## Validation

```bash
python3 -m py_compile scripts/*.py
python3 scripts/test_codex_profile_switch.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
python3 -m json.tool evals/evals.json >/dev/null
```

For isolated runtime validation:

```bash
tmp="$(mktemp -d)"
mkdir -p "$tmp/live"
printf '[features]\nhooks = true\n' > "$tmp/live/config.toml"
scripts/codex-switch \
  --store-dir "$tmp/store" \
  --live-codex-home "$tmp/live" \
  --launch-agent-path "$tmp/agent.plist" \
  init --codex-bin /bin/echo --app-cli-path /bin/echo
scripts/codex-switch \
  --store-dir "$tmp/store" \
  --live-codex-home "$tmp/live" \
  --launch-agent-path "$tmp/agent.plist" \
  switch openai-official --dry-run
scripts/codex-switch \
  --store-dir "$tmp/store" \
  --live-codex-home "$tmp/live" \
  --launch-agent-path "$tmp/agent.plist" \
  switch openai-official --skip-launchctl
scripts/codex-switch \
  --store-dir "$tmp/store" \
  --live-codex-home "$tmp/live" \
  --launch-agent-path "$tmp/agent.plist" \
  official --skip-launchctl --skip-doctor --no-status
scripts/codex-switch \
  --store-dir "$tmp/store" \
  --live-codex-home "$tmp/live" \
  --launch-agent-path "$tmp/agent.plist" \
  doctor
```
