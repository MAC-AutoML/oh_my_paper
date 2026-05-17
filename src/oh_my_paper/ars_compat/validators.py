"""Small stdlib validators for Codex-native ARS compatibility artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]
    warnings: list[str] | None = None

    def to_dict(self) -> dict[str, object]:
        return {"ok": self.ok, "errors": self.errors, "warnings": self.warnings or []}


def load_json(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def validate_material_passport(path: str | Path) -> ValidationResult:
    data = load_json(path)
    errors: list[str] = []
    _require(data, "passport_id", str, errors)
    _require(data, "verification_status", str, errors)
    if data.get("verification_status") not in {"draft", "partial", "verified", "blocked"}:
        errors.append("verification_status must be draft|partial|verified|blocked")
    boundaries = data.get("reset_boundaries", [])
    if boundaries is not None:
        if not isinstance(boundaries, list):
            errors.append("reset_boundaries must be a list when present")
        else:
            for index, item in enumerate(boundaries):
                if not isinstance(item, dict) or not _valid_hash(str(item.get("hash", ""))):
                    errors.append(f"reset_boundaries[{index}].hash must be sha256 hex")
    return ValidationResult(not errors, errors)


def validate_sprint_contract(path: str | Path) -> ValidationResult:
    data = load_json(path)
    errors: list[str] = []
    _require(data, "contract_id", str, errors)
    _require(data, "reviewer_role", str, errors)
    _require(data, "phase1_commitment", dict, errors)
    if data.get("reviewer_role") not in {"eic", "methodology", "domain", "perspective", "devils_advocate"}:
        errors.append("reviewer_role is not recognized")
    return ValidationResult(not errors, errors)


def validate_citation_anchors(path: str | Path) -> ValidationResult:
    data = load_json(path)
    anchors = data.get("anchors")
    errors: list[str] = []
    if not isinstance(anchors, list):
        errors.append("anchors must be a list")
    else:
        for index, anchor in enumerate(anchors):
            if not isinstance(anchor, dict):
                errors.append(f"anchors[{index}] must be an object")
                continue
            for key in ("claim_id", "citation_key", "locator"):
                _require(anchor, key, str, errors, prefix=f"anchors[{index}].")
    return ValidationResult(not errors, errors)


def validate_integrity_report(path: str | Path) -> ValidationResult:
    data = load_json(path)
    errors: list[str] = []
    _require(data, "stage", str, errors)
    _require(data, "gate_outcome", str, errors)
    if data.get("gate_outcome") not in {"pass", "fail", "blocked", "advisory"}:
        errors.append("gate_outcome must be pass|fail|blocked|advisory")
    checks = data.get("checks", [])
    if not isinstance(checks, list):
        errors.append("checks must be a list")
    return ValidationResult(not errors, errors)


def validate_claim_support(claims: list[dict[str, Any]]) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    for claim in claims:
        claim_id = str(claim.get("id", "<missing>"))
        status = claim.get("status")
        evidence = claim.get("evidence", [])
        if status == "supported" and not evidence:
            errors.append(f"{claim_id}: supported claim has no evidence")
        if status == "partial" and not claim.get("caveat"):
            warnings.append(f"{claim_id}: partial claim should include caveat")
        if status not in {"supported", "partial", "planned", "unsupported", "removed"}:
            errors.append(f"{claim_id}: unknown status")
    return ValidationResult(not errors, errors, warnings)


def canonical_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _valid_hash(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())


def _require(data: dict[str, Any], key: str, typ: type, errors: list[str], prefix: str = "") -> None:
    if not isinstance(data.get(key), typ):
        errors.append(f"{prefix}{key} must be {typ.__name__}")
