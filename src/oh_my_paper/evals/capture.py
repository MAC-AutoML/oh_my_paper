"""Capture failed or risky workflow runs as regression fixtures."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from oh_my_paper.evals.privacy import assert_fixture_privacy_allowed, redact_text
from oh_my_paper.traces.events import read_trace_events

DEFAULT_ARTIFACTS = ["paper/CLAIMS.md", "paper/EVIDENCE_MAP.md", ".paper-ai/TRACE.jsonl"]


@dataclass(frozen=True)
class CaptureResult:
    fixture_id: str
    output_path: Path
    privacy: str
    captured_artifacts: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "fixture_id": self.fixture_id,
            "output_path": str(self.output_path),
            "privacy": self.privacy,
            "captured_artifacts": self.captured_artifacts,
        }


def capture_fixture(
    workspace: str | Path,
    output_path: str | Path,
    *,
    fixture_id: str,
    purpose: str,
    privacy: str = "redacted",
    artifact_paths: list[str] | None = None,
) -> CaptureResult:
    root = Path(workspace).resolve()
    out = Path(output_path)
    assert_fixture_privacy_allowed(out, privacy)
    paths = artifact_paths or DEFAULT_ARTIFACTS
    input_artifacts: dict[str, str] = {}
    captured: list[str] = []
    for relative in paths:
        path = root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        input_artifacts[relative] = redact_text(text) if privacy == "redacted" else text
        captured.append(relative)
    trace_events = read_trace_events(root / ".paper-ai" / "TRACE.jsonl") if (root / ".paper-ai" / "TRACE.jsonl").exists() else []
    target_event = _select_risky_event(trace_events)
    fixture = _build_fixture(fixture_id, purpose, privacy, input_artifacts, target_event)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(fixture, ensure_ascii=False, separators=(",", ":")) + "\n")
    return CaptureResult(fixture_id, out, privacy, captured)


def _select_risky_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    for event in reversed(events):
        gate = event.get("gate", {})
        human = event.get("human_decision", {})
        if gate.get("status") in {"fail", "warn"} or human.get("required") is True:
            return event
    return events[-1] if events else None


def _build_fixture(
    fixture_id: str,
    purpose: str,
    privacy: str,
    input_artifacts: dict[str, str],
    event: dict[str, Any] | None,
) -> dict[str, object]:
    phase = str(event.get("phase", "eval-loop")) if event else "eval-loop"
    skill = str(event.get("skill", "paper-ai-eval-loop")) if event else "paper-ai-eval-loop"
    gate = event.get("gate", {}) if event else {}
    expected: dict[str, object]
    if "paper/CLAIMS.md" in input_artifacts and "paper/EVIDENCE_MAP.md" in input_artifacts:
        expected = {"must_flag_claim_ids": _claim_ids_from_trace_or_text(input_artifacts), "gate_status": "fail"}
    else:
        expected = {"trace_integrity": True}
    if gate.get("status") in {"warn", "fail"}:
        expected["captured_gate_status"] = gate.get("status")
    return {
        "schema_version": "0.1",
        "fixture_id": fixture_id,
        "phase": phase,
        "skill": skill,
        "purpose": purpose,
        "input_artifacts": input_artifacts,
        "prompt": "Captured from a workflow trace for regression testing.",
        "expected": expected,
        "material_refs": [],
        "privacy": privacy,
    }


def _claim_ids_from_trace_or_text(input_artifacts: dict[str, str]) -> list[str]:
    claims = input_artifacts.get("paper/CLAIMS.md", "")
    ids: list[str] = []
    for line in claims.splitlines():
        if "| unsupported |" in line.lower():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells:
                ids.append(cells[0])
    return ids
