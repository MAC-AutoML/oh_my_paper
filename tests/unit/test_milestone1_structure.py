from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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


class Milestone1StructureTest(unittest.TestCase):
    def test_plugin_manifest_points_to_skills(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "oh-my-paper")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue((ROOT / "skills").is_dir())

    def test_pyproject_has_uv_ready_entrypoint(self) -> None:
        project = tomllib.loads((ROOT / "pyproject.toml").read_text())
        self.assertEqual(project["project"]["name"], "oh-my-paper")
        self.assertEqual(project["project"]["scripts"]["oh-my-paper"], "oh_my_paper.cli:main")
        self.assertEqual(project["project"]["dependencies"], [])

    def test_all_skill_stubs_are_concise_and_gated(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill):
                text = (ROOT / "skills" / skill / "SKILL.md").read_text()
                self.assertIn(f"name: {skill}", text)
                self.assertIn("## Use when", text)
                self.assertIn("## Outputs", text)
                self.assertIn("## Gate", text)
                self.assertIn("Do not invent experiments", text)
                self.assertLessEqual(len(text.splitlines()), 220)

    def test_skill_references_are_substantive_not_placeholders(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill):
                refs = sorted((ROOT / "skills" / skill / "references").glob("*.md"))
                self.assertGreaterEqual(len(refs), 1)
                for ref in refs:
                    lines = [line for line in ref.read_text(encoding="utf-8").splitlines() if line.strip()]
                    self.assertGreaterEqual(len(lines), 20, f"{ref} is too sparse")

    def test_toy_workspace_is_synthetic_and_gate_aware(self) -> None:
        claims = (ROOT / "examples/toy-paper-workspace/paper/CLAIMS.md").read_text()
        materials_used = (ROOT / "examples/toy-paper-workspace/.paper-ai/MATERIALS_USED.md").read_text()
        self.assertIn("unsupported", claims)
        self.assertIn("synthetic", materials_used.lower())
        self.assertIn("Copied raw text", materials_used)

    def test_eval_fixture_directory_has_synthetic_jsonl_after_m2(self) -> None:
        fixture_dir = ROOT / "tests/fixtures/evals"
        self.assertTrue((fixture_dir / "README.md").exists())
        fixture_paths = sorted(fixture_dir.glob("*.jsonl"))
        self.assertGreaterEqual(len(fixture_paths), 3)
        for path in fixture_paths:
            for line in path.read_text().splitlines():
                if line.strip():
                    self.assertIn('"privacy":"synthetic"', line)


if __name__ == "__main__":
    unittest.main()
