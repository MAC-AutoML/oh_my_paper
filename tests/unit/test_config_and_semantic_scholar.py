from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from oh_my_paper.ars_compat.config import resolve_config, config_status_report
from oh_my_paper.ars_compat.semantic_scholar import SemanticScholarVerifier
from oh_my_paper.cli import main

ROOT = Path(__file__).resolve().parents[2]


class ArsConfigResolutionTest(unittest.TestCase):
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
            config.write_text("models:\n  writer:\n    api_key_env: OPENAI_API_KEY\nsemantic_scholar:\n  api_key_env: SEMANTIC_SCHOLAR_API_KEY\n", encoding="utf-8")
            report = config_status_report(config, root=root, env={"OPENAI_API_KEY": "secret-value", "SEMANTIC_SCHOLAR_API_KEY": "ss-key"})
        payload = json.dumps(report, ensure_ascii=False)
        self.assertNotIn("secret-value", payload)
        self.assertNotIn("ss-key", payload)
        self.assertTrue(report["models"]["writer"]["api_key_present"])
        self.assertTrue(report["semantic_scholar"]["api_key_present"])

    def test_semantic_scholar_no_key_mode_does_not_require_api_key(self) -> None:
        report = resolve_config(None, root=ROOT, env={"SEMANTIC_SCHOLAR_MODE": "no_key"})
        self.assertEqual(report.semantic_scholar["effective_mode"], "no_key")
        self.assertEqual(report.status, "ok")

    def test_semantic_scholar_api_key_mode_requires_key_or_reports_error(self) -> None:
        report = resolve_config(None, root=ROOT, env={"SEMANTIC_SCHOLAR_MODE": "api_key"})
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
            (fixtures / "search_ppo.json").write_text(json.dumps({"data": [{"paperId": "p1", "title": "Proximal Policy Optimization Algorithms", "authors": [{"name": "Schulman"}], "year": 2017}]}), encoding="utf-8")
            code = main(["verify-citations", str(citations), "--offline-fixtures", str(fixtures), "--config", "config.example.yaml"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
