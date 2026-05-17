"""Codex-native oh my paper pipeline stage helpers."""

from __future__ import annotations

from dataclasses import dataclass

PIPELINE_STAGES = [
    "research",
    "write",
    "integrity_before_review",
    "review",
    "revision_coaching",
    "revise",
    "re_review",
    "final_integrity",
    "finalize_disclosure",
    "process_summary",
]


@dataclass(frozen=True)
class StagePlan:
    stages: list[str]
    current_stage: str
    next_stage: str | None
    required_artifacts: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "stages": self.stages,
            "current_stage": self.current_stage,
            "next_stage": self.next_stage,
            "required_artifacts": self.required_artifacts,
        }


def pipeline_plan(current_stage: str = "research") -> StagePlan:
    if current_stage not in PIPELINE_STAGES:
        raise ValueError(f"unknown pipeline stage: {current_stage}")
    index = PIPELINE_STAGES.index(current_stage)
    next_stage = PIPELINE_STAGES[index + 1] if index + 1 < len(PIPELINE_STAGES) else None
    return StagePlan(
        stages=list(PIPELINE_STAGES),
        current_stage=current_stage,
        next_stage=next_stage,
        required_artifacts=_required_artifacts(current_stage),
    )


def resume_stage_from_passport(passport: dict[str, object]) -> str | None:
    status = passport.get("verification_status")
    if status == "verified":
        return "finalize_disclosure"
    if status in {"draft", "partial"}:
        return "integrity_before_review"
    return None


def _required_artifacts(stage: str) -> list[str]:
    return {
        "research": ["paper/RESEARCH_BRIEF.md", "paper/EVIDENCE_MAP.md"],
        "write": ["paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        "integrity_before_review": ["paper/MATERIAL_PASSPORT.json", "paper/CLAIMS.md"],
        "review": ["paper/REVIEW_SIMULATION.md", "paper/FIX_PLAN.md"],
        "revision_coaching": ["paper/FIX_PLAN.md"],
        "revise": ["paper/REVISION_TRACEABILITY_MATRIX.json"],
        "re_review": ["paper/REVIEW_SIMULATION.md", "paper/REVISION_TRACEABILITY_MATRIX.json"],
        "final_integrity": ["paper/INTEGRITY_REPORT_FINAL.json"],
        "finalize_disclosure": ["paper/AI_DISCLOSURE.md"],
        "process_summary": ["paper/PROCESS_SUMMARY.json"],
    }[stage]
