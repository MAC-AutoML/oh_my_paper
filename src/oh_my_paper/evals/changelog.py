"""Regression changelog helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from oh_my_paper.evals.report import EvalReport


def append_changelog(path: str | Path, report: EvalReport, note: str) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"## {datetime.now(timezone.utc).isoformat()}",
        "",
        f"- Note: {note}",
        f"- Fixtures: {', '.join(report.fixture_files)}",
        f"- Result: {'pass' if report.ok else 'fail'}",
        f"- Total: {len(report.results)}",
        "",
    ]
    with target.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return target
