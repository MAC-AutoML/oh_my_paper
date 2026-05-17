from __future__ import annotations

import os
import tempfile
import unittest
from importlib import resources
from pathlib import Path
from unittest import mock

from oh_my_paper.ars_compat.pipeline import pipeline_plan, resume_stage_from_passport
from oh_my_paper.ars_compat.registry import agent_registry, mode_registry, route_for_trigger, validate_agents, validate_modes
from oh_my_paper.ars_compat.validators import (
    validate_citation_anchors,
    validate_integrity_report,
    validate_material_passport,
    validate_sprint_contract,
    validate_claim_support,
)
from oh_my_paper.llm.config import load_llm_config

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_TARGETS = [ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / ".codex-plugin" / "plugin.json"]
PUBLIC_TARGETS.extend((ROOT / "docs").glob("**/*.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("paper-ai-*/SKILL.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("paper-ai-*/references/**/*.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("paper-ai-*/agents/openai.yaml"))
PUBLIC_TARGETS.extend((ROOT / "templates").glob("**/*"))
FORBIDDEN = ["OMX", "oh-my-codex", "$ralph", "$team", "$ultragoal", "$autoresearch-goal", "$performance-goal", "omx team", "omx state", ".omx/"]


class ArsCompatRegistryTest(unittest.TestCase):
    def test_mode_registry_schema_and_count(self) -> None:
        modes = mode_registry()
        self.assertEqual(len(modes), 25)
        self.assertTrue(validate_modes(modes).ok)
        for row in modes:
            self.assertIsInstance(row["owner_skill"], str)
            self.assertIsInstance(row["secondary_skills"], list)
            self.assertIn(row["status"], {"implemented", "partial", "advisory", "deferred"})
            self.assertNotIn("→", row["status"])

    def test_agent_registry_covers_38_old_paths(self) -> None:
        agents = agent_registry()
        paths = [path for row in agents for path in row["old_agent_paths"]]
        self.assertEqual(len(paths), 38)
        self.assertEqual(len(set(paths)), 38)
        self.assertTrue(validate_agents(agents).ok)

    def test_routes_cover_old_intents(self) -> None:
        cases = {
            "/ars-plan": ("academic-paper", "plan", "paper-ai-idea"),
            "/ars-full": ("academic-pipeline", "pipeline", "paper-ai-orchestrator"),
            "帮我审查这篇论文": ("academic-paper-reviewer", "full", "paper-ai-reviewer"),
            "帮我做系统性文献回顾": ("deep-research", "systematic-review", "paper-ai-research"),
        }
        for trigger, expected in cases.items():
            route = route_for_trigger(trigger)
            self.assertIsNotNone(route)
            self.assertEqual((route["subsystem"], route["mode"], route["owner_skill"]), expected)

    def test_registry_resources_load_with_importlib_resources(self) -> None:
        files = resources.files("oh_my_paper.ars_compat.resources")
        self.assertTrue(files.joinpath("modes.json").is_file())
        self.assertTrue(files.joinpath("agents.json").is_file())
        self.assertTrue(files.joinpath("routes.json").is_file())


class ArsCompatValidatorTest(unittest.TestCase):
    def _json_file(self, payload: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".json")
        handle.write(payload)
        handle.close()
        return Path(handle.name)

    def test_material_passport_json_validates(self) -> None:
        path = self._json_file('{"passport_id":"p1","verification_status":"draft","reset_boundaries":[]}')
        self.assertTrue(validate_material_passport(path).ok)

    def test_sprint_contract_requires_precommitment(self) -> None:
        path = self._json_file('{"contract_id":"c1","reviewer_role":"eic"}')
        result = validate_sprint_contract(path)
        self.assertFalse(result.ok)
        self.assertIn("phase1_commitment", " ".join(result.errors))

    def test_citation_anchor_shape_validates(self) -> None:
        path = self._json_file('{"anchors":[{"claim_id":"C1","citation_key":"smith2026","locator":"p. 3"}]}')
        self.assertTrue(validate_citation_anchors(path).ok)

    def test_integrity_report_requires_gate_outcome(self) -> None:
        path = self._json_file('{"stage":"final","checks":[]}')
        self.assertFalse(validate_integrity_report(path).ok)

    def test_claim_support_gate_flags_supported_without_evidence(self) -> None:
        result = validate_claim_support([{"id": "C1", "status": "supported", "evidence": []}])
        self.assertFalse(result.ok)


class ArsCompatPipelineTest(unittest.TestCase):
    def test_pipeline_plan_has_expected_next_stage(self) -> None:
        plan = pipeline_plan("review")
        self.assertEqual(plan.next_stage, "revision_coaching")
        self.assertIn("paper/REVIEW_SIMULATION.md", plan.required_artifacts)

    def test_resume_stage_from_passport_status(self) -> None:
        self.assertEqual(resume_stage_from_passport({"verification_status": "verified"}), "finalize_disclosure")
        self.assertEqual(resume_stage_from_passport({"verification_status": "draft"}), "integrity_before_review")
        self.assertIsNone(resume_stage_from_passport({"verification_status": "blocked"}))


class ArsCompatBoundaryTest(unittest.TestCase):
    def test_public_product_files_do_not_expose_omx_boundary(self) -> None:
        offenders: list[str] = []
        for path in PUBLIC_TARGETS:
            if not path.is_file() or ".omx" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN:
                if token in text:
                    offenders.append(f"{path.relative_to(ROOT)} contains {token}")
        self.assertEqual(offenders, [])

    def test_codex_agent_tomls_exist_for_implemented_roles(self) -> None:
        missing = []
        for row in agent_registry():
            if row["status"] == "implemented":
                path = ROOT / ".codex" / "agents" / f"{row['codex_agent_name']}.toml"
                if not path.exists():
                    missing.append(str(path.relative_to(ROOT)))
        self.assertEqual(missing, [])

    def test_ars_compat_files_under_line_budget(self) -> None:
        offenders = []
        for path in (ROOT / "src" / "oh_my_paper" / "ars_compat").glob("*.py"):
            lines = len(path.read_text(encoding="utf-8").splitlines())
            if lines > 550:
                offenders.append(f"{path}: {lines}")
        self.assertEqual(offenders, [])


class LLMConfigPrecedenceTest(unittest.TestCase):
    def test_environment_overrides_env_file(self) -> None:
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as handle:
            handle.write("OPENAI_API_KEY=file-key\nOPENAI_BASE_URL=https://file.example\nOPENAI_MODEL=file-model\nmodel_2=file-reviewer\n")
            env_path = handle.name
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "env-key", "OPENAI_MODEL": "env-model", "OPENAI_REVIEWER_MODEL": "env-reviewer"}, clear=False):
            config = load_llm_config(env_path)
        self.assertEqual(config.api_key, "env-key")
        self.assertEqual(config.base_url, "https://file.example")
        self.assertEqual(config.writer_model, "env-model")
        self.assertEqual(config.reviewer_model, "env-reviewer")


if __name__ == "__main__":
    unittest.main()
