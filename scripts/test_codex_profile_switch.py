#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import plistlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from codex_switch_running_app import (
    RunningCodexProcess,
    parse_env_app_cli_path,
    parse_ps_processes,
    running_desktop_problems,
)
from codex_switch_config import build_base_config_text, build_profile_v2_config_text
from codex_switch_store import Store


SCRIPT = Path(__file__).with_name("codex_profile_switch.py")
WRAPPER = Path(__file__).with_name("codex-switch")


def write_fake_codex(path: Path, label: str) -> None:
    path.write_text(
        "#!/usr/bin/env sh\n"
        "if [ \"${1:-}\" = \"login\" ]; then\n"
        "  if grep -q '^profile = ' \"$CODEX_HOME/config.toml\" 2>/dev/null; then\n"
        "    echo legacy-profile-config >&2\n"
        "    exit 42\n"
        "  fi\n"
        "  mkdir -p \"$CODEX_HOME\"\n"
        "  printf '{\"fake\":\"auth\"}\\n' > \"$CODEX_HOME/auth.json\"\n"
        f"  echo {label}-login\n"
        "  exit 0\n"
        "fi\n"
        f"echo {label}\n"
    )
    path.chmod(0o755)


def write_fake_script(path: Path, body: str) -> None:
    path.write_text(body)
    path.chmod(0o755)


class CodexProfileSwitchTests(unittest.TestCase):
    def make_workspace(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        (root / "live").mkdir()
        (root / "live" / "config.toml").write_text(
            'profile = "internal"\n\n[profiles.internal]\n'
        )
        return temp_dir, root

    def run_switcher(
        self,
        root: Path,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(SCRIPT),
            "--store-dir",
            str(root / "store"),
            "--live-codex-home",
            str(root / "live"),
            "--launch-agent-path",
            str(root / "agent.plist"),
            *args,
        ]
        return subprocess.run(
            command,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

    def run_wrapper(
        self,
        root: Path,
        *args: str,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            str(WRAPPER),
            "--store-dir",
            str(root / "store"),
            "--live-codex-home",
            str(root / "live"),
            "--launch-agent-path",
            str(root / "agent.plist"),
            *args,
        ]
        clean_env = dict(env or os.environ)
        clean_env.pop("CODEX_CLI_PATH", None)
        clean_env.pop("CODEX_SWITCH_SCRIPT", None)
        clean_env.pop("CODEX_SWITCH_HOME", None)
        return subprocess.run(
            command,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=clean_env,
        )

    def prepare_profiles(self, root: Path) -> tuple[Path, Path, dict[str, str]]:
        path_dir = root / "path"
        path_dir.mkdir()
        internal = root / "internal-codex"
        official = root / "official-codex"
        write_fake_codex(internal, "internal-codex")
        write_fake_codex(official, "official-codex")
        (path_dir / "codex").symlink_to(internal)
        env = os.environ.copy()
        env.pop("CODEX_CLI_PATH", None)
        env["PATH"] = f"{path_dir}{os.pathsep}{env.get('PATH', '')}"
        return path_dir / "codex", official, env

    def read_manifest(self, root: Path, name: str) -> dict[str, str]:
        path = root / "store" / "profiles" / name / "manifest.json"
        return json.loads(path.read_text())

    def test_init_defaults_official_codex_bin_to_app_cli_not_path_codex(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)

            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            official = self.read_manifest(root, "openai-official")
            internal = self.read_manifest(root, "internal")
            self.assertEqual(official["codex_bin"], str(official_codex))
            self.assertEqual(official["app_cli_path"], str(official_codex))
            self.assertEqual(internal["codex_bin"], str(internal_codex))
            self.assertEqual(internal["app_cli_path"], str(internal_codex))

    def test_switch_updates_shim_and_app_cli_to_target_profile(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            self.run_switcher(root, "switch", "openai-official", "--skip-launchctl")
            shim = root / "store" / "bin" / "codex"
            self.assertIn(f'exec "{official_codex}" "$@"', shim.read_text())
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["app_cli_path"], str(official_codex))
            agent = plistlib.loads((root / "agent.plist").read_bytes())
            self.assertEqual(agent["ProgramArguments"][-1], str(official_codex))
            dirty_env = dict(env)
            dirty_env["CODEX_CLI_PATH"] = "/tmp/not-the-isolated-app-cli"
            self.run_switcher(root, "doctor", env=dirty_env)

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            self.assertIn(f'exec "{internal_codex}" "$@"', shim.read_text())
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["app_cli_path"], str(internal_codex))
            agent = plistlib.loads((root / "agent.plist").read_bytes())
            self.assertEqual(agent["ProgramArguments"][-1], str(internal_codex))

    def test_switch_writes_profile_v2_config_and_removes_non_file_auth(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            (root / "live" / "auth.json").write_text("{}\n")
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            (root / "live" / "internal.config.toml").write_text('model = "old-internal"\n')

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            live_config = (root / "live" / "config.toml").read_text()
            self.assertNotIn('profile = "internal"', live_config)
            self.assertNotIn("[profiles.internal]", live_config)
            self.assertTrue((root / "live" / "internal.config.toml").exists())
            self.assertFalse((root / "live" / "auth.json").exists())
            active = json.loads((root / "store" / "active.json").read_text())
            backup_dir = Path(active["backup_dir"])
            self.assertEqual(
                (backup_dir / "internal.config.toml").read_text(),
                'model = "old-internal"\n',
            )

    def test_switch_preserves_live_shared_preferences(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            (root / "live" / "config.toml").write_text(
                'model = "gpt-5.5-2026-04-24"\n'
                'model_provider = "azure"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
                "\n"
                "[tui]\n"
                'theme = "catppuccin-latte"\n'
            )
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            self.run_switcher(root, "switch", "openai-official", "--skip-launchctl")

            live_config = (root / "live" / "config.toml").read_text()
            self.assertNotIn('model = "gpt-5.5-2026-04-24"', live_config)
            self.assertNotIn('model_provider = "azure"', live_config)
            self.assertNotIn('cli_auth_credentials_store = "file"', live_config)
            self.assertIn("[features]", live_config)
            self.assertIn("memory = true", live_config)
            self.assertIn("[tui]", live_config)
            self.assertIn('theme = "catppuccin-latte"', live_config)
            profile_config = (root / "live" / "openai-official.config.toml").read_text()
            self.assertIn('cli_auth_credentials_store = "file"', profile_config)

    def test_profile_v2_config_flattens_legacy_profile_table(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            (root / "live" / "config.toml").write_text(
                'theme = "dark"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
            )
            profile_config = root / "profile.toml"
            profile_config.write_text(
                'profile = "internal"\n'
                'background_terminal_max_timeout = 10\n'
                "\n"
                "[profiles.internal]\n"
                'model = "gpt-5.5-2026-04-24"\n'
                'model_provider = "azure"\n'
                'model_catalog_json = "/Users/me/.codex/model-catalogs/azure-models.json"\n'
                "\n"
                "[model_providers.azure]\n"
                'name = "Azure"\n'
                "\n"
                "[model_providers.azure.query_params]\n"
                'api-version = "2025-03-01-preview"\n'
            )

            config = build_profile_v2_config_text("internal", profile_config)
            base = build_base_config_text(root / "live" / "config.toml")

            self.assertNotIn('profile = "internal"', config)
            self.assertNotIn("[profiles.internal]", config)
            self.assertIn('model = "gpt-5.5-2026-04-24"', config)
            self.assertIn('model_provider = "azure"', config)
            self.assertIn(
                'model_catalog_json = "/Users/me/.codex/model-catalogs/azure-models.json"',
                config,
            )
            self.assertIn("[model_providers.azure]", config)
            self.assertIn('name = "Azure"', config)
            self.assertIn("[model_providers.azure.query_params]", config)
            self.assertIn('api-version = "2025-03-01-preview"', config)
            self.assertIn('theme = "dark"', base)
            self.assertIn("[features]", base)
            self.assertIn("memory = true", base)

    def test_profile_v2_config_replaces_target_model_provider_table(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            (root / "live" / "config.toml").write_text(
                "[model_providers.azure]\n"
                'name = "Old Azure"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
            )
            profile_config = root / "profile.toml"
            profile_config.write_text(
                "[profiles.internal]\n"
                'model_provider = "azure"\n'
                "\n"
                "[model_providers.azure]\n"
                'name = "New Azure"\n'
            )

            config = build_profile_v2_config_text("internal", profile_config)

            self.assertIn('model_provider = "azure"', config)
            self.assertIn('name = "New Azure"', config)
            self.assertNotIn('name = "Old Azure"', config)

    def test_base_config_removes_profile_keys_and_profile_layer_keeps_target_keys(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            (root / "live" / "config.toml").write_text(
                'model = "gpt-5.5-2026-04-24"\n'
                'model_provider = "azure"\n'
                'model_catalog_json = "/Users/me/.codex/model-catalogs/azure-models.json"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
                "\n"
                "[tui]\n"
                'theme = "catppuccin-latte"\n'
            )
            profile_config = root / "profile.toml"
            profile_config.write_text(
                'profile = "openai-official"\n'
                'cli_auth_credentials_store = "file"\n'
                "\n"
                "[profiles.openai-official]\n"
            )

            config = build_base_config_text(root / "live" / "config.toml")
            profile_layer = build_profile_v2_config_text("openai-official", profile_config)

            self.assertNotIn('profile = "openai-official"', config)
            self.assertNotIn("[profiles.openai-official]", config)
            self.assertNotIn('model = "gpt-5.5-2026-04-24"', config)
            self.assertNotIn('model_provider = "azure"', config)
            self.assertNotIn("model_catalog_json", config)
            self.assertNotIn("model_catalog_json", profile_layer)
            self.assertIn('cli_auth_credentials_store = "file"', profile_layer)
            self.assertIn("[features]", config)
            self.assertIn("memory = true", config)
            self.assertIn("[tui]", config)
            self.assertIn('theme = "catppuccin-latte"', config)

    def test_snapshot_switch_preserves_live_plugin_and_skill_config(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            (root / "live" / "config.toml").write_text(
                'model = "gpt-5.5-2026-04-24"\n'
                "\n"
                "[marketplaces.local-personal-plugins]\n"
                'source_type = "local"\n'
                f'source = "{root / "personal-marketplace"}"\n'
                "\n"
                '[plugins."dev-flow@local-personal-plugins"]\n'
                "enabled = true\n"
                "\n"
                "[[skills.config]]\n"
                f'path = "{root / "skills" / "dev-flow" / "SKILL.md"}"\n'
                "\n"
                '[hooks.state."dev-flow@local-personal-plugins:hooks.json:stop:0:0"]\n'
                "enabled = true\n"
            )
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            self.run_switcher(
                root,
                "switch",
                "openai-official",
                "--config-mode",
                "snapshot",
                "--skip-launchctl",
            )

            live_config = (root / "live" / "config.toml").read_text()
            self.assertIn("[marketplaces.local-personal-plugins]", live_config)
            self.assertIn('[plugins."dev-flow@local-personal-plugins"]', live_config)
            self.assertIn("[[skills.config]]", live_config)
            self.assertIn(
                '[hooks.state."dev-flow@local-personal-plugins:hooks.json:stop:0:0"]',
                live_config,
            )
            self.assertNotIn('cli_auth_credentials_store = "file"', live_config)
            self.assertNotIn('model = "gpt-5.5-2026-04-24"', live_config)
            profile_config = (root / "live" / "openai-official.config.toml").read_text()
            self.assertIn('cli_auth_credentials_store = "file"', profile_config)

    def test_wrapper_one_key_official_checks_update_before_switch(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            result = self.run_wrapper(
                root,
                "official",
                "--skip-launchctl",
                "--skip-doctor",
                "--no-status",
                env=env,
            )

            output = result.stdout + result.stderr
            self.assertIn("Checking Codex CLI update for openai-official", output)
            self.assertIn(f"Official profile codex: {official_codex}", output)
            self.assertIn("Official login: missing", output)
            self.assertTrue(
                (root / "store" / "profiles" / "openai-official" / "auth.json").exists()
            )
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "openai-official")

    def test_wrapper_one_key_official_can_skip_auto_login(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            result = self.run_wrapper(
                root,
                "official",
                "--skip-login",
                "--skip-update-check",
                "--skip-launchctl",
                "--skip-doctor",
                "--no-status",
                env=env,
            )

            output = result.stdout + result.stderr
            self.assertNotIn("Official login: missing", output)
            self.assertFalse(
                (root / "store" / "profiles" / "openai-official" / "auth.json").exists()
            )
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "openai-official")

    def test_wrapper_one_key_can_skip_update_check(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            result = self.run_wrapper(
                root,
                "official",
                "--skip-launchctl",
                "--skip-update-check",
                "--skip-doctor",
                "--no-status",
                env=env,
            )

            output = result.stdout + result.stderr
            self.assertNotIn("Checking Codex CLI update", output)
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "openai-official")

    def test_wrapper_profile_dry_run_allows_empty_switch_args_on_bash_32(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            result = self.run_wrapper(
                root,
                "internal",
                "--dry-run",
                env=env,
                check=False,
            )

            output = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, output)
            self.assertIn("Outcome: DRY RUN OK", output)
            self.assertNotIn("unbound variable", output)

    def test_wrapper_prints_final_action_required_when_doctor_fails(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            manifest_path = root / "store" / "profiles" / "openai-official" / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["app_cli_path"] = str(root / "missing-app-cli")
            manifest_path.write_text(json.dumps(manifest))

            result = self.run_wrapper(
                root,
                "official",
                "--skip-login",
                "--skip-update-check",
                "--skip-shim",
                "--skip-app-cli",
                "--no-status",
                env=env,
                check=False,
            )

            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("== Final result ==", output)
            self.assertIn("Outcome: ACTION REQUIRED", output)
            self.assertIn("Switch: succeeded", output)
            self.assertIn("Doctor: failed", output)
            self.assertIn("Next steps:", output)
            self.assertIn("Re-run doctor: codex-switch doctor", output)
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "openai-official")

    def test_wrapper_internal_update_check_failure_does_not_block_switch(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            env["CODEX_SWITCH_INTERNAL_LATEST_URL"] = "http://127.0.0.1:1/latest"
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            result = self.run_wrapper(
                root,
                "internal",
                "--skip-launchctl",
                "--skip-doctor",
                "--no-status",
                env=env,
            )

            output = result.stdout + result.stderr
            self.assertIn("Checking Codex CLI update for internal", output)
            self.assertIn(f"Internal profile codex: {internal_codex}", output)
            self.assertIn(
                "Update check did not complete; continuing with switch.",
                output,
            )
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "internal")

    def test_wrapper_internal_auto_updates_when_latest_differs(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            write_fake_codex(root / "internal-codex", "codex-cli 1.0.0")
            fake_tools = root / "fake-tools"
            fake_tools.mkdir()
            update_args = root / "update-args.txt"
            write_fake_script(
                fake_tools / "curl",
                "#!/usr/bin/env sh\n"
                "cat <<'EOF'\n"
                "HTTP/2 302\n"
                "location: https://github.com/SDGLBL/codex/releases/tag/internal-rust-v9.9.9\n"
                "EOF\n",
            )
            write_fake_script(
                fake_tools / "codex-env-setup",
                "#!/usr/bin/env sh\n"
                f"printf '%s\\n' \"$*\" > {update_args}\n"
                "exit 0\n",
            )
            env["PATH"] = f"{fake_tools}{os.pathsep}{env.get('PATH', '')}"
            env["CODEX_SWITCH_ENV_SETUP"] = str(fake_tools / "codex-env-setup")
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            check_result = self.run_wrapper(root, "check-update", "internal", env=env)
            check_output = check_result.stdout + check_result.stderr
            self.assertIn("Update: available", check_output)
            self.assertFalse(update_args.exists())

            result = self.run_wrapper(
                root,
                "internal",
                "--skip-launchctl",
                "--skip-doctor",
                "--no-status",
                env=env,
            )

            output = result.stdout + result.stderr
            self.assertIn("Auto-update: internal Codex update detected.", output)
            self.assertIn("Auto-update: running codex-switch update-internal", output)
            self.assertEqual(
                update_args.read_text().strip(),
                f"update-internal --install-dir {internal_codex.parent}",
            )
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "internal")

    def test_parse_running_processes_ignores_headers_and_bad_lines(self) -> None:
        output = """
          PID ARGS
        123 /Applications/Codex.app/Contents/MacOS/Codex
        nope
        456 /Users/cY/.local/bin/codex app-server --analytics-default-enabled
        """

        self.assertEqual(
            parse_ps_processes(output),
            [
                (123, "/Applications/Codex.app/Contents/MacOS/Codex"),
                (456, "/Users/cY/.local/bin/codex app-server --analytics-default-enabled"),
            ],
        )

    def test_parse_env_app_cli_path_only_extracts_safe_value(self) -> None:
        output = (
            "PID COMMAND SECRET_TOKEN=should-not-print "
            "CODEX_CLI_PATH=/Users/cY/.local/bin/codex OTHER=value"
        )

        self.assertEqual(parse_env_app_cli_path(output), "/Users/cY/.local/bin/codex")

    def test_running_desktop_problem_reports_stale_app_server(self) -> None:
        store = Store(
            root=Path("/tmp/store"),
            live_codex_home=Path("/tmp/live"),
            launch_agent_path=Path("/tmp/agent.plist"),
            launch_agent_label="test",
        )
        observations = [
            RunningCodexProcess(
                pid=42,
                kind="app-server",
                command_path="/Applications/Codex.app/Contents/Resources/codex",
                app_cli_env="/Applications/Codex.app/Contents/Resources/codex",
            )
        ]

        problems = running_desktop_problems(
            store,
            active_profile="internal",
            expected_app_cli="/Users/cY/.local/bin/codex",
            observations=observations,
            enforce_default_context=False,
        )

        self.assertEqual(len(problems), 1)
        self.assertIn("running Codex app-server pid 42 uses", problems[0])


if __name__ == "__main__":
    unittest.main()
