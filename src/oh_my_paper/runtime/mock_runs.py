"""Convenience mocked App Server run scenarios."""

from __future__ import annotations

from pathlib import Path

from oh_my_paper.runtime.app_server_adapter import MockAppServerRuntimeAdapter
from oh_my_paper.runtime.protocol import ArtifactChangeRequest, GateRequest, ToolRunRequest
from oh_my_paper.traces.recorder import TraceEvent


def run_mock_app_server_probe(workspace: str | Path, fixture_path: str | Path) -> dict[str, object]:
    adapter = MockAppServerRuntimeAdapter(workspace)
    handle = adapter.start_run("writing", "mock App Server adapter probe")
    adapter.emit_event(
        TraceEvent(
            project_id=Path(workspace).resolve().name,
            phase="writing",
            skill="paper-ai-writing",
            action="run_gate",
            inputs=["paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
            outputs=["paper/DEMO_DRAFT.md"],
            gate_name="evidence",
            gate_status="warn",
            human_required=True,
            summary="Mock App Server mapped a writing gate to a trace event.",
        )
    )
    adapter.request_human_gate(
        GateRequest(
            gate_id="gate_mock_001",
            name="evidence",
            severity="high",
            reason="Unsupported claim needs removal, softening, or evidence.",
            options=["revise", "remove", "approve"],
            phase="writing",
        )
    )
    adapter.request_file_change(
        ArtifactChangeRequest(path="paper/DEMO_DRAFT.md", purpose="write safe synthetic draft", requires_approval=True)
    )
    adapter.run_tool_or_command(ToolRunRequest(command=["uv", "run", "oh-my-paper", "status"], purpose="smoke status"))
    adapter.run_eval(str(fixture_path))
    summary = adapter.summary(handle).to_dict()
    summary["messages"] = [message.to_dict() for message in adapter.messages]
    return summary
