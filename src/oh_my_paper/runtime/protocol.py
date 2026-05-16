"""Runtime-neutral adapter protocol and gate decision types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from oh_my_paper.evals.fixtures import EvalResult
from oh_my_paper.traces.recorder import TraceEvent


@dataclass(frozen=True)
class RunHandle:
    run_id: str
    thread_id: str
    phase: str
    intent: str


@dataclass(frozen=True)
class GateRequest:
    gate_id: str
    name: str
    severity: str
    reason: str
    options: list[str]
    phase: str | None = None


@dataclass(frozen=True)
class GateDecision:
    gate_id: str
    decision: str
    decider: str
    approved: bool
    reason: str = ""


@dataclass(frozen=True)
class ArtifactChangeRequest:
    path: str
    purpose: str
    content_preview: str = ""
    requires_approval: bool = True


@dataclass(frozen=True)
class ChangeDecision:
    path: str
    approved: bool
    decision: str
    reason: str = ""


@dataclass(frozen=True)
class ToolRunRequest:
    command: list[str]
    purpose: str
    requires_approval: bool = True


@dataclass(frozen=True)
class ToolRunResult:
    command: list[str]
    approved: bool
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""


@dataclass
class AdapterRunSummary:
    handle: RunHandle
    trace_events: int = 0
    approvals: list[GateDecision | ChangeDecision] = field(default_factory=list)
    eval_results: list[EvalResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "handle": self.handle.__dict__,
            "trace_events": self.trace_events,
            "approvals": [decision.__dict__ for decision in self.approvals],
            "eval_results": [result.to_dict() for result in self.eval_results],
        }


class RuntimeAdapter(Protocol):
    def start_run(self, phase: str, intent: str) -> RunHandle: ...

    def emit_event(self, event: TraceEvent) -> None: ...

    def request_human_gate(self, gate: GateRequest) -> GateDecision: ...

    def request_file_change(self, change: ArtifactChangeRequest) -> ChangeDecision: ...

    def run_tool_or_command(self, request: ToolRunRequest) -> ToolRunResult: ...

    def run_eval(self, fixture_path: str) -> list[EvalResult]: ...
