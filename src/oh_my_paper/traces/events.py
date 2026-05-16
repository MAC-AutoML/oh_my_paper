"""TRACE.jsonl parsing and integrity validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from oh_my_paper.artifacts.types import ValidationReport

REQUIRED_TRACE_FIELDS = {
    "schema_version",
    "event_id",
    "timestamp",
    "project_id",
    "runtime",
    "phase",
    "skill",
    "action",
    "inputs",
    "outputs",
    "gate",
    "human_decision",
    "summary",
}
VALID_GATE_STATUSES = {"pass", "fail", "warn", "not_run"}
VALID_RUNTIMES = {"local-skill", "app-server"}


def read_trace_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"{path}:{line_number}: trace event must be an object")
        event["_line"] = line_number
        events.append(event)
    return events


def validate_trace(path: Path) -> ValidationReport:
    report = ValidationReport(name="trace", inspected=[str(path)])
    if not path.exists():
        report.add("error", "missing TRACE.jsonl", str(path))
        return report
    try:
        events = read_trace_events(path)
    except ValueError as exc:
        report.add("error", str(exc), str(path))
        return report
    if not events:
        report.add("error", "TRACE.jsonl must contain at least one event", str(path))
        return report
    seen: set[str] = set()
    for event in events:
        subject = str(event.get("event_id") or f"line {event.get('_line')}")
        missing = sorted(REQUIRED_TRACE_FIELDS - set(event))
        for field in missing:
            report.add("error", f"trace event missing {field}", str(path), subject)
        if event.get("event_id") in seen:
            report.add("error", "duplicate trace event_id", str(path), subject)
        seen.add(str(event.get("event_id")))
        if event.get("runtime") not in VALID_RUNTIMES:
            report.add("error", "runtime must be local-skill or app-server", str(path), subject)
        for field in ["phase", "skill", "action", "summary"]:
            if field in event and not str(event.get(field) or "").strip():
                report.add("error", f"{field} must be non-empty", str(path), subject)
        for field in ["inputs", "outputs"]:
            if field in event and not isinstance(event[field], list):
                report.add("error", f"{field} must be a list", str(path), subject)
            elif field in event and not all(isinstance(item, str) and item.strip() for item in event[field]):
                report.add("error", f"{field} must contain non-empty path strings", str(path), subject)
        gate = event.get("gate")
        if not isinstance(gate, dict):
            report.add("error", "gate must be an object", str(path), subject)
        else:
            if not str(gate.get("name") or "").strip():
                report.add("error", "gate.name must be non-empty", str(path), subject)
            if gate.get("status") not in VALID_GATE_STATUSES:
                report.add("error", f"gate.status must be one of {sorted(VALID_GATE_STATUSES)}", str(path), subject)
        human = event.get("human_decision")
        if not isinstance(human, dict):
            report.add("error", "human_decision must be an object", str(path), subject)
        elif "required" not in human:
            report.add("error", "human_decision.required must be present", str(path), subject)
    return report
