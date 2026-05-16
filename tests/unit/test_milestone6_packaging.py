from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from oh_my_paper.packaging.skills import install_skills, list_installed_skills, uninstall_skills

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SKILLS = {
    "paper-ai-orchestrator",
    "paper-ai-research-process",
    "paper-ai-writing",
    "paper-ai-figures",
    "paper-ai-layout",
    "paper-ai-reviewer",
    "paper-ai-rebuttal",
    "paper-ai-eval-loop",
}


class Milestone6PackagingTest(unittest.TestCase):
    def test_install_list_and_uninstall_skills_in_target_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            target = Path(tempdir) / "skills"
            result = install_skills(target, root=ROOT)
            self.assertEqual(set(result.installed), EXPECTED_SKILLS)
            self.assertEqual(set(list_installed_skills(target)), EXPECTED_SKILLS)
            for skill in EXPECTED_SKILLS:
                self.assertTrue((target / skill / "SKILL.md").exists())
            skipped = install_skills(target, root=ROOT)
            self.assertEqual(set(skipped.skipped), EXPECTED_SKILLS)
            overwritten = install_skills(target, overwrite=True, root=ROOT)
            self.assertEqual(set(overwritten.installed), EXPECTED_SKILLS)
            removed = uninstall_skills(target)
            self.assertEqual(set(removed.removed), EXPECTED_SKILLS)
            self.assertEqual(list_installed_skills(target), [])

    def test_config_templates_are_safe_placeholders(self) -> None:
        env_example = (ROOT / "templates/env.example").read_text(encoding="utf-8")
        config_example = (ROOT / "templates/config.example.yaml").read_text(encoding="utf-8")
        self.assertIn("OPENAI_API_KEY=", env_example)
        self.assertNotIn("sk-", env_example)
        self.assertIn("transport: stdio", config_example)
        self.assertIn("websocket remains experimental", config_example)


if __name__ == "__main__":
    unittest.main()
