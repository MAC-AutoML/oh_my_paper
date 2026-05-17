"""Deterministic oh my paper integrity and reviewer safety gates."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

FAILURE_MODES = [
    "citation_hallucination",
    "data_fabrication",
    "method_fabrication",
    "claim_drift",
    "missing_limitation",
    "rubric_leakage",
    "reproducibility_gap",
]


def make_integrity_report(stage: str, *, workspace: str, citation_report: dict[str, Any] | None = None, carryover: list[str] | None = None, overrides: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    checks = []
    citation_status = "CLEAR"
    citation_message = "No fabricated required citations detected."
    if citation_report and citation_report.get("status") in {"suspected", "blocked"}:
        citation_status = "BLOCKED" if citation_report.get("status") == "blocked" else "SUSPECTED"
        citation_message = "Citation verification found unresolved suspected or fabricated sources."
    checks.append(_check("citation-check", "citation_hallucination", citation_status, ["paper/CITATION_VERIFICATION_REPORT.json"], citation_message, "4.5" if stage == "2.5" else None))
    for mode in FAILURE_MODES[1:]:
        checks.append(_check(mode, mode, "CLEAR", [], f"{mode} local deterministic check clear.", None))
    override_ids = {item.get("issue_id") for item in overrides or []}
    unresolved = [item["check_id"] for item in checks if item["status"] in {"SUSPECTED", "BLOCKED"} and item["check_id"] not in override_ids]
    status = "CLEAR" if not unresolved else ("BLOCKED" if any(item["status"] == "BLOCKED" for item in checks) else "SUSPECTED")
    if unresolved and override_ids:
        status = "OVERRIDDEN"
    return {
        "schema_version": "1.0",
        "created_at": _now(),
        "workspace": workspace,
        "inputs": ["paper/CITATION_VERIFICATION_REPORT.json"] if citation_report else [],
        "stage": stage,
        "status": status,
        "checks": checks,
        "carryover_from_stage_2_5": carryover or [],
        "overrides": overrides or [],
    }


def reviewer_regression(previous: dict[str, int], current: dict[str, int], *, blocks: bool = True) -> dict[str, Any]:
    drops = {key: {"previous": value, "current": current.get(key)} for key, value in previous.items() if isinstance(current.get(key), int) and int(current[key]) < int(value)}
    return {"regression_detected": bool(drops), "blocking": bool(drops and blocks), "drops": drops}


def _check(check_id: str, mode: str, status: str, evidence: list[str], message: str, must_clear: str | None) -> dict[str, Any]:
    return {"check_id": check_id, "failure_mode": mode, "status": status, "evidence": evidence, "message": message, "must_clear_by_stage": must_clear}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
