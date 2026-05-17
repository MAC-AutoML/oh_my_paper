"""Small stdlib config loader for root config.yaml/config.example.yaml."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
SEMANTIC_MODES = {"auto", "api_key", "no_key", "disabled"}
_ENV_REF = re.compile(r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$")


@dataclass(frozen=True)
class ProjectConfig:
    data: dict[str, Any]
    sources: list[dict[str, Any]]
    config_path: Path | None
    root: Path

    def semantic_mode(self) -> str:
        semantic = self.data.get("semantic_scholar", {})
        mode = str(semantic.get("mode", "auto"))
        if mode not in SEMANTIC_MODES:
            return "disabled"
        if mode == "auto":
            return "api_key" if self.semantic_api_key() else "no_key"
        return mode

    def semantic_api_key(self) -> str | None:
        env_name = str(self.data.get("semantic_scholar", {}).get("api_key_env", "SEMANTIC_SCHOLAR_API_KEY"))
        value = os.environ.get(env_name)
        return value if value else None

    def semantic_cache_dir(self, workspace: str | Path | None = None) -> Path:
        raw = str(self.data.get("semantic_scholar", {}).get("cache_dir", ".paper-ai/cache/semantic-scholar"))
        path = Path(raw)
        if path.is_absolute():
            return path
        return (Path(workspace) if workspace else self.root) / path


def load_project_config(config_path: str | Path | None = None, *, root: str | Path | None = None) -> ProjectConfig:
    repo = Path(root or Path.cwd()).resolve()
    cli_path = Path(config_path).resolve() if config_path else None
    root_yaml = repo / "config.yaml"
    example_yaml = repo / "config.example.yaml"
    sources: list[dict[str, Any]] = []
    chosen: Path | None = None
    if cli_path is not None:
        chosen = cli_path
        sources.append(_source("cli", cli_path, cli_path.exists(), True))
        sources.append(_source("root", root_yaml, root_yaml.exists(), False))
    elif root_yaml.exists():
        chosen = root_yaml
        sources.append(_source("root", root_yaml, True, True))
    else:
        sources.append(_source("root", root_yaml, False, False))
        if example_yaml.exists():
            chosen = example_yaml
            sources.append(_source("defaults", example_yaml, True, True))
    if chosen is None:
        data: dict[str, Any] = {}
    else:
        data = _parse_simple_yaml(chosen.read_text(encoding="utf-8"))
    data = _merge_defaults(data)
    data = _resolve_env_refs(data)
    sources.append(_source("environment", Path("<process-env>"), True, False))
    env_file = repo / ".env"
    sources.append(_source("dotenv", env_file, env_file.exists(), False))
    return ProjectConfig(data=data, sources=sources, config_path=chosen, root=repo)


def config_status_report(config_path: str | Path | None = None, *, root: str | Path | None = None, workspace: str | Path | None = None) -> dict[str, Any]:
    config = load_project_config(config_path, root=root)
    data = config.data
    warnings: list[str] = []
    semantic = data["semantic_scholar"]
    mode = str(semantic.get("mode", "auto"))
    if mode not in SEMANTIC_MODES:
        warnings.append(f"unknown semantic_scholar.mode {mode!r}; effective mode disabled")
    effective_mode = config.semantic_mode()
    if mode == "api_key" and not config.semantic_api_key():
        warnings.append("semantic_scholar.mode api_key requires SEMANTIC_SCHOLAR_API_KEY")
    report = {
        "schema_version": SCHEMA_VERSION,
        "producer": "oh-my-paper:config-status",
        "created_at": _now(),
        "workspace": str(Path(workspace or config.root)),
        "inputs": [str(config.config_path)] if config.config_path else [],
        "status": "error" if any("requires" in item for item in warnings) else ("warning" if warnings else "ok"),
        "config_sources": config.sources,
        "models": _redacted_models(data.get("models", {})),
        "semantic_scholar": {
            "mode": mode,
            "effective_mode": effective_mode if effective_mode != "auto" else "no_key",
            "api_key_env": semantic.get("api_key_env", "SEMANTIC_SCHOLAR_API_KEY"),
            "api_key_present": bool(config.semantic_api_key()),
            "cache_dir": str(config.semantic_cache_dir(workspace)),
            "title_similarity_threshold": float(semantic.get("title_similarity_threshold", 0.70)),
            "request_interval_seconds": _request_interval(semantic, effective_mode),
        },
        "privacy": data["privacy"],
        "warnings": warnings,
    }
    return report


def write_config_resolution(workspace: str | Path, config_path: str | Path | None = None) -> Path:
    workspace_path = Path(workspace)
    state_dir = workspace_path / ".paper-ai"
    state_dir.mkdir(parents=True, exist_ok=True)
    report = config_status_report(config_path, root=Path.cwd(), workspace=workspace_path)
    out = state_dir / "CONFIG_RESOLUTION.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def config_hash(path: str | Path) -> str:
    text = Path(path).read_text(encoding="utf-8") if Path(path).exists() else ""
    redacted = re.sub(r"(?i)(api[_-]?key\s*[:=]\s*)\S+", r"\1<redacted>", text)
    return hashlib.sha256(redacted.encode("utf-8")).hexdigest()


def _source(kind: str, path: Path, present: bool, used: bool) -> dict[str, Any]:
    return {"source": kind, "path": str(path), "present": bool(present), "used": bool(used)}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _request_interval(semantic: dict[str, Any], effective_mode: str) -> float:
    key = "request_interval_seconds_api_key" if effective_mode == "api_key" else "request_interval_seconds_no_key"
    return float(semantic.get(key, 0.25 if effective_mode == "api_key" else 2.0))


def _redacted_models(models: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for role, settings in models.items():
        if not isinstance(settings, dict):
            continue
        env_name = str(settings.get("api_key_env", "OPENAI_API_KEY"))
        redacted[role] = {
            "provider": settings.get("provider", "openai-compatible"),
            "base_url": settings.get("base_url", ""),
            "model": settings.get("model", ""),
            "api_key_env": env_name,
            "api_key_present": bool(os.environ.get(env_name)),
        }
    return redacted


def _merge_defaults(data: dict[str, Any]) -> dict[str, Any]:
    merged = {
        "models": {
            "writer": {"provider": "openai-compatible", "base_url": "${OPENAI_BASE_URL}", "api_key_env": "OPENAI_API_KEY", "model": "${OPENAI_MODEL}"},
            "reviewer": {"provider": "openai-compatible", "base_url": "${OPENAI_BASE_URL}", "api_key_env": "OPENAI_API_KEY", "model": "${OPENAI_REVIEWER_MODEL}"},
        },
        "semantic_scholar": {
            "mode": "auto",
            "api_key_env": "SEMANTIC_SCHOLAR_API_KEY",
            "request_interval_seconds_no_key": 2.0,
            "request_interval_seconds_api_key": 0.25,
            "cache_dir": ".paper-ai/cache/semantic-scholar",
            "title_similarity_threshold": 0.70,
        },
        "pipeline": {"integrity_stage_2_5_required": True, "integrity_stage_4_5_required": True, "reviewer_score_regression_blocks": True},
        "privacy": {"raw_materials_dir": "materials", "generated_temp_dir": "temp", "hidden_rubric_dirs": ["hidden", "rubrics"]},
    }
    return _deep_merge(merged, data)


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _resolve_env_refs(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _resolve_env_refs(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_resolve_env_refs(item) for item in value]
    if isinstance(value, str):
        match = _ENV_REF.match(value.strip())
        if match:
            return os.environ.get(match.group(1), "")
    return value


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if value in {"true", "false"}:
        return value == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value.strip('"\'')


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    last_key_at_indent: dict[int, tuple[dict[str, Any], str]] = {}
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            item = _parse_scalar(line[2:])
            if not isinstance(parent, list):
                container, key = last_key_at_indent[indent]
                parent = []
                container[key] = parent
                stack.append((indent, parent))
            parent.append(item)
            continue
        key, _, remainder = line.partition(":")
        key = key.strip()
        if remainder.strip():
            value = _parse_scalar(remainder)
            parent[key] = value
        else:
            value = {}
            parent[key] = value
            stack.append((indent, value))
            last_key_at_indent[indent + 2] = (parent, key)
    return root
