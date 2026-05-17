from __future__ import annotations

import os
import tempfile
import unittest
from importlib import resources
from pathlib import Path
from unittest import mock

from oh_my_paper.paper_core.pipeline import pipeline_plan, resume_stage_from_passport
from oh_my_paper.paper_core.registry import (
    REQUIRED_AGENT_LANES,
    agent_registry,
    agent_role_map_registry,
    mode_registry,
    route_for_trigger,
    validate_agent_role_map,
    validate_agents,
    validate_modes,
)
from oh_my_paper.paper_core.validators import (
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
PUBLIC_TARGETS.extend((ROOT / "skills").glob("deep-research/SKILL.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("academic-paper/SKILL.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("academic-paper-reviewer/SKILL.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("academic-pipeline/SKILL.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("paper-ai-*/SKILL.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("paper-ai-*/references/**/*.md"))
PUBLIC_TARGETS.extend((ROOT / "skills").glob("paper-ai-*/agents/openai.yaml"))
PUBLIC_TARGETS.extend((ROOT / "templates").glob("**/*"))
FORBIDDEN = [
    "".join(["O", "M", "X"]),
    "-".join(["oh", "my", "codex"]),
    "$" + "ralph",
    "$" + "team",
    "$" + "ultragoal",
    "$" + "autoresearch-goal",
    "$" + "performance-goal",
    " ".join(["omx", "team"]),
    " ".join(["omx", "state"]),
    "." + "omx/",
]


class PaperCoreRegistryTest(unittest.TestCase):
    def test_four_top_level_skills_have_bilingual_descriptions(self) -> None:
        for skill in ["deep-research", "academic-paper", "academic-paper-reviewer", "academic-pipeline"]:
            with self.subTest(skill=skill):
                text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("description:", text)
                self.assertRegex(text, r"[\u4e00-\u9fff]")
                self.assertIn(" / ", text)
                self.assertIn("Root config", text)

    def test_mode_registry_schema_and_count(self) -> None:
        modes = mode_registry()
        self.assertEqual(len(modes), 25)
        self.assertTrue(validate_modes(modes).ok)
        for row in modes:
            self.assertIsInstance(row["owner_skill"], str)
            self.assertIsInstance(row["secondary_skills"], list)
            self.assertIn(row["status"], {"implemented", "partial", "advisory", "deferred"})
            self.assertNotIn("→", row["status"])

    def test_agent_registry_covers_38_source_role_refs(self) -> None:
        agents = agent_registry()
        paths = [path for row in agents for path in row["source_role_refs"]]
        self.assertEqual(len(paths), 38)
        self.assertEqual(len(set(paths)), 38)
        self.assertTrue(validate_agents(agents).ok)

    def test_routes_cover_paper_intents(self) -> None:
        cases = {
            "/paper-plan": ("academic-paper", "plan", "paper-ai-idea"),
            "/paper-full": ("academic-pipeline", "pipeline", "paper-ai-orchestrator"),
            "帮我审查这篇论文": ("academic-paper-reviewer", "full", "paper-ai-reviewer"),
            "帮我做系统性文献回顾": ("deep-research", "systematic-review", "paper-ai-research"),
        }
        for trigger, expected in cases.items():
            route = route_for_trigger(trigger)
            self.assertIsNotNone(route)
            self.assertEqual((route["subsystem"], route["mode"], route["owner_skill"]), expected)

    def test_registry_resources_load_with_importlib_resources(self) -> None:
        files = resources.files("oh_my_paper.paper_core.resources")
        self.assertTrue(files.joinpath("modes.json").is_file())
        self.assertTrue(files.joinpath("agents.json").is_file())
        self.assertTrue(files.joinpath("routes.json").is_file())
        self.assertTrue(files.joinpath("agent_role_map.json").is_file())

    def test_agent_role_map_exists_and_validates(self) -> None:
        role_map = agent_role_map_registry()
        self.assertTrue(validate_agent_role_map(role_map).ok)
        self.assertEqual(role_map["schema_version"], "1.0")

    def test_required_research_writing_review_pipeline_lanes_covered(self) -> None:
        role_map = agent_role_map_registry()
        covered = {
            (row["team"], row["required_lane"])
            for row in role_map["required_lanes"]
            if row["status"] == "covered"
        }
        expected = {
            (team, lane)
            for team, lanes in REQUIRED_AGENT_LANES.items()
            for lane in lanes
        }
        self.assertEqual(covered, expected)

    def test_no_duplicate_agent_lane_without_rejection_reason(self) -> None:
        role_map = agent_role_map_registry()
        duplicated = [*role_map["required_lanes"], dict(role_map["required_lanes"][0])]
        result = validate_agent_role_map({**role_map, "required_lanes": duplicated})
        self.assertFalse(result.ok)
        self.assertIn("duplicate required lane", " ".join(issue.message for issue in result.issues))

    def test_existing_agent_reuse_preferred_over_new_duplicate(self) -> None:
        role_map = agent_role_map_registry()
        lanes_by_name = {row["required_lane"]: row for row in role_map["required_lanes"]}
        reused_equivalents = {
            "paper-research-lead": "paper-research-architect",
            "paper-drafting-lead": "paper-draft-writer",
            "paper-integrity-auditor": "paper-integrity-verifier",
        }
        for lane, existing_agent in reused_equivalents.items():
            self.assertEqual(lanes_by_name[lane]["codex_agent_name"], existing_agent)
            self.assertIs(lanes_by_name[lane]["reuse_existing_agent"], True)
            self.assertTrue(lanes_by_name[lane]["reuse_rationale"])
        self.assertFalse((ROOT / ".codex" / "agents" / "paper-research-lead.toml").exists())
        self.assertFalse((ROOT / ".codex" / "agents" / "paper-drafting-lead.toml").exists())
        self.assertFalse((ROOT / ".codex" / "agents" / "paper-integrity-auditor.toml").exists())

    def test_agent_role_map_files_have_owner_and_data_access_level(self) -> None:
        for row in agent_role_map_registry()["required_lanes"]:
            agent_path = ROOT / row["agent_file"]
            self.assertTrue(agent_path.exists(), row["agent_file"])
            text = agent_path.read_text(encoding="utf-8")
            self.assertIn(f"Owner skill: {row['owner_skill']}.", text)
            self.assertIn(f"Data access level: {row['data_access_level']}.", text)


class PaperCoreValidatorTest(unittest.TestCase):
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


class PaperCorePipelineTest(unittest.TestCase):
    def test_pipeline_plan_has_expected_next_stage(self) -> None:
        plan = pipeline_plan("review")
        self.assertEqual(plan.next_stage, "revision_coaching")
        self.assertIn("paper/REVIEW_SIMULATION.md", plan.required_artifacts)

    def test_resume_stage_from_passport_status(self) -> None:
        self.assertEqual(resume_stage_from_passport({"verification_status": "verified"}), "finalize_disclosure")
        self.assertEqual(resume_stage_from_passport({"verification_status": "draft"}), "integrity_before_review")
        self.assertIsNone(resume_stage_from_passport({"verification_status": "blocked"}))


class PaperCoreBoundaryTest(unittest.TestCase):
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

    def test_paper_core_files_under_line_budget(self) -> None:
        offenders = []
        for path in (ROOT / "src" / "oh_my_paper" / "paper_core").glob("*.py"):
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
