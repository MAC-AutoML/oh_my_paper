from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from oh_my_paper.artifacts.store import ArtifactStore
from oh_my_paper.evals.fixtures import run_fixture_file
from oh_my_paper.gates.evidence import run_evidence_gate
from oh_my_paper.traces.events import validate_trace

ROOT = Path(__file__).resolve().parents[2]
TOY = ROOT / "examples/toy-paper-workspace"
FIXTURES = ROOT / "tests/fixtures/evals"


class Milestone2ArtifactValidationTest(unittest.TestCase):
    def test_toy_workspace_schema_is_valid(self) -> None:
        report = ArtifactStore.from_path(TOY).validate()
        self.assertTrue(report.ok, report.to_dict())
        self.assertIn(str(TOY / "paper/CLAIMS.md"), report.inspected)
        self.assertIn(str(TOY / ".paper-ai/TRACE.jsonl"), report.inspected)

    def test_missing_workspace_artifacts_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            report = ArtifactStore.from_path(tempdir).validate()
        self.assertFalse(report.ok)
        messages = "\n".join(issue.message for issue in report.issues)
        self.assertIn("missing CLAIMS.md", messages)
        self.assertIn("missing EVIDENCE_MAP.md", messages)
        self.assertIn("missing TRACE.jsonl", messages)

    def test_evidence_gate_flags_toy_unsupported_claim(self) -> None:
        result = run_evidence_gate(TOY / "paper/CLAIMS.md", TOY / "paper/EVIDENCE_MAP.md")
        self.assertEqual(result.status, "fail")
        self.assertIn("C3", {finding.claim_id for finding in result.findings})

    def test_trace_integrity_requires_gate_status(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            trace = Path(tempdir) / "TRACE.jsonl"
            trace.write_text(
                '{"schema_version":"0.1","event_id":"evt_bad","timestamp":"now",'
                '"project_id":"p","runtime":"local-skill","phase":"writing",'
                '"skill":"paper-ai-writing","action":"run_gate","inputs":[],'
                '"outputs":[],"gate":{"name":"evidence"},'
                '"human_decision":{"required":false},"summary":"bad"}\n',
                encoding="utf-8",
            )
            report = validate_trace(trace)
        self.assertFalse(report.ok)
        self.assertIn("gate.status", "\n".join(issue.message for issue in report.issues))

    def test_eval_fixtures_have_expected_outcomes(self) -> None:
        unsupported = run_fixture_file(FIXTURES / "unsupported_claim.jsonl")
        supported = run_fixture_file(FIXTURES / "supported_claim.jsonl")
        trace = run_fixture_file(FIXTURES / "trace_integrity.jsonl")
        self.assertTrue(all(result.ok for result in unsupported), [r.to_dict() for r in unsupported])
        self.assertTrue(all(result.ok for result in supported), [r.to_dict() for r in supported])
        self.assertTrue(all(result.ok for result in trace), [r.to_dict() for r in trace])


if __name__ == "__main__":
    unittest.main()
