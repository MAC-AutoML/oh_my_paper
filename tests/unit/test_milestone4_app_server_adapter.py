from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from oh_my_paper.runtime.app_server_adapter import MockAppServerRuntimeAdapter
from oh_my_paper.runtime.mock_runs import run_mock_app_server_probe
from oh_my_paper.runtime.protocol import ArtifactChangeRequest, GateRequest, ToolRunRequest
from oh_my_paper.traces.events import read_trace_events, validate_trace
from oh_my_paper.traces.recorder import TraceEvent
from oh_my_paper.workflows.demo import initialize_demo_workspace

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/evals/unsupported_claim.jsonl"


class Milestone4AppServerAdapterTest(unittest.TestCase):
    def test_mock_app_server_maps_thread_event_to_app_server_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            adapter = MockAppServerRuntimeAdapter(workspace)
            handle = adapter.start_run("writing", "draft with evidence gate")
            adapter.emit_event(
                TraceEvent(
                    project_id=workspace.name,
                    phase="writing",
                    skill="paper-ai-writing",
                    action="run_gate",
                    inputs=["paper/CLAIMS.md"],
                    outputs=["paper/DEMO_DRAFT.md"],
                    gate_name="evidence",
                    gate_status="warn",
                    human_required=True,
                    summary="mock event",
                )
            )
            self.assertEqual(handle.thread_id, adapter.thread.thread_id)
            self.assertTrue(any(message.method == "thread.item.created" for message in adapter.messages))
            events = read_trace_events(workspace / ".paper-ai/TRACE.jsonl")
            self.assertEqual(events[-1]["runtime"], "app-server")
            self.assertEqual(events[-1]["phase"], "writing")
            self.assertTrue(validate_trace(workspace / ".paper-ai/TRACE.jsonl").ok)

    def test_approval_and_user_gate_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            adapter = MockAppServerRuntimeAdapter(workspace)
            adapter.start_run("rebuttal", "answer reviewer safely")
            gate = adapter.request_human_gate(
                GateRequest(
                    gate_id="gate_test",
                    name="rebuttal_promise",
                    severity="high",
                    reason="new experiment promise lacks evidence",
                    options=["revise", "remove"],
                )
            )
            change = adapter.request_file_change(ArtifactChangeRequest("paper/REBUTTAL_PLAN.md", "write plan"))
            blocked = adapter.request_file_change(ArtifactChangeRequest("../outside.md", "unsafe path"))
            command = adapter.run_tool_or_command(ToolRunRequest(["uv", "run", "oh-my-paper", "status"], "status"))
            self.assertEqual(gate.decision, "revise")
            self.assertTrue(change.approved)
            self.assertFalse(blocked.approved)
            self.assertTrue(command.approved)
            methods = [message.method for message in adapter.messages]
            self.assertIn("approval.requested", methods)
            self.assertIn("file_change.approval.requested", methods)
            self.assertIn("command.approval.requested", methods)

    def test_mock_adapter_shares_eval_fixture_expectations(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            workspace = initialize_demo_workspace(Path(tempdir) / "paper-demo")
            summary = run_mock_app_server_probe(workspace, FIXTURE)
            self.assertEqual(summary["trace_events"], 1)
            self.assertTrue(summary["eval_results"])
            self.assertTrue(all(result["status"] == "pass" for result in summary["eval_results"]))
            methods = [message["method"] for message in summary["messages"]]
            self.assertIn("eval.completed", methods)
            self.assertIn("approval.resolved", methods)


if __name__ == "__main__":
    unittest.main()
