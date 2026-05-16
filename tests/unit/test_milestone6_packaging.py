from __future__ import annotations

import unittest
from pathlib import Path

from oh_my_paper.packaging.skills import official_install_command, packaging_status, skill_package_info

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SKILLS = {
    "paper-ai-ac-simulator",
    "paper-ai-camera-ready",
    "paper-ai-claim-evidence",
    "paper-ai-eval-loop",
    "paper-ai-experiment-planner",
    "paper-ai-experiment-writing",
    "paper-ai-figures",
    "paper-ai-introduction",
    "paper-ai-language-polish",
    "paper-ai-layout",
    "paper-ai-limitations",
    "paper-ai-literature-map",
    "paper-ai-material-intake",
    "paper-ai-method-writing",
    "paper-ai-orchestrator",
    "paper-ai-project-planner",
    "paper-ai-rebuttal",
    "paper-ai-related-work",
    "paper-ai-research-process",
    "paper-ai-research-question",
    "paper-ai-reviewer",
    "paper-ai-revision-plan",
    "paper-ai-submission-check",
    "paper-ai-tables",
    "paper-ai-title-abstract",
    "paper-ai-writing",
}


class Milestone6PackagingTest(unittest.TestCase):
    def test_skill_folders_match_official_skill_anatomy(self) -> None:
        infos = skill_package_info(ROOT)
        self.assertEqual({info.name for info in infos}, EXPECTED_SKILLS)
        for info in infos:
            self.assertTrue(info.has_skill_md, info)
            self.assertTrue(info.path.startswith("skills/paper-ai-"))
            text = (ROOT / info.path / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {info.name}", text)
            self.assertIn("description:", text)

    def test_official_installer_command_uses_repo_and_path_flags(self) -> None:
        command = official_install_command(root=ROOT)
        self.assertEqual(command[:3], ["install-skill-from-github.py", "--repo", "MAC-AutoML/oh_my_paper"])
        paths = [command[index + 1] for index, item in enumerate(command) if item == "--path"]
        self.assertEqual(set(paths), {f"skills/{skill}" for skill in EXPECTED_SKILLS})
        self.assertNotIn("--dest", command)

    def test_packaging_status_is_official_installer_metadata_not_custom_copy(self) -> None:
        status = packaging_status(ROOT)
        self.assertTrue(status["ok"])
        self.assertEqual(status["installer"], "Codex system skill-installer")
        self.assertIn("official_command", status)

    def test_config_templates_are_safe_placeholders(self) -> None:
        env_example = (ROOT / "templates/env.example").read_text(encoding="utf-8")
        config_example = (ROOT / "templates/config.example.yaml").read_text(encoding="utf-8")
        self.assertIn("OPENAI_API_KEY=", env_example)
        self.assertNotIn("sk-", env_example)
        self.assertIn("transport: stdio", config_example)
        self.assertIn("websocket remains experimental", config_example)


if __name__ == "__main__":
    unittest.main()
