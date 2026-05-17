"""Load and validate ARS compatibility registries."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

RESOURCE_PACKAGE = "oh_my_paper.ars_compat.resources"
MODE_STATUSES = {"implemented", "partial", "advisory", "deferred"}
DATA_ACCESS_LEVELS = {"raw", "redacted", "verified_only"}


@dataclass(frozen=True)
class RegistryIssue:
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"path": self.path, "message": self.message}


@dataclass(frozen=True)
class RegistryValidation:
    ok: bool
    issues: list[RegistryIssue]

    def to_dict(self) -> dict[str, object]:
        return {"ok": self.ok, "issues": [issue.to_dict() for issue in self.issues]}


def _load_json(name: str) -> dict[str, object]:
    text = resources.files(RESOURCE_PACKAGE).joinpath(name).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"registry resource {name} must contain a JSON object")
    return data


def mode_registry() -> list[dict[str, object]]:
    data = _load_json("modes.json")
    modes = data.get("modes")
    if not isinstance(modes, list):
        raise ValueError("modes.json must contain a modes list")
    return [item for item in modes if isinstance(item, dict)]


def agent_registry() -> list[dict[str, object]]:
    data = _load_json("agents.json")
    agents = data.get("agents")
    if not isinstance(agents, list):
        raise ValueError("agents.json must contain an agents list")
    return [item for item in agents if isinstance(item, dict)]


def route_registry() -> list[dict[str, object]]:
    data = _load_json("routes.json")
    routes = data.get("routes")
    if not isinstance(routes, list):
        raise ValueError("routes.json must contain a routes list")
    return [item for item in routes if isinstance(item, dict)]


def validate_modes(modes: list[dict[str, object]] | None = None) -> RegistryValidation:
    rows = modes if modes is not None else mode_registry()
    issues: list[RegistryIssue] = []
    seen: set[tuple[str, str]] = set()
    for index, row in enumerate(rows):
        path = f"modes[{index}]"
        subsystem = row.get("subsystem")
        mode = row.get("mode")
        key = (str(subsystem), str(mode))
        if key in seen:
            issues.append(RegistryIssue(path, f"duplicate mode {key}"))
        seen.add(key)
        _expect_str(row, "owner_skill", path, issues)
        _expect_list(row, "secondary_skills", path, issues)
        _expect_list(row, "outputs", path, issues)
        _expect_list(row, "gates", path, issues)
        if row.get("status") not in MODE_STATUSES:
            issues.append(RegistryIssue(path, "status must be implemented|partial|advisory|deferred"))
        if row.get("data_access_level") not in DATA_ACCESS_LEVELS:
            issues.append(RegistryIssue(path, "data_access_level must be raw|redacted|verified_only"))
        if "→" in str(row.get("status", "")):
            issues.append(RegistryIssue(path, "status must not encode next action"))
        _expect_str(row, "next_action", path, issues)
    if len(rows) != 25:
        issues.append(RegistryIssue("modes", f"expected 25 modes, found {len(rows)}"))
    return RegistryValidation(not issues, issues)


def validate_agents(agents: list[dict[str, object]] | None = None) -> RegistryValidation:
    rows = agents if agents is not None else agent_registry()
    issues: list[RegistryIssue] = []
    old_paths: list[str] = []
    name_counts: dict[str, int] = {}
    for index, row in enumerate(rows):
        path = f"agents[{index}]"
        paths = row.get("old_agent_paths")
        if not isinstance(paths, list) or not paths or not all(isinstance(item, str) for item in paths):
            issues.append(RegistryIssue(path, "old_agent_paths must be a non-empty string list"))
        else:
            old_paths.extend(paths)
        name = row.get("codex_agent_name")
        if not isinstance(name, str) or not name:
            issues.append(RegistryIssue(path, "codex_agent_name must be a string"))
        else:
            name_counts[name] = name_counts.get(name, 0) + 1
        _expect_str(row, "owner_skill", path, issues)
        _expect_list(row, "input_artifacts", path, issues)
        _expect_list(row, "output_artifacts", path, issues)
        if row.get("status") not in MODE_STATUSES:
            issues.append(RegistryIssue(path, "status must be implemented|partial|advisory|deferred"))
        if row.get("data_access_level") not in DATA_ACCESS_LEVELS:
            issues.append(RegistryIssue(path, "data_access_level must be raw|redacted|verified_only"))
        if row.get("consolidation") is True and not str(row.get("parity_rationale", "")).strip():
            issues.append(RegistryIssue(path, "consolidated entries require parity_rationale"))
    if len(old_paths) != 38 or len(set(old_paths)) != 38:
        issues.append(RegistryIssue("agents", f"expected 38 unique old_agent_paths, found {len(set(old_paths))}/{len(old_paths)}"))
    for name, count in name_counts.items():
        if count > 1:
            issues.append(RegistryIssue("agents", f"codex_agent_name {name} appears in multiple rows"))
    return RegistryValidation(not issues, issues)


def route_for_trigger(trigger: str) -> dict[str, object] | None:
    normalized = trigger.strip().lower()
    for row in route_registry():
        candidate = str(row.get("trigger", "")).strip().lower()
        if candidate == normalized:
            return row
    for row in route_registry():
        candidate = str(row.get("trigger", "")).strip().lower()
        if candidate and candidate in normalized:
            return row
    return None


def _expect_str(row: dict[str, object], key: str, path: str, issues: list[RegistryIssue]) -> None:
    if not isinstance(row.get(key), str) or not str(row.get(key)).strip():
        issues.append(RegistryIssue(path, f"{key} must be a non-empty string"))


def _expect_list(row: dict[str, object], key: str, path: str, issues: list[RegistryIssue]) -> None:
    value = row.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        issues.append(RegistryIssue(path, f"{key} must be a string list"))
