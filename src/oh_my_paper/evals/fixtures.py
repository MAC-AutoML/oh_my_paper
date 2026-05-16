"""Synthetic JSONL fixture loading and evaluator dispatch."""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PUBLIC_FIXTURE_ROOT = Path("tests/fixtures/evals")

from oh_my_paper.artifacts.store import ArtifactStore
from oh_my_paper.gates.evidence import evaluate_claim_grounding
from oh_my_paper.artifacts.claims import parse_claims_text
from oh_my_paper.artifacts.evidence import parse_evidence_text
from oh_my_paper.traces.events import validate_trace

REQUIRED_FIXTURE_FIELDS = {
    "schema_version",
    "fixture_id",
    "phase",
    "skill",
    "purpose",
    "input_artifacts",
    "expected",
    "privacy",
}


@dataclass(frozen=True)
class Fixture:
    data: dict[str, Any]

    @property
    def fixture_id(self) -> str:
        return str(self.data["fixture_id"])


@dataclass
class EvalResult:
    fixture_id: str
    status: str
    reasons: list[str] = field(default_factory=list)
    inspected: list[str] = field(default_factory=list)
    suggested_fix: str | None = None

    @property
    def ok(self) -> bool:
        return self.status == "pass"

    def to_dict(self) -> dict[str, object]:
        return {
            "fixture_id": self.fixture_id,
            "status": self.status,
            "reasons": self.reasons,
            "inspected": self.inspected,
            "suggested_fix": self.suggested_fix,
        }


def load_fixtures(path: Path) -> list[Fixture]:
    fixtures: list[Fixture] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        data = json.loads(line)
        missing = REQUIRED_FIXTURE_FIELDS - set(data)
        if missing:
            raise ValueError(f"{path}:{line_number}: missing fixture fields {sorted(missing)}")
        if data["privacy"] not in {"synthetic", "redacted", "private"}:
            raise ValueError(f"{path}:{line_number}: invalid privacy mode")
        if data["privacy"] != "synthetic" and _is_public_fixture_path(path):
            raise ValueError(f"{path}:{line_number}: tracked fixtures must be synthetic")
        fixtures.append(Fixture(data))
    return fixtures


def run_fixture(fixture: Fixture) -> EvalResult:
    expected = fixture.data.get("expected", {})
    artifacts = fixture.data.get("input_artifacts", {})
    if "must_flag_claim_ids" in expected:
        return _run_evidence_fixture(fixture, artifacts, expected)
    if expected.get("trace_integrity"):
        return _run_trace_fixture(fixture, artifacts)
    if expected.get("artifact_completeness"):
        return _run_artifact_fixture(fixture, artifacts)
    return EvalResult(fixture.fixture_id, "warn", ["no supported evaluator expectation found"])


def run_fixture_file(path: Path) -> list[EvalResult]:
    return [run_fixture(fixture) for fixture in load_fixtures(path)]


def _run_evidence_fixture(fixture: Fixture, artifacts: dict[str, str], expected: dict[str, Any]) -> EvalResult:
    claims_text = artifacts.get("paper/CLAIMS.md", "")
    evidence_text = artifacts.get("paper/EVIDENCE_MAP.md", "")
    gate = evaluate_claim_grounding(parse_claims_text(claims_text), parse_evidence_text(evidence_text))
    flagged = {finding.claim_id for finding in gate.findings}
    required = set(expected.get("must_flag_claim_ids", []))
    forbidden = set(expected.get("must_not_flag_claim_ids", []))
    reasons: list[str] = []
    if not required <= flagged:
        reasons.append(f"missing expected flagged claims: {sorted(required - flagged)}")
    if forbidden & flagged:
        reasons.append(f"unexpected flagged claims: {sorted(forbidden & flagged)}")
    expected_status = expected.get("gate_status")
    if expected_status and gate.status != expected_status:
        reasons.append(f"expected gate status {expected_status}, got {gate.status}")
    return EvalResult(
        fixture.fixture_id,
        "fail" if reasons else "pass",
        reasons,
        ["paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        None if not reasons else "align claim statuses and evidence rows before drafting",
    )


def _run_trace_fixture(fixture: Fixture, artifacts: dict[str, str]) -> EvalResult:
    with tempfile.TemporaryDirectory() as tempdir:
        trace_path = Path(tempdir) / "TRACE.jsonl"
        trace_path.write_text(artifacts.get(".paper-ai/TRACE.jsonl", ""), encoding="utf-8")
        report = validate_trace(trace_path)
    reasons = [issue.message for issue in report.issues]
    return EvalResult(
        fixture.fixture_id,
        "fail" if reasons else "pass",
        reasons,
        [".paper-ai/TRACE.jsonl"],
        None if not reasons else "emit complete trace events with phase, skill, IO, gate, and human decision",
    )


def _run_artifact_fixture(fixture: Fixture, artifacts: dict[str, str]) -> EvalResult:
    with tempfile.TemporaryDirectory() as tempdir:
        root = Path(tempdir)
        for relative, content in artifacts.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        report = ArtifactStore.from_path(root).validate()
    reasons = [f"{issue.subject or issue.path}: {issue.message}" for issue in report.issues]
    return EvalResult(
        fixture.fixture_id,
        "fail" if reasons else "pass",
        reasons,
        report.inspected,
        None if not reasons else "create required paper and .paper-ai artifacts using the documented schemas",
    )


def _is_public_fixture_path(path: Path) -> bool:
    normalized = path.as_posix()
    return normalized.startswith(PUBLIC_FIXTURE_ROOT.as_posix() + "/") or normalized == PUBLIC_FIXTURE_ROOT.as_posix()
