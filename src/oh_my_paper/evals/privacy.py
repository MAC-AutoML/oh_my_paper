"""Privacy and redaction helpers for fixture capture."""

from __future__ import annotations

import re
from pathlib import Path

PUBLIC_FIXTURE_ROOT = Path("tests/fixtures/evals")
SENSITIVE_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\b(?:api[_-]?key|token|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
]


def redact_text(text: str) -> str:
    redacted = text
    for pattern in SENSITIVE_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def is_public_fixture_path(path: Path) -> bool:
    normalized = Path(path).resolve().as_posix()
    marker = "/" + PUBLIC_FIXTURE_ROOT.as_posix() + "/"
    return normalized.endswith("/" + PUBLIC_FIXTURE_ROOT.as_posix()) or marker in normalized


def assert_fixture_privacy_allowed(output_path: Path, privacy: str) -> None:
    if privacy not in {"synthetic", "redacted", "private"}:
        raise ValueError("privacy must be synthetic, redacted, or private")
    if privacy == "private" and is_public_fixture_path(output_path):
        raise ValueError("private fixtures cannot be written under tests/fixtures/evals")
