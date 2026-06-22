#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import plistlib
import shutil
import tarfile
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from codex_switch_running_app import (
    RunningCodexProcess,
    app_server_command_path,
    parse_env_app_cli_path,
    parse_ps_processes,
    running_desktop_problems,
)
from codex_switch_app_proxy import (
    mask_backend_message_for_desktop,
    translate_desktop_message_for_backend,
)
from codex_switch_config import build_base_config_text, build_profile_v2_config_text
from codex_switch_home_sync import refresh_profile_canonical_config, sync_shared_support
from codex_switch_store import Store


SCRIPT = Path(__file__).with_name("codex_profile_switch.py")
WRAPPER = Path(__file__).with_name("codex-switch")
INSTALLER = Path(__file__).parents[1] / "install.sh"
REMOTE_RUNNER = Path(__file__).parents[1] / "run.sh"
RELEASE_WORKFLOW = Path(__file__).parents[1] / ".github" / "workflows" / "release.yml"
AUTO_RELEASE_WORKFLOW = (
    Path(__file__).parents[1] / ".github" / "workflows" / "auto-release.yml"
)
RELEASE_AUTO = Path(__file__).with_name("release_auto.py")


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
        check: bool = True,
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
            check=check,
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

    def make_installed_wrapper(self, root: Path, version: str = "0.1.1") -> Path:
        current = root / "lib" / "current"
        scripts_dir = current / "scripts"
        scripts_dir.mkdir(parents=True)
        shutil.copy2(WRAPPER, scripts_dir / "codex-switch")
        (scripts_dir / "codex-switch").chmod(0o755)
        (current / "VERSION").write_text(f"{version}\n")
        fake_switcher = scripts_dir / "codex_profile_switch.py"
        fake_switcher.write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "print('old-switcher:' + ' '.join(sys.argv[1:]))\n"
        )
        fake_switcher.chmod(0o755)
        return scripts_dir / "codex-switch"

    def make_remote_wrapper_tarball(self, root: Path, version: str = "9.9.9") -> Path:
        release_root = root / "remote-release" / "codex-switch"
        scripts_dir = release_root / "scripts"
        scripts_dir.mkdir(parents=True)
        fake_wrapper = scripts_dir / "codex-switch"
        fake_wrapper.write_text(
            "#!/usr/bin/env sh\n"
            "printf 'synced-wrapper:%s\\n' \"$*\"\n"
            "printf 'skip-self-update:%s\\n' \"${CODEX_SWITCH_SKIP_SELF_UPDATE:-}\"\n"
        )
        fake_wrapper.chmod(0o755)
        (release_root / "VERSION").write_text(f"{version}\n")
        tarball = root / "remote-codex-switch.tar.gz"
        with tarfile.open(tarball, "w:gz") as archive:
            archive.add(release_root, arcname="codex-switch")
        return tarball

    def make_source_archive(self, root: Path, version: str = "9.9.9") -> Path:
        source_root = root / "source-release" / f"codex-switch-{version}"
        scripts_dir = source_root / "scripts"
        scripts_dir.mkdir(parents=True)
        (source_root / "README.md").write_text("source archive\n")
        (source_root / "SKILL.md").write_text("source archive\n")
        (source_root / "VERSION").write_text(f"{version}\n")
        raw_wrapper = scripts_dir / "codex-switch"
        raw_wrapper.write_text(
            "#!/usr/bin/env sh\n"
            "printf 'raw-source:%s\\n' \"$*\"\n"
        )
        raw_wrapper.chmod(0o755)
        package_script = scripts_dir / "package-release.sh"
        package_script.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            'out="${CODEX_SWITCH_DIST_DIR:-$PWD/dist}"\n'
            'pkg="$out/codex-switch"\n'
            'rm -rf "$pkg"\n'
            'mkdir -p "$pkg/scripts"\n'
            f"printf '{version}\\n' > \"$pkg/VERSION\"\n"
            "cat > \"$pkg/scripts/codex-switch\" <<'SH'\n"
            "#!/usr/bin/env sh\n"
            "printf 'packaged-source:%s\\n' \"$*\"\n"
            "printf 'skip-self-update:%s\\n' \"${CODEX_SWITCH_SKIP_SELF_UPDATE:-}\"\n"
            "SH\n"
            'chmod +x "$pkg/scripts/codex-switch"\n'
            'echo "$out/codex-switch.tar.gz"\n'
        )
        package_script.chmod(0o755)
        tarball = root / "source-codex-switch.tar.gz"
        with tarfile.open(tarball, "w:gz") as archive:
            archive.add(source_root, arcname=f"codex-switch-{version}")
        return tarball

    def init_release_repo(self, root: Path, version: str = "0.1.3") -> Path:
        repo = root / "release-repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
        (repo / "scripts").mkdir()
        (repo / "scripts" / "codex-switch").write_text("#!/usr/bin/env sh\necho old\n")
        (repo / "scripts" / "codex-switch").chmod(0o755)
        (repo / "VERSION").write_text(f"{version}\n")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial release"], cwd=repo, check=True)
        subprocess.run(["git", "tag", f"v{version}"], cwd=repo, check=True)
        return repo

    def run_release_auto(
        self,
        repo: Path,
        *args: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(RELEASE_AUTO), "--repo", str(repo), *args],
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def release_plan(self, repo: Path) -> dict[str, object]:
        result = self.run_release_auto(repo, "plan", "--json")
        return json.loads(result.stdout)

    def self_update_env(self, root: Path, tarball: Path) -> dict[str, str]:
        env = os.environ.copy()
        env["CODEX_SWITCH_LIB_DIR"] = str(root / "lib")
        env["CODEX_SWITCH_TARBALL_URL"] = tarball.as_uri()
        env["CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS"] = "0"
        return env

    def test_remote_runner_downloads_release_and_execs_command(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            release_root = root / "release" / "codex-switch"
            scripts_dir = release_root / "scripts"
            scripts_dir.mkdir(parents=True)
            fake_wrapper = scripts_dir / "codex-switch"
            fake_wrapper.write_text(
                "#!/usr/bin/env sh\n"
                "printf 'fake-codex-switch:%s\\n' \"$*\"\n"
                "printf 'skip-self-update:%s\\n' \"${CODEX_SWITCH_SKIP_SELF_UPDATE:-}\"\n"
                "printf 'script-dir:%s\\n' \"$(cd -- \"$(dirname -- \"$0\")\" && pwd)\"\n"
            )
            fake_wrapper.chmod(0o755)
            tarball = root / "codex-switch.tar.gz"
            with tarfile.open(tarball, "w:gz") as archive:
                archive.add(release_root, arcname="codex-switch")

            install_dir = root / "bin"
            lib_dir = root / "lib"
            env = os.environ.copy()
            env["CODEX_SWITCH_TARBALL_URL"] = tarball.as_uri()
            env["CODEX_SWITCH_INSTALL_DIR"] = str(install_dir)
            env["CODEX_SWITCH_LIB_DIR"] = str(lib_dir)

            result = subprocess.run(
                [str(REMOTE_RUNNER), "status", "--verbose"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("fake-codex-switch:status --verbose", result.stdout)
            self.assertIn("skip-self-update:1", result.stdout)
            self.assertIn(f"script-dir:{lib_dir / 'current' / 'scripts'}", result.stdout)
            self.assertTrue((lib_dir / "current" / "scripts" / "codex-switch").exists())
            self.assertFalse((install_dir / "codex-switch").exists())

    def test_installer_falls_back_to_source_archive_and_installs_path_command(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            source_archive = self.make_source_archive(root)
            install_dir = root / "bin"
            lib_dir = root / "lib"
            missing_tarball = root / "missing-codex-switch.tar.gz"
            env = os.environ.copy()
            env["CODEX_SWITCH_TARBALL_URL"] = missing_tarball.as_uri()
            env["CODEX_SWITCH_SOURCE_TARBALL_URL"] = source_archive.as_uri()
            env["CODEX_SWITCH_INSTALL_DIR"] = str(install_dir)
            env["CODEX_SWITCH_LIB_DIR"] = str(lib_dir)

            subprocess.run(
                [str(INSTALLER)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            result = subprocess.run(
                [str(install_dir / "codex-switch"), "status", "--verbose"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("packaged-source:status --verbose", result.stdout)
            self.assertEqual("9.9.9\n", (lib_dir / "current" / "VERSION").read_text())
            self.assertTrue((install_dir / "codex-switch").exists())

    def test_remote_runner_falls_back_to_source_archive_and_execs_command(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            source_archive = self.make_source_archive(root)
            install_dir = root / "bin"
            lib_dir = root / "lib"
            missing_tarball = root / "missing-codex-switch.tar.gz"
            env = os.environ.copy()
            env["CODEX_SWITCH_TARBALL_URL"] = missing_tarball.as_uri()
            env["CODEX_SWITCH_SOURCE_TARBALL_URL"] = source_archive.as_uri()
            env["CODEX_SWITCH_INSTALL_DIR"] = str(install_dir)
            env["CODEX_SWITCH_LIB_DIR"] = str(lib_dir)

            result = subprocess.run(
                [str(REMOTE_RUNNER), "status", "--verbose"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("packaged-source:status --verbose", result.stdout)
            self.assertIn("skip-self-update:1", result.stdout)
            self.assertEqual("9.9.9\n", (lib_dir / "current" / "VERSION").read_text())
            self.assertFalse((install_dir / "codex-switch").exists())

    def test_local_wrapper_self_updates_release_install_before_command(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            local_wrapper = self.make_installed_wrapper(root)
            tarball = self.make_remote_wrapper_tarball(root)
            env = self.self_update_env(root, tarball)

            result = subprocess.run(
                [str(local_wrapper), "status", "--verbose"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("synced-wrapper:status --verbose", result.stdout)
            self.assertIn("codex-switch self-update: checking latest release", result.stderr)
            self.assertIn(
                "codex-switch self-update: synced implementation 0.1.1 -> 9.9.9",
                result.stderr,
            )
            self.assertEqual("9.9.9\n", (root / "lib" / "current" / "VERSION").read_text())

    def test_local_wrapper_self_update_reports_already_up_to_date(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            local_wrapper = self.make_installed_wrapper(root, version="9.9.9")
            tarball = self.make_remote_wrapper_tarball(root, version="9.9.9")
            env = self.self_update_env(root, tarball)

            result = subprocess.run(
                [str(local_wrapper), "status"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("old-switcher:status", result.stdout)
            self.assertIn("codex-switch self-update: checking latest release", result.stderr)
            self.assertIn(
                "codex-switch self-update: already up to date 9.9.9",
                result.stderr,
            )
            self.assertEqual("9.9.9\n", (root / "lib" / "current" / "VERSION").read_text())

    def test_local_wrapper_skip_self_update_keeps_existing_install(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            local_wrapper = self.make_installed_wrapper(root)
            tarball = self.make_remote_wrapper_tarball(root)
            env = self.self_update_env(root, tarball)

            result = subprocess.run(
                [str(local_wrapper), "--skip-self-update", "status"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("old-switcher:status", result.stdout)
            self.assertNotIn("self-update", result.stderr)
            self.assertEqual("0.1.1\n", (root / "lib" / "current" / "VERSION").read_text())

    def test_source_checkout_wrapper_does_not_self_update(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            fake_switcher = root / "fake_switcher.py"
            fake_switcher.write_text(
                "#!/usr/bin/env python3\n"
                "import sys\n"
                "print('source-switcher:' + ' '.join(sys.argv[1:]))\n"
            )
            fake_switcher.chmod(0o755)
            tarball = self.make_remote_wrapper_tarball(root)
            env = self.self_update_env(root, tarball)
            env["CODEX_SWITCH_SCRIPT"] = str(fake_switcher)

            result = subprocess.run(
                [str(WRAPPER), "status"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("source-switcher:status", result.stdout)
            self.assertFalse((root / "lib" / "current" / "VERSION").exists())

    def test_self_update_failure_does_not_block_local_command(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            local_wrapper = self.make_installed_wrapper(root)
            env = self.self_update_env(root, root / "missing-release.tar.gz")

            result = subprocess.run(
                [str(local_wrapper), "status"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("old-switcher:status", result.stdout)
            self.assertIn("sync failed; continuing", result.stderr)
            self.assertEqual("0.1.1\n", (root / "lib" / "current" / "VERSION").read_text())

    def test_local_wrapper_self_update_falls_back_to_source_archive(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            local_wrapper = self.make_installed_wrapper(root)
            source_archive = self.make_source_archive(root)
            env = self.self_update_env(root, root / "missing-release.tar.gz")
            env["CODEX_SWITCH_SOURCE_TARBALL_URL"] = source_archive.as_uri()

            result = subprocess.run(
                [str(local_wrapper), "status", "--verbose"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("packaged-source:status --verbose", result.stdout)
            self.assertEqual("9.9.9\n", (root / "lib" / "current" / "VERSION").read_text())

    def test_release_workflow_uploads_required_assets(self) -> None:
        workflow = RELEASE_WORKFLOW.read_text()

        self.assertIn("contents: write", workflow)
        self.assertIn("@fission-ai/openspec@1.3.1", workflow)
        self.assertIn("scripts/package-release.sh", workflow)
        self.assertIn("gh release upload", workflow)
        self.assertIn("--clobber", workflow)
        self.assertIn("install.sh", workflow)
        self.assertIn("dist/run.sh", workflow)
        self.assertIn("dist/codex-switch.tar.gz", workflow)

    def test_auto_release_plan_detects_runtime_change_and_next_patch_tag(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        with temp_dir:
            repo = self.init_release_repo(root)
            (repo / "scripts" / "codex-switch").write_text(
                "#!/usr/bin/env sh\necho changed\n"
            )
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "feat: change runtime"],
                cwd=repo,
                check=True,
            )

            plan = self.release_plan(repo)

        self.assertTrue(plan["release_required"])
        self.assertEqual(plan["latest_tag"], "v0.1.3")
        self.assertEqual(plan["next_tag"], "v0.1.4")
        self.assertEqual(plan["next_version"], "0.1.4")
        self.assertIn("scripts/codex-switch", plan["release_relevant_files"])

    def test_auto_release_plan_skips_planning_only_changes(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        with temp_dir:
            repo = self.init_release_repo(root)
            planning = repo / ".planning" / "verification"
            planning.mkdir(parents=True)
            (planning / "note.md").write_text("verified\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "docs: record verification"],
                cwd=repo,
                check=True,
            )

            plan = self.release_plan(repo)

        self.assertFalse(plan["release_required"])
        self.assertEqual(plan["latest_tag"], "v0.1.3")
        self.assertEqual(plan["next_tag"], "")
        self.assertEqual(plan["release_relevant_files"], [])

    def test_auto_release_bump_updates_version_for_tag(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        with temp_dir:
            repo = self.init_release_repo(root)

            self.run_release_auto(repo, "bump", "--tag", "v0.1.4")

            self.assertEqual((repo / "VERSION").read_text(), "0.1.4\n")

    def test_auto_release_workflow_creates_tag_and_release_assets(self) -> None:
        workflow = AUTO_RELEASE_WORKFLOW.read_text()

        self.assertIn("branches:", workflow)
        self.assertIn("- main", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("scripts/release_auto.py plan", workflow)
        self.assertIn("release_required", workflow)
        self.assertIn("scripts/release_auto.py bump --tag", workflow)
        self.assertIn('git tag "$NEXT_TAG"', workflow)
        self.assertIn('git push origin "HEAD:main" "refs/tags/$NEXT_TAG"', workflow)
        self.assertIn("scripts/package-release.sh", workflow)
        self.assertIn("gh release", workflow)
        self.assertIn("dist/run.sh", workflow)
        self.assertIn("dist/codex-switch.tar.gz", workflow)

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
            internal_app = root / "store" / "bin" / "codex-internal-app"
            self.assertEqual(active["app_cli_path"], str(internal_app))
            agent = plistlib.loads((root / "agent.plist").read_bytes())
            self.assertEqual(agent["ProgramArguments"][-1], str(internal_app))

    def test_internal_switch_uses_managed_home_and_backup_plan(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text(
                "[features]\n"
                "memory = true\n"
                "\n"
                "[mcp_servers.shared]\n"
                'command = "shared-mcp"\n'
            )
            (live_home / "auth.json").write_text('{"official":"auth"}\n')
            (live_home / "sessions").mkdir()
            (live_home / "history.jsonl").write_text("official history\n")
            (live_home / "stable-support").mkdir()
            (live_home / "stable-support" / "tool.json").write_text("{}\n")

            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            internal_profile_config = root / "store" / "profiles" / "internal" / "config.toml"
            internal_profile_config.write_text(
                'model = "internal-model"\n'
                'model_provider = "internal-provider"\n'
                "\n"
                "[model_providers.internal-provider]\n"
                'name = "Internal"\n'
            )

            dry_run = self.run_switcher(root, "switch", "internal", "--dry-run")
            dry_output = dry_run.stdout + dry_run.stderr
            self.assertIn("Backup plan:", dry_output)
            self.assertIn("Mutation plan:", dry_output)
            self.assertIn(str(root / "store" / "homes" / "internal"), dry_output)

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            internal_home = root / "store" / "homes" / "internal"
            internal_config = (internal_home / "config.toml").read_text()
            self.assertIn("[features]", internal_config)
            self.assertIn("[mcp_servers.shared]", internal_config)
            self.assertIn('model = "internal-model"', internal_config)
            self.assertFalse((internal_home / "auth.json").exists())
            self.assertFalse((internal_home / "sessions").exists())
            self.assertFalse((internal_home / "history.jsonl").exists())
            self.assertTrue((live_home / "auth.json").exists())

            shim = root / "store" / "bin" / "codex"
            shim_text = shim.read_text()
            self.assertIn(f'export CODEX_HOME="{internal_home}"', shim_text)
            self.assertIn(f'exec "{internal_codex}" "$@"', shim_text)
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "internal")
            self.assertEqual(active["home_mode"], "managed")
            self.assertEqual(active["codex_home"], str(internal_home))
            self.assertTrue(active.get("backup_id"))
            backup_manifest = (
                root / "store" / "backups" / active["backup_id"] / "backup.json"
            )
            self.assertTrue(backup_manifest.exists())
            backup = json.loads(backup_manifest.read_text())
            self.assertEqual(backup["operation"], "switch")
            self.assertEqual(backup["to_profile"], "internal")

    def test_official_switch_syncs_shared_state_back_without_internal_runtime(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text("[features]\nmemory = true\n")
            (live_home / "auth.json").write_text('{"official":"auth"}\n')
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            (root / "store" / "profiles" / "internal" / "config.toml").write_text(
                'model = "internal-model"\n'
            )
            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            internal_home = root / "store" / "homes" / "internal"
            (internal_home / "config.toml").write_text(
                'notify = ["turn-ended"]\n'
                'model = "internal-runtime-model"\n'
                "\n"
                "[features]\n"
                "codex_hooks = true\n"
                "\n"
                "[mcp_servers.internal_shared]\n"
                'command = "internal-mcp"\n'
            )
            (internal_home / "auth.json").write_text('{"internal":"auth"}\n')
            (internal_home / "history.jsonl").write_text("internal history\n")

            self.run_switcher(
                root,
                "switch",
                "openai-official",
                "--skip-launchctl",
                "--skip-app-cli",
                "--skip-shim",
            )

            official_config = (live_home / "config.toml").read_text()
            self.assertIn('notify = ["turn-ended"]', official_config)
            self.assertIn("[features]", official_config)
            self.assertIn("codex_hooks = true", official_config)
            self.assertIn("[mcp_servers.internal_shared]", official_config)
            self.assertNotIn("internal-runtime-model", official_config)
            self.assertEqual('{"official":"auth"}\n', (live_home / "auth.json").read_text())
            self.assertFalse((live_home / "history.jsonl").exists())
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "openai-official")
            self.assertEqual(active["home_mode"], "official")
            self.assertEqual(active["codex_home"], str(live_home))

    def test_official_switch_does_not_create_self_referential_rules_symlink(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text("[features]\nmemory = true\n")
            rules = live_home / "rules"
            rules.mkdir()
            (rules / "workflow.md").write_text("keep rules\n")
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            (root / "store" / "profiles" / "internal" / "config.toml").write_text(
                'model = "internal-model"\n'
            )

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            internal_rules = root / "store" / "homes" / "internal" / "rules"
            self.assertTrue(internal_rules.is_symlink())
            self.assertEqual(os.readlink(internal_rules), str(rules))

            self.run_switcher(
                root,
                "switch",
                "openai-official",
                "--skip-launchctl",
                "--skip-app-cli",
                "--skip-shim",
            )

            self.assertFalse(rules.is_symlink())
            self.assertEqual("keep rules\n", (rules / "workflow.md").read_text())

    def test_shared_support_sync_removes_target_home_symlink_instead_of_copying_loop(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            source_home = root / "source"
            target_home = root / "target"
            source_home.mkdir()
            target_home.mkdir()
            (target_home / "shared-tool").mkdir()
            (target_home / "shared-tool" / "state.json").write_text("{}\n")
            (source_home / "shared-tool").symlink_to(target_home / "shared-tool")
            (source_home / "shared-cache").symlink_to(target_home / "shared-cache")
            (target_home / "shared-cache").symlink_to(target_home / "shared-cache")

            mutated = sync_shared_support(source_home, target_home, prefer_link=False)

            self.assertIn(target_home / "shared-tool", mutated)
            self.assertFalse((target_home / "shared-tool").is_symlink())
            self.assertEqual("{}\n", (target_home / "shared-tool" / "state.json").read_text())
            self.assertIn(target_home / "shared-cache", mutated)
            self.assertFalse((target_home / "shared-cache").exists())
            self.assertFalse((target_home / "shared-cache").is_symlink())

    def test_shared_support_sync_does_not_propagate_source_self_symlink(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            source_home = root / "source"
            target_home = root / "target"
            source_home.mkdir()
            target_home.mkdir()
            (source_home / "prompts").symlink_to(source_home / "prompts")
            (source_home / "skills").symlink_to(source_home / "skills")
            (target_home / "skills").symlink_to(target_home / "skills")

            mutated = sync_shared_support(source_home, target_home, prefer_link=False)

            self.assertNotIn(target_home / "prompts", mutated)
            self.assertFalse((target_home / "prompts").exists())
            self.assertFalse((target_home / "prompts").is_symlink())
            self.assertIn(target_home / "skills", mutated)
            self.assertFalse((target_home / "skills").exists())
            self.assertFalse((target_home / "skills").is_symlink())

    def test_shared_support_directory_copy_skips_nested_target_home_symlinks(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            source_home = root / "source"
            target_home = root / "target"
            source_home.mkdir()
            target_home.mkdir()
            source_tool = source_home / "tool"
            source_tool.mkdir()
            (source_tool / "settings.json").write_text("{}\n")
            (source_tool / "nested-loop").symlink_to(
                target_home / "tool" / "nested-loop"
            )

            sync_shared_support(source_home, target_home, prefer_link=False)

            target_tool = target_home / "tool"
            self.assertTrue(target_tool.is_dir())
            self.assertEqual("{}\n", (target_tool / "settings.json").read_text())
            self.assertFalse((target_tool / "nested-loop").exists())
            self.assertFalse((target_tool / "nested-loop").is_symlink())

    def test_official_switch_excludes_bulky_support_state_from_sync_plan(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text("[features]\nmemory = true\n")
            for name in (
                "agent-kb",
                "plugins",
                "computer-use",
                "cache",
                "model-catalogs",
                "sqlite",
            ):
                directory = live_home / name
                directory.mkdir()
                (directory / "payload.txt").write_text(f"{name}\n")
            for name in (
                ".credentials.json",
                ".codex-global-state.json",
                "models_cache.json",
                "version.json",
            ):
                (live_home / name).write_text(f"{name}\n")
            (live_home / "stable-support").mkdir()
            (live_home / "stable-support" / "tool.json").write_text("{}\n")

            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            dry_run = self.run_switcher(
                root,
                "switch",
                "openai-official",
                "--internal-codex-home",
                str(live_home),
                "--dry-run",
            )
            dry_output = dry_run.stdout + dry_run.stderr
            self.assertIn(
                str(root / "store" / "homes" / "openai-official" / "stable-support"),
                dry_output,
            )
            for name in (
                "agent-kb",
                "plugins",
                "computer-use",
                "cache",
                "model-catalogs",
                "sqlite",
                ".credentials.json",
                ".codex-global-state.json",
                "models_cache.json",
                "version.json",
            ):
                self.assertNotIn(
                    str(root / "store" / "homes" / "openai-official" / name),
                    dry_output,
                )

            self.run_switcher(
                root,
                "switch",
                "openai-official",
                "--internal-codex-home",
                str(live_home),
                "--skip-launchctl",
                "--skip-app-cli",
                "--skip-shim",
            )

            official_home = root / "store" / "homes" / "openai-official"
            self.assertTrue((official_home / "stable-support" / "tool.json").exists())
            for name in (
                "agent-kb",
                "plugins",
                "computer-use",
                "cache",
                "model-catalogs",
                "sqlite",
                ".credentials.json",
                ".codex-global-state.json",
                "models_cache.json",
                "version.json",
            ):
                self.assertFalse((official_home / name).exists(), name)
            active = json.loads((root / "store" / "active.json").read_text())
            backup = json.loads(
                (
                    root / "store" / "backups" / active["backup_id"] / "backup.json"
                ).read_text()
            )
            backup_paths = {entry["path"] for entry in backup["entries"]}
            for name in (
                "agent-kb",
                "plugins",
                "computer-use",
                "cache",
                "model-catalogs",
                "sqlite",
                ".credentials.json",
                ".codex-global-state.json",
                "models_cache.json",
                "version.json",
            ):
                self.assertNotIn(str(official_home / name), backup_paths)

    def test_internal_switch_prefers_last_runtime_config_and_refreshes_canonical(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text("[features]\nmemory = true\n")
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            canonical = root / "store" / "profiles" / "internal" / "config.toml"
            canonical.write_text('model = "canonical-internal"\n')
            internal_home = root / "store" / "homes" / "internal"
            internal_home.mkdir(parents=True)
            (internal_home / "config.toml").write_text(
                'model = "runtime-internal"\n'
                'model_provider = "runtime-provider"\n'
                "\n"
                "[model_providers.runtime-provider]\n"
                'name = "Runtime Provider"\n'
            )

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            runtime_config = (internal_home / "config.toml").read_text()
            self.assertIn("# codex-switch: managed runtime config for profile internal", runtime_config)
            self.assertIn("# codex-switch: shared settings are merged from", runtime_config)
            self.assertIn("\n# codex-switch: profile-specific settings\n", runtime_config)
            self.assertIn("\n# codex-switch: shared settings\n", runtime_config)
            self.assertIn('model = "runtime-internal"', runtime_config)
            self.assertIn('model_provider = "runtime-provider"', runtime_config)
            self.assertIn("[model_providers.runtime-provider]", runtime_config)
            self.assertIn("[features]", runtime_config)
            canonical_config = canonical.read_text()
            self.assertIn("# codex-switch: canonical fallback config for profile internal", canonical_config)
            self.assertIn('model = "runtime-internal"', canonical_config)
            self.assertIn('model_provider = "runtime-provider"', canonical_config)
            self.assertNotIn("[features]", canonical_config)

    def test_internal_switch_falls_back_to_canonical_when_last_runtime_config_is_invalid(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text("[features]\nmemory = true\n")
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            canonical = root / "store" / "profiles" / "internal" / "config.toml"
            canonical.write_text('model = "canonical-internal"\n')
            internal_home = root / "store" / "homes" / "internal"
            internal_home.mkdir(parents=True)
            (internal_home / "config.toml").write_text("model = [\n")

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            runtime_config = (internal_home / "config.toml").read_text()
            self.assertIn('model = "canonical-internal"', runtime_config)
            self.assertIn("[features]", runtime_config)
            self.assertIn("# codex-switch: profile-specific settings are preserved from fallback", runtime_config)

    def test_internal_switch_falls_back_when_runtime_reasoning_effort_is_unsupported(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text("[features]\nmemory = true\n")
            catalog = root / "azure-models.json"
            catalog.write_text(
                json.dumps(
                    {
                        "models": [
                            {
                                "slug": "gpt-5.5-2026-04-24",
                                "default_reasoning_level": "xhigh",
                                "supported_reasoning_levels": [
                                    {"effort": "low"},
                                    {"effort": "medium"},
                                    {"effort": "high"},
                                    {"effort": "xhigh"},
                                ],
                            }
                        ]
                    }
                )
                + "\n"
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
            canonical = root / "store" / "profiles" / "internal" / "config.toml"
            canonical.write_text(
                'model = "gpt-5.5-2026-04-24"\n'
                f'model_catalog_json = "{catalog}"\n'
                'model_reasoning_effort = "xhigh"\n'
            )
            internal_home = root / "store" / "homes" / "internal"
            internal_home.mkdir(parents=True)
            (internal_home / "config.toml").write_text(
                'model = "gpt-5.5-2026-04-24"\n'
                f'model_catalog_json = "{catalog}"\n'
                'model_reasoning_effort = "max"\n'
            )

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            runtime_config = (internal_home / "config.toml").read_text()
            canonical_config = canonical.read_text()
            self.assertIn('model_reasoning_effort = "xhigh"', runtime_config)
            self.assertIn('model_reasoning_effort = "xhigh"', canonical_config)
            self.assertNotIn('model_reasoning_effort = "max"', runtime_config)
            self.assertNotIn('model_reasoning_effort = "max"', canonical_config)
            self.assertIn("# codex-switch: profile-specific settings are preserved from fallback", runtime_config)

    def test_desktop_app_proxy_masks_versioned_model_alias_without_max_effort(self) -> None:
        actual_model = "gpt-5.5-2026-04-24"
        desktop_model = "gpt-5.5"
        message = {
            "id": 2,
            "result": {
                "data": [
                    {
                        "id": actual_model,
                        "model": actual_model,
                        "displayName": "Azure / GPT-5.5 2026-04-24",
                        "hidden": False,
                        "isDefault": True,
                        "defaultReasoningEffort": "xhigh",
                        "supportedReasoningEfforts": [
                            {"reasoningEffort": "low", "description": "low effort"},
                            {"reasoningEffort": "medium", "description": "medium effort"},
                            {"reasoningEffort": "high", "description": "high effort"},
                            {"reasoningEffort": "xhigh", "description": "xhigh effort"},
                        ],
                    }
                ]
            },
        }

        masked = mask_backend_message_for_desktop(
            message,
            method="model/list",
            actual_model=actual_model,
            desktop_model=desktop_model,
        )

        [model] = masked["result"]["data"]
        self.assertEqual(model["id"], desktop_model)
        self.assertEqual(model["model"], desktop_model)
        self.assertEqual(model["defaultReasoningEffort"], "xhigh")
        self.assertEqual(
            [effort["reasoningEffort"] for effort in model["supportedReasoningEfforts"]],
            ["low", "medium", "high", "xhigh"],
        )

    def test_desktop_app_proxy_masks_thread_model_fields_for_reasoning_lookup(self) -> None:
        actual_model = "gpt-5.5-2026-04-24"
        desktop_model = "gpt-5.5"
        message = {
            "id": 4,
            "result": {
                "conversation": {
                    "model": actual_model,
                    "latestModel": actual_model,
                    "previousTurnModel": actual_model,
                    "settings": {
                        "model": actual_model,
                        "reasoning_effort": "xhigh",
                    },
                },
                "writes": [
                    {"key": "model", "value": actual_model},
                ],
            },
        }

        masked = mask_backend_message_for_desktop(
            message,
            method="thread/load",
            actual_model=actual_model,
            desktop_model=desktop_model,
        )

        conversation = masked["result"]["conversation"]
        self.assertEqual(conversation["model"], desktop_model)
        self.assertEqual(conversation["latestModel"], desktop_model)
        self.assertEqual(conversation["previousTurnModel"], desktop_model)
        self.assertEqual(conversation["settings"]["model"], desktop_model)
        self.assertEqual(masked["result"]["writes"][0]["value"], desktop_model)
        self.assertEqual(message["result"]["conversation"]["latestModel"], actual_model)

    def test_desktop_app_proxy_translates_desktop_model_alias_for_backend(self) -> None:
        actual_model = "gpt-5.5-2026-04-24"
        desktop_model = "gpt-5.5"
        message = {
            "id": 9,
            "method": "thread/start",
            "params": {
                "model": desktop_model,
                "threadSettings": {
                    "model": desktop_model,
                    "reasoning_effort": "xhigh",
                },
                "writes": [
                    {"key": "model", "value": desktop_model},
                    {"key": "model_reasoning_effort", "value": "xhigh"},
                ],
            },
        }

        translated = translate_desktop_message_for_backend(
            message,
            actual_model=actual_model,
            desktop_model=desktop_model,
        )

        self.assertEqual(translated["params"]["model"], actual_model)
        self.assertEqual(translated["params"]["threadSettings"]["model"], actual_model)
        self.assertEqual(translated["params"]["writes"][0]["value"], actual_model)
        self.assertEqual(message["params"]["model"], desktop_model)

    def test_desktop_app_proxy_flattens_namespace_dynamic_tools_for_older_backend(self) -> None:
        actual_model = "gpt-5.5-2026-04-24"
        desktop_model = "gpt-5.5"
        message = {
            "id": 10,
            "method": "thread/start",
            "params": {
                "model": desktop_model,
                "dynamicTools": [
                    {
                        "type": "namespace",
                        "name": "tool_search",
                        "description": "Search available tools.",
                        "tools": [
                            {
                                "type": "function",
                                "name": "search",
                                "description": "Search tool catalog.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"query": {"type": "string"}},
                                },
                                "deferLoading": True,
                            }
                        ],
                    },
                    {
                        "type": "function",
                        "name": "read_file",
                        "description": "Read a file.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"path": {"type": "string"}},
                        },
                    },
                ],
            },
        }

        translated = translate_desktop_message_for_backend(
            message,
            actual_model=actual_model,
            desktop_model=desktop_model,
        )

        self.assertEqual(
            translated["params"]["dynamicTools"],
            [
                {
                    "namespace": "tool_search",
                    "type": "function",
                    "name": "search",
                    "description": "Search tool catalog.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                    },
                    "deferLoading": True,
                },
                {
                    "type": "function",
                    "name": "read_file",
                    "description": "Read a file.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                    },
                },
            ],
        )
        self.assertEqual(translated["params"]["model"], actual_model)
        self.assertEqual(message["params"]["dynamicTools"][0]["type"], "namespace")

    def test_desktop_app_proxy_filters_unsupported_plugin_marketplace_kind(self) -> None:
        actual_model = "gpt-5.5-2026-04-24"
        desktop_model = "gpt-5.5"
        message = {
            "id": 11,
            "method": "plugin/list",
            "params": {
                "marketplaceKinds": [
                    "local",
                    "created-by-me-remote",
                    "shared-with-me",
                ],
                "cwds": ["/Users/cY/dev/codex-switch"],
            },
        }

        translated = translate_desktop_message_for_backend(
            message,
            actual_model=actual_model,
            desktop_model=desktop_model,
        )

        self.assertEqual(
            translated["params"]["marketplaceKinds"],
            ["local", "shared-with-me"],
        )
        self.assertEqual(
            message["params"]["marketplaceKinds"],
            ["local", "created-by-me-remote", "shared-with-me"],
        )

    def test_canonical_refresh_does_not_resurrect_removed_profile_settings(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            runtime_config = root / "runtime.toml"
            canonical_config = root / "canonical.toml"
            runtime_config.write_text('model = "runtime-model"\n')
            canonical_config.write_text(
                'cli_auth_credentials_store = "file"\n'
                'model = "old-model"\n'
                'model_provider = "old-provider"\n'
                'personality = "pragmatic"\n'
                "\n"
                "[model_providers.old-provider]\n"
                'name = "Old Provider"\n'
            )

            refresh_profile_canonical_config(
                "openai-official",
                runtime_config,
                canonical_config,
            )

            canonical_text = canonical_config.read_text()
            self.assertIn('cli_auth_credentials_store = "file"', canonical_text)
            self.assertIn('model = "runtime-model"', canonical_text)
            self.assertNotIn("old-provider", canonical_text)
            self.assertNotIn('personality = "pragmatic"', canonical_text)

    def test_official_switch_preserves_last_official_runtime_profile_settings(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text(
                'model = "official-runtime"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
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
            (root / "store" / "profiles" / "internal" / "config.toml").write_text(
                'model = "internal-model"\n'
            )
            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            internal_home = root / "store" / "homes" / "internal"
            (internal_home / "config.toml").write_text(
                (internal_home / "config.toml").read_text()
                + "\n[mcp_servers.from-internal]\n"
                + 'command = "internal-mcp"\n'
            )

            self.run_switcher(root, "switch", "openai-official", "--skip-launchctl")

            official_config = (live_home / "config.toml").read_text()
            self.assertIn('model = "official-runtime"', official_config)
            self.assertIn("[mcp_servers.from-internal]", official_config)
            self.assertIn("# codex-switch: managed runtime config for profile openai-official", official_config)
            self.assertIn("\n# codex-switch: profile-specific settings\n", official_config)
            self.assertIn("\n# codex-switch: shared settings\n", official_config)
            canonical_config = (
                root / "store" / "profiles" / "openai-official" / "config.toml"
            ).read_text()
            self.assertIn("# codex-switch: canonical fallback config for profile openai-official", canonical_config)
            self.assertIn('model = "official-runtime"', canonical_config)
            self.assertNotIn("[mcp_servers.from-internal]", canonical_config)

    def test_internal_switch_can_adopt_live_home_and_move_official_home(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text(
                'model = "legacy-internal-runtime"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
            )
            (live_home / "sessions").mkdir()
            (live_home / "history.jsonl").write_text("legacy internal history\n")
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
                "internal",
                "--internal-codex-home",
                str(live_home),
                "--skip-launchctl",
            )

            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "internal")
            self.assertEqual(active["codex_home"], str(live_home))
            self.assertEqual(active["home_mode"], "adopted")
            self.assertEqual("legacy internal history\n", (live_home / "history.jsonl").read_text())
            internal_manifest = self.read_manifest(root, "internal")
            official_manifest = self.read_manifest(root, "openai-official")
            official_home = root / "store" / "homes" / "openai-official"
            self.assertEqual(internal_manifest["codex_home"], str(live_home))
            self.assertEqual(internal_manifest["home_mode"], "adopted")
            self.assertEqual(official_manifest["codex_home"], str(official_home))
            self.assertEqual(official_manifest["home_mode"], "managed")

            shim = root / "store" / "bin" / "codex"
            self.assertIn(f'export CODEX_HOME="{live_home}"', shim.read_text())
            self.assertIn(f'exec "{internal_codex}" "$@"', shim.read_text())

            self.run_switcher(root, "switch", "openai-official", "--skip-launchctl")

            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "openai-official")
            self.assertEqual(active["codex_home"], str(official_home))
            self.assertEqual(active["home_mode"], "managed")
            self.assertTrue((official_home / "config.toml").exists())
            self.assertEqual("legacy internal history\n", (live_home / "history.jsonl").read_text())
            self.assertFalse((official_home / "history.jsonl").exists())

    def test_switch_rejects_explicit_identical_independent_homes(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--store-dir",
                    str(root / "store"),
                    "--official-codex-home",
                    str(live_home),
                    "--internal-codex-home",
                    str(live_home),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "switch",
                    "internal",
                    "--skip-launchctl",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to use the same Codex home", result.stderr)
            self.assertFalse((root / "store" / "active.json").exists())

    def test_wrapper_forwards_internal_codex_home_option(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            fake_switcher = root / "fake_switcher.py"
            fake_switcher.write_text(
                "#!/usr/bin/env python3\n"
                "import sys\n"
                "print('ARGS:' + ' '.join(sys.argv[1:]))\n"
            )
            fake_switcher.chmod(0o755)
            adopted_home = root / "live"
            env = os.environ.copy()
            env["CODEX_SWITCH_SCRIPT"] = str(fake_switcher)
            env["CODEX_SWITCH_SKIP_SELF_UPDATE"] = "1"

            result = subprocess.run(
                [
                    str(WRAPPER),
                    "--store-dir",
                    str(root / "store"),
                    "--live-codex-home",
                    str(root / "live"),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "internal",
                    "--internal-codex-home",
                    str(adopted_home),
                    "--dry-run",
                    "--skip-update-check",
                    "--skip-login",
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn(f"--internal-codex-home {adopted_home}", result.stdout)

    def test_interactive_home_prompt_prioritizes_target_profile_and_recommended_option(self) -> None:
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
            prompt_env = dict(env)
            prompt_env["CODEX_SWITCH_FORCE_HOME_PROMPT"] = "1"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--store-dir",
                    str(root / "store"),
                    "--live-codex-home",
                    str(root / "live"),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "switch",
                    "openai-official",
                    "--skip-launchctl",
                    "--skip-app-cli",
                    "--skip-shim",
                ],
                input="\n\n\n",
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=prompt_env,
            )

            output = result.stdout
            official_prompt = output.index("Select Codex home for openai-official:")
            internal_prompt = output.index("Select Codex home for internal:")
            self.assertLess(official_prompt, internal_prompt)
            self.assertIn(f"  1. {root / 'live'} (Recommended)", output)
            self.assertIn(
                f"  1. {root / 'store' / 'homes' / 'internal'} (Recommended)",
                output,
            )

    def test_interactive_prompt_prefers_semantic_default_for_unconfirmed_internal_home(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            managed_internal_home = root / "store" / "homes" / "internal"
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            internal_manifest_path = root / "store" / "profiles" / "internal" / "manifest.json"
            internal_manifest = json.loads(internal_manifest_path.read_text())
            internal_manifest["codex_home"] = str(live_home)
            internal_manifest["home_mode"] = "adopted"
            internal_manifest.pop("home_selection_confirmed", None)
            internal_manifest_path.write_text(json.dumps(internal_manifest))

            prompt_env = dict(env)
            prompt_env["CODEX_SWITCH_FORCE_HOME_PROMPT"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--store-dir",
                    str(root / "store"),
                    "--live-codex-home",
                    str(live_home),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "switch",
                    "internal",
                    "--skip-launchctl",
                    "--skip-app-cli",
                    "--skip-shim",
                ],
                input="\n\n\n",
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=prompt_env,
            )

            output = result.stdout
            self.assertIn("Select Codex home for internal:", output)
            self.assertIn(f"  1. {managed_internal_home} (Recommended)", output)
            self.assertIn(str(live_home), output)
            confirmed_manifest = self.read_manifest(root, "internal")
            self.assertEqual(confirmed_manifest["codex_home"], str(managed_internal_home))
            self.assertTrue(confirmed_manifest["home_selection_confirmed"])

    def test_interactive_prompt_prefers_official_home_for_unconfirmed_official_home(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            managed_official_home = root / "store" / "homes" / "openai-official"
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            official_manifest_path = (
                root / "store" / "profiles" / "openai-official" / "manifest.json"
            )
            official_manifest = json.loads(official_manifest_path.read_text())
            official_manifest["codex_home"] = str(managed_official_home)
            official_manifest["home_mode"] = "managed"
            official_manifest.pop("home_selection_confirmed", None)
            official_manifest_path.write_text(json.dumps(official_manifest))

            prompt_env = dict(env)
            prompt_env["CODEX_SWITCH_FORCE_HOME_PROMPT"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--store-dir",
                    str(root / "store"),
                    "--live-codex-home",
                    str(live_home),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "switch",
                    "openai-official",
                    "--skip-launchctl",
                    "--skip-app-cli",
                    "--skip-shim",
                ],
                input="\n\n",
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=prompt_env,
            )

            output = result.stdout
            self.assertIn("Select Codex home for openai-official:", output)
            self.assertIn(f"  1. {live_home} (Recommended)", output)
            self.assertIn(str(managed_official_home), output)
            confirmed_manifest = self.read_manifest(root, "openai-official")
            self.assertEqual(confirmed_manifest["codex_home"], str(live_home))
            self.assertTrue(confirmed_manifest["home_selection_confirmed"])

    def test_interactive_profile_change_prompts_target_away_from_active_home(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            (root / "store" / "active.json").write_text(
                json.dumps(
                    {
                        "profile": "openai-official",
                        "codex_home": str(live_home),
                    }
                )
            )
            internal_manifest_path = root / "store" / "profiles" / "internal" / "manifest.json"
            internal_manifest = json.loads(internal_manifest_path.read_text())
            internal_manifest["codex_home"] = str(live_home)
            internal_manifest["home_mode"] = "adopted"
            internal_manifest["home_selection_confirmed"] = True
            internal_manifest_path.write_text(json.dumps(internal_manifest))

            prompt_env = dict(env)
            prompt_env["CODEX_SWITCH_FORCE_HOME_PROMPT"] = "1"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--store-dir",
                    str(root / "store"),
                    "--official-codex-home",
                    str(live_home),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "switch",
                    "internal",
                    "--skip-launchctl",
                    "--skip-app-cli",
                    "--skip-shim",
                ],
                input="\n",
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=prompt_env,
            )

            output = result.stdout
            internal_home = root / "store" / "homes" / "internal"
            self.assertIn(
                f"openai-official currently uses {live_home}; "
                "choose a different Codex home for internal.",
                output,
            )
            self.assertIn("Select Codex home for internal:", output)
            self.assertIn(f"  1. {internal_home} (Recommended)", output)
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "internal")
            self.assertEqual(active["codex_home"], str(internal_home))
            confirmed_manifest = self.read_manifest(root, "internal")
            self.assertEqual(confirmed_manifest["codex_home"], str(internal_home))
            self.assertTrue(confirmed_manifest["home_selection_confirmed"])

    def test_interactive_same_home_collision_prompts_for_other_profile_home(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            prompt_env = dict(env)
            prompt_env["CODEX_SWITCH_FORCE_HOME_PROMPT"] = "1"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--store-dir",
                    str(root / "store"),
                    "--official-codex-home",
                    str(live_home),
                    "--internal-codex-home",
                    str(live_home),
                    "--launch-agent-path",
                    str(root / "agent.plist"),
                    "switch",
                    "internal",
                    "--skip-launchctl",
                    "--skip-app-cli",
                    "--skip-shim",
                ],
                input="\n",
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=prompt_env,
            )

            output = result.stdout
            official_home = root / "store" / "homes" / "openai-official"
            self.assertIn("already uses", output)
            self.assertIn("Select Codex home for openai-official:", output)
            self.assertIn(f"  1. {official_home} (Recommended)", output)
            official_manifest = self.read_manifest(root, "openai-official")
            self.assertEqual(official_manifest["codex_home"], str(official_home))
            active = json.loads((root / "store" / "active.json").read_text())
            self.assertEqual(active["profile"], "internal")
            self.assertEqual(active["codex_home"], str(live_home))

    def test_restore_backup_dry_run_and_apply(self) -> None:
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
            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            active = json.loads((root / "store" / "active.json").read_text())
            backup_id = active["backup_id"]
            shim = root / "store" / "bin" / "codex"
            self.assertTrue(shim.exists())

            dry_run = self.run_switcher(root, "restore", backup_id, "--dry-run")
            self.assertIn("Dry run: restore backup", dry_run.stdout)
            self.assertTrue(shim.exists())

            self.run_switcher(root, "restore", backup_id, "--apply")

            self.assertFalse(shim.exists())
            self.assertFalse((root / "store" / "active.json").exists())

    def test_backup_failure_aborts_before_mutation(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            original_config = "[features]\nmemory = true\n"
            (live_home / "config.toml").write_text(original_config)
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            shutil.rmtree(root / "store" / "backups")
            (root / "store" / "backups").write_text("not a directory\n")

            result = self.run_switcher(
                root,
                "switch",
                "internal",
                "--skip-launchctl",
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(original_config, (live_home / "config.toml").read_text())
            self.assertFalse((root / "store" / "homes" / "internal").exists())
            self.assertFalse((root / "store" / "bin" / "codex").exists())
            self.assertFalse((root / "agent.plist").exists())

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
            self.assertIn('profile = "internal"', live_config)
            internal_config = (root / "store" / "homes" / "internal" / "config.toml").read_text()
            self.assertNotIn('profile = "internal"', internal_config)
            self.assertNotIn("[profiles.internal]", internal_config)
            self.assertTrue((root / "live" / "internal.config.toml").exists())
            self.assertTrue((root / "live" / "auth.json").exists())
            active = json.loads((root / "store" / "active.json").read_text())
            backup_dir = Path(active["backup_dir"])
            backup = json.loads((backup_dir / "backup.json").read_text())
            self.assertEqual(backup["to_profile"], "internal")

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
            self.assertIn('model = "gpt-5.5-2026-04-24"', live_config)
            self.assertIn('model_provider = "azure"', live_config)
            self.assertNotIn('cli_auth_credentials_store = "file"', live_config)
            self.assertIn("[features]", live_config)
            self.assertIn("memory = true", live_config)
            self.assertIn("[tui]", live_config)
            self.assertIn('theme = "catppuccin-latte"', live_config)
            profile_config = (
                root / "store" / "profiles" / "openai-official" / "config.toml"
            ).read_text()
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

    def test_internal_switch_refreshes_desktop_wrapper_with_shared_config(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            (root / "live" / "config.toml").write_text(
                'model = "gpt-5.5-2026-04-24"\n'
                'model_provider = "azure"\n'
                "\n"
                "[marketplaces.cy-codex-skills]\n"
                'source_type = "local"\n'
                f'source = "{root / "cy-codex-skills"}"\n'
                "\n"
                '[plugins."agent-kb@cy-codex-skills"]\n'
                "enabled = true\n"
                "\n"
                '[hooks.state."agent-kb@cy-codex-skills:hooks.json:stop:0:0"]\n'
                'trusted_hash = "sha256:test"\n'
            )
            (root / "live" / "auth.json").write_text('{"official":"auth"}\n')
            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            manifest_path = root / "store" / "profiles" / "internal" / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["app_cli_path"] = str(root / "store" / "bin" / "codex-internal-app")
            manifest_path.write_text(json.dumps(manifest))
            (root / "store" / "bin").mkdir(parents=True, exist_ok=True)
            (root / "store" / "bin" / "codex-internal-app").write_text(
                "#!/usr/bin/env sh\n"
                "SWITCH_SCRIPTS=/old/missing/path\n"
                "exit 99\n"
            )
            (root / "store" / "bin" / "codex-internal-app").chmod(0o755)

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")

            app_wrapper = root / "store" / "bin" / "codex-internal-app"
            wrapper_text = app_wrapper.read_text()
            self.assertIn(str(Path(__file__).parent), wrapper_text)
            self.assertNotIn("/old/missing/path", wrapper_text)
            self.assertIn("codex_switch_app_proxy.py", wrapper_text)
            self.assertIn('if [ "${1:-}" = "app-server" ]; then', wrapper_text)
            self.assertNotIn('&& [ "${2:-}" = "--stdio" ]', wrapper_text)

            result = subprocess.run(
                [str(app_wrapper), "--version"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            self.assertIn("internal-codex", result.stdout)
            app_home_config = (
                root / "store" / "homes" / "internal" / "config.toml"
            ).read_text()
            self.assertIn("[marketplaces.cy-codex-skills]", app_home_config)
            self.assertIn('[plugins."agent-kb@cy-codex-skills"]', app_home_config)
            self.assertIn(
                '[hooks.state."agent-kb@cy-codex-skills:hooks.json:stop:0:0"]',
                app_home_config,
            )
            self.assertIn('model = "gpt-5.5-2026-04-24"', app_home_config)
            self.assertIn("# codex-switch: managed runtime config for profile internal", app_home_config)
            self.assertIn("\n# codex-switch: profile-specific settings\n", app_home_config)
            self.assertIn("\n# codex-switch: shared settings\n", app_home_config)
            self.assertFalse(
                (root / "store" / "homes" / "internal" / "auth.json").exists()
            )

    def test_internal_desktop_wrapper_persists_app_home_plugin_state(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            (root / "live" / "config.toml").write_text(
                "[marketplaces.openai-bundled]\n"
                'source_type = "local"\n'
                f'source = "{root / "openai-bundled"}"\n'
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
            manifest_path = root / "store" / "profiles" / "internal" / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["app_cli_path"] = str(root / "store" / "bin" / "codex-internal-app")
            manifest_path.write_text(json.dumps(manifest))

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            app_wrapper = root / "store" / "bin" / "codex-internal-app"
            subprocess.run(
                [str(app_wrapper), "--version"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            app_home_config_path = root / "store" / "homes" / "internal" / "config.toml"
            app_home_config_path.write_text(
                'notify = ["turn-ended"]\n'
                + "\n"
                + app_home_config_path.read_text()
                + "\n"
                + "[features]\n"
                + "codex_hooks = true\n"
                + "\n"
                + "[mcp_servers.local-test]\n"
                + 'command = "local-mcp"\n'
                + "\n"
                + '[plugins."computer-use@openai-bundled"]\n'
                + "enabled = true\n"
                + "\n"
                + '[hooks.state."computer-use@openai-bundled:hooks.json:stop:0:0"]\n'
                + 'trusted_hash = "sha256:computer-use"\n'
            )

            subprocess.run(
                [str(app_wrapper), "--version"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            live_config = (root / "live" / "config.toml").read_text()
            app_home_config = app_home_config_path.read_text()
            for config_text in (live_config, app_home_config):
                self.assertIn('notify = ["turn-ended"]', config_text)
                self.assertIn("[features]", config_text)
                self.assertIn("codex_hooks = true", config_text)
                self.assertIn("[mcp_servers.local-test]", config_text)
                self.assertIn('[plugins."computer-use@openai-bundled"]', config_text)
                self.assertIn(
                    '[hooks.state."computer-use@openai-bundled:hooks.json:stop:0:0"]',
                    config_text,
                )
            self.assertNotIn('model = "gpt-5.5-2026-04-24"', live_config)

    def test_internal_desktop_wrapper_preserves_official_personality(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            _, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            live_home_config = live_home / "config.toml"
            live_home_config.write_text(
                'model = "official-runtime"\n'
                'personality = "friendly"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
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
            manifest_path = root / "store" / "profiles" / "internal" / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["app_cli_path"] = str(root / "store" / "bin" / "codex-internal-app")
            manifest_path.write_text(json.dumps(manifest))

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            app_wrapper = root / "store" / "bin" / "codex-internal-app"
            app_home_config_path = root / "store" / "homes" / "internal" / "config.toml"
            app_home_config_path.write_text(
                app_home_config_path.read_text()
                + "\n"
                + "[mcp_servers.local-test]\n"
                + 'command = "local-mcp"\n'
            )

            subprocess.run(
                [str(app_wrapper), "--version"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            live_config = live_home_config.read_text()
            self.assertIn('model = "official-runtime"', live_config)
            self.assertIn('personality = "friendly"', live_config)
            self.assertIn("[mcp_servers.local-test]", live_config)

    def test_internal_desktop_wrapper_isolates_response_runtime_state(self) -> None:
        temp_dir, root = self.make_workspace()
        with temp_dir:
            internal_codex, official_codex, env = self.prepare_profiles(root)
            live_home = root / "live"
            (live_home / "config.toml").write_text(
                'profile = "internal"\n'
                "\n"
                "[profiles.internal]\n"
                "\n"
                "[plugins.local]\n"
                "enabled = true\n"
            )
            for dirname in (
                "sessions",
                "archived_sessions",
                "browser",
                "log",
                "tmp",
                ".tmp",
                "process_manager",
                "node_repl",
                "shell_snapshots",
                "ambient-suggestions",
                "agent-kb",
                "cache",
                "computer-use",
                "model-catalogs",
                "plugins",
                "sqlite",
            ):
                (live_home / dirname).mkdir()
            for filename in (
                "history.jsonl",
                "session_index.jsonl",
                "state_5.sqlite",
                "state_5.sqlite-shm",
                "state_5.sqlite-wal",
                "state_5.sqlite.corrupt.20260522-173044",
                "state_5.sqlite-shm.corrupt.20260522-173044",
                "state_5.sqlite-wal.corrupt.20260522-173044",
                ".credentials.json",
                ".codex-global-state.json",
                "models_cache.json",
                "version.json",
            ):
                (live_home / filename).write_text(f"{filename}\n")

            self.run_switcher(
                root,
                "init",
                "--app-cli-path",
                str(official_codex),
                "--capture-current",
                "internal",
                env=env,
            )
            manifest_path = root / "store" / "profiles" / "internal" / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["app_cli_path"] = str(root / "store" / "bin" / "codex-internal-app")
            manifest_path.write_text(json.dumps(manifest))

            self.run_switcher(root, "switch", "internal", "--skip-launchctl")
            app_home = root / "store" / "homes" / "internal"
            app_home.mkdir(parents=True, exist_ok=True)
            for stale_name in ("sessions", "state_5.sqlite"):
                (app_home / stale_name).symlink_to(
                    live_home / stale_name,
                    target_is_directory=(live_home / stale_name).is_dir(),
                )

            result = subprocess.run(
                [str(root / "store" / "bin" / "codex-internal-app"), "--version"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

            self.assertIn("internal-codex", result.stdout)
            excluded_names = (
                "sessions",
                "archived_sessions",
                "browser",
                "log",
                "tmp",
                ".tmp",
                "process_manager",
                "node_repl",
                "shell_snapshots",
                "ambient-suggestions",
                "agent-kb",
                "cache",
                "computer-use",
                "model-catalogs",
                "plugins",
                "sqlite",
                "history.jsonl",
                "session_index.jsonl",
                "state_5.sqlite",
                "state_5.sqlite-shm",
                "state_5.sqlite-wal",
                "state_5.sqlite.corrupt.20260522-173044",
                "state_5.sqlite-shm.corrupt.20260522-173044",
                "state_5.sqlite-wal.corrupt.20260522-173044",
                ".credentials.json",
                ".codex-global-state.json",
                "models_cache.json",
                "version.json",
            )
            for name in excluded_names:
                self.assertFalse(
                    (app_home / name).is_symlink(),
                    f"{name} must not be shared from live CODEX_HOME",
                )
            self.assertFalse((app_home / "auth.json").exists())

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

    def test_app_server_command_path_ignores_payload_mentions(self) -> None:
        args = (
            "/Users/cY/.codex/computer-use/Codex Computer Use.app/Contents/"
            "SharedSupport/SkyComputerUseClient.app/Contents/MacOS/SkyComputerUseClient "
            "turn-ended "
            '{"last-assistant-message":"Host --> AppServer[\\"codex app-server --stdio\\"]"}'
        )

        self.assertEqual(app_server_command_path(args), "")

    def test_app_server_command_path_accepts_codex_executables(self) -> None:
        self.assertEqual(
            app_server_command_path(
                "/Users/cY/.codex-switch/bin/codex-internal-app "
                "app-server --analytics-default-enabled"
            ),
            "/Users/cY/.codex-switch/bin/codex-internal-app",
        )
        self.assertEqual(
            app_server_command_path(
                "/Users/cY/.vscode/extensions/openai.chatgpt/bin/macos-aarch64/codex "
                "app-server --analytics-default-enabled"
            ),
            "/Users/cY/.vscode/extensions/openai.chatgpt/bin/macos-aarch64/codex",
        )

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
