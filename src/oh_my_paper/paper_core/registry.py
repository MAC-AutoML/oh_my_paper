"""Load and validate oh my paper registries."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

RESOURCE_PACKAGE = "oh_my_paper.paper_core.resources"
MODE_STATUSES = {"implemented", "partial", "advisory", "deferred"}
DATA_ACCESS_LEVELS = {"raw", "redacted", "verified_only"}
ROLE_MAP_STATUSES = {"covered", "advisory", "missing"}
REQUIRED_AGENT_LANES: dict[str, tuple[str, ...]] = {
    "research": (
        "paper-research-lead",
        "paper-source-verifier",
        "paper-socratic-mentor",
        "paper-devils-advocate",
    ),
    "writing": (
        "paper-structure-architect",
        "paper-drafting-lead",
        "paper-style-calibrator",
        "paper-visualization-planner",
    ),
    "reviewer": (
        "paper-review-eic",
        "paper-methodology-reviewer",
        "paper-domain-reviewer",
        "paper-devils-advocate-reviewer",
        "paper-revision-coach",
    ),
    "pipeline": (
        "paper-pipeline-orchestrator",
        "paper-integrity-auditor",
        "paper-run-monitor",
    ),
}


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


def agent_role_map_registry() -> dict[str, object]:
    return _load_json("agent_role_map.json")


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
    source_refs: list[str] = []
    name_counts: dict[str, int] = {}
    for index, row in enumerate(rows):
        path = f"agents[{index}]"
        refs = row.get("source_role_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(item, str) for item in refs):
            issues.append(RegistryIssue(path, "source_role_refs must be a non-empty string list"))
        else:
            source_refs.extend(refs)
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
        if row.get("consolidation") is True and not str(row.get("role_rationale", "")).strip():
            issues.append(RegistryIssue(path, "consolidated entries require role_rationale"))
    if len(source_refs) != 38 or len(set(source_refs)) != 38:
        issues.append(RegistryIssue("agents", f"expected 38 unique source_role_refs, found {len(set(source_refs))}/{len(source_refs)}"))
    for name, count in name_counts.items():
        if count > 1:
            issues.append(RegistryIssue("agents", f"codex_agent_name {name} appears in multiple rows"))
    return RegistryValidation(not issues, issues)


def validate_agent_role_map(role_map: dict[str, object] | None = None) -> RegistryValidation:
    data = role_map if role_map is not None else agent_role_map_registry()
    issues: list[RegistryIssue] = []
    if not isinstance(data.get("schema_version"), str):
        issues.append(RegistryIssue("agent_role_map", "schema_version must be a string"))

    lanes = data.get("required_lanes")
    if not isinstance(lanes, list):
        return RegistryValidation(False, [*issues, RegistryIssue("required_lanes", "required_lanes must be a list")])

    seen_lanes: set[tuple[str, str]] = set()
    seen_agent_names: dict[str, str] = {}
    covered_lanes: set[tuple[str, str]] = set()
    for index, row in enumerate(lanes):
        path = f"required_lanes[{index}]"
        if not isinstance(row, dict):
            issues.append(RegistryIssue(path, "lane row must be an object"))
            continue
        team = row.get("team")
        lane = row.get("required_lane")
        agent_name = row.get("codex_agent_name")
        if not isinstance(team, str) or team not in REQUIRED_AGENT_LANES:
            issues.append(RegistryIssue(path, "team must be research|writing|reviewer|pipeline"))
        if not isinstance(lane, str) or lane not in REQUIRED_AGENT_LANES.get(str(team), ()):
            issues.append(RegistryIssue(path, "required_lane is not expected for its team"))
        key = (str(team), str(lane))
        if key in seen_lanes:
            issues.append(RegistryIssue(path, f"duplicate required lane {key}"))
        seen_lanes.add(key)
        if row.get("status") == "covered":
            covered_lanes.add(key)
        if not isinstance(agent_name, str) or not agent_name:
            issues.append(RegistryIssue(path, "codex_agent_name must be a string"))
        elif agent_name in seen_agent_names:
            issues.append(RegistryIssue(path, f"codex_agent_name {agent_name} already covers {seen_agent_names[agent_name]}"))
        else:
            seen_agent_names[agent_name] = f"{team}/{lane}"
        _expect_str(row, "agent_file", path, issues)
        _expect_str(row, "owner_skill", path, issues)
        if row.get("data_access_level") not in DATA_ACCESS_LEVELS:
            issues.append(RegistryIssue(path, "data_access_level must be raw|redacted|verified_only"))
        if row.get("status") not in ROLE_MAP_STATUSES:
            issues.append(RegistryIssue(path, "status must be covered|advisory|missing"))
        reuse = row.get("reuse_existing_agent")
        if not isinstance(reuse, bool):
            issues.append(RegistryIssue(path, "reuse_existing_agent must be boolean"))
        if reuse and not str(row.get("reuse_rationale", "")).strip():
            issues.append(RegistryIssue(path, "reused lanes require reuse_rationale"))
        if lane != agent_name and reuse is not True:
            issues.append(RegistryIssue(path, "renamed/equivalent lanes must set reuse_existing_agent true"))

    expected = {(team, lane) for team, lanes_for_team in REQUIRED_AGENT_LANES.items() for lane in lanes_for_team}
    missing = sorted(expected - covered_lanes)
    if missing:
        issues.append(RegistryIssue("required_lanes", f"missing covered lanes: {missing}"))
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
