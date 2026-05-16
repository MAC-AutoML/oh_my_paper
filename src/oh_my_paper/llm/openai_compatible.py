"""Tiny OpenAI-compatible chat client used by local paper workflows."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from oh_my_paper.llm.config import LLMConfig


@dataclass(frozen=True)
class ChatResult:
    content: str
    raw: dict[str, object]


def chat_completion(
    config: LLMConfig,
    *,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.2,
    max_tokens: int = 12000,
    timeout_s: int = 900,
) -> ChatResult:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        config.chat_completions_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:1000]
        raise RuntimeError(f"LLM endpoint HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"LLM endpoint request failed: {exc}") from exc
    content = _extract_content(raw)
    if not content.strip():
        raise RuntimeError("LLM endpoint returned an empty assistant message")
    return ChatResult(content=content, raw=raw)


def _extract_content(raw: dict[str, object]) -> str:
    choices = raw.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        if isinstance(content, str):
            return content
    text = first.get("text")
    return text if isinstance(text, str) else ""
