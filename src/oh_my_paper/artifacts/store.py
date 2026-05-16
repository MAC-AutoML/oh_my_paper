"""Workspace artifact store and aggregate validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from oh_my_paper.artifacts.claims import read_claims, validate_claims
from oh_my_paper.artifacts.evidence import validate_evidence
from oh_my_paper.artifacts.types import ValidationReport
from oh_my_paper.traces.events import validate_trace


@dataclass(frozen=True)
class ArtifactStore:
    """Path resolver for a paper workspace."""

    root: Path

    @classmethod
    def from_path(cls, root: str | Path) -> "ArtifactStore":
        return cls(Path(root).resolve())

    @property
    def paper_dir(self) -> Path:
        return self.root / "paper"

    @property
    def state_dir(self) -> Path:
        return self.root / ".paper-ai"

    @property
    def claims_path(self) -> Path:
        return self.paper_dir / "CLAIMS.md"

    @property
    def evidence_path(self) -> Path:
        return self.paper_dir / "EVIDENCE_MAP.md"

    @property
    def trace_path(self) -> Path:
        return self.state_dir / "TRACE.jsonl"

    def validate(self) -> ValidationReport:
        report = ValidationReport(name="artifact_store")
        claims_report = validate_claims(self.claims_path)
        report.extend(claims_report)
        claim_ids: set[str] | None = None
        if self.claims_path.exists() and claims_report.ok:
            claim_ids = {claim.claim_id for claim in read_claims(self.claims_path)}
        report.extend(validate_evidence(self.evidence_path, claim_ids))
        report.extend(validate_trace(self.trace_path))
        return report
