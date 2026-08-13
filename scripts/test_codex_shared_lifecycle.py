#!/usr/bin/env python3

from __future__ import annotations

import importlib
import hashlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import codex_switch_doctor as doctor_module
import codex_switch_runtime_binding as runtime_binding_module
import codex_switch_status as status_module
import codex_switch_verify as verify_module
from codex_switch_constants import SwitchError
from codex_switch_runtime_binding import RuntimeBinding, RuntimeObservation
from codex_switch_selection import ProfileSelection
from codex_switch_store import Store


class BackendExecIntercept(Exception):
    """Stop a patched os.execve after its ordering evidence is recorded."""


def write_executable(path: Path, body: str = "#!/bin/sh\nexit 0\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    path.chmod(0o755)
    return path


def tree_snapshot(root: Path) -> tuple[tuple[object, ...], ...]:
    if not root.exists():
        return ()
    entries: list[tuple[object, ...]] = []
    for path in sorted(root.rglob("*"), key=lambda item: str(item.relative_to(root))):
        relative = str(path.relative_to(root))
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        if path.is_symlink():
            entries.append((relative, "link", mode, os.readlink(path)))
        elif path.is_file():
            entries.append((relative, "file", mode, path.read_bytes()))
        else:
            entries.append((relative, "dir", mode))
    return tuple(entries)


class SharedLifecycleFixture(unittest.TestCase):
    def shared_module(self):
        return importlib.import_module("codex_switch_shared_configuration")

    def make_store(self, root: Path) -> tuple[Store, ProfileSelection]:
        official_home = root / "official-home"
        internal_home = root / "internal-home"
        store = Store(
            root=root / "store",
            official_codex_home=official_home,
            internal_codex_home=internal_home,
            internal_codex_home_source="explicit",
            launch_agent_path=root / "agent.plist",
            launch_agent_label="test",
        )
        store.ensure()
        official_home.mkdir(parents=True)
        internal_home.mkdir(parents=True)
        (official_home / "plugins").mkdir()
        (internal_home / "plugins").mkdir()
        (official_home / "skills").mkdir()
        (internal_home / "skills").symlink_to(
            official_home / "skills",
            target_is_directory=True,
        )
        (official_home / "config.toml").write_text('model = "official"\n')
        (internal_home / "config.toml").write_text('model = "internal"\n')

        official_bin = write_executable(root / "official-bin" / "codex")
        internal_bin = write_executable(root / "internal-bin" / "codex")
        manifests = {
            "internal": {
                "name": "internal",
                "codex_home": str(internal_home),
                "codex_bin": str(internal_bin),
                "app_cli_path": str(internal_bin),
            },
            "openai-official": {
                "name": "openai-official",
                "codex_home": str(official_home),
                "codex_bin": str(official_bin),
                "app_cli_path": str(official_bin),
            },
        }
        for name, manifest in manifests.items():
            profile = store.profile_dir(name)
            profile.mkdir(parents=True)
            (profile / "manifest.json").write_text(json.dumps(manifest))
            (profile / "config.toml").write_text(
                (internal_home if name == "internal" else official_home)
                .joinpath("config.toml")
                .read_text()
            )
        store.active_path.write_text(
            json.dumps(
                {
                    "profile": "internal",
                    "cli_profile": "internal",
                    "app_profile": "openai-official",
                    "codex_home": str(internal_home),
                    "shell_cli_path": str(internal_bin),
                    "app_cli_path": str(official_bin),
                }
            )
        )
        return store, ProfileSelection("internal", "openai-official")

    def adapters(
        self,
        *,
        app_running: bool = False,
        materialization_log: list[dict[str, object]] | None = None,
    ) -> SimpleNamespace:
        def materialize_plugins(**kwargs: object) -> tuple[dict[str, object], ...]:
            if materialization_log is not None:
                materialization_log.append(dict(kwargs))
            return ()

        return SimpleNamespace(
            read_stable=lambda path: Path(path).read_text(),
            app_is_running=lambda _store, _selection: app_running,
            materialize_plugins=materialize_plugins,
            before_commit=lambda *_args, **_kwargs: None,
        )

    def bootstrap(
        self,
        store: Store,
        selection: ProfileSelection,
    ) -> object:
        return self.shared_module().reconcile_shared_configuration(
            store,
            selection,
            boundary="explicit-sync",
            mode="apply",
            adapters=self.adapters(),
        )


class InternalCliPreflightTests(SharedLifecycleFixture):
    def blocked_receipt(self) -> object:
        module = self.shared_module()
        return module.SharedConfigurationReceipt(
            status="blocked",
            generation_before=7,
            generation_after=7,
            cli_ready=False,
            findings=(
                module.SharedConfigurationFinding(
                    code="shared_configuration.secret_field",
                    severity="error",
                    message="Credential-like plugin fields cannot enter shared state.",
                ),
            ),
            source_profile="openai-official",
            target_profile="internal",
            changes=(
                module.SharedConfigurationChange(
                    profile="openai-official",
                    operation="update",
                    path="/plugins/dev-flow@cy-codex-skills",
                ),
            ),
            remediation=module.SHARED_REMEDIATION_COMMANDS,
        )

    def test_blocked_preflight_never_prompts_or_retries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, _selection = self.make_store(root)
            internal_home = store.internal_codex_home
            assert internal_home is not None
            module = self.shared_module()
            reconcile = Mock(return_value=self.blocked_receipt())
            output = io.StringIO()

            with (
                patch.object(module, "reconcile_shared_configuration", reconcile),
                redirect_stderr(output),
                self.assertRaisesRegex(
                    SwitchError,
                    "shared_configuration.preflight_blocked",
                ),
            ):
                module.preflight_internal_shared_configuration(
                    store_root=store.root,
                    internal_home=internal_home,
                    backend_args=("exec", "hello"),
                )

            reconcile.assert_called_once()
            rendered = output.getvalue()
            self.assertIn("shared_configuration.secret_field", rendered)
            self.assertIn("codex-switch sync-shared --dry-run", rendered)
            self.assertIn("codex-switch sync-shared", rendered)
            self.assertIn("codex-switch doctor", rendered)
            self.assertNotIn("resolve-shared", rendered)
            self.assertFalse(hasattr(module, "_shared_prompt_enabled"))
            self.assertFalse(hasattr(module, "_read_shared_resolution_choice"))

    def test_applied_preflight_reconciles_once_and_reports_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, _selection = self.make_store(root)
            internal_home = store.internal_codex_home
            assert internal_home is not None
            module = self.shared_module()
            applied = module.SharedConfigurationReceipt(
                status="applied",
                generation_before=7,
                generation_after=8,
                cli_ready=True,
                source_profile="openai-official",
                target_profile="internal",
            )
            reconcile = Mock(return_value=applied)
            output = io.StringIO()

            with (
                patch.object(module, "reconcile_shared_configuration", reconcile),
                redirect_stderr(output),
            ):
                receipt = module.preflight_internal_shared_configuration(
                    store_root=store.root,
                    internal_home=internal_home,
                    backend_args=("exec", "hello"),
                )

            self.assertIs(receipt, applied)
            reconcile.assert_called_once()
            self.assertIn(
                "Shared configuration synchronized: generation 7 -> 8",
                output.getvalue(),
            )
            self.assertIn(
                "Shared configuration ready: generation 8",
                output.getvalue(),
            )

    def test_unsafe_preflight_prints_cause_and_exact_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, _selection = self.make_store(root)
            store.official_codex_home.joinpath("config.toml").write_text(
                'model = "official"\n'
                '\n[plugins."unsafe@example"]\n'
                'enabled = true\n'
                'access_token = "must-not-be-shared"\n'
            )
            output = io.StringIO()

            with redirect_stderr(output), self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.preflight_blocked: "
                "shared_configuration.secret_field",
            ):
                self.shared_module().preflight_internal_shared_configuration(
                    store_root=store.root,
                    internal_home=store.internal_codex_home,
                    backend_args=("features", "list"),
                )

            rendered = output.getvalue()
            self.assertIn(
                "Credential-like plugin fields cannot enter shared state.",
                rendered,
            )
            self.assertIn("codex-switch sync-shared --dry-run", rendered)
            self.assertIn("codex-switch sync-shared", rendered)
            self.assertIn("codex-switch doctor", rendered)
            self.assertNotIn("must-not-be-shared", rendered)

    def test_repairable_preflight_reports_verified_generation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, selection = self.make_store(root)
            bootstrapped = self.bootstrap(store, selection)
            self.assertEqual("applied", bootstrapped.status)
            store.official_codex_home.joinpath("config.toml").write_text(
                'model = "official"\n'
                '\n[plugins."disabled@example"]\n'
                'enabled = false\n'
            )
            output = io.StringIO()

            with redirect_stderr(output):
                receipt = self.shared_module().preflight_internal_shared_configuration(
                    store_root=store.root,
                    internal_home=store.internal_codex_home,
                    backend_args=("features", "list"),
                )

            self.assertEqual("applied", receipt.status)
            self.assertTrue(receipt.cli_ready)
            self.assertEqual(1, receipt.generation_before)
            self.assertEqual(2, receipt.generation_after)
            rendered = output.getvalue()
            self.assertIn(
                "Shared configuration synchronized: generation 1 -> 2",
                rendered,
            )
            self.assertIn(
                "Shared configuration ready: generation 2",
                rendered,
            )

    def generation_argv(
        self,
        root: Path,
        backend_args: tuple[str, ...],
    ) -> tuple[list[str], Path, Path, Path]:
        store_root = root / "store"
        manifest_path = store_root / "profiles" / "internal" / "manifest.json"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(json.dumps({"name": "internal"}))
        fallback_home = root / "internal-home"
        fallback_home.mkdir()
        fallback_backend = write_executable(root / "internal-bin" / "codex")
        return (
            [
                "exec-internal-shell",
                "--store-root",
                str(store_root),
                "--fallback-home",
                str(fallback_home),
                "--fallback-backend",
                str(fallback_backend),
                "--",
                *backend_args,
            ],
            store_root,
            fallback_home,
            fallback_backend,
        )

    def run_with_fakes(
        self,
        root: Path,
        backend_args: tuple[str, ...],
        *,
        preflight: object,
        execve: object,
    ) -> None:
        argv, _store_root, _home, _backend = self.generation_argv(
            root,
            backend_args,
        )
        with patch.object(
            runtime_binding_module,
            "preflight_internal_shared_configuration",
            preflight,
            create=True,
        ), patch.object(runtime_binding_module.os, "execve", execve):
            runtime_binding_module._run_internal_generation_command(argv)

    def test_functional_preflight_completes_before_backend_execve(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            events: list[str] = []

            def preflight(*_args: object, **_kwargs: object) -> object:
                events.append("preflight-ready")
                return SimpleNamespace(
                    status="applied",
                    cli_ready=True,
                    findings=(),
                )

            def execve(*_args: object, **_kwargs: object) -> None:
                events.append("backend-execve")
                raise BackendExecIntercept

            with self.assertRaises(BackendExecIntercept):
                self.run_with_fakes(
                    root,
                    ("exec", "--json", "hello"),
                    preflight=preflight,
                    execve=execve,
                )

            self.assertEqual(["preflight-ready", "backend-execve"], events)

    def test_cli_only_generation_ignores_stale_app_parity_and_executes_bound_cli(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            argv, store_root, fallback_home, backend = self.generation_argv(
                root,
                ("exec", "hello"),
            )
            backend_payload = backend.read_bytes()
            manifest_path = (
                store_root / "profiles" / "internal" / "manifest.json"
            )
            manifest = json.loads(manifest_path.read_text())
            manifest.update(
                {
                    "codex_bin": str(backend),
                    "internal_cli_generation": {
                        "schema_version": 1,
                        "scope": "cli-only",
                        "backend_sha256": hashlib.sha256(
                            backend_payload
                        ).hexdigest(),
                        "backend_version": "2.0.0",
                    },
                    "internal_app_readiness": "unverified",
                    "parity_receipt_path": str(
                        store_root / "stale-app-parity.json"
                    ),
                }
            )
            manifest_path.write_text(json.dumps(manifest))
            observed: list[tuple[object, ...]] = []

            def execve(*args: object) -> None:
                observed.append(args)
                raise BackendExecIntercept

            with patch.object(
                runtime_binding_module,
                "preflight_internal_shared_configuration",
                return_value=SimpleNamespace(
                    status="current",
                    cli_ready=True,
                    findings=(),
                ),
            ), patch.object(
                runtime_binding_module.os,
                "execve",
                side_effect=execve,
            ), self.assertRaises(BackendExecIntercept):
                runtime_binding_module._run_internal_generation_command(argv)

            self.assertEqual(1, len(observed))
            executable, command, environment = observed[0]
            self.assertEqual(backend.resolve(), executable)
            self.assertEqual([str(backend.resolve()), "exec", "hello"], command)
            self.assertEqual(
                str(fallback_home.resolve()),
                environment["CODEX_HOME"],
            )
            self.assertNotIn(
                "CODEX_SWITCH_CAPABILITY_RECEIPT",
                environment,
            )

    def test_cli_only_generation_streams_production_sized_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            argv, store_root, _fallback_home, backend = self.generation_argv(
                root,
                ("--version",),
            )
            with backend.open("r+b") as handle:
                handle.truncate(17 * 1024 * 1024)
            with backend.open("rb") as handle:
                backend_sha256 = hashlib.file_digest(
                    handle,
                    "sha256",
                ).hexdigest()
            manifest_path = (
                store_root / "profiles" / "internal" / "manifest.json"
            )
            manifest = json.loads(manifest_path.read_text())
            manifest.update(
                {
                    "codex_bin": str(backend),
                    "internal_cli_generation": {
                        "schema_version": 1,
                        "scope": "cli-only",
                        "backend_sha256": backend_sha256,
                        "backend_version": "2.0.0",
                    },
                    "internal_app_readiness": "unverified",
                }
            )
            manifest_path.write_text(json.dumps(manifest))
            execve = Mock(side_effect=BackendExecIntercept)

            with patch.object(
                runtime_binding_module.os,
                "execve",
                execve,
            ), self.assertRaises(BackendExecIntercept):
                runtime_binding_module._run_internal_generation_command(argv)

            execve.assert_called_once()
            self.assertEqual(backend.resolve(), execve.call_args.args[0])

    def test_cli_only_generation_rejects_executable_beyond_safety_bound(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            argv, store_root, _fallback_home, backend = self.generation_argv(
                root,
                ("--version",),
            )
            with backend.open("r+b") as handle:
                handle.truncate((2 * 1024 * 1024 * 1024) + 1)
            manifest_path = (
                store_root / "profiles" / "internal" / "manifest.json"
            )
            manifest = json.loads(manifest_path.read_text())
            manifest.update(
                {
                    "codex_bin": str(backend),
                    "internal_cli_generation": {
                        "schema_version": 1,
                        "scope": "cli-only",
                        "backend_sha256": "0" * 64,
                        "backend_version": "2.0.0",
                    },
                    "internal_app_readiness": "unverified",
                }
            )
            manifest_path.write_text(json.dumps(manifest))
            execve = Mock(side_effect=BackendExecIntercept)

            with patch.object(
                runtime_binding_module.os,
                "execve",
                execve,
            ), self.assertRaisesRegex(
                SwitchError,
                "CLI backend exceeds the executable size limit",
            ):
                runtime_binding_module._run_internal_generation_command(argv)

            execve.assert_not_called()

    def test_cli_only_generation_digest_drift_fails_before_execve(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            argv, store_root, _fallback_home, backend = self.generation_argv(
                root,
                ("--version",),
            )
            manifest_path = (
                store_root / "profiles" / "internal" / "manifest.json"
            )
            manifest = json.loads(manifest_path.read_text())
            manifest.update(
                {
                    "codex_bin": str(backend),
                    "internal_cli_generation": {
                        "schema_version": 1,
                        "scope": "cli-only",
                        "backend_sha256": "0" * 64,
                        "backend_version": "2.0.0",
                    },
                    "internal_app_readiness": "unverified",
                }
            )
            manifest_path.write_text(json.dumps(manifest))
            execve = Mock(side_effect=BackendExecIntercept)

            with patch.object(
                runtime_binding_module.os,
                "execve",
                execve,
            ), self.assertRaisesRegex(
                SwitchError,
                "CLI generation.*digest",
            ):
                runtime_binding_module._run_internal_generation_command(argv)

            execve.assert_not_called()

    def test_internal_app_generation_rejects_cli_only_readiness_first(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _argv, store_root, fallback_home, backend = self.generation_argv(
                root,
                ("--version",),
            )
            manifest_path = (
                store_root / "profiles" / "internal" / "manifest.json"
            )
            manifest = json.loads(manifest_path.read_text())
            manifest.update(
                {
                    "codex_bin": str(backend),
                    "internal_cli_generation": {
                        "schema_version": 1,
                        "scope": "cli-only",
                        "backend_sha256": hashlib.sha256(
                            backend.read_bytes()
                        ).hexdigest(),
                        "backend_version": "2.0.0",
                    },
                    "internal_app_readiness": "unverified",
                }
            )
            manifest_path.write_text(json.dumps(manifest))

            with self.assertRaisesRegex(
                SwitchError,
                "internal.app_readiness.unverified",
            ):
                runtime_binding_module.validate_internal_runtime_generation(
                    store_root=store_root,
                    fallback_home=fallback_home,
                )

    def test_blocked_preflight_never_calls_backend_execve(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            backend_calls: list[tuple[object, ...]] = []

            def blocked(*_args: object, **_kwargs: object) -> object:
                raise SwitchError(
                    "materialization_failed: shared generation is not CLI-ready"
                )

            def execve(*args: object, **_kwargs: object) -> None:
                backend_calls.append(args)
                raise BackendExecIntercept

            with self.assertRaisesRegex(SwitchError, "materialization_failed"):
                self.run_with_fakes(
                    root,
                    ("exec", "hello"),
                    preflight=blocked,
                    execve=execve,
                )

            self.assertEqual([], backend_calls)

    def test_unchanged_preflight_executes_backend_exactly_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            preflight = Mock(
                return_value=SimpleNamespace(
                    status="current",
                    cli_ready=True,
                    findings=(),
                )
            )
            execve = Mock(side_effect=BackendExecIntercept)

            with self.assertRaises(BackendExecIntercept):
                self.run_with_fakes(
                    root,
                    ("exec", "unchanged"),
                    preflight=preflight,
                    execve=execve,
                )

            preflight.assert_called_once()
            execve.assert_called_once()

    def test_help_and_version_are_read_only_and_skip_preflight(self) -> None:
        for backend_args in (("--help",), ("--version",)):
            with self.subTest(backend_args=backend_args), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                preflight = Mock(
                    side_effect=AssertionError(
                        "informational invocation must not reconcile"
                    )
                )
                execve = Mock(side_effect=BackendExecIntercept)

                with self.assertRaises(BackendExecIntercept):
                    self.run_with_fakes(
                        root,
                        backend_args,
                        preflight=preflight,
                        execve=execve,
                    )

                preflight.assert_not_called()
                execve.assert_called_once()


class ExplicitSharedSyncTests(SharedLifecycleFixture):
    def run_split_wrapper_scenario(
        self,
        root: Path,
        command_form: tuple[str, ...],
        *,
        extra_args: tuple[str, ...] = (),
        sync_exit: int = 0,
        skip_self_update: bool = True,
    ) -> tuple[subprocess.CompletedProcess[str], tuple[str, ...], Path]:
        store_root = root / "store"
        command_log = root / "commands.jsonl"
        fake_switcher = write_executable(
            root / "split-lifecycle-switcher.py",
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "from pathlib import Path\n"
            "args = sys.argv[1:]\n"
            "commands = {'switch', 'sync-shared', 'repair-plugins', "
            "'verify', 'doctor', 'status'}\n"
            "command = next(arg for arg in args if arg in commands)\n"
            "event = command\n"
            "if command == 'switch':\n"
            "    event += ':dry-run' if '--dry-run' in args else ':apply'\n"
            "with Path(os.environ['CODEX_SWITCH_COMMAND_LOG']).open('a') as log:\n"
            "    log.write(json.dumps(event) + '\\n')\n"
            "store = Path(args[args.index('--store-dir') + 1])\n"
            "if command == 'switch':\n"
            "    print('CLI profile: internal')\n"
            "    print('App profile: openai-official')\n"
            "    print('App action: preserve')\n"
            "    if '--dry-run' not in args:\n"
            "        store.mkdir(parents=True, exist_ok=True)\n"
            "        (store / 'active.json').write_text(json.dumps({\n"
            "            'profile': 'internal',\n"
            "            'cli_profile': 'internal',\n"
            "            'app_profile': 'openai-official',\n"
            "            'codex_home': str(store / 'homes' / 'internal'),\n"
            "        }))\n"
            "elif command == 'sync-shared':\n"
            "    sync_exit = int(os.environ['CODEX_SWITCH_SYNC_EXIT'])\n"
            "    if sync_exit:\n"
            "        print('shared_configuration.source_changed_during_plan: "
            "Official source changed', file=sys.stderr)\n"
            "        raise SystemExit(sync_exit)\n"
            "    print('Shared configuration ready: generation 8')\n",
        )
        environment = {
            **os.environ,
            "CODEX_SWITCH_COMMAND_LOG": str(command_log),
            "CODEX_SWITCH_PYTHON": sys.executable,
            "CODEX_SWITCH_SCRIPT": str(fake_switcher),
            "CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP": "1",
            "CODEX_SWITCH_SYNC_EXIT": str(sync_exit),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        global_args = ("--skip-self-update",) if skip_self_update else ()
        result = subprocess.run(
            [
                str(Path(__file__).with_name("codex-switch")),
                "--store-dir",
                str(store_root),
                "--official-codex-home",
                str(root / "official-home"),
                "--internal-codex-home",
                str(root / "internal-home"),
                "--launch-agent-path",
                str(root / "agent.plist"),
                *global_args,
                *command_form,
                *extra_args,
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )
        events = tuple(
            json.loads(line) for line in command_log.read_text().splitlines()
        )
        return result, events, store_root

    def test_split_apply_synchronizes_once_before_later_wrapper_steps(self) -> None:
        command_forms = (
            ("split",),
            ("internal", "--app-profile", "official"),
            ("internal", "--app-profile=official"),
        )

        for command_form in command_forms:
            with (
                self.subTest(command_form=command_form),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                result, events, _store_root = self.run_split_wrapper_scenario(
                    root,
                    command_form,
                    extra_args=("--skip-update-check", "--skip-login"),
                )

                output = result.stdout + result.stderr
                self.assertEqual(0, result.returncode, output)
                self.assertEqual(
                    (
                        "switch:dry-run",
                        "switch:apply",
                        "sync-shared",
                        "repair-plugins",
                        "verify",
                        "doctor",
                        "status",
                    ),
                    events,
                )
                self.assertIn("== Shared configuration ==", output)
                self.assertIn("Shared configuration ready: generation 8", output)

    def test_split_sync_failure_stops_later_steps_with_exact_remediation(self) -> None:
        command_forms = (
            ("split",),
            ("internal", "--app-profile", "official"),
            ("internal", "--app-profile=official"),
        )

        for command_form in command_forms:
            with (
                self.subTest(command_form=command_form),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                root = Path(temp_dir)
                result, events, store_root = self.run_split_wrapper_scenario(
                    root,
                    command_form,
                    extra_args=("--skip-update-check", "--skip-login"),
                    sync_exit=47,
                )
                output = result.stdout + result.stderr
                self.assertEqual(47, result.returncode, output)
                self.assertEqual(
                    ("switch:dry-run", "switch:apply", "sync-shared"),
                    events,
                )
                self.assertIn("Outcome: ACTION REQUIRED", output)
                self.assertIn("Failed step: shared synchronization", output)
                self.assertIn("codex-switch sync-shared --dry-run", output)
                self.assertIn("codex-switch sync-shared", output)
                self.assertIn("codex-switch doctor", output)
                active = json.loads((store_root / "active.json").read_text())
                self.assertEqual("internal", active["cli_profile"])
                self.assertEqual("openai-official", active["app_profile"])

    def test_split_sync_runs_when_every_later_step_is_skipped(self) -> None:
        command_forms = (
            ("split",),
            ("internal", "--app-profile", "official"),
            ("internal", "--app-profile=official"),
        )
        later_skip_args = (
            "--skip-update-check",
            "--skip-login",
            "--skip-plugin-repair",
            "--skip-verify",
            "--skip-doctor",
            "--no-status",
        )

        for command_form in command_forms:
            with (
                self.subTest(command_form=command_form),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                result, events, _store_root = self.run_split_wrapper_scenario(
                    Path(temp_dir),
                    command_form,
                    extra_args=later_skip_args,
                )
                output = result.stdout + result.stderr
                self.assertEqual(0, result.returncode, output)
                self.assertEqual(
                    ("switch:dry-run", "switch:apply", "sync-shared"),
                    events,
                )
                self.assertIn("Shared configuration ready: generation 8", output)

    def test_split_dry_run_names_shared_readiness_without_applying_it(self) -> None:
        command_forms = (
            ("split", "--dry-run"),
            ("internal", "--app-profile", "official", "--dry-run"),
            ("internal", "--app-profile=official", "--dry-run"),
        )

        for command_form in command_forms:
            with (
                self.subTest(command_form=command_form),
                tempfile.TemporaryDirectory() as temp_dir,
            ):
                result, events, store_root = self.run_split_wrapper_scenario(
                    Path(temp_dir),
                    command_form,
                    skip_self_update=False,
                )
                output = result.stdout + result.stderr
                self.assertEqual(0, result.returncode, output)
                self.assertEqual(("switch:dry-run",), events)
                self.assertIn("== Shared configuration ==", output)
                self.assertIn(
                    "Shared configuration: will synchronize "
                    "openai-official -> internal after a successful switch.",
                    output,
                )
                self.assertIn(
                    "Dry-run: shared synchronization was not applied.",
                    output,
                )
                self.assertFalse(store_root.exists())

    def test_wrapper_help_exposes_sync_without_manual_resolution(self) -> None:
        wrapper = Path(__file__).with_name("codex-switch")

        result = subprocess.run(
            [str(wrapper), "--help"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("sync-shared", result.stdout)
        self.assertNotIn("resolve-shared", result.stdout)

    def test_resolve_shared_command_is_not_exposed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, _selection = self.make_store(root)
            before = tree_snapshot(root)
            script = Path(__file__).with_name("codex_profile_switch.py")

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--store-dir",
                    str(store.root),
                    "--official-codex-home",
                    str(store.official_codex_home),
                    "--internal-codex-home",
                    str(store.internal_codex_home),
                    "--launch-agent-path",
                    str(store.launch_agent_path),
                    "resolve-shared",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("invalid choice", result.stderr)
            self.assertNotIn("ImportError", result.stderr)
            self.assertEqual(before, tree_snapshot(root))
    def test_sync_shared_dry_run_reports_plan_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, _selection = self.make_store(root)
            before = tree_snapshot(root)
            script = Path(__file__).with_name("codex_profile_switch.py")
            environment = dict(os.environ)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--store-dir",
                    str(store.root),
                    "--official-codex-home",
                    str(store.official_codex_home),
                    "--internal-codex-home",
                    str(store.internal_codex_home),
                    "--launch-agent-path",
                    str(store.launch_agent_path),
                    "sync-shared",
                    "--dry-run",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            output = (result.stdout + result.stderr).lower()
            for label in (
                "source",
                "target",
                "generation",
                "cli ready",
                "change",
                "action",
            ):
                self.assertIn(label, output)
            self.assertEqual(before, tree_snapshot(root))

    def test_running_app_does_not_block_internal_auto_sync(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, selection = self.make_store(root)
            bootstrapped = self.bootstrap(store, selection)
            self.assertEqual("applied", bootstrapped.status)
            official_config = store.official_codex_home / "config.toml"
            internal_home = store.internal_codex_home
            assert internal_home is not None
            internal_config = internal_home / "config.toml"
            official_before = official_config.read_bytes()
            official_cache_before = tree_snapshot(
                store.official_codex_home / "plugins"
            )
            internal_config.write_text(
                internal_config.read_text()
                + '\n[plugins."internal-drift@example"]\nenabled = false\n'
            )

            applied = self.shared_module().reconcile_shared_configuration(
                store,
                selection,
                boundary="cli-preflight",
                mode="apply",
                adapters=self.adapters(app_running=True),
            )

            self.assertEqual("applied", applied.status)
            self.assertTrue(applied.cli_ready)
            self.assertIsNone(applied.pending_target)
            self.assertNotIn(
                '[plugins."internal-drift@example"]',
                internal_config.read_text(),
            )
            self.assertEqual(official_before, official_config.read_bytes())
            self.assertEqual(
                official_cache_before,
                tree_snapshot(store.official_codex_home / "plugins"),
            )
            report = self.shared_module().shared_configuration_report(
                store,
                selection,
            )
            self.assertEqual(applied.generation_after, report.generation)
            self.assertEqual("current", report.status)
    def test_explicit_sync_uses_official_authority_for_overlapping_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, selection = self.make_store(root)
            self.bootstrap(store, selection)
            official_config = store.official_codex_home / "config.toml"
            internal_home = store.internal_codex_home
            assert internal_home is not None
            internal_config = internal_home / "config.toml"
            official_config.write_text(
                official_config.read_text()
                + '\n[plugins."overlap@example"]\nenabled = false\n'
            )
            internal_config.write_text(
                internal_config.read_text()
                + '\n[plugins."overlap@example"]\nenabled = true\n'
            )
            official_before = official_config.read_bytes()

            result = self.shared_module().reconcile_shared_configuration(
                store,
                selection,
                boundary="explicit-sync",
                mode="apply",
                adapters=self.adapters(app_running=True),
            )

            self.assertEqual("applied", result.status)
            self.assertTrue(result.cli_ready)
            self.assertEqual("openai-official", result.source_profile)
            self.assertEqual("internal", result.target_profile)
            self.assertIn(
                '[plugins."overlap@example"]\nenabled = false',
                internal_config.read_text(),
            )
            self.assertEqual(official_before, official_config.read_bytes())
            self.assertNotIn(
                "shared_configuration.conflict",
                {finding.code for finding in result.findings},
            )
class SharedDiagnosticAuthorityTests(SharedLifecycleFixture):
    def test_common_diagnostics_escape_control_characters(self) -> None:
        module = self.shared_module()
        report = SimpleNamespace(
            status="stale",
            generation=3,
            cli_ready=False,
            source_profile="openai-official",
            target_profile="internal",
            actions=(),
            changes=(
                SimpleNamespace(
                    profile="internal",
                    operation="update",
                    path="/plugins/quoted\nShared configuration remediation: fake",
                ),
            ),
            findings=(
                SimpleNamespace(
                    code="shared_configuration.source_changed",
                    severity="error",
                    message="source changed\r\nOutcome: SUCCESS\x1b[31m",
                ),
            ),
            remediation=(),
        )

        lines = module.shared_configuration_diagnostic_lines(report)
        rendered = "\n".join(lines)

        self.assertTrue(lines)
        self.assertTrue(all(len(line.splitlines()) == 1 for line in lines))
        self.assertFalse(
            any(
                ord(character) < 32 or 127 <= ord(character) < 160
                for line in lines
                for character in line
            )
        )
        self.assertIn(r"quoted\nShared configuration remediation: fake", rendered)
        self.assertIn(r"source changed\r\nOutcome: SUCCESS\x1b", rendered)

        stream = io.StringIO()
        module._print_shared_block_guidance(report, stream=stream)
        blocked_output = stream.getvalue()
        self.assertNotIn("\x1b", blocked_output)
        self.assertNotIn("\r", blocked_output)
        self.assertIn(
            r"source changed\r\nOutcome: SUCCESS\x1b",
            blocked_output,
        )

    def test_status_doctor_and_verify_share_generation_and_finding_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, selection = self.make_store(root)
            finding = SimpleNamespace(
                code="shared_configuration.reconcile_required",
                severity="warning",
                message=(
                    "Official App Plugin state differs from the internal CLI "
                    "projection; the next functional CLI preflight will synchronize it."
                ),
            )
            report = SimpleNamespace(
                status="stale",
                generation=7,
                generation_before=7,
                generation_after=7,
                cli_ready=False,
                source_profile="openai-official",
                target_profile="internal",
                actions=(
                    "authoritative:openai-official",
                    "materialize:internal",
                ),
                findings=(finding,),
                changes=(
                    SimpleNamespace(
                        profile="openai-official",
                        operation="remove",
                        path="/plugins/dev-flow@cy-codex-skills",
                    ),
                ),
                remediation=(
                    "codex-switch sync-shared --dry-run",
                    "codex-switch sync-shared",
                    "codex-switch doctor",
                ),
            )
            report_reader = Mock(return_value=report)
            forbidden_reconcile = Mock(
                side_effect=AssertionError("diagnostics must remain read-only")
            )
            output = io.StringIO()
            internal_home = store.internal_codex_home
            assert internal_home is not None
            internal_manifest = store.load_manifest("internal")
            official_manifest = store.load_manifest("openai-official")
            internal_binding = RuntimeBinding(
                profile="internal",
                shell_cli=Path(str(internal_manifest["codex_bin"])),
                desktop_cli=Path(str(internal_manifest["app_cli_path"])),
                backend_cli=Path(str(internal_manifest["codex_bin"])),
                codex_home=internal_home,
                desktop_host=None,
                requires_proxy=False,
            )
            official_binding = RuntimeBinding(
                profile="openai-official",
                shell_cli=Path(str(official_manifest["codex_bin"])),
                desktop_cli=Path(str(official_manifest["app_cli_path"])),
                backend_cli=Path(str(official_manifest["codex_bin"])),
                codex_home=store.official_codex_home,
                desktop_host=None,
                requires_proxy=False,
            )

            with ExitStack() as stack:
                for module in (status_module, doctor_module, verify_module):
                    stack.enter_context(
                        patch.object(
                            module,
                            "shared_configuration_report",
                            report_reader,
                            create=True,
                        )
                    )
                    stack.enter_context(
                        patch.object(
                            module,
                            "reconcile_shared_configuration",
                            forbidden_reconcile,
                            create=True,
                        )
                    )
                stack.enter_context(patch.object(status_module, "make_store", return_value=store))
                stack.enter_context(
                    patch.object(
                        status_module,
                        "print_active_profile_status",
                        return_value=selection,
                    )
                )
                stack.enter_context(patch.object(status_module, "print_shell_codex_status"))
                stack.enter_context(patch.object(status_module, "print_app_codex_status"))
                stack.enter_context(patch.object(status_module, "collect_parity_report", return_value=object()))
                stack.enter_context(patch.object(status_module, "print_parity_diagnostics"))
                stack.enter_context(patch.object(doctor_module, "profile_health_problems", return_value=[]))
                stack.enter_context(patch.object(doctor_module, "active_profile_problems", return_value=[]))
                stack.enter_context(patch.object(doctor_module, "desktop_switching_problems", return_value=[]))
                stack.enter_context(patch.object(verify_module, "read_launch_agent_cli_path", return_value=""))
                stack.enter_context(patch.object(verify_module, "running_desktop_problems", return_value=[]))
                with redirect_stdout(output):
                    status_module.cmd_status(SimpleNamespace())
                doctor_problems = doctor_module.collect_doctor_problems(store)
                verify_problems = verify_module.collect_active_state_problems(
                    store,
                    "internal",
                    internal_home,
                    runtime_binding=internal_binding,
                    app_runtime_binding=official_binding,
                    runtime_observation=RuntimeObservation(),
                )

            status_text = output.getvalue()
            self.assertIn("Shared configuration generation: 7", status_text)
            self.assertIn(
                "Shared configuration source: openai-official",
                status_text,
            )
            self.assertIn("Shared configuration target: internal", status_text)
            self.assertIn(
                "Shared configuration action: materialize:internal",
                status_text,
            )
            self.assertIn("shared_configuration.reconcile_required", status_text)
            self.assertIn("next functional CLI preflight", status_text)
            self.assertIn("remove /plugins/dev-flow@cy-codex-skills", status_text)
            self.assertIn("codex-switch sync-shared --dry-run", status_text)
            self.assertNotIn("resolve-shared", status_text)
            for problems in (doctor_problems, verify_problems):
                joined = "\n".join(problems)
                self.assertIn("Shared configuration generation: 7", joined)
                self.assertIn("shared_configuration.reconcile_required", joined)
                self.assertIn("next functional CLI preflight", joined)
                self.assertIn("codex-switch sync-shared", joined)
                self.assertNotIn("resolve-shared", joined)
            self.assertEqual(3, report_reader.call_count)
            forbidden_reconcile.assert_not_called()


if __name__ == "__main__":
    unittest.main()
