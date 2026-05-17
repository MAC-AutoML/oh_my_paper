"""Small stdlib validators for Codex-native oh my paper artifacts."""

from __future__ import annotations

import hashlib
import json
import re
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


def validate_config_resolution(report: dict[str, Any] | str | Path) -> ValidationResult:
    data = _coerce(report)
    errors = _base_artifact_errors(data)
    _enum(data, "status", {"ok", "warning", "error"}, errors)
    for key in ("config_sources", "models", "semantic_scholar", "privacy", "warnings"):
        _require_any(data, key, errors)
    if _contains_secret(data):
        errors.append("config resolution must not contain raw secret values")
    semantic = data.get("semantic_scholar", {})
    if isinstance(semantic, dict):
        _enum(semantic, "mode", {"auto", "api_key", "no_key", "disabled"}, errors, prefix="semantic_scholar.")
        _enum(semantic, "effective_mode", {"api_key", "no_key", "disabled"}, errors, prefix="semantic_scholar.")
    return ValidationResult(not errors, errors)


def validate_literature_corpus(report: dict[str, Any] | str | Path) -> ValidationResult:
    data = _coerce(report)
    errors = _base_artifact_errors(data, require_producer=False)
    _enum(data, "status", {"draft", "verified", "partial", "blocked"}, errors)
    _list(data, "query_plan", errors)
    sources = data.get("sources")
    if not isinstance(sources, list):
        errors.append("sources must be list")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"sources[{index}] must be object")
                continue
            for key in ("source_id", "title", "authors", "verification_status", "evidence_role"):
                _require_any(source, key, errors, prefix=f"sources[{index}].")
            _enum(source, "verification_status", {"unverified", "verified", "ambiguous", "not_found", "rate_limited", "error", "skipped"}, errors, prefix=f"sources[{index}].")
            _enum(source, "evidence_role", {"primary", "baseline", "related", "method", "background", "limitation"}, errors, prefix=f"sources[{index}].")
    _list(data, "notes", errors)
    return ValidationResult(not errors, errors)


def validate_citation_verification_report(report: dict[str, Any] | str | Path) -> ValidationResult:
    data = _coerce(report)
    errors = _base_artifact_errors(data)
    _enum(data, "status", {"clear", "suspected", "blocked", "skipped"}, errors)
    _enum(data, "semantic_scholar_mode", {"api_key", "no_key", "disabled"}, errors)
    for key in ("cache", "rate_limits", "checks", "summary"):
        _require_any(data, key, errors)
    for index, check in enumerate(data.get("checks", []) if isinstance(data.get("checks"), list) else []):
        if not isinstance(check, dict):
            errors.append(f"checks[{index}] must be object")
            continue
        for key in ("citation_id", "input_title", "status", "reasons", "raw_cache_key"):
            _require_any(check, key, errors, prefix=f"checks[{index}].")
        _enum(check, "status", {"verified", "ambiguous", "not_found", "rate_limited", "error", "skipped"}, errors, prefix=f"checks[{index}].")
    if _contains_secret(data):
        errors.append("citation report must not contain raw secrets")
    return ValidationResult(not errors, errors)


def validate_integrity_report(report: dict[str, Any] | str | Path) -> ValidationResult:
    data = _coerce(report)
    # Minimal template support for early integrity-report fixtures.
    if "gate_outcome" in data:
        errors: list[str] = []
        _require(data, "stage", str, errors)
        _require(data, "gate_outcome", str, errors)
        if data.get("gate_outcome") not in {"pass", "fail", "blocked", "advisory"}:
            errors.append("gate_outcome must be pass|fail|blocked|advisory")
        _list(data, "checks", errors)
        return ValidationResult(not errors, errors)
    errors = _base_artifact_errors(data, require_producer=False)
    _enum(data, "stage", {"2.5", "4.5", "final"}, errors)
    _enum(data, "status", {"CLEAR", "SUSPECTED", "BLOCKED", "OVERRIDDEN"}, errors)
    checks = data.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be list")
    else:
        unresolved = []
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{index}] must be object")
                continue
            for key in ("check_id", "failure_mode", "status", "evidence", "message"):
                _require_any(check, key, errors, prefix=f"checks[{index}].")
            _enum(check, "failure_mode", {"citation_hallucination", "data_fabrication", "method_fabrication", "claim_drift", "missing_limitation", "rubric_leakage", "reproducibility_gap"}, errors, prefix=f"checks[{index}].")
            _enum(check, "status", {"CLEAR", "SUSPECTED", "BLOCKED", "OVERRIDDEN"}, errors, prefix=f"checks[{index}].")
            if check.get("status") in {"SUSPECTED", "BLOCKED"}:
                unresolved.append(str(check.get("check_id")))
        overrides = {str(item.get("issue_id")) for item in data.get("overrides", []) if isinstance(item, dict)}
        if data.get("stage") in {"4.5", "final"}:
            remaining = [issue for issue in unresolved if issue not in overrides]
            if remaining:
                errors.append(f"unresolved Stage 2.5 issues remain without override: {', '.join(remaining)}")
    _list(data, "carryover_from_stage_2_5", errors)
    _list(data, "overrides", errors)
    return ValidationResult(not errors, errors)


def validate_pipeline_state(report: dict[str, Any] | str | Path, *, root: str | Path | None = None) -> ValidationResult:
    data = _coerce(report)
    errors = _base_artifact_errors(data, require_producer=False, require_workspace=False, require_inputs=False)
    stages = {"intake", "research", "integrity_2_5", "writing", "review", "revision", "integrity_4_5", "finalize", "complete", "blocked"}
    _enum(data, "current_stage", stages, errors)
    for key in ("completed_stages", "stage_artifacts", "gate_outcomes", "resume", "semantic_scholar", "review", "overrides"):
        _require_any(data, key, errors)
    stage_artifacts = data.get("stage_artifacts", {})
    if isinstance(stage_artifacts, dict):
        for stage, artifacts in stage_artifacts.items():
            if not isinstance(artifacts, list):
                errors.append(f"stage_artifacts.{stage} must be list")
                continue
            for index, artifact in enumerate(artifacts):
                if not isinstance(artifact, dict):
                    errors.append(f"stage_artifacts.{stage}[{index}] must be object")
                    continue
                for key in ("path", "sha256", "required"):
                    _require_any(artifact, key, errors, prefix=f"stage_artifacts.{stage}[{index}].")
                if artifact.get("required") and not _valid_hash(str(artifact.get("sha256", ""))):
                    errors.append(f"stage_artifacts.{stage}[{index}].sha256 must be sha256 hex")
    resume = data.get("resume", {})
    if isinstance(resume, dict):
        _enum(resume, "next_stage", stages, errors, prefix="resume.")
        if data.get("current_stage") == "blocked" and not resume.get("blocked_reasons"):
            errors.append("blocked state must list blocked_reasons")
    return ValidationResult(not errors, errors)


def validate_repro_lock(report: dict[str, Any] | str | Path) -> ValidationResult:
    data = _coerce(report)
    errors = _base_artifact_errors(data, require_producer=False, require_workspace=False, require_inputs=False)
    _enum(data, "status", {"documented"}, errors)
    notice = str(data.get("llm_reproducibility_notice", ""))
    if "not bitwise reproducible" not in notice or "may change" not in notice:
        errors.append("llm_reproducibility_notice must state not bitwise reproducible and provider outputs may change")
    for key in ("commands", "config_hashes", "model_config", "external_services", "artifacts"):
        _require_any(data, key, errors)
    if _contains_secret(data):
        errors.append("repro lock must not contain raw secrets")
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


def file_hash(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _coerce(report: dict[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(report, dict):
        return report
    return load_json(report)


def _base_artifact_errors(data: dict[str, Any], *, require_producer: bool = True, require_workspace: bool = True, require_inputs: bool = True) -> list[str]:
    errors: list[str] = []
    _require(data, "schema_version", str, errors)
    if require_producer:
        _require(data, "producer", str, errors)
    _require(data, "created_at", str, errors)
    if require_workspace:
        _require(data, "workspace", str, errors)
    if require_inputs:
        _list(data, "inputs", errors)
    return errors


def _valid_hash(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())


def _require(data: dict[str, Any], key: str, typ: type, errors: list[str], prefix: str = "") -> None:
    if not isinstance(data.get(key), typ):
        errors.append(f"{prefix}{key} must be {typ.__name__}")


def _require_any(data: dict[str, Any], key: str, errors: list[str], prefix: str = "") -> None:
    if key not in data:
        errors.append(f"{prefix}{key} is required")


def _list(data: dict[str, Any], key: str, errors: list[str], prefix: str = "") -> None:
    if not isinstance(data.get(key), list):
        errors.append(f"{prefix}{key} must be list")


def _enum(data: dict[str, Any], key: str, choices: set[str], errors: list[str], prefix: str = "") -> None:
    if data.get(key) not in choices:
        errors.append(f"{prefix}{key} must be one of {sorted(choices)}")


def _contains_secret(data: Any) -> bool:
    text = json.dumps(data, ensure_ascii=False)
    return bool(re.search(r"sk-[A-Za-z0-9_-]{8,}|secret-value|raw-api-key", text))
