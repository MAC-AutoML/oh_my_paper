"""Eval registry and report generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from oh_my_paper.evals.fixtures import EvalResult, run_fixture_file


@dataclass(frozen=True)
class EvalReport:
    fixture_files: list[str]
    results: list[EvalResult]

    @property
    def ok(self) -> bool:
        return all(result.ok for result in self.results)

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "fixture_files": self.fixture_files,
            "summary": {
                "total": len(self.results),
                "pass": sum(1 for result in self.results if result.status == "pass"),
                "fail": sum(1 for result in self.results if result.status == "fail"),
                "warn": sum(1 for result in self.results if result.status == "warn"),
            },
            "results": [result.to_dict() for result in self.results],
        }

    def to_markdown(self) -> str:
        rows = ["| Fixture | Status | Reasons |", "| --- | --- | --- |"]
        for result in self.results:
            reasons = "; ".join(result.reasons) if result.reasons else "-"
            rows.append(f"| `{result.fixture_id}` | {result.status} | {reasons} |")
        return "# Eval Regression Report\n\n" + "\n".join(rows) + "\n"


def run_eval_report(fixture_files: list[str | Path]) -> EvalReport:
    results: list[EvalResult] = []
    names: list[str] = []
    for fixture_file in fixture_files:
        path = Path(fixture_file)
        names.append(str(path))
        results.extend(run_fixture_file(path))
    return EvalReport(names, results)


def write_eval_report(report: EvalReport, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".json":
        path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        path.write_text(report.to_markdown(), encoding="utf-8")
    return path
