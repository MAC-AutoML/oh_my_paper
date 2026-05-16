"""Mocked Codex App Server adapter preserving local workflow semantics."""

from __future__ import annotations

from pathlib import Path

from oh_my_paper.evals.fixtures import EvalResult, run_fixture_file
from oh_my_paper.runtime.app_server_events import AppServerMessage, MockThread
from oh_my_paper.runtime.protocol import (
    AdapterRunSummary,
    ArtifactChangeRequest,
    ChangeDecision,
    GateDecision,
    GateRequest,
    RunHandle,
    ToolRunRequest,
    ToolRunResult,
)
from oh_my_paper.traces.recorder import TraceEvent, TraceRecorder


class MockAppServerRuntimeAdapter:
    """In-memory adapter for App Server protocol mapping tests.

    It does not launch Codex or require API credentials. It records JSON-RPC-like
    messages and writes normalized `app-server` trace events to the same artifact
    store used by local workflows.
    """

    def __init__(self, workspace: str | Path, *, thread: MockThread | None = None) -> None:
        self.workspace = Path(workspace).resolve()
        self.thread = thread or MockThread()
        self.messages: list[AppServerMessage] = []
        self.current_turn_id: str | None = None
        self.recorder = TraceRecorder(self.workspace / ".paper-ai" / "TRACE.jsonl", project_id=self.workspace.name)

    def start_run(self, phase: str, intent: str) -> RunHandle:
        self.workspace.joinpath(".paper-ai").mkdir(parents=True, exist_ok=True)
        turn_id = self.thread.new_turn(phase, intent)
        self.current_turn_id = turn_id
        self.messages.append(
            AppServerMessage(
                method="thread.turn.start",
                params={"thread_id": self.thread.thread_id, "turn_id": turn_id, "phase": phase, "intent": intent},
            )
        )
        return RunHandle(run_id=turn_id, thread_id=self.thread.thread_id, phase=phase, intent=intent)

    def emit_event(self, event: TraceEvent) -> None:
        app_event = TraceEvent(
            project_id=event.project_id,
            phase=event.phase,
            skill=event.skill,
            action=event.action,
            inputs=event.inputs,
            outputs=event.outputs,
            gate_name=event.gate_name,
            gate_status=event.gate_status,
            human_required=event.human_required,
            human_decision=event.human_decision,
            summary=event.summary,
            runtime="app-server",
        )
        self.recorder.append(app_event)
        self.messages.append(
            AppServerMessage(
                method="thread.item.created",
                params={
                    "thread_id": self.thread.thread_id,
                    "turn_id": self.current_turn_id,
                    "item_type": "paper_trace_event",
                    "phase": app_event.phase,
                    "skill": app_event.skill,
                    "gate_status": app_event.gate_status,
                },
            )
        )

    def request_human_gate(self, gate: GateRequest) -> GateDecision:
        self.messages.append(
            AppServerMessage(
                method="approval.requested",
                params={"gate_id": gate.gate_id, "name": gate.name, "severity": gate.severity, "options": gate.options},
                id=gate.gate_id,
            )
        )
        decision = "revise" if "revise" in gate.options else gate.options[0]
        approved = decision in {"approve", "revise"}
        result = GateDecision(gate_id=gate.gate_id, decision=decision, decider="mock-app-server", approved=approved, reason=gate.reason)
        self.messages.append(AppServerMessage(method="approval.resolved", params=result.__dict__, id=gate.gate_id))
        return result

    def request_file_change(self, change: ArtifactChangeRequest) -> ChangeDecision:
        self.messages.append(
            AppServerMessage(
                method="file_change.approval.requested",
                params={"path": change.path, "purpose": change.purpose, "requires_approval": change.requires_approval},
            )
        )
        approved = change.requires_approval is False or change.path.startswith(("paper/", ".paper-ai/"))
        decision = ChangeDecision(change.path, approved, "approve" if approved else "reject", "mock policy")
        self.messages.append(AppServerMessage(method="file_change.approval.resolved", params=decision.__dict__))
        return decision

    def run_tool_or_command(self, request: ToolRunRequest) -> ToolRunResult:
        self.messages.append(
            AppServerMessage(
                method="command.approval.requested",
                params={"command": request.command, "purpose": request.purpose, "requires_approval": request.requires_approval},
            )
        )
        safe = request.command[:2] == ["uv", "run"] or request.requires_approval is False
        result = ToolRunResult(request.command, approved=safe, exit_code=0 if safe else None, stdout="mocked" if safe else "")
        self.messages.append(AppServerMessage(method="command.approval.resolved", params=result.__dict__))
        return result

    def run_eval(self, fixture_path: str) -> list[EvalResult]:
        results = run_fixture_file(Path(fixture_path))
        self.messages.append(
            AppServerMessage(
                method="eval.completed",
                params={"fixture_path": fixture_path, "results": [result.to_dict() for result in results]},
            )
        )
        return results

    def summary(self, handle: RunHandle) -> AdapterRunSummary:
        approvals: list[GateDecision | ChangeDecision] = []
        eval_results: list[EvalResult] = []
        for message in self.messages:
            if message.method.endswith("resolved") and "gate_id" in message.params:
                approvals.append(GateDecision(**message.params))
            if message.method.endswith("resolved") and "path" in message.params:
                approvals.append(ChangeDecision(**message.params))
            if message.method == "eval.completed":
                eval_results.extend(run_fixture_file(Path(str(message.params["fixture_path"]))))
        trace_events = sum(1 for message in self.messages if message.method == "thread.item.created")
        return AdapterRunSummary(handle=handle, trace_events=trace_events, approvals=approvals, eval_results=eval_results)
