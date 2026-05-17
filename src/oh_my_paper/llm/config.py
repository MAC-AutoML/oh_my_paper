"""Local .env loading for OpenAI-compatible LLM endpoints."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str
    writer_model: str
    reviewer_model: str

    @property
    def chat_completions_url(self) -> str:
        return self.base_url.rstrip("/") + "/chat/completions"


def _parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].strip()
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    return key.strip(), value.strip().strip('"\'')


def load_env_file(path: str | Path) -> dict[str, str]:
    env_path = Path(path)
    if not env_path.exists():
        return {}
    values: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        parsed = _parse_env_line(line)
        if parsed is not None:
            values[parsed[0]] = parsed[1]
    return values


def load_llm_config(path: str | Path = ".env") -> LLMConfig:
    values = load_env_file(path)
    values.update({key: value for key, value in os.environ.items() if value})
    api_key = values.get("OPENAI_API_KEY") or values.get("api_key") or values.get("GEMINI_API_KEY")
    base_url = values.get("OPENAI_BASE_URL") or values.get("base_url")
    writer_model = values.get("OPENAI_MODEL") or values.get("MODEL") or values.get("model_1")
    reviewer_model = values.get("OPENAI_REVIEWER_MODEL") or values.get("model_2") or writer_model
    missing = [name for name, value in {"api_key": api_key, "base_url": base_url, "model_1": writer_model}.items() if not value]
    if missing:
        raise ValueError(f"missing LLM config field(s): {', '.join(missing)}")
    return LLMConfig(
        api_key=str(api_key),
        base_url=str(base_url),
        writer_model=str(writer_model),
        reviewer_model=str(reviewer_model),
    )
