"""Root config resolution and redacted status reporting for ARS workflows."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    base_url: str
    model: str
    api_key_env: str
    api_key_present: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "base_url": self.base_url,
            "model": self.model,
            "api_key_env": self.api_key_env,
            "api_key_present": self.api_key_present,
        }


@dataclass(frozen=True)
class ConfigResolution:
    schema_version: str
    status: str
    config_sources: list[dict[str, object]]
    models: dict[str, ModelConfig]
    semantic_scholar: dict[str, object]
    privacy: dict[str, object]
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "producer": "oh-my-paper:config-status",
            "status": self.status,
            "config_sources": self.config_sources,
            "models": {name: model.to_dict() for name, model in self.models.items()},
            "semantic_scholar": self.semantic_scholar,
            "privacy": self.privacy,
            "warnings": self.warnings,
        }


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    """Parse the small documented config subset without adding YAML deps."""

    if not path.exists():
        return {}
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, sep, value = line.strip().partition(":")
        if not sep:
            continue
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value.strip() == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _scalar(value.strip())
    return root


def _scalar(value: str) -> object:
    value = value.strip().strip('"\'')
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def resolve_config(config_path: str | Path | None = None, *, root: str | Path | None = None, env: dict[str, str] | None = None) -> ConfigResolution:
    repo = Path(root or Path.cwd())
    environ = dict(os.environ if env is None else env)
    cli_path = Path(config_path) if config_path else None
    if cli_path and not cli_path.is_absolute():
        cli_path = repo / cli_path
    root_config = repo / "config.yaml"
    env_path = repo / ".env"
    default_path = repo / "config.example.yaml"

    sources = [
        {"source": "cli", "path": str(cli_path) if cli_path else None, "present": bool(cli_path and cli_path.exists()), "used": False},
        {"source": "root", "path": str(root_config), "present": root_config.exists(), "used": False},
        {"source": "environment", "path": None, "present": bool(environ), "used": False},
        {"source": "env_file", "path": str(env_path), "present": env_path.exists(), "used": False},
        {"source": "defaults", "path": str(default_path), "present": default_path.exists(), "used": False},
    ]

    selected: dict[str, Any] = {}
    if cli_path and cli_path.exists():
        selected = parse_simple_yaml(cli_path)
        sources[0]["used"] = True
    elif root_config.exists():
        selected = parse_simple_yaml(root_config)
        sources[1]["used"] = True
    elif env_path.exists():
        selected = {"models": {"writer": _env_model(_load_env_file(env_path) | environ, "writer")}}
        sources[3]["used"] = True
    elif default_path.exists():
        selected = parse_simple_yaml(default_path)
        sources[4]["used"] = True
    else:
        sources[2]["used"] = True

    models = _resolve_models(selected, environ)
    scholar = _resolve_semantic_scholar(selected, environ)
    warnings: list[str] = []
    if scholar["mode"] == "api_key" and not scholar["api_key_present"]:
        warnings.append(f"Semantic Scholar api_key mode requires {scholar['api_key_env']}")
    status = "error" if warnings and scholar["mode"] == "api_key" else "ok"
    return ConfigResolution(
        schema_version="1.0",
        status=status,
        config_sources=sources,
        models=models,
        semantic_scholar=scholar,
        privacy={"raw_materials_dir": "materials", "generated_temp_dir": "temp", "hidden_rubric_dirs": [".paper-ai/private"]},
        warnings=warnings,
    )


def config_status_report(config_path: str | Path | None = None, *, root: str | Path | None = None, env: dict[str, str] | None = None) -> dict[str, object]:
    return resolve_config(config_path, root=root, env=env).to_dict()


def dump_config_status(config_path: str | Path | None = None) -> str:
    return json.dumps(config_status_report(config_path), indent=2, ensure_ascii=False)


def _resolve_models(data: dict[str, Any], env: dict[str, str]) -> dict[str, ModelConfig]:
    raw_models = data.get("models") if isinstance(data.get("models"), dict) else {}
    writer = dict(raw_models.get("writer", {})) if isinstance(raw_models.get("writer"), dict) else {}
    reviewer = dict(raw_models.get("reviewer", {})) if isinstance(raw_models.get("reviewer"), dict) else {}
    if not writer:
        writer = _env_model(env, "writer")
    if not reviewer:
        reviewer = {**writer, "model": env.get("OPENAI_REVIEWER_MODEL") or writer.get("model") or ""}
    return {"writer": _model_config(writer, env), "reviewer": _model_config(reviewer, env)}


def _env_model(env: dict[str, str], _name: str) -> dict[str, object]:
    return {
        "provider": "openai-compatible",
        "base_url": env.get("OPENAI_BASE_URL", ""),
        "model": env.get("OPENAI_MODEL", ""),
        "api_key_env": "OPENAI_API_KEY",
    }


def _model_config(raw: dict[str, object], env: dict[str, str]) -> ModelConfig:
    key_env = str(raw.get("api_key_env") or "OPENAI_API_KEY")
    return ModelConfig(
        provider=str(raw.get("provider") or "openai-compatible"),
        base_url=str(raw.get("base_url") or env.get("OPENAI_BASE_URL", "")),
        model=str(raw.get("model") or env.get("OPENAI_MODEL", "")),
        api_key_env=key_env,
        api_key_present=bool(env.get(key_env)),
    )


def _resolve_semantic_scholar(data: dict[str, Any], env: dict[str, str]) -> dict[str, object]:
    raw = data.get("semantic_scholar") if isinstance(data.get("semantic_scholar"), dict) else {}
    mode = str(env.get("SEMANTIC_SCHOLAR_MODE") or raw.get("mode") or "auto")
    key_env = str(raw.get("api_key_env") or "SEMANTIC_SCHOLAR_API_KEY")
    present = bool(env.get(key_env))
    effective = "api_key" if mode == "auto" and present else "no_key" if mode == "auto" else mode
    interval_key = "request_interval_seconds_api_key" if effective == "api_key" else "request_interval_seconds_no_key"
    default_interval = 0.25 if effective == "api_key" else 2.0
    return {
        "mode": mode,
        "effective_mode": effective,
        "api_key_env": key_env,
        "api_key_present": present,
        "cache_dir": str(raw.get("cache_dir") or ".paper-ai/cache/semantic-scholar"),
        "title_similarity_threshold": float(raw.get("title_similarity_threshold") or 0.7),
        "request_interval_seconds": float(raw.get(interval_key) or raw.get("request_interval_seconds") or default_interval),
    }


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values
