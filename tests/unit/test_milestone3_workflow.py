from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from oh_my_paper.traces.events import read_trace_events
from oh_my_paper.workflows.demo import initialize_demo_workspace, run_demo_workflow


class Milestone3WorkflowTest(unittest.TestCase):
    def test_demo_workflow_writes_full_artifact_chain_and_traces(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            result = run_demo_workflow(root)
            self.assertTrue(result.ok, result.to_dict())
            expected = {
                "paper/DEMO_DRAFT.md",
                "paper/FIGURE_PLAN.md",
                "paper/TABLE_PLAN.md",
                "paper/LAYOUT_REPORT.md",
                "paper/REVIEW_SIMULATION.md",
                "paper/FIX_PLAN.md",
                "paper/REBUTTAL_PLAN.md",
                "paper/PROMISED_REVISIONS.md",
                "paper/EVAL_REPORT.md",
            }
            self.assertTrue(expected <= set(result.outputs))
            draft = (root / "paper/DEMO_DRAFT.md").read_text(encoding="utf-8")
            self.assertIn("C3", draft)
            self.assertIn("unsupported claim must be removed", draft)
            phases = {event["phase"] for event in read_trace_events(root / ".paper-ai/TRACE.jsonl")}
            self.assertTrue(
                {"research-process", "writing", "figures", "layout", "reviewer", "rebuttal", "eval-loop"} <= phases
            )

    def test_demo_workflow_keeps_human_gates_visible_for_risky_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            result = run_demo_workflow(root)
            self.assertEqual(result.evidence_gate.status, "fail")
            events = read_trace_events(root / ".paper-ai/TRACE.jsonl")
            risky = [event for event in events if event["human_decision"]["required"]]
            self.assertGreaterEqual(len(risky), 3)
            self.assertIn("paper/REBUTTAL_PLAN.md", result.outputs)


if __name__ == "__main__":
    unittest.main()
