"""End-to-end deterministic local MVP workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from oh_my_paper.artifacts.claims import read_claims
from oh_my_paper.artifacts.evidence import read_evidence
from oh_my_paper.artifacts.store import ArtifactStore
from oh_my_paper.artifacts.types import ValidationReport
from oh_my_paper.gates.evidence import GateResult, run_evidence_gate
from oh_my_paper.traces.events import validate_trace
from oh_my_paper.traces.recorder import TraceRecorder
from oh_my_paper.workflows.reports import (
    build_eval_report,
    build_figure_plan,
    build_fix_plan,
    build_layout_report,
    build_promised_revisions,
    build_rebuttal_plan,
    build_review_simulation,
    build_table_plan,
    build_writing_draft,
)


@dataclass(frozen=True)
class WorkflowResult:
    workspace: Path
    outputs: list[str]
    evidence_gate: GateResult
    artifact_report: ValidationReport
    trace_report: ValidationReport

    @property
    def ok(self) -> bool:
        return self.artifact_report.ok and self.trace_report.ok

    def to_dict(self) -> dict[str, object]:
        return {
            "workspace": str(self.workspace),
            "ok": self.ok,
            "outputs": self.outputs,
            "evidence_gate": self.evidence_gate.to_dict(),
            "artifact_report": self.artifact_report.to_dict(),
            "trace_report": self.trace_report.to_dict(),
        }


def initialize_demo_workspace(workspace: str | Path, *, overwrite: bool = False) -> Path:
    root = Path(workspace).resolve()
    paper = root / "paper"
    state = root / ".paper-ai"
    paper.mkdir(parents=True, exist_ok=True)
    state.mkdir(parents=True, exist_ok=True)
    templates = {
        paper / "PAPER_BRIEF.md": "# Toy Paper Brief\n\n## Working title\n\nEvidence-Gated Toy Agent for Table Reasoning\n\n## Problem\n\nSmall research teams need a safe way to draft paper claims without overstating missing evidence.\n",
        paper / "CLAIMS.md": "# Claims\n\n| ID | Claim | Status | Evidence | Notes |\n| --- | --- | --- | --- | --- |\n| C1 | Claim-ledger prompts reduce unsupported claims in the toy setting. | supported | Pilot result summary | Synthetic example only. |\n| C2 | The workflow makes missing evidence visible before drafting. | partial | Trace and gate design | Needs user study later. |\n| C3 | The approach improves robustness across real venues. | unsupported | none | Must be removed, softened, or marked as future work. |\n",
        paper / "EVIDENCE_MAP.md": "# Evidence Map\n\n| Claim ID | Evidence artifact | Evidence status | Caveat |\n| --- | --- | --- | --- |\n| C1 | Synthetic pilot note | available | Toy data only. |\n| C2 | Trace/gate schema | partial | Not behaviorally validated yet. |\n| C3 | none | missing | Do not write as a result. |\n",
        state / "PAPER_AI_STATE.md": "# Paper AI State\n\n- Current phase: research-process\n- Last completed phase: none\n- Blockers: unsupported claim C3 needs evidence or removal\n",
        state / "MATERIALS_USED.md": "# Materials Used\n\nThis synthetic example uses no copied raw material.\n",
        state / "TRACE.jsonl": _initial_trace(root.name),
    }
    for path, content in templates.items():
        if overwrite or not path.exists():
            path.write_text(content, encoding="utf-8")
    return root


def run_demo_workflow(workspace: str | Path) -> WorkflowResult:
    store = ArtifactStore.from_path(workspace)
    store.paper_dir.mkdir(parents=True, exist_ok=True)
    store.state_dir.mkdir(parents=True, exist_ok=True)
    recorder = TraceRecorder(store.trace_path, project_id=store.root.name)

    artifact_report = store.validate()
    recorder.record(
        phase="research-process",
        skill="paper-ai-research-process",
        action="validate_artifacts",
        inputs=["paper/PAPER_BRIEF.md", "paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        outputs=[".paper-ai/TRACE.jsonl"],
        gate_name="artifact_schema",
        gate_status="pass" if artifact_report.ok else "fail",
        human_required=not artifact_report.ok,
        summary="Validated core toy workspace artifacts before demo routing.",
    )

    claims = read_claims(store.claims_path)
    evidence = read_evidence(store.evidence_path)
    evidence_gate = run_evidence_gate(store.claims_path, store.evidence_path)
    outputs: list[str] = []

    _write(store.paper_dir / "DEMO_DRAFT.md", build_writing_draft(claims, evidence_gate), outputs, store)
    recorder.record(
        phase="writing",
        skill="paper-ai-writing",
        action="draft_safe_section",
        inputs=["paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        outputs=["paper/DEMO_DRAFT.md"],
        gate_name="evidence",
        gate_status=evidence_gate.status,
        human_required=not evidence_gate.ok,
        summary="Drafted only supported/caveated synthetic claims; unsupported claims are withheld.",
    )

    _write(store.paper_dir / "FIGURE_PLAN.md", build_figure_plan(claims), outputs, store)
    _write(store.paper_dir / "TABLE_PLAN.md", build_table_plan(evidence), outputs, store)
    recorder.record(
        phase="figures",
        skill="paper-ai-figures",
        action="plan_visuals",
        inputs=["paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        outputs=["paper/FIGURE_PLAN.md", "paper/TABLE_PLAN.md"],
        gate_name="visual",
        gate_status="pass",
        summary="Created claim-linked synthetic figure and table plans.",
    )

    _write(store.paper_dir / "LAYOUT_REPORT.md", build_layout_report(), outputs, store)
    recorder.record(
        phase="layout",
        skill="paper-ai-layout",
        action="check_page_budget",
        inputs=["paper/DEMO_DRAFT.md", "paper/FIGURE_PLAN.md"],
        outputs=["paper/LAYOUT_REPORT.md"],
        gate_name="layout",
        gate_status="warn",
        human_required=True,
        summary="Recorded generic layout warning because no target venue template is configured.",
    )

    _write(store.paper_dir / "REVIEW_SIMULATION.md", build_review_simulation(evidence_gate), outputs, store)
    _write(store.paper_dir / "FIX_PLAN.md", build_fix_plan(evidence_gate), outputs, store)
    recorder.record(
        phase="reviewer",
        skill="paper-ai-reviewer",
        action="simulate_review",
        inputs=["paper/DEMO_DRAFT.md", "paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        outputs=["paper/REVIEW_SIMULATION.md", "paper/FIX_PLAN.md"],
        gate_name="reviewer",
        gate_status="warn" if evidence_gate.findings else "pass",
        human_required=bool(evidence_gate.findings),
        summary="Reviewer simulation surfaced evidence risks and prioritized fixes.",
    )

    _write(store.paper_dir / "REBUTTAL_PLAN.md", build_rebuttal_plan(evidence_gate), outputs, store)
    _write(store.paper_dir / "PROMISED_REVISIONS.md", build_promised_revisions(evidence_gate), outputs, store)
    recorder.record(
        phase="rebuttal",
        skill="paper-ai-rebuttal",
        action="draft_rebuttal_plan",
        inputs=["paper/REVIEW_SIMULATION.md", "paper/FIX_PLAN.md"],
        outputs=["paper/REBUTTAL_PLAN.md", "paper/PROMISED_REVISIONS.md"],
        gate_name="rebuttal",
        gate_status="warn" if evidence_gate.findings else "pass",
        human_required=bool(evidence_gate.findings),
        summary="Built conservative rebuttal plan without promising unsupported experiments.",
    )

    phase_statuses = {
        "research-process": "pass" if artifact_report.ok else "fail",
        "writing": evidence_gate.status,
        "figures": "pass",
        "layout": "warn",
        "reviewer": "warn" if evidence_gate.findings else "pass",
        "rebuttal": "warn" if evidence_gate.findings else "pass",
    }
    _write(store.paper_dir / "EVAL_REPORT.md", build_eval_report(phase_statuses, evidence_gate), outputs, store)
    recorder.record(
        phase="eval-loop",
        skill="paper-ai-eval-loop",
        action="write_eval_report",
        inputs=[".paper-ai/TRACE.jsonl", "paper/REVIEW_SIMULATION.md"],
        outputs=["paper/EVAL_REPORT.md"],
        gate_name="eval",
        gate_status="pass",
        summary="Recorded deterministic MVP eval report from phase gates.",
    )

    return WorkflowResult(
        workspace=store.root,
        outputs=outputs,
        evidence_gate=evidence_gate,
        artifact_report=store.validate(),
        trace_report=validate_trace(store.trace_path),
    )


def _write(path: Path, content: str, outputs: list[str], store: ArtifactStore) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    outputs.append(str(path.relative_to(store.root)))


def _initial_trace(project_id: str) -> str:
    event = {
        "schema_version": "0.1",
        "event_id": "evt_demo_init_001",
        "timestamp": "2026-05-17T00:00:00+08:00",
        "project_id": project_id,
        "runtime": "local-skill",
        "phase": "research-process",
        "skill": "paper-ai-research-process",
        "action": "initialize_synthetic_workspace",
        "inputs": [],
        "outputs": ["paper/PAPER_BRIEF.md", "paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        "gate": {"name": "evidence", "status": "warn"},
        "human_decision": {"required": True, "decision": None},
        "summary": "Synthetic workspace initialized with one unsupported claim for demo workflow.",
    }
    return json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n"
