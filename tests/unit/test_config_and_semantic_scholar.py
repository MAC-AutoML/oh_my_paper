from __future__ import annotations

import json
import os
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

from oh_my_paper.paper_core.config import resolve_config, config_status_report
from oh_my_paper.paper_core.semantic_scholar import SemanticScholarVerifier
from oh_my_paper.citations.semantic_scholar import verify_citations
from oh_my_paper.paper_core.validators import validate_pipeline_state, validate_repro_lock
from oh_my_paper.cli import main

ROOT = Path(__file__).resolve().parents[2]


class PaperConfigResolutionTest(unittest.TestCase):
    def test_root_config_example_exists_and_config_yaml_is_ignored(self) -> None:
        self.assertTrue((ROOT / "config.example.yaml").is_file())
        self.assertIn("config.yaml", (ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_config_precedence_cli_path_over_root_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "config.yaml").write_text("models:\n  writer:\n    model: root-model\n", encoding="utf-8")
            cli_config = root / "custom.yaml"
            cli_config.write_text("models:\n  writer:\n    model: cli-model\n", encoding="utf-8")
            report = resolve_config(cli_config, root=root, env={})
        self.assertEqual(report.models["writer"].model, "cli-model")
        self.assertTrue(report.config_sources[0]["used"])

    def test_config_precedence_root_yaml_over_env_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "config.yaml").write_text("models:\n  writer:\n    model: root-model\n", encoding="utf-8")
            report = resolve_config(None, root=root, env={"OPENAI_MODEL": "env-model"})
        self.assertEqual(report.models["writer"].model, "root-model")

    def test_config_status_redacts_api_keys_and_prints_presence_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            config = root / "config.example.yaml"
            config.write_text("models:\n  writer:\n    api_key_env: OPENAI_API_KEY\nsemantic_scholar:\n  api_key_env: s2_api_key\n", encoding="utf-8")
            report = config_status_report(config, root=root, env={"OPENAI_API_KEY": "secret-value", "s2_api_key": "ss-key"})
        payload = json.dumps(report, ensure_ascii=False)
        self.assertNotIn("secret-value", payload)
        self.assertNotIn("ss-key", payload)
        self.assertTrue(report["models"]["writer"]["api_key_present"])
        self.assertTrue(report["semantic_scholar"]["api_key_present"])

    def test_semantic_scholar_no_key_mode_does_not_require_api_key(self) -> None:
        report = resolve_config(None, root=ROOT, env={"SEMANTIC_SCHOLAR_MODE": "no_key"})
        self.assertEqual(report.semantic_scholar["effective_mode"], "no_key")
        self.assertEqual(report.status, "ok")

    def test_semantic_scholar_auto_mode_detects_s2_api_key_from_dotenv(self) -> None:
        report = resolve_config(None, root=ROOT, env={})
        self.assertEqual(report.semantic_scholar["api_key_env"], "s2_api_key")
        self.assertTrue(report.semantic_scholar["api_key_present"])
        self.assertEqual(report.semantic_scholar["effective_mode"], "api_key")
        self.assertGreaterEqual(float(report.semantic_scholar["request_interval_seconds"]), 1.0)

    def test_root_env_example_documents_s2_api_key_and_relay_url(self) -> None:
        text = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("s2_api_key=", text)
        self.assertIn("OPENAI_BASE_URL=https://automl.aiserverai.online/v1", text)

    def test_semantic_scholar_api_key_mode_requires_key_or_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            (root / "config.example.yaml").write_text("semantic_scholar:\n  mode: api_key\n  api_key_env: s2_api_key\n", encoding="utf-8")
            report = resolve_config(None, root=root, env={})
        self.assertEqual(report.status, "error")
        self.assertIn("Semantic Scholar api_key mode requires", " ".join(report.warnings))

    def test_config_status_cli_outputs_json(self) -> None:
        with mock.patch("sys.stdout") as stdout:
            code = main(["config-status", "--config", "config.example.yaml"])
        self.assertEqual(code, 0)
        printed = "".join(call.args[0] for call in stdout.write.call_args_list if call.args)
        self.assertIn('"semantic_scholar"', printed)


class SemanticScholarVerifierTest(unittest.TestCase):
    def test_keyed_request_sends_x_api_key(self) -> None:
        calls: list[dict[str, str]] = []

        def http_get(_url: str, headers: dict[str, str], _timeout: float) -> dict[str, object]:
            calls.append(headers)
            return {"data": [{"paperId": "p1", "title": "Proximal Policy Optimization Algorithms", "authors": [{"name": "Schulman"}], "year": 2017, "venue": "arXiv", "externalIds": {"DOI": "10.48550/arXiv.1707.06347"}, "url": "https://example.test"}]}

        verifier = SemanticScholarVerifier(mode="api_key", api_key="key", http_get=http_get)
        report = verifier.verify([{"citation_id": "ppo", "title": "Proximal Policy Optimization Algorithms", "authors": ["Schulman"], "year": 2017}])
        self.assertEqual(calls[0]["x-api-key"], "key")
        self.assertEqual(report["checks"][0]["status"], "verified")

    def test_no_key_request_omits_x_api_key_and_cache_hit_avoids_http(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            calls = 0

            def http_get(_url: str, headers: dict[str, str], _timeout: float) -> dict[str, object]:
                nonlocal calls
                calls += 1
                self.assertNotIn("x-api-key", headers)
                return {"data": [{"paperId": "p1", "title": "Proximal Policy Optimization Algorithms", "authors": [{"name": "Schulman"}], "year": 2017}]}

            verifier = SemanticScholarVerifier(mode="no_key", cache_dir=Path(tempdir), http_get=http_get)
            citation = {"citation_id": "ppo", "title": "Proximal Policy Optimization Algorithms", "authors": ["Schulman"], "year": 2017}
            self.assertEqual(verifier.verify([citation])["cache"]["misses"], 1)
            self.assertEqual(verifier.verify([citation])["cache"]["hits"], 1)
            self.assertEqual(calls, 1)

    def test_rate_limit_and_network_failure_never_verify(self) -> None:
        def rate_limited(_url: str, _headers: dict[str, str], _timeout: float) -> dict[str, object]:
            return {"status_code": 429, "retry_after": 7}

        report = SemanticScholarVerifier(mode="no_key", http_get=rate_limited).verify([{"citation_id": "x", "title": "X"}])
        self.assertEqual(report["checks"][0]["status"], "rate_limited")

        def broken(_url: str, _headers: dict[str, str], _timeout: float) -> dict[str, object]:
            raise OSError("offline")

        report = SemanticScholarVerifier(mode="no_key", http_get=broken).verify([{"citation_id": "x", "title": "X"}])
        self.assertEqual(report["checks"][0]["status"], "error")

    def test_verify_citations_cli_with_offline_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            citations = root / "citations.json"
            fixtures = root / "semantic_scholar"
            fixtures.mkdir()
            citations.write_text(json.dumps([{"citation_id": "ppo", "title": "Proximal Policy Optimization Algorithms", "authors": ["Schulman"], "year": 2017}]), encoding="utf-8")
            (fixtures / "search_proximal_policy_optimization_algorithms.json").write_text(json.dumps({"data": [{"paperId": "p1", "title": "Proximal Policy Optimization Algorithms", "authors": [{"name": "Schulman"}], "year": 2017}]}), encoding="utf-8")
            with mock.patch("sys.stdout") as stdout:
                code = main(["verify-citations", str(citations), "--offline-fixtures", str(fixtures), "--config", "config.example.yaml"])
        printed = "".join(call.args[0] for call in stdout.write.call_args_list if call.args)
        report = json.loads(printed)
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"][0]["status"], "verified")
        self.assertEqual(report["semantic_scholar_mode"], "no_key")

    def test_pipeline_verifier_sends_s2_api_key_header_and_respects_interval(self) -> None:
        captured: dict[str, object] = {}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self) -> bytes:
                return json.dumps({"data": [{"paperId": "p1", "title": "Proximal Policy Optimization Algorithms", "authors": [{"name": "Schulman"}], "year": 2017}]}).encode()

        def fake_urlopen(request: urllib.request.Request, timeout: int):
            captured["header"] = request.headers.get("X-api-key") or request.headers.get("x-api-key")
            captured["timeout"] = timeout
            return FakeResponse()

        with tempfile.TemporaryDirectory() as tempdir, mock.patch("urllib.request.urlopen", side_effect=fake_urlopen), mock.patch("time.sleep") as sleep:
            root = Path(tempdir)
            (root / "config.example.yaml").write_text(
                "semantic_scholar:\n  mode: auto\n  api_key_env: s2_api_key\n  request_interval_seconds_api_key: 1.1\n",
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {"s2_api_key": "keyed"}, clear=False):
                report = verify_citations(
                    [{"citation_id": "ppo", "title": "Proximal Policy Optimization Algorithms", "authors": ["Schulman"], "year": 2017}],
                    config_path=root / "config.example.yaml",
                    workspace=root,
                )
        self.assertEqual(captured["header"], "keyed")
        sleep.assert_called_once_with(1.1)
        self.assertEqual(report["semantic_scholar_mode"], "api_key")
        self.assertEqual(report["checks"][0]["status"], "verified")


class PaperPipelineCommandTest(unittest.TestCase):
    def test_run_paper_pipeline_offline_fixtures_produces_required_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = Path(tempdir) / "workspace"
            material = ROOT / "tests/fixtures/paper_pipeline/ppo_excerpt.txt"
            fixtures = ROOT / "tests/fixtures/paper_pipeline"
            with mock.patch("sys.stdout") as stdout:
                code = main([
                    "run-paper-pipeline",
                    str(material),
                    str(workspace),
                    "--config",
                    "config.example.yaml",
                    "--offline-fixtures",
                    str(fixtures),
                ])
            printed = "".join(call.args[0] for call in stdout.write.call_args_list if call.args)
            result = json.loads(printed)
            self.assertEqual(code, 0)
            self.assertTrue(result["ok"])
            for relative in [
                "paper/CITATION_VERIFICATION_REPORT.json",
                "paper/INTEGRITY_REPORT_STAGE_2_5.json",
                "paper/FULL_PAPER_DRAFT.md",
                "paper/GEMINI_REVIEW_ROUND_1.json",
                "paper/INTEGRITY_REPORT_FINAL.json",
                "paper/REPRO_LOCK.json",
                "paper/PIPELINE_SUMMARY.md",
                ".paper-ai/PIPELINE_STATE.json",
            ]:
                self.assertTrue((workspace / relative).exists(), relative)
            self.assertTrue(validate_pipeline_state(workspace / ".paper-ai/PIPELINE_STATE.json").ok)
            self.assertTrue(validate_repro_lock(workspace / "paper/REPRO_LOCK.json").ok)

    def test_paper_stage_status_uses_pipeline_state_next_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = Path(tempdir) / "workspace"
            fixtures = ROOT / "tests/fixtures/paper_pipeline"
            material = fixtures / "ppo_excerpt.txt"
            with mock.patch("sys.stdout"):
                self.assertEqual(main(["run-paper-pipeline", str(material), str(workspace), "--config", "config.example.yaml", "--offline-fixtures", str(fixtures)]), 0)
            with mock.patch("sys.stdout") as stdout:
                code = main(["paper-stage-status", str(workspace)])
        printed = "".join(call.args[0] for call in stdout.write.call_args_list if call.args)
        status = json.loads(printed)
        self.assertEqual(code, 0)
        self.assertEqual(status["next_stage"], "complete")
        self.assertEqual(status["blocked_reasons"], [])


if __name__ == "__main__":
    unittest.main()
