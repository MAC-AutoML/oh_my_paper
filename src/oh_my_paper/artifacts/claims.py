"""CLAIMS.md parsing and schema validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from oh_my_paper.artifacts.markdown_tables import parse_first_table
from oh_my_paper.artifacts.types import ValidationReport

VALID_STATUSES = {"supported", "partial", "unsupported"}
CLAIM_ID_RE = re.compile(r"^[A-Za-z]+[0-9]+$")


@dataclass(frozen=True)
class Claim:
    claim_id: str
    text: str
    status: str
    evidence: str
    notes: str


def parse_claims_text(text: str) -> list[Claim]:
    claims: list[Claim] = []
    for row in parse_first_table(text):
        claim_id = row.get("ID", "").strip()
        claims.append(
            Claim(
                claim_id=claim_id,
                text=row.get("Claim", "").strip(),
                status=row.get("Status", "").strip().lower(),
                evidence=row.get("Evidence", "").strip(),
                notes=row.get("Notes", "").strip(),
            )
        )
    return claims


def read_claims(path: Path) -> list[Claim]:
    return parse_claims_text(path.read_text(encoding="utf-8"))


def validate_claims(path: Path) -> ValidationReport:
    report = ValidationReport(name="claims", inspected=[str(path)])
    if not path.exists():
        report.add("error", "missing CLAIMS.md", str(path))
        return report
    claims = read_claims(path)
    if not claims:
        report.add("error", "CLAIMS.md must contain a markdown table with claim rows", str(path))
        return report
    seen: set[str] = set()
    for claim in claims:
        if not CLAIM_ID_RE.match(claim.claim_id):
            report.add("error", "claim ID must look like C1 or CLAIM1", str(path), claim.claim_id)
        if claim.claim_id in seen:
            report.add("error", "duplicate claim ID", str(path), claim.claim_id)
        seen.add(claim.claim_id)
        if not claim.text:
            report.add("error", "claim text is required", str(path), claim.claim_id)
        if claim.status not in VALID_STATUSES:
            report.add("error", f"claim status must be one of {sorted(VALID_STATUSES)}", str(path), claim.claim_id)
        if claim.status == "supported" and claim.evidence.lower() in {"", "none", "missing"}:
            report.add("error", "supported claim must name evidence", str(path), claim.claim_id)
    return report
