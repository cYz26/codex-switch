#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import inspect
import io
import json
import os
import signal
import shutil
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import codex_switch_verify as verify
from codex_switch_app_wrapper import write_profile_app_wrapper
from codex_switch_parity import (
    PARITY_POLICY_VERSION,
    InternalFingerprint,
    OfficialReference,
    ParityFinding,
    ParityPolicyVersion,
    ParityQueueItem,
    ParityReport,
)
from codex_switch_protocol_adapter import (
    BackendCapabilities,
    CapabilityReceipt,
    capability_receipt_path_for_launcher,
)
from codex_switch_runtime_binding import (
    CURRENT_CHATGPT_BUNDLE_ID,
    RuntimeBinding,
)
from codex_switch_selection import ProfileSelection
from codex_switch_store import Store


def write_script(path: Path, body: str) -> None:
    path.write_text(body)
    path.chmod(0o755)


def write_protocol_app_server(path: Path, mode: str) -> None:
    write_script(
        path,
        "#!/usr/bin/env python3\n"
        "import json\n"
        "import sys\n"
        f"mode = {mode!r}\n"
        "plugin_error = {\n"
        "    'id': 'plugin-list-smoke',\n"
        "    'error': {\n"
        "        'code': -32600,\n"
        "        'message': 'chatgpt authentication required for remote plugin catalog',\n"
        "    },\n"
        "}\n"
        "if mode == 'pre_init_plugin_auth':\n"
        "    print(json.dumps(plugin_error), flush=True)\n"
        "for raw in sys.stdin:\n"
        "    message = json.loads(raw)\n"
        "    method = message.get('method')\n"
        "    if method == 'initialize':\n"
        "        if mode == 'initialize_error':\n"
        "            response = {\n"
        "                'id': '__codex_initialize__',\n"
        "                'error': {'code': -32000, 'message': 'rejected'},\n"
        "            }\n"
        "        elif mode == 'initialize_missing_result':\n"
        "            response = {'id': '__codex_initialize__'}\n"
        "        else:\n"
        "            if mode == 'malformed_line':\n"
        "                print('not-json', flush=True)\n"
        "            elif mode == 'oversized_line':\n"
        "                print('X' * 131072, flush=True)\n"
        "            response = {\n"
        "                'id': '__codex_initialize__',\n"
        "                'result': {'userAgent': 'test'},\n"
        "            }\n"
        "        print(json.dumps(response), flush=True)\n"
        "    elif method == 'plugin/list':\n"
        "        print(json.dumps(plugin_error), flush=True)\n",
    )


def write_recording_protocol_app_server(path: Path, record_path: Path) -> None:
    write_script(
        path,
        "#!/usr/bin/env python3\n"
        "import json\n"
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n"
        f"record_path = Path({str(record_path)!r})\n"
        "if '--version' in sys.argv[1:]:\n"
        "    print('codex-cli 0.146.0')\n"
        "    raise SystemExit(0)\n"
        "record_path.write_text(json.dumps({\n"
        "    'args': sys.argv[1:],\n"
        "    'codex_home': os.environ.get('CODEX_HOME', ''),\n"
        "}))\n"
        "for raw in sys.stdin:\n"
        "    message = json.loads(raw)\n"
        "    method = message.get('method')\n"
        "    if method == 'initialize':\n"
        "        print(json.dumps({\n"
        "            'id': '__codex_initialize__',\n"
        "            'result': {'userAgent': 'test'},\n"
        "        }), flush=True)\n"
        "    elif method == 'plugin/list':\n"
        "        print(json.dumps({\n"
        "            'id': 'plugin-list-smoke',\n"
        "            'result': {'marketplaces': []},\n"
        "        }), flush=True)\n",
    )


class BoundedVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        if sys.version_info >= (3, 11):
            return
        python = shutil.which("python3.12") or shutil.which("python3.11")
        if python is None:
            self.fail("Python 3.11+ is required for verifier wrapper tests")
        environment = mock.patch.dict(
            os.environ,
            {"CODEX_SWITCH_PYTHON": python},
        )
        environment.start()
        self.addCleanup(environment.stop)

    def arrange_managed_internal_smoke(
        self,
        root: Path,
    ) -> tuple[
        Store,
        RuntimeBinding,
        Path,
        Path,
        Path,
        dict[str, object],
    ]:
        live = root / "live"
        live.mkdir(parents=True)
        store = Store(root / "store", live, root / "agent.plist")
        store.ensure()
        profile = store.profile_dir("internal")
        profile.mkdir(parents=True, exist_ok=True)
        home = store.managed_home("internal")
        home.mkdir(parents=True, exist_ok=True)
        (home / "config.toml").write_text('model = "test"\n')
        record_path = root / "backend-record.json"
        backend = root / "backend" / "codex"
        backend.parent.mkdir(parents=True)
        write_recording_protocol_app_server(backend, record_path)
        launcher = store.bin_dir / "codex-internal-app"
        receipt_path = capability_receipt_path_for_launcher(launcher)
        receipt = CapabilityReceipt(
            backend_sha256=hashlib.sha256(backend.read_bytes()).hexdigest(),
            schema_sha256="a" * 64,
            capabilities=BackendCapabilities(True, True, True),
            schema_version=2,
        )
        receipt_payload = (
            json.dumps(receipt.to_dict(), indent=2, sort_keys=True).encode()
            + b"\n"
        )
        receipt_path.write_bytes(receipt_payload)
        receipt_path.chmod(0o600)
        manifest: dict[str, object] = {
            "name": "internal",
            "codex_bin": str(backend),
            "codex_home": str(home),
            "app_cli_path": str(launcher),
            "runtime_binding": "canonical",
            "app_capability_receipt_path": str(receipt_path),
            "app_capability_receipt_sha256": hashlib.sha256(
                receipt_payload
            ).hexdigest(),
            "app_schema_sha256": receipt.schema_sha256,
        }
        manifest_path = store.manifest_path("internal")
        manifest_path.write_text(json.dumps(manifest) + "\n")
        write_profile_app_wrapper(
            store=store,
            name="internal",
            app_cli_path=str(launcher),
            codex_bin=str(backend),
            switch_scripts=Path(__file__).resolve().parent,
            capability_receipt_path=receipt_path,
            schema_sha256=receipt.schema_sha256,
            capability_receipt_sha256=str(
                manifest["app_capability_receipt_sha256"]
            ),
        )
        binding = RuntimeBinding(
            profile="internal",
            shell_cli=backend,
            desktop_cli=launcher,
            backend_cli=backend,
            codex_home=home,
            desktop_host=None,
            requires_proxy=True,
        )
        return (
            store,
            binding,
            backend,
            launcher,
            record_path,
            manifest,
        )

    def test_bounded_process_times_out_hanging_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            script = root / "hang.py"
            write_script(
                script,
                "#!/usr/bin/env python3\n"
                "import time\n"
                "print('ready', flush=True)\n"
                "while True:\n"
                "    time.sleep(0.1)\n",
            )

            started = time.monotonic()
            outcome = verify.run_bounded_process(
                [sys.executable, str(script)],
                kind="runtime smoke",
                timeout_seconds=0.5,
                terminate_grace_seconds=0.2,
                kill_grace_seconds=0.5,
            )

            self.assertEqual("failed", outcome.status)
            self.assertTrue(outcome.timed_out)
            self.assertIn("ready", outcome.stdout)
            self.assertLess(time.monotonic() - started, 2.0)

    def test_bounded_process_kills_term_resistant_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            script = root / "term-resistant.py"
            write_script(
                script,
                "#!/usr/bin/env python3\n"
                "import signal\n"
                "import time\n"
                "signal.signal(signal.SIGTERM, lambda *_: None)\n"
                "print('term-resistant-ready', flush=True)\n"
                "while True:\n"
                "    time.sleep(0.1)\n",
            )

            outcome = verify.run_bounded_process(
                [sys.executable, str(script)],
                kind="exec smoke",
                timeout_seconds=0.5,
                terminate_grace_seconds=0.1,
                kill_grace_seconds=0.5,
            )

            self.assertEqual("failed", outcome.status)
            self.assertTrue(outcome.timed_out)
            self.assertIn("term-resistant-ready", outcome.stdout)
            self.assertEqual(-signal.SIGKILL, outcome.returncode)

    def test_bounded_process_kills_descendant_holding_output_pipes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            child_pid_path = root / "child.pid"
            script = root / "parent.py"
            write_script(
                script,
                "#!/usr/bin/env python3\n"
                "import subprocess\n"
                "import sys\n"
                "import time\n"
                f"pid_path = {str(child_pid_path)!r}\n"
                "child = subprocess.Popen([\n"
                "    sys.executable,\n"
                "    '-c',\n"
                "    'import os, signal, time; '\n"
                "    f'open({pid_path!r}, \"w\").write(str(os.getpid())); '\n"
                "    'signal.signal(signal.SIGTERM, lambda *_: None); '\n"
                "    'time.sleep(60)',\n"
                "])\n"
                "for _ in range(100):\n"
                "    if __import__('pathlib').Path(pid_path).exists():\n"
                "        break\n"
                "    time.sleep(0.01)\n"
                "print('parent-exit', flush=True)\n",
            )

            outcome = verify.run_bounded_process(
                [sys.executable, str(script)],
                kind="runtime smoke",
                timeout_seconds=2.0,
                terminate_grace_seconds=0.1,
                kill_grace_seconds=0.2,
            )

            child_pid = int(child_pid_path.read_text())
            self.assertEqual("failed", outcome.status)
            self.assertTrue(outcome.timed_out)
            self.assertIn("parent-exit", outcome.stdout)
            deadline = time.monotonic() + 1.0
            while time.monotonic() < deadline:
                try:
                    os.kill(child_pid, 0)
                except ProcessLookupError:
                    break
                time.sleep(0.02)
            else:
                self.fail(f"descendant process remained alive: {child_pid}")

    def test_bounded_process_separates_and_bounds_malformed_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            script = root / "output.py"
            write_script(
                script,
                "#!/usr/bin/env python3\n"
                "import os\n"
                "os.write(1, b'OUT-BEGIN\\n' + b'A' * 50000 + b'\\xffOUT-END\\n')\n"
                "os.write(2, b'ERR-BEGIN\\n' + b'B' * 50000 + b'\\xfeERR-END\\n')\n"
                "raise SystemExit(7)\n",
            )

            outcome = verify.run_bounded_process(
                [str(script)],
                kind="runtime smoke",
                timeout_seconds=2.0,
                max_stream_bytes=256,
            )

            self.assertEqual("failed", outcome.status)
            self.assertEqual(7, outcome.returncode)
            self.assertTrue(outcome.stdout_truncated)
            self.assertTrue(outcome.stderr_truncated)
            self.assertIn("OUT-END", outcome.stdout)
            self.assertIn("ERR-END", outcome.stderr)
            self.assertNotIn("ERR-END", outcome.stdout)
            self.assertNotIn("OUT-END", outcome.stderr)
            self.assertLessEqual(len(outcome.stdout.encode()), 512)
            self.assertLessEqual(len(outcome.stderr.encode()), 512)

    def test_bounded_process_missing_binary_is_not_run(self) -> None:
        outcome = verify.run_bounded_process(
            ["/definitely/missing/codex-switch-test-binary"],
            kind="runtime smoke",
            timeout_seconds=0.1,
        )

        self.assertEqual("not_run", outcome.status)
        self.assertIsNone(outcome.returncode)
        self.assertFalse(outcome.timed_out)
        self.assertIn("not found", outcome.summary)

    def test_profile_command_returns_structured_bounded_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            script = root / "codex"
            write_script(
                script,
                "#!/usr/bin/env python3\n"
                "import os\n"
                "os.write(1, b'profile-stdout\\n')\n"
                "os.write(2, b'profile-stderr\\n')\n"
                "raise SystemExit(9)\n",
            )

            outcome = verify.run_profile_command(
                str(script),
                home,
                ["--version"],
                kind="runtime smoke",
                timeout_seconds=2.0,
            )

            self.assertIsInstance(outcome, verify.SmokeOutcome)
            self.assertEqual("failed", outcome.status)
            self.assertEqual(9, outcome.returncode)
            self.assertEqual("profile-stdout\n", outcome.stdout)
            self.assertEqual("profile-stderr\n", outcome.stderr)

    def test_runtime_smoke_missing_binary_is_not_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True)
            (profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "internal",
                        "codex_bin": "/definitely/missing/codex",
                    }
                )
            )

            problems, diagnostics, outcomes = verify.runtime_smoke_problems(
                store,
                "internal",
                live,
                runtime_smoke=True,
            )

            self.assertEqual([], diagnostics)
            self.assertTrue(problems)
            self.assertEqual(
                ["not_run", "not_run"],
                [outcome.status for outcome in outcomes],
            )
            self.assertTrue(
                all("not run" in outcome.summary for outcome in outcomes)
            )

    def test_runtime_smoke_uses_canonical_binding_backend(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True)
            home = store.managed_home("internal")
            home.mkdir(parents=True)
            (home / "config.toml").write_text('model = "test"\n')

            stale_log = root / "stale.log"
            canonical_log = root / "canonical.log"
            stale = root / "stale-codex"
            canonical = root / "canonical-codex"
            write_script(
                stale,
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> {stale_log}\n",
            )
            write_script(
                canonical,
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> {canonical_log}\n",
            )
            launcher = store.bin_dir / "codex-internal-app"
            (profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "internal",
                        "codex_bin": str(stale),
                        "app_cli_path": str(launcher),
                    }
                )
            )
            store.root.mkdir(exist_ok=True)
            store.active_path.write_text(
                json.dumps(
                    {
                        "profile": "internal",
                        "codex_home": str(home),
                        "shell_cli_path": str(canonical),
                        "app_cli_path": str(launcher),
                    }
                )
            )
            binding = RuntimeBinding(
                profile="internal",
                shell_cli=canonical,
                desktop_cli=launcher,
                backend_cli=canonical,
                codex_home=home,
                desktop_host=None,
                requires_proxy=True,
            )

            _, _, outcomes = verify.collect_verification_problems(
                store,
                "internal",
                runtime_smoke=True,
                runtime_binding=binding,
            )

            self.assertFalse(stale_log.exists())
            self.assertEqual(
                ["--version", "plugin list --json"],
                canonical_log.read_text().splitlines(),
            )
            self.assertEqual(
                [str(canonical), str(canonical)],
                [outcome.command[0] for outcome in outcomes],
            )

    def test_split_verifier_routes_cli_and_app_checks_to_distinct_bindings(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            internal_home = root / "internal-home"
            official_home = root / "official-home"
            internal_home.mkdir()
            official_home.mkdir()
            store = Store(root / "store", official_home, root / "agent.plist")
            store.ensure()
            internal_profile = store.profile_dir("internal")
            official_profile = store.profile_dir("openai-official")
            internal_profile.mkdir(parents=True)
            official_profile.mkdir(parents=True)
            internal_bin = root / "internal-codex"
            internal_app = root / "internal-app"
            official_bin = root / "official-codex"
            for path in (internal_bin, internal_app, official_bin):
                write_script(path, "#!/bin/sh\nexit 0\n")
            internal_manifest = {
                "name": "internal",
                "codex_bin": str(internal_bin),
                "app_cli_path": str(internal_app),
            }
            official_manifest = {
                "name": "openai-official",
                "codex_bin": str(official_bin),
                "app_cli_path": str(official_bin),
            }
            (internal_profile / "manifest.json").write_text(
                json.dumps(internal_manifest)
            )
            (official_profile / "manifest.json").write_text(
                json.dumps(official_manifest)
            )
            internal_binding = RuntimeBinding(
                profile="internal",
                shell_cli=internal_bin,
                desktop_cli=internal_app,
                backend_cli=internal_bin,
                codex_home=internal_home,
                desktop_host=None,
                requires_proxy=True,
            )
            official_binding = RuntimeBinding(
                profile="openai-official",
                shell_cli=official_bin,
                desktop_cli=official_bin,
                backend_cli=official_bin,
                codex_home=official_home,
                desktop_host=None,
                requires_proxy=False,
            )
            passed = verify.SmokeOutcome(
                status="passed",
                kind="runtime smoke",
                summary="passed",
                command=(str(internal_bin), "--version"),
                returncode=0,
                stdout="",
                stderr="",
                timed_out=False,
                stdout_truncated=False,
                stderr_truncated=False,
                duration_seconds=0.01,
            )

            with (
                mock.patch.object(
                    verify,
                    "run_profile_command",
                    return_value=passed,
                ) as run_cli,
                mock.patch.object(
                    verify,
                    "run_binding_app_server_smoke",
                    return_value=(0, "app-server smoke passed"),
                ) as run_app,
            ):
                problems, _diagnostics, outcomes = verify.runtime_smoke_problems(
                    store,
                    "internal",
                    internal_home,
                    app_server_smoke=True,
                    runtime_smoke=True,
                    runtime_binding=internal_binding,
                    app_runtime_binding=official_binding,
                )

            self.assertEqual([], problems)
            self.assertEqual(3, len(outcomes))
            self.assertTrue(
                all(call.args[0] == str(internal_bin) for call in run_cli.call_args_list)
            )
            self.assertTrue(
                all(call.args[1] == internal_home for call in run_cli.call_args_list)
            )
            self.assertIs(official_binding, run_app.call_args.args[0])
            observed_app_manifest = run_app.call_args.args[1]
            self.assertEqual(
                official_manifest["name"],
                observed_app_manifest["name"],
            )
            self.assertEqual(
                official_manifest["codex_bin"],
                observed_app_manifest["codex_bin"],
            )
            self.assertEqual(
                official_manifest["app_cli_path"],
                observed_app_manifest["app_cli_path"],
            )

    def test_cli_only_runtime_smoke_uses_managed_store_shim(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            internal_home = root / "internal-home"
            official_home = root / "official-home"
            internal_home.mkdir()
            official_home.mkdir()
            store = Store(
                root / "store",
                official_home,
                root / "agent.plist",
                internal_codex_home=internal_home,
            )
            store.ensure()
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True)
            backend = root / "internal-backend"
            write_script(
                backend,
                "#!/bin/sh\n"
                "printf 'raw backend smoke bypassed managed generation\\n' >&2\n"
                "exit 47\n",
            )
            shim_log = root / "managed-shim.log"
            managed_shim = store.bin_dir / "codex"
            write_script(
                managed_shim,
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> {str(shim_log)!r}\n"
                "case \"$*\" in\n"
                "  --version) printf 'codex-cli 2.0.0\\n' ;;\n"
                "  'plugin list --json') printf '{\"plugins\":[]}\\n' ;;\n"
                "  *) exit 48 ;;\n"
                "esac\n",
            )
            backend_sha256 = hashlib.sha256(backend.read_bytes()).hexdigest()
            (profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "internal",
                        "codex_bin": str(backend),
                        "codex_home": str(internal_home),
                        "app_cli_path": str(store.bin_dir / "codex-internal-app"),
                        "internal_cli_generation": {
                            "schema_version": 1,
                            "scope": "cli-only",
                            "backend_sha256": backend_sha256,
                            "backend_version": "2.0.0",
                        },
                        "internal_app_readiness": "unverified",
                    }
                )
            )
            binding = RuntimeBinding(
                profile="internal",
                shell_cli=backend,
                desktop_cli=store.bin_dir / "codex-internal-app",
                backend_cli=backend,
                codex_home=internal_home,
                desktop_host=None,
                requires_proxy=True,
            )

            problems, diagnostics, outcomes = verify.runtime_smoke_problems(
                store,
                "internal",
                internal_home,
                runtime_smoke=True,
                runtime_binding=binding,
            )

            self.assertEqual([], problems)
            self.assertEqual([], diagnostics)
            self.assertEqual(
                ["--version", "plugin list --json"],
                shim_log.read_text().splitlines(),
            )
            self.assertEqual(
                [str(managed_shim), str(managed_shim)],
                [outcome.command[0] for outcome in outcomes],
            )

    def test_split_active_verification_attests_official_app_and_internal_home(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            internal_home = root / "internal-home"
            official_home = root / "official-home"
            internal_home.mkdir()
            official_home.mkdir()
            store = Store(root / "store", official_home, root / "agent.plist")
            store.ensure()
            internal_profile = store.profile_dir("internal")
            official_profile = store.profile_dir("openai-official")
            internal_profile.mkdir(parents=True)
            official_profile.mkdir(parents=True)
            internal_bin = root / "internal-codex"
            internal_app = root / "internal-app"
            official_bin = root / "official-codex"
            for path in (internal_bin, internal_app, official_bin):
                write_script(path, "#!/bin/sh\nexit 0\n")
            (internal_profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "internal",
                        "codex_bin": str(internal_bin),
                        "app_cli_path": str(internal_app),
                    }
                )
            )
            (official_profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "openai-official",
                        "codex_bin": str(official_bin),
                        "app_cli_path": str(official_bin),
                    }
                )
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
            internal_binding = RuntimeBinding(
                profile="internal",
                shell_cli=internal_bin,
                desktop_cli=internal_app,
                backend_cli=internal_bin,
                codex_home=internal_home,
                desktop_host=None,
                requires_proxy=True,
            )
            official_binding = RuntimeBinding(
                profile="openai-official",
                shell_cli=official_bin,
                desktop_cli=official_bin,
                backend_cli=official_bin,
                codex_home=official_home,
                desktop_host=None,
                requires_proxy=False,
            )
            observation = verify.RuntimeObservation(
                gui_app_cli=str(official_bin),
                launch_agent_cli=str(official_bin),
            )

            problems = verify.collect_active_state_problems(
                store,
                "internal",
                internal_home,
                runtime_binding=internal_binding,
                app_runtime_binding=official_binding,
                runtime_observation=observation,
            )

            self.assertEqual([], problems)

    def test_malformed_active_selection_blocks_all_runtime_smokes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "official-home"
            home.mkdir()
            (home / "config.toml").write_text('model = "test"\n')
            store = Store(root / "store", home, root / "agent.plist")
            store.ensure()
            profile = store.profile_dir("openai-official")
            profile.mkdir(parents=True)
            binary = root / "official-codex"
            write_script(binary, "#!/bin/sh\nexit 0\n")
            (profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "openai-official",
                        "codex_bin": str(binary),
                        "app_cli_path": str(binary),
                    }
                )
            )
            store.active_path.write_text(
                json.dumps(
                    {
                        "profile": "openai-official",
                        "cli_profile": "openai-official",
                        "codex_home": str(home),
                    }
                )
            )
            binding = RuntimeBinding(
                profile="openai-official",
                shell_cli=binary,
                desktop_cli=binary,
                backend_cli=binary,
                codex_home=home,
                desktop_host=None,
                requires_proxy=False,
            )

            with mock.patch.object(
                verify,
                "runtime_smoke_problems",
                return_value=([], [], []),
            ) as run_smokes:
                problems, _diagnostics, outcomes = (
                    verify.collect_verification_problems(
                        store,
                        "openai-official",
                        app_server_smoke=True,
                        runtime_smoke=True,
                        exec_smoke="printf should-not-run",
                        responses_tool_smoke=True,
                        runtime_binding=binding,
                    )
                )

            self.assertTrue(
                any("active.selection.partial" in problem for problem in problems),
                problems,
            )
            run_smokes.assert_not_called()
            self.assertEqual([], outcomes)

            args = argparse.Namespace(
                name="openai-official",
                repair="safe",
                app_server_smoke=True,
                runtime_smoke=True,
                exec_smoke="printf should-not-run",
                responses_tool_smoke=True,
                report=False,
            )
            with (
                mock.patch.object(verify, "make_store", return_value=store),
                mock.patch.object(verify, "profile_home", return_value=home),
                mock.patch.object(verify, "run_safe_repair", return_value=[]) as repair,
                mock.patch.object(
                    verify,
                    "collect_store_runtime_observation",
                    return_value=None,
                ) as observe,
                mock.patch.object(
                    verify,
                    "runtime_smoke_problems",
                    return_value=([], [], []),
                ) as cmd_smokes,
                redirect_stdout(io.StringIO()),
            ):
                with self.assertRaises(SystemExit) as raised:
                    verify.cmd_verify(args)

            self.assertEqual(1, raised.exception.code)
            repair.assert_not_called()
            observe.assert_not_called()
            cmd_smokes.assert_not_called()

    def test_app_server_smoke_uses_managed_desktop_chain_and_temp_home(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (
                store,
                binding,
                _backend,
                launcher,
                record_path,
                _manifest,
            ) = self.arrange_managed_internal_smoke(root)

            problems, diagnostics, outcomes = verify.runtime_smoke_problems(
                store,
                "internal",
                binding.codex_home,
                app_server_smoke=True,
                runtime_binding=binding,
            )

            self.assertEqual([], problems)
            self.assertEqual([], diagnostics)
            self.assertEqual(1, len(outcomes))
            self.assertEqual("passed", outcomes[0].status)
            self.assertEqual(str(launcher), outcomes[0].command[0])
            backend_record = json.loads(record_path.read_text())
            self.assertEqual(verify.app_server_smoke_args(), backend_record["args"])
            smoke_home = Path(backend_record["codex_home"])
            self.assertNotEqual(binding.codex_home, smoke_home)
            self.assertIn("codex-switch-app-server-smoke-", smoke_home.parent.name)

    def test_app_server_smoke_rejects_managed_receipt_drift(self) -> None:
        cases = (
            "manifest_path",
            "payload",
            "schema",
            "backend",
            "wrapper_path",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (
                    store,
                    binding,
                    backend,
                    launcher,
                    record_path,
                    manifest,
                ) = self.arrange_managed_internal_smoke(root)
                manifest_path = store.manifest_path("internal")
                receipt_path = capability_receipt_path_for_launcher(launcher)
                if case == "manifest_path":
                    manifest["app_capability_receipt_path"] = str(
                        root / "other-receipt.json"
                    )
                    manifest_path.write_text(json.dumps(manifest) + "\n")
                elif case == "payload":
                    receipt_path.write_bytes(receipt_path.read_bytes() + b" ")
                elif case == "schema":
                    manifest["app_schema_sha256"] = "b" * 64
                    manifest_path.write_text(json.dumps(manifest) + "\n")
                elif case == "backend":
                    backend.write_text(backend.read_text() + "\n# backend drift\n")
                else:
                    alternate = root / "alternate-receipt.json"
                    alternate.write_bytes(receipt_path.read_bytes())
                    alternate.chmod(0o600)
                    write_profile_app_wrapper(
                        store=store,
                        name="internal",
                        app_cli_path=str(launcher),
                        codex_bin=str(backend),
                        switch_scripts=Path(__file__).resolve().parent,
                        capability_receipt_path=alternate,
                        schema_sha256=str(manifest["app_schema_sha256"]),
                        capability_receipt_sha256=str(
                            manifest["app_capability_receipt_sha256"]
                        ),
                    )

                problems, diagnostics, outcomes = verify.runtime_smoke_problems(
                    store,
                    "internal",
                    binding.codex_home,
                    app_server_smoke=True,
                    runtime_binding=binding,
                )

                self.assertEqual([], diagnostics)
                self.assertTrue(problems)
                self.assertEqual("failed", outcomes[0].status)
                self.assertIn("capability receipt", "\n".join(problems))
                if case != "wrapper_path":
                    self.assertFalse(record_path.exists())

    def test_app_server_smoke_rejects_proxy_child_binding_drift(self) -> None:
        for case in ("backend", "args"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (
                    store,
                    binding,
                    _backend,
                    launcher,
                    _record_path,
                    manifest,
                ) = self.arrange_managed_internal_smoke(root)

                def fake_smoke(
                    codex_bin: str,
                    home: Path,
                    *,
                    extra_env: dict[str, str] | None = None,
                    **_kwargs,
                ) -> tuple[int, str]:
                    self.assertEqual(str(launcher), codex_bin)
                    assert extra_env is not None
                    child_path = Path(
                        extra_env["CODEX_SWITCH_PROXY_CHILD_RECEIPT"]
                    )
                    child_path.write_text(
                        json.dumps(
                            {
                                "codex_bin": (
                                    str(root / "wrong-backend")
                                    if case == "backend"
                                    else str(binding.backend_cli)
                                ),
                                "args": (
                                    ["app-server", "--wrong"]
                                    if case == "args"
                                    else verify.app_server_smoke_args()
                                ),
                                "codex_home": str(home),
                                "capability_receipt_path": str(
                                    capability_receipt_path_for_launcher(
                                        launcher
                                    )
                                ),
                                "expected_schema_sha256": manifest[
                                    "app_schema_sha256"
                                ],
                                "expected_receipt_sha256": manifest[
                                    "app_capability_receipt_sha256"
                                ],
                                "config_write_proven": True,
                            }
                        )
                    )
                    return 0, "app-server smoke passed"

                with mock.patch.object(
                    verify,
                    "run_app_server_smoke",
                    side_effect=fake_smoke,
                ):
                    problems, diagnostics, outcomes = (
                        verify.runtime_smoke_problems(
                            store,
                            "internal",
                            binding.codex_home,
                            app_server_smoke=True,
                            runtime_binding=binding,
                        )
                    )

                self.assertEqual([], diagnostics)
                self.assertEqual("failed", outcomes[0].status)
                self.assertTrue(problems)
                self.assertIn(
                    f"child {'backend' if case == 'backend' else 'arguments'} drift",
                    "\n".join(problems),
                )

    def test_canonical_runtime_smoke_stops_when_binding_resolution_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            store.ensure()
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True)
            home = store.managed_home("internal")
            home.mkdir(parents=True)
            (home / "config.toml").write_text('model = "test"\n')

            invocation_log = root / "recursive.log"
            recursive_backend = store.bin_dir / "codex"
            write_script(
                recursive_backend,
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$*\" >> {invocation_log}\n",
            )
            launcher = store.bin_dir / "codex-internal-app"
            (profile / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "internal",
                        "codex_bin": str(recursive_backend),
                        "app_cli_path": str(launcher),
                    }
                )
            )

            problems, _, outcomes = verify.collect_verification_problems(
                store,
                "internal",
                runtime_smoke=True,
            )

            self.assertTrue(
                any("binding.internal.recursive_backend" in item for item in problems)
            )
            self.assertFalse(invocation_log.exists())
            self.assertEqual([], outcomes)

    def test_report_records_structured_smoke_outcomes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            outcome = verify.SmokeOutcome(
                status="failed",
                kind="runtime smoke",
                summary="runtime smoke timed out after 1s",
                command=("/fake/codex", "--version"),
                returncode=-signal.SIGKILL,
                stdout="",
                stderr="",
                timed_out=True,
                stdout_truncated=False,
                stderr_truncated=False,
                duration_seconds=1.25,
            )

            path = verify.write_verification_report(
                store,
                name="internal",
                repair="none",
                app_server_smoke=False,
                runtime_smoke=True,
                exec_smoke=None,
                responses_tool_smoke=False,
                problems=[outcome.summary],
                smoke_diagnostics=[],
                repair_messages=[],
                smoke_outcomes=[outcome],
            )

            report = json.loads(path.read_text())
            self.assertEqual(
                [
                    {
                        "status": "failed",
                        "kind": "runtime smoke",
                        "summary": "runtime smoke timed out after 1s",
                        "returncode": -signal.SIGKILL,
                        "timed_out": True,
                        "stdout_truncated": False,
                        "stderr_truncated": False,
                        "duration_seconds": 1.25,
                    }
                ],
                report["smoke_outcomes"],
            )

    def test_sanitizer_redacts_secrets_and_preserves_safe_routing(self) -> None:
        raw = (
            "Authorization: Bearer auth-secret\n"
            "Bearer standalone-secret\n"
            "api-key: api-secret\n"
            "OPENAI_API_KEY=env-secret\n"
            "Cookie: session=cookie-secret\n"
            "https://example.test/path?sig=signed-secret&safe=value\n"
            "exception: password=exception-secret\n"
            "x-account-id: safe-route-123\n"
            "x-model-request-id: safe-request-456\n"
        )

        sanitized = verify.sanitize_external_text(raw)

        for secret in (
            "auth-secret",
            "standalone-secret",
            "api-secret",
            "env-secret",
            "cookie-secret",
            "signed-secret",
            "exception-secret",
        ):
            self.assertNotIn(secret, sanitized)
        self.assertIn("x-account-id: safe-route-123", sanitized)
        self.assertIn("x-model-request-id: safe-request-456", sanitized)
        self.assertIn("[REDACTED]", sanitized)

    def test_report_sanitizes_exception_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")

            path = verify.write_verification_report(
                store,
                name="internal",
                repair="none",
                app_server_smoke=False,
                runtime_smoke=False,
                exec_smoke="prompt-secret",
                responses_tool_smoke=False,
                problems=[
                    "exception Authorization: Bearer exception-secret",
                    "x-account-id: safe-route-123",
                ],
                smoke_diagnostics=[],
                repair_messages=["Cookie: session=repair-secret"],
            )

            report_text = path.read_text()
            self.assertNotIn("prompt-secret", report_text)
            self.assertNotIn("exception-secret", report_text)
            self.assertNotIn("repair-secret", report_text)
            self.assertIn("safe-route-123", report_text)

    def test_app_server_initialize_error_is_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            backend = root / "codex"
            write_protocol_app_server(backend, "initialize_error")

            code, output = verify.run_app_server_smoke(str(backend), home)

            self.assertNotEqual(0, code)
            self.assertIn("initialize", output)
            self.assertIn("error", output)

    def test_app_server_initialize_missing_result_is_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            backend = root / "codex"
            write_protocol_app_server(backend, "initialize_missing_result")

            code, output = verify.run_app_server_smoke(str(backend), home)

            self.assertNotEqual(0, code)
            self.assertIn("neither result nor error", output)

    def test_app_server_malformed_line_is_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            backend = root / "codex"
            write_protocol_app_server(backend, "malformed_line")

            code, output = verify.run_app_server_smoke(str(backend), home)

            self.assertNotEqual(0, code)
            self.assertIn("malformed", output)

    def test_app_server_oversized_line_is_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            backend = root / "codex"
            write_protocol_app_server(backend, "oversized_line")

            code, output = verify.run_app_server_smoke(str(backend), home)

            self.assertNotEqual(0, code)
            self.assertIn("oversized", output)

    def test_app_server_pre_initialize_plugin_auth_is_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            backend = root / "codex"
            write_protocol_app_server(backend, "pre_init_plugin_auth")

            code, output = verify.run_app_server_smoke(str(backend), home)

            self.assertNotEqual(0, code)
            self.assertIn("before initialize", output)

    def test_app_server_post_initialize_plugin_auth_is_permitted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            home = root / "home"
            home.mkdir()
            backend = root / "codex"
            write_protocol_app_server(backend, "post_init_plugin_auth")

            code, output = verify.run_app_server_smoke(str(backend), home)

            self.assertEqual(0, code, output)

    def test_verification_reports_are_unique_and_no_clobber(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            common = {
                "name": "internal",
                "repair": "none",
                "app_server_smoke": False,
                "runtime_smoke": False,
                "exec_smoke": None,
                "responses_tool_smoke": False,
                "problems": [],
                "smoke_diagnostics": [],
                "repair_messages": [],
            }

            first = verify.write_verification_report(store, **common)
            second = verify.write_verification_report(store, **common)

            self.assertNotEqual(first, second)
            self.assertTrue(first.exists())
            self.assertTrue(second.exists())
            self.assertEqual(2, len(list(first.parent.glob("*-internal.json"))))


class ParityVerificationTests(unittest.TestCase):
    def make_store_and_binding(
        self,
        root: Path,
    ) -> tuple[Store, RuntimeBinding]:
        live = root / "live"
        live.mkdir()
        store = Store(root / "store", live, root / "agent.plist")
        binding = RuntimeBinding(
            profile="internal",
            shell_cli=root / "internal" / "codex",
            desktop_cli=root / "store" / "bin" / "codex-internal-app",
            backend_cli=root / "internal" / "codex",
            codex_home=root / "store" / "homes" / "internal",
            desktop_host=None,
            requires_proxy=True,
        )
        return store, binding

    def make_report(
        self,
        root: Path,
        *,
        findings: tuple[ParityFinding, ...] = (),
        queue: tuple[ParityQueueItem, ...] = (),
    ) -> ParityReport:
        bundle_root = root / "Applications" / "ChatGPT.app"
        return ParityReport(
            healthy=not any(
                finding.severity == "error"
                for finding in findings
            ),
            policy_version=ParityPolicyVersion(PARITY_POLICY_VERSION),
            official_reference=OfficialReference(
                authority="chatgpt-bundle",
                bundle_root=bundle_root,
                bundle_id=CURRENT_CHATGPT_BUNDLE_ID,
                bundle_version="1.2026.196",
                bundled_cli=(
                    bundle_root / "Contents" / "Resources" / "codex"
                ),
                cli_version="0.146.0-alpha.3.1",
                binary_sha256="a" * 64,
                schema_sha256="b" * 64,
                feature_inventory_sha256="c" * 64,
            ),
            internal_fingerprint=InternalFingerprint(
                backend_cli=root / "internal" / "codex",
                cli_version="0.144.6",
                binary_sha256="d" * 64,
                active_model="gpt-5.6-sol",
                provider_id="azure",
                wire_api="responses",
                endpoint_sha256="e" * 64,
                auth_source_kind="env",
                capability_receipt_sha256="f" * 64,
                source_catalog=root / "internal" / "models.json",
                source_catalog_sha256="a" * 64,
                config_sha256s=(
                    ("profile", "b" * 64),
                    ("runtime", "c" * 64),
                ),
            ),
            findings=findings,
            synchronization_queue=queue,
        )

    def collect_with_report(
        self,
        store: Store,
        binding: RuntimeBinding,
        report: ParityReport,
    ) -> tuple[
        list[str],
        list[dict[str, object]],
        list[verify.SmokeOutcome],
    ]:
        self.assertIn(
            "parity_report",
            inspect.signature(
                verify.collect_verification_problems
            ).parameters,
            "Verifier collection must accept one preloaded parity report.",
        )
        with (
            mock.patch.object(
                verify,
                "collect_active_state_problems",
                return_value=[],
            ),
            mock.patch.object(
                verify,
                "collect_runtime_config_problems",
                return_value=[],
            ),
            mock.patch.object(
                verify,
                "collect_parity_report",
                side_effect=AssertionError(
                    "supplied parity report must not be loaded twice"
                ),
                create=True,
            ),
        ):
            return verify.collect_verification_problems(
                store,
                "internal",
                runtime_binding=binding,
                parity_report=report,
            )

    def parity_diagnostic(
        self,
        diagnostics: list[dict[str, object]],
    ) -> dict[str, object]:
        matches = [
            item
            for item in diagnostics
            if item.get("kind") == "parity"
        ]
        self.assertEqual(1, len(matches))
        return matches[0]

    def test_collect_parity_report_marks_missing_receipt_unhealthy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            store.ensure()
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True, exist_ok=True)
            store.manifest_path("internal").write_text(
                json.dumps({"name": "internal"}) + "\n"
            )

            report = verify.collect_parity_report(store, binding)

            self.assertFalse(report.healthy)
            self.assertEqual(
                ["parity.receipt.missing"],
                [finding.code for finding in report.findings],
            )

    def test_evidence_failures_preserve_stable_finding_codes(self) -> None:
        cases = (
            ("receipt", "parity.receipt.missing", "receipt is missing"),
            ("receipt", "parity.receipt.malformed", "receipt is malformed"),
            ("reference", "parity.reference.stale", "reference is stale"),
            ("runtime", "parity.receipt.stale", "runtime is stale"),
            ("provider", "parity.receipt.stale", "provider is stale"),
            ("config", "parity.config.source_stale", "config is stale"),
            ("overlay", "parity.overlay.source_stale", "overlay is stale"),
            (
                "adapter",
                "parity.preparation.adapter_stale",
                "adapter is stale",
            ),
        )
        findings = tuple(
            ParityFinding(
                category=category,
                code=code,
                severity="error",
                message=message,
            )
            for category, code, message in cases
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            report = self.make_report(root, findings=findings)

            problems, diagnostics, outcomes = self.collect_with_report(
                store,
                binding,
                report,
            )

            self.assertEqual([], outcomes)
            self.assertEqual(
                [f"{finding.code}: {finding.message}" for finding in findings],
                problems,
            )
            parity = self.parity_diagnostic(diagnostics)
            self.assertFalse(parity["healthy"])
            self.assertEqual(
                [finding.code for finding in findings],
                [
                    item["code"]
                    for item in parity["findings"]
                ],
            )

    def test_core_unclassified_and_probe_failures_are_unhealthy(self) -> None:
        findings = (
            ParityFinding(
                category="protocol",
                code="parity.protocol.core_incompatible",
                severity="error",
                message="core protocol is incompatible",
            ),
            ParityFinding(
                category="feature",
                code="parity.feature.unclassified_drift",
                severity="error",
                message="feature drift is unclassified",
            ),
            ParityFinding(
                category="probe",
                code="parity.probe.v1_fallback",
                severity="error",
                message="typed-role probe fell back to v1",
            ),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            report = self.make_report(root, findings=findings)

            problems, diagnostics, _outcomes = self.collect_with_report(
                store,
                binding,
                report,
            )

            self.assertEqual(
                [f"{finding.code}: {finding.message}" for finding in findings],
                problems,
            )
            self.assertFalse(self.parity_diagnostic(diagnostics)["healthy"])

    def test_optional_only_queue_is_healthy_and_deterministic(self) -> None:
        findings = (
            ParityFinding(
                category="protocol",
                code="parity.protocol.optional_missing",
                severity="warning",
                message="optional protocol method is absent",
            ),
            ParityFinding(
                category="feature",
                code="parity.feature.optional_missing",
                severity="warning",
                message="optional feature is absent",
            ),
        )
        queue = (
            ParityQueueItem(
                category="protocol",
                identifier="client_request:app/read",
                finding_code="parity.protocol.optional_missing",
            ),
            ParityQueueItem(
                category="feature",
                identifier="skill_search",
                finding_code="parity.feature.optional_missing",
            ),
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            report = self.make_report(
                root,
                findings=findings,
                queue=queue,
            )

            problems, diagnostics, outcomes = self.collect_with_report(
                store,
                binding,
                report,
            )

            self.assertEqual([], problems)
            self.assertEqual([], outcomes)
            parity = self.parity_diagnostic(diagnostics)
            self.assertTrue(parity["healthy"])
            queue_rows = parity["synchronization_queue"]
            self.assertEqual(
                sorted(
                    queue_rows,
                    key=lambda item: (
                        item["category"],
                        item["identifier"],
                        item["finding_code"],
                    ),
                ),
                queue_rows,
            )
            self.assertEqual(
                {
                    "parity.feature.optional_missing",
                    "parity.protocol.optional_missing",
                },
                {
                    item["finding_code"]
                    for item in queue_rows
                },
            )

    def test_report_sanitizes_parity_messages_and_keeps_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, _binding = self.make_store_and_binding(root)
            report = self.make_report(
                root,
                findings=(
                    ParityFinding(
                        category="probe",
                        code="parity.probe.v1_fallback",
                        severity="error",
                        message=(
                            "Authorization: Bearer parity-report-secret"
                        ),
                    ),
                ),
                queue=(
                    ParityQueueItem(
                        category="feature",
                        identifier="skill_search",
                        finding_code="parity.feature.optional_missing",
                    ),
                ),
            )
            self.assertIn(
                "parity_report",
                inspect.signature(
                    verify.write_verification_report
                ).parameters,
                "Structured reports must accept the collected parity report.",
            )

            path = verify.write_verification_report(
                store,
                name="internal",
                repair="none",
                app_server_smoke=False,
                runtime_smoke=False,
                exec_smoke=None,
                responses_tool_smoke=False,
                problems=[
                    "parity.probe.v1_fallback: typed-role probe failed"
                ],
                smoke_diagnostics=[],
                repair_messages=[],
                parity_report=report,
            )

            payload = path.read_text()
            document = json.loads(payload)
            self.assertNotIn("parity-report-secret", payload)
            self.assertEqual(
                "parity.probe.v1_fallback",
                document["parity"]["findings"][0]["code"],
            )
            self.assertEqual(
                "skill_search",
                document["parity"]["synchronization_queue"][0]["identifier"],
            )

    def test_repair_none_parity_verification_has_zero_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            store.ensure()
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True, exist_ok=True)
            binding.codex_home.mkdir(parents=True, exist_ok=True)
            (binding.codex_home / "config.toml").write_text(
                'model = "test"\n'
            )
            store.manifest_path("internal").write_text("{}\n")
            report = self.make_report(
                root,
                findings=(
                    ParityFinding(
                        category="receipt",
                        code="parity.receipt.missing",
                        severity="error",
                        message="receipt is missing",
                    ),
                ),
            )

            def snapshot() -> tuple[tuple[str, int, bytes], ...]:
                rows: list[tuple[str, int, bytes]] = []
                for path in sorted(store.root.rglob("*")):
                    if path.is_file():
                        rows.append(
                            (
                                str(path.relative_to(store.root)),
                                path.stat().st_mode,
                                path.read_bytes(),
                            )
                        )
                return tuple(rows)

            before = snapshot()
            args = argparse.Namespace(
                name="internal",
                repair="none",
                app_server_smoke=False,
                runtime_smoke=False,
                exec_smoke=None,
                responses_tool_smoke=False,
                report=False,
            )
            output = io.StringIO()
            with (
                mock.patch.object(verify, "make_store", return_value=store),
                mock.patch.object(
                    verify,
                    "profile_home",
                    return_value=binding.codex_home,
                ),
                mock.patch.object(
                    verify,
                    "manifest_uses_canonical_binding",
                    return_value=False,
                ),
                mock.patch.object(
                    verify,
                    "collect_store_runtime_observation",
                    return_value=None,
                ),
                mock.patch.object(
                    verify,
                    "collect_active_state_problems",
                    return_value=[],
                ),
                mock.patch.object(
                    verify,
                    "collect_runtime_config_problems",
                    return_value=[],
                ),
                mock.patch.object(
                    verify,
                    "collect_parity_report",
                    return_value=report,
                    create=True,
                ) as collect_parity,
                redirect_stdout(output),
            ):
                with self.assertRaises(SystemExit) as raised:
                    verify.cmd_verify(args)

            self.assertEqual(1, raised.exception.code)
            collect_parity.assert_called_once()
            self.assertIn("parity.receipt.missing", output.getvalue())
            self.assertEqual(before, snapshot())

    def test_explicit_parity_repair_uses_current_backend_set_bin(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            args = argparse.Namespace(
                store_dir=store.root,
                official_codex_home=store.official_codex_home,
                official_codex_home_source="explicit",
                internal_codex_home=store.internal_codex_home,
                internal_codex_home_source="explicit",
                launch_agent_path=store.launch_agent_path,
                launch_agent_label=store.launch_agent_label,
                name="internal",
                repair="safe",
            )
            self.assertTrue(
                hasattr(verify, "repair_internal_parity"),
                "Explicit parity repair must delegate to staged internal rebind.",
            )

            with mock.patch(
                "codex_switch_bindings.cmd_set_bin",
                return_value=object(),
            ) as set_bin:
                verify.repair_internal_parity(args, binding)

            set_bin.assert_called_once()
            rebind_args = set_bin.call_args.args[0]
            self.assertEqual("internal", rebind_args.name)
            self.assertEqual(str(binding.backend_cli), rebind_args.codex_bin)
            self.assertFalse(rebind_args.preserve_app_cli)

    def test_verify_uses_one_active_selection_snapshot_for_parity_owner(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            store.ensure()
            for profile_name in ("internal", "openai-official"):
                profile = store.profile_dir(profile_name)
                profile.mkdir(parents=True, exist_ok=True)
                store.manifest_path(profile_name).write_text("{}\n")
            binding.codex_home.mkdir(parents=True, exist_ok=True)
            (binding.codex_home / "config.toml").write_text(
                'model = "test"\n'
            )
            current = {
                "profile": "internal",
                "cli_profile": "internal",
                "app_profile": "internal",
                "codex_home": str(binding.codex_home),
            }
            store.active_path.write_text(json.dumps(current) + "\n")
            split = {
                **current,
                "app_profile": "openai-official",
            }
            snapshot = SimpleNamespace(
                record=split,
                selection=ProfileSelection(
                    cli_profile="internal",
                    app_profile="openai-official",
                ),
                problem=None,
                payload=(json.dumps(split) + "\n").encode(),
            )
            args = argparse.Namespace(
                name="internal",
                repair="none",
                app_server_smoke=False,
                runtime_smoke=False,
                exec_smoke=None,
                responses_tool_smoke=False,
                report=False,
            )
            output = io.StringIO()
            with (
                mock.patch.object(verify, "make_store", return_value=store),
                mock.patch.object(
                    verify,
                    "profile_home",
                    return_value=binding.codex_home,
                ),
                mock.patch.object(
                    verify,
                    "read_active_profile_selection_snapshot",
                    return_value=snapshot,
                    create=True,
                ) as read_snapshot,
                mock.patch.object(
                    verify,
                    "manifest_uses_canonical_binding",
                    return_value=False,
                ),
                mock.patch.object(
                    verify,
                    "collect_store_runtime_observation",
                    return_value=None,
                ),
                mock.patch.object(
                    verify,
                    "collect_verification_problems",
                    return_value=([], [], []),
                ),
                mock.patch.object(
                    verify,
                    "collect_parity_report",
                    side_effect=AssertionError(
                        "split snapshot must not collect internal App parity"
                    ),
                ) as collect_parity,
                redirect_stdout(output),
            ):
                verify.cmd_verify(args)

            read_snapshot.assert_called_once_with(
                store.active_path,
                fallback_cli_profile="internal",
            )
            collect_parity.assert_not_called()
            self.assertIn(
                "Internal App parity: not applicable "
                "(App profile: openai-official)",
                output.getvalue(),
            )

    def test_safe_repair_rechecks_parity_after_staged_rebind(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            store, binding = self.make_store_and_binding(root)
            store.ensure()
            profile = store.profile_dir("internal")
            profile.mkdir(parents=True, exist_ok=True)
            binding.codex_home.mkdir(parents=True, exist_ok=True)
            (binding.codex_home / "config.toml").write_text(
                'model = "test"\n'
            )
            store.manifest_path("internal").write_text("{}\n")
            unhealthy = self.make_report(
                root,
                findings=(
                    ParityFinding(
                        category="receipt",
                        code="parity.receipt.missing",
                        severity="error",
                        message="receipt is missing",
                    ),
                ),
            )
            healthy = self.make_report(root)
            args = argparse.Namespace(
                store_dir=store.root,
                official_codex_home=store.official_codex_home,
                official_codex_home_source="explicit",
                internal_codex_home=store.internal_codex_home,
                internal_codex_home_source="explicit",
                launch_agent_path=store.launch_agent_path,
                launch_agent_label=store.launch_agent_label,
                name="internal",
                repair="safe",
                app_server_smoke=False,
                runtime_smoke=False,
                exec_smoke=None,
                responses_tool_smoke=False,
                report=False,
            )
            output = io.StringIO()
            with (
                mock.patch.object(verify, "make_store", return_value=store),
                mock.patch.object(
                    verify,
                    "profile_home",
                    return_value=binding.codex_home,
                ),
                mock.patch.object(verify, "run_safe_repair", return_value=[]),
                mock.patch.object(
                    verify,
                    "manifest_uses_canonical_binding",
                    return_value=True,
                ),
                mock.patch.object(
                    verify,
                    "resolve_store_runtime_binding",
                    return_value=binding,
                ),
                mock.patch.object(
                    verify,
                    "collect_store_runtime_observation",
                    return_value=None,
                ),
                mock.patch.object(
                    verify,
                    "collect_active_state_problems",
                    return_value=[],
                ),
                mock.patch.object(
                    verify,
                    "collect_runtime_config_problems",
                    return_value=[],
                ),
                mock.patch.object(
                    verify,
                    "collect_parity_report",
                    side_effect=(unhealthy, healthy),
                ) as collect_parity,
                mock.patch.object(
                    verify,
                    "repair_internal_parity",
                    create=True,
                ) as repair_parity,
                redirect_stdout(output),
            ):
                try:
                    verify.cmd_verify(args)
                except SystemExit as exc:
                    code = int(exc.code)
                else:
                    code = 0

            self.assertEqual(0, code, output.getvalue())
            repair_parity.assert_called_once()
            repair_args = repair_parity.call_args.args
            self.assertEqual((args, binding), repair_args[:2])
            self.assertIsNone(repair_args[2].payload)
            self.assertEqual(
                "internal",
                repair_args[2].selection.app_profile,
            )
            self.assertEqual(2, collect_parity.call_count)
            self.assertIn("Parity health: healthy", output.getvalue())


if __name__ == "__main__":
    unittest.main()
