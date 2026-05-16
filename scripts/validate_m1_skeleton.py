#!/usr/bin/env python3
"""Validate the Milestone 1 oh-my-paper skeleton.

This is intentionally structural. It does not run paper workflow behavior,
artifact gates, runtime adapters, or eval harness logic; those start in
Milestone 2.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    "paper-ai-orchestrator",
    "paper-ai-idea",
    "paper-ai-writing",
    "paper-ai-title-abstract",
    "paper-ai-introduction",
    "paper-ai-related-work",
    "paper-ai-method",
    "paper-ai-experiments",
    "paper-ai-figures",
    "paper-ai-limitations",
    "paper-ai-layout",
    "paper-ai-reviewer",
    "paper-ai-rebuttal",
]
REQUIRED_DOCS = [
    "README.md",
    ".gitignore",
    "docs/00_OVERVIEW.md",
    "docs/PRD.md",
    "docs/SKILL_GROUP_ARCHITECTURE.md",
    "docs/DUAL_MODE_TECH_DESIGN.md",
    "docs/HARNESS_EVAL_LOOP.md",
    "docs/ROADMAP.md",
    "docs/REPO_STRUCTURE_SPEC.md",
    "docs/ACCEPTANCE_EVALS.md",
    "docs/MATERIALS_MAPPING.md",
    "docs/MILESTONE1_SKELETON.md",
]
PRIVATE_PATHS = [
    ".omx/",
    ".spec-workflow/",
    "materials/",
    "temp/",
    "node_modules/",
    "package-lock.json",
    "package.json",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def check_exists() -> None:
    for item in REQUIRED_DOCS:
        if not (ROOT / item).exists():
            fail(f"missing required doc: {item}")
    for item in [".codex-plugin/plugin.json", "pyproject.toml", "AGENTS.md"]:
        if not (ROOT / item).exists():
            fail(f"missing required root skeleton file: {item}")


def check_ignored_paths() -> None:
    result = subprocess.run(
        ["git", "check-ignore", *PRIVATE_PATHS],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    ignored = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    missing = [path for path in PRIVATE_PATHS if path not in ignored]
    if missing:
        fail(f"private/local paths are not ignored: {missing}")

    tracked = subprocess.run(
        ["git", "ls-files", ".omx", ".spec-workflow", "materials", "temp", "node_modules", "package-lock.json", "package.json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.strip()
    if tracked:
        fail(f"private/local paths are tracked: {tracked}")


def check_plugin() -> None:
    data = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    if data.get("name") != "oh-my-paper":
        fail("plugin name must be oh-my-paper")
    if data.get("skills") != "./skills/":
        fail("plugin skills path must be ./skills/")


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path} missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path} has unterminated frontmatter")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"{path} invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def check_skills() -> None:
    for skill in SKILLS:
        root = ROOT / "skills" / skill
        skill_md = root / "SKILL.md"
        if not skill_md.exists():
            fail(f"missing skill file: {skill_md.relative_to(ROOT)}")
        text = skill_md.read_text()
        fm = parse_frontmatter(text, skill_md)
        if fm.get("name") != skill:
            fail(f"{skill} frontmatter name mismatch")
        if not fm.get("description"):
            fail(f"{skill} missing description")
        for heading in ["## Use when", "## Do not use when", "## Inputs", "## Outputs", "## Workflow", "## Gate"]:
            if heading not in text:
                fail(f"{skill} missing heading {heading}")
        if len(text.splitlines()) > 220:
            fail(f"{skill} SKILL.md too long for a stub")
        for sub in ["references", "evals", "agents"]:
            if not (root / sub).exists():
                fail(f"{skill} missing {sub}/")
        if not (root / "evals" / "README.md").exists():
            fail(f"{skill} missing evals/README.md")


def check_examples_and_fixtures() -> None:
    for item in [
        "examples/toy-paper-workspace/.paper-ai/PAPER_AI_STATE.md",
        "examples/toy-paper-workspace/.paper-ai/MATERIALS_USED.md",
        "examples/toy-paper-workspace/.paper-ai/TRACE.jsonl",
        "examples/toy-paper-workspace/paper/PAPER_BRIEF.md",
        "examples/toy-paper-workspace/paper/CLAIMS.md",
        "examples/toy-paper-workspace/paper/EVIDENCE_MAP.md",
        "tests/fixtures/evals/README.md",
    ]:
        if not (ROOT / item).exists():
            fail(f"missing synthetic example or fixture placeholder: {item}")
    for path in (ROOT / "tests/fixtures/evals").glob("*.jsonl"):
        for idx, line in enumerate(path.read_text().splitlines(), 1):
            data = json.loads(line)
            for key in ["schema_version", "fixture_id", "phase", "skill", "purpose", "expected", "privacy"]:
                if key not in data:
                    fail(f"{path.relative_to(ROOT)} line {idx} missing {key}")
            if data["privacy"] != "synthetic":
                fail(f"{path.relative_to(ROOT)} line {idx} is not synthetic")


def check_public_safety() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.splitlines()
    suffixes = (".md", ".json", ".toml", ".yaml")
    public_files = [ROOT / item for item in tracked if item.endswith(suffixes)]
    forbidden_terms = [
        "zlab-princeton-internal",
        "raw private material",
        "copied private material",
    ]
    for path in public_files:
        text = path.read_text(errors="ignore").lower() if path.exists() else ""
        for term in forbidden_terms:
            if term in text:
                fail(f"potential private material leak in {path.relative_to(ROOT)}")


def main() -> int:
    check_exists()
    check_ignored_paths()
    check_plugin()
    check_skills()
    check_examples_and_fixtures()
    check_public_safety()
    print("Milestone 1 skeleton validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
