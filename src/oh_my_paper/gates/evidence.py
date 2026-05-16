"""Evidence gate for unsupported and inconsistent claims."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from oh_my_paper.artifacts.claims import Claim, read_claims
from oh_my_paper.artifacts.evidence import EvidenceItem, read_evidence

MISSING_TOKENS = {"", "none", "missing", "n/a", "na"}


@dataclass(frozen=True)
class GateFinding:
    claim_id: str
    severity: str
    message: str


@dataclass
class GateResult:
    name: str
    status: str
    findings: list[GateFinding] = field(default_factory=list)
    inspected: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.status == "pass"

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "status": self.status,
            "findings": [finding.__dict__ for finding in self.findings],
            "inspected": self.inspected,
        }


def _missing(value: str) -> bool:
    return value.strip().lower() in MISSING_TOKENS


def evaluate_claim_grounding(claims: list[Claim], evidence: list[EvidenceItem]) -> GateResult:
    evidence_by_claim = {item.claim_id: item for item in evidence}
    findings: list[GateFinding] = []
    for claim in claims:
        item = evidence_by_claim.get(claim.claim_id)
        if item is None:
            findings.append(GateFinding(claim.claim_id, "blocking", "claim has no evidence-map row"))
            continue
        if claim.status == "unsupported":
            findings.append(GateFinding(claim.claim_id, "blocking", "unsupported claim must be removed, softened, or gated"))
        if claim.status == "supported" and item.status != "available":
            findings.append(GateFinding(claim.claim_id, "blocking", "supported claim requires available evidence"))
        if claim.status == "partial" and item.status == "missing":
            findings.append(GateFinding(claim.claim_id, "warn", "partial claim has missing evidence; keep caveat visible"))
        if item.status == "available" and _missing(item.artifact):
            findings.append(GateFinding(claim.claim_id, "blocking", "available evidence must name an artifact"))
        if item.status == "missing" and not _missing(claim.evidence):
            findings.append(GateFinding(claim.claim_id, "warn", "claim evidence text conflicts with missing evidence map"))
    status = "fail" if any(f.severity == "blocking" for f in findings) else "warn" if findings else "pass"
    return GateResult(name="evidence", status=status, findings=findings)


def run_evidence_gate(claims_path: Path, evidence_path: Path) -> GateResult:
    result = evaluate_claim_grounding(read_claims(claims_path), read_evidence(evidence_path))
    result.inspected = [str(claims_path), str(evidence_path)]
    return result
