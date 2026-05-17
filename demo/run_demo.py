"""Deterministic oh my paper demo generator.

Run with:
    uv run python demo/run_demo.py

The script uses stdlib-only templates and synthetic numbers so the demo is
stable, explainable, and safe to commit.
"""

from __future__ import annotations

from pathlib import Path

from demo_figures import figure_hierarchy, figure_pipeline, figure_results
from demo_paper import build_explain, build_paper
from demo_process import (
    build_figure_prompts,
    build_imagegen_process,
    build_iteration_log,
    build_manifest,
    build_process_log,
    build_structured_input,
    build_workflow_plan,
)

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input_material.md"
PAPER = ROOT / "paper.md"
EXPLAIN_DIR = ROOT / "explain"
FIG_DIR = ROOT / "figures"
PROCESS = ROOT / "PROCESS_LOG.md"
MANIFEST = ROOT / "MANIFEST.md"


def main() -> int:
    material = INPUT.read_text(encoding="utf-8")
    EXPLAIN_DIR.mkdir(exist_ok=True)
    FIG_DIR.mkdir(exist_ok=True)
    outputs = {
        PAPER: build_paper(material),
        EXPLAIN_DIR / "why_each_section.md": build_explain(),
        ROOT / "STRUCTURED_INPUT.yaml": build_structured_input(material),
        ROOT / "WORKFLOW_PLAN.md": build_workflow_plan(),
        ROOT / "ITERATION_LOG.md": build_iteration_log(),
        FIG_DIR / "figure1_pipeline.svg": figure_pipeline(),
        FIG_DIR / "figure2_results.svg": figure_results(),
        FIG_DIR / "figure3_hierarchy.svg": figure_hierarchy(),
        FIG_DIR / "figure_prompts.md": build_figure_prompts(),
        FIG_DIR / "IMAGEGEN_PROCESS.md": build_imagegen_process(),
        PROCESS: build_process_log(material),
    }
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    MANIFEST.write_text(build_manifest(outputs, ROOT), encoding="utf-8")
    print(f"Generated demo outputs under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
