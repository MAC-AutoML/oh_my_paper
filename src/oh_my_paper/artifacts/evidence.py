"""EVIDENCE_MAP.md parsing and schema validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from oh_my_paper.artifacts.markdown_tables import parse_first_table
from oh_my_paper.artifacts.types import ValidationReport

VALID_EVIDENCE_STATUSES = {"available", "partial", "missing"}


@dataclass(frozen=True)
class EvidenceItem:
    claim_id: str
    artifact: str
    status: str
    caveat: str


def parse_evidence_text(text: str) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for row in parse_first_table(text):
        items.append(
            EvidenceItem(
                claim_id=row.get("Claim ID", "").strip(),
                artifact=row.get("Evidence artifact", "").strip(),
                status=row.get("Evidence status", "").strip().lower(),
                caveat=row.get("Caveat", "").strip(),
            )
        )
    return items


def read_evidence(path: Path) -> list[EvidenceItem]:
    return parse_evidence_text(path.read_text(encoding="utf-8"))


def validate_evidence(path: Path, claim_ids: set[str] | None = None) -> ValidationReport:
    report = ValidationReport(name="evidence_map", inspected=[str(path)])
    if not path.exists():
        report.add("error", "missing EVIDENCE_MAP.md", str(path))
        return report
    items = read_evidence(path)
    if not items:
        report.add("error", "EVIDENCE_MAP.md must contain a markdown table with evidence rows", str(path))
        return report
    seen: set[str] = set()
    for item in items:
        if not item.claim_id:
            report.add("error", "evidence row missing Claim ID", str(path))
            continue
        if item.claim_id in seen:
            report.add("error", "duplicate evidence row for claim", str(path), item.claim_id)
        seen.add(item.claim_id)
        if claim_ids is not None and item.claim_id not in claim_ids:
            report.add("error", "evidence row references unknown claim", str(path), item.claim_id)
        if item.status not in VALID_EVIDENCE_STATUSES:
            report.add("error", f"evidence status must be one of {sorted(VALID_EVIDENCE_STATUSES)}", str(path), item.claim_id)
        if item.status == "available" and item.artifact.lower() in {"", "none", "missing"}:
            report.add("error", "available evidence must name an artifact", str(path), item.claim_id)
    if claim_ids is not None:
        missing = sorted(claim_ids - seen)
        for claim_id in missing:
            report.add("error", "claim missing from evidence map", str(path), claim_id)
    return report
