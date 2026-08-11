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
from contextlib import ExitStack, redirect_stdout
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
                "codex_bin": str(internal_bin),
                "app_cli_path": str(internal_bin),
            },
            "openai-official": {
                "name": "openai-official",
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
                "pending",
                "conflict",
                "materialization",
            ):
                self.assertIn(label, output)
            self.assertEqual(before, tree_snapshot(root))

    def test_running_app_records_pending_then_stopped_app_sync_applies(self) -> None:
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
            official_cache_before = tree_snapshot(store.official_codex_home / "plugins")
            internal_config.write_text(
                internal_config.read_text()
                + '\n[plugins."pending@example"]\nenabled = false\n'
            )

            pending = self.shared_module().reconcile_shared_configuration(
                store,
                selection,
                boundary="cli-preflight",
                mode="apply",
                adapters=self.adapters(app_running=True),
            )

            self.assertEqual("pending", pending.status)
            self.assertEqual("openai-official", pending.pending_target)
            self.assertTrue(pending.cli_ready)
            self.assertEqual(official_before, official_config.read_bytes())
            self.assertEqual(
                official_cache_before,
                tree_snapshot(store.official_codex_home / "plugins"),
            )

            applied = self.shared_module().reconcile_shared_configuration(
                store,
                selection,
                boundary="explicit-sync",
                mode="apply",
                adapters=self.adapters(app_running=False),
            )

            self.assertEqual("applied", applied.status)
            self.assertIsNone(applied.pending_target)
            self.assertIn(
                '[plugins."pending@example"]',
                official_config.read_text(),
            )
            report = self.shared_module().shared_configuration_report(
                store,
                selection,
            )
            self.assertEqual(applied.generation_after, report.generation)
            self.assertNotEqual("pending", report.status)

    def test_explicit_sync_conflict_is_zero_write(self) -> None:
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
                + '\n[plugins."conflict@example"]\nenabled = false\n'
            )
            internal_config.write_text(
                internal_config.read_text()
                + '\n[plugins."conflict@example"]\nenabled = true\n'
            )
            before = tree_snapshot(root)
            materialization_calls: list[dict[str, object]] = []

            result = self.shared_module().reconcile_shared_configuration(
                store,
                selection,
                boundary="explicit-sync",
                mode="apply",
                adapters=self.adapters(
                    app_running=False,
                    materialization_log=materialization_calls,
                ),
            )

            self.assertEqual("conflict", result.status)
            self.assertFalse(result.cli_ready)
            self.assertIn(
                "shared_configuration.conflict",
                {finding.code for finding in result.findings},
            )
            self.assertEqual([], materialization_calls)
            self.assertEqual(before, tree_snapshot(root))


class SharedDiagnosticAuthorityTests(SharedLifecycleFixture):
    def test_status_doctor_and_verify_share_generation_and_finding_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, selection = self.make_store(root)
            finding = SimpleNamespace(
                code="shared_configuration.conflict",
                severity="error",
                message="The App and CLI projections diverged.",
            )
            report = SimpleNamespace(
                status="conflict",
                generation=7,
                generation_before=7,
                generation_after=7,
                cli_ready=False,
                pending_target=None,
                findings=(finding,),
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
            self.assertIn("shared_configuration.conflict", status_text)
            for problems in (doctor_problems, verify_problems):
                joined = "\n".join(problems)
                self.assertIn("Shared configuration generation: 7", joined)
                self.assertIn("shared_configuration.conflict", joined)
            self.assertEqual(3, report_reader.call_count)
            forbidden_reconcile.assert_not_called()


if __name__ == "__main__":
    unittest.main()
