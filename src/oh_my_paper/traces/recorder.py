"""Trace event writer for local workflow runs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class TraceEvent:
    project_id: str
    phase: str
    skill: str
    action: str
    inputs: list[str]
    outputs: list[str]
    gate_name: str = "workflow"
    gate_status: str = "not_run"
    human_required: bool = False
    human_decision: str | None = None
    summary: str = ""
    runtime: str = "local-skill"
    schema_version: str = "0.1"
    event_id: str = field(default_factory=lambda: f"evt_{uuid4().hex[:12]}")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "project_id": self.project_id,
            "runtime": self.runtime,
            "phase": self.phase,
            "skill": self.skill,
            "action": self.action,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "gate": {"name": self.gate_name, "status": self.gate_status},
            "human_decision": {"required": self.human_required, "decision": self.human_decision},
            "summary": self.summary,
        }


class TraceRecorder:
    """Append-only JSONL recorder."""

    def __init__(self, trace_path: Path, project_id: str) -> None:
        self.trace_path = trace_path
        self.project_id = project_id
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: TraceEvent) -> None:
        with self.trace_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False, separators=(",", ":")) + "\n")

    def record(
        self,
        *,
        phase: str,
        skill: str,
        action: str,
        inputs: list[str],
        outputs: list[str],
        gate_name: str = "workflow",
        gate_status: str = "not_run",
        human_required: bool = False,
        summary: str = "",
    ) -> None:
        self.append(
            TraceEvent(
                project_id=self.project_id,
                phase=phase,
                skill=skill,
                action=action,
                inputs=inputs,
                outputs=outputs,
                gate_name=gate_name,
                gate_status=gate_status,
                human_required=human_required,
                summary=summary,
            )
        )
