from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from oh_my_paper.evals.capture import capture_fixture
from oh_my_paper.evals.changelog import append_changelog
from oh_my_paper.evals.fixtures import load_fixtures, run_fixture_file
from oh_my_paper.evals.privacy import redact_text
from oh_my_paper.evals.report import run_eval_report, write_eval_report
from oh_my_paper.workflows.demo import initialize_demo_workspace, run_demo_workflow

ROOT = Path(__file__).resolve().parents[2]
UNSUPPORTED = ROOT / "tests/fixtures/evals/unsupported_claim.jsonl"
SUPPORTED = ROOT / "tests/fixtures/evals/supported_claim.jsonl"


class Milestone5HarnessFlywheelTest(unittest.TestCase):
    def test_capture_redacted_fixture_from_failed_gate_run(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            run_demo_workflow(workspace)
            fixture_path = Path(tempdir) / "captured.jsonl"
            result = capture_fixture(
                workspace,
                fixture_path,
                fixture_id="captured_c3_regression",
                purpose="capture unsupported C3 as regression fixture",
                privacy="redacted",
            )
            self.assertEqual(result.privacy, "redacted")
            fixture = load_fixtures(fixture_path)[0]
            self.assertEqual(fixture.data["fixture_id"], "captured_c3_regression")
            self.assertEqual(fixture.data["privacy"], "redacted")
            self.assertIn("C3", fixture.data["expected"]["must_flag_claim_ids"])
            eval_results = run_fixture_file(fixture_path)
            self.assertTrue(all(item.ok for item in eval_results), [item.to_dict() for item in eval_results])

    def test_private_fixture_cannot_be_written_to_public_fixture_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            run_demo_workflow(workspace)
            with self.assertRaises(ValueError):
                capture_fixture(
                    workspace,
                    ROOT / "tests/fixtures/evals/private_capture.jsonl",
                    fixture_id="private_capture",
                    purpose="should be blocked",
                    privacy="private",
                )

    def test_redaction_masks_common_secret_patterns(self) -> None:
        text = "Contact a@example.com token=abc123 ghp_abcdefghijklmnopqrstuvwxyz123456"
        redacted = redact_text(text)
        self.assertNotIn("a@example.com", redacted)
        self.assertNotIn("token=abc123", redacted)
        self.assertNotIn("ghp_abcdefghijklmnopqrstuvwxyz123456", redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_eval_report_and_changelog_show_before_after_status(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            report = run_eval_report([UNSUPPORTED, SUPPORTED])
            self.assertTrue(report.ok)
            report_path = write_eval_report(report, Path(tempdir) / "report.md")
            changelog = append_changelog(Path(tempdir) / "CHANGELOG.md", report, "verified fixture set")
            self.assertIn("Eval Regression Report", report_path.read_text(encoding="utf-8"))
            self.assertIn("verified fixture set", changelog.read_text(encoding="utf-8"))
            as_json = json.dumps(report.to_dict())
            self.assertIn("writing_claim_support_unsupported_001", as_json)


if __name__ == "__main__":
    unittest.main()
