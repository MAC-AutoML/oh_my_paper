from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from oh_my_paper.llm.openai_compatible import ChatResult
from oh_my_paper.workflows import full_paper


class Milestone7FullPaperWorkflowTest(unittest.TestCase):
    def test_section_based_demo_layout_replaces_single_paper_output(self) -> None:
        root = Path(__file__).resolve().parents[2] / "demo"
        self.assertTrue((root / "sections/01_sec_abstract.md").exists())
        self.assertTrue((root / "figures/fig_01_workflow_prompt.md").exists())
        self.assertTrue((root / "explain/01_why_abstract.md").exists())
        self.assertTrue((root / "MODEL_SELECTION_PROTOCOL.md").exists())
        self.assertTrue((root / "REVIEW_LOOP_PROTOCOL.md").exists())
        self.assertFalse((root / "paper.md").exists())
        self.assertFalse((root / "figures/figure_prompts.md").exists())

        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in root.glob("**/*")
            if path.is_file() and path.suffix in {".md", ".py"}
        )
        self.assertNotIn("MME", combined)
        self.assertIn("score >= 85", combined)
        self.assertIn("Gemini-compatible", combined)

    def test_section_validator_requires_complete_long_paper(self) -> None:
        paper = "# Descriptive Paper Title\n\n" + "\n\n".join(
            [
                "## Abstract " + "word " * 350,
                "## 1. Introduction " + "word " * 350,
                "## 2. Related Work " + "word " * 350,
                "## 3. Method " + "word " * 350,
                "## 4. Experiments and Results " + "word " * 350,
                "## 5. Limitations " + "word " * 350,
                "## 6. Conclusion " + "word " * 350,
                "## References " + "word " * 350,
            ]
        )
        self.assertTrue(full_paper.validate_paper_sections(paper))
        self.assertFalse(full_paper.validate_paper_sections(paper.replace("# Descriptive Paper Title", "# Title")))
        self.assertFalse(full_paper.validate_paper_sections("## Abstract\nshort"))
        self.assertFalse(full_paper.validate_paper_sections(paper.replace("## 2. Related Work", "## 2. Background")))

    def test_generate_full_paper_writes_core_outputs_with_mock_llm(self) -> None:
        generated = "# Draft\n\n" + "\n\n".join(
            [
                "## Abstract " + "claim-driven draft " * 350,
                "## 1. Introduction " + "consistent context " * 350,
                "## 2. Related Work " + "recent work " * 350,
                "## 3. Method\n- C1: The system uses evidence-keyed orchestration. " + "method detail " * 330,
                "## 4. Experiments and Results " + "evaluation protocol " * 350,
                "## 5. Limitations " + "limitations remain visible " * 350,
                "## 6. Conclusion " + "conclusion " * 350,
                "## References " + "reference entry " * 350,
            ]
        )

        def fake_chat(config, *, model, messages, temperature=0.2, max_tokens=12000, timeout_s=900):
            del config, model, messages, temperature, max_tokens, timeout_s
            return ChatResult(generated, {"choices": []})

        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(full_paper, "extract_pdf_text") as extract:
            root = (Path(tempdir) / "workspace").resolve()
            source = root / ".paper-ai/SOURCE_TEXT.txt"
            extract.side_effect = lambda _pdf, _out: source
            source.parent.mkdir(parents=True)
            source.write_text("source pdf text", encoding="utf-8")
            with mock.patch.object(full_paper, "load_llm_config") as cfg, mock.patch.object(full_paper, "chat_completion", fake_chat):
                cfg.return_value = type("Config", (), {"writer_model": "writer", "reviewer_model": "reviewer"})()
                result = full_paper.generate_full_paper_from_pdf("paper.pdf", root, reviewer=False)
            self.assertTrue(result.trace_ok, result.to_dict())
            self.assertTrue(result.section_ok, result.to_dict())
            self.assertTrue((root / "paper/FULL_PAPER_DRAFT.md").exists())
            self.assertTrue((root / "paper/CLAIMS.md").exists())
            self.assertTrue((root / "paper/EVIDENCE_MAP.md").exists())

    def test_full_paper_writer_uses_multi_round_calls(self) -> None:
        generated = "# Draft\n\n" + "\n\n".join(
            [
                "## Abstract " + "multi round " * 350,
                "## 1. Introduction " + "multi round " * 350,
                "## 2. Related Work " + "multi round " * 350,
                "## 3. Method " + "multi round " * 350,
                "## 4. Experiments and Results " + "multi round " * 350,
                "## 5. Limitations " + "multi round " * 350,
                "## 6. Conclusion " + "multi round " * 350,
                "## References " + "multi round " * 350,
            ]
        )
        calls: list[str] = []

        def fake_chat(config, *, model, messages, temperature=0.2, max_tokens=12000, timeout_s=900):
            del config, model, temperature, max_tokens, timeout_s
            calls.append(messages[0]["content"])
            if "reviewer agent" in messages[0]["content"]:
                return ChatResult('{"score": 87, "verdict": "pass"}', {"choices": []})
            return ChatResult(generated, {"choices": []})

        with mock.patch.object(full_paper, "chat_completion", fake_chat):
            config = type("Config", (), {"writer_model": "writer", "reviewer_model": "reviewer"})()
            paper = full_paper._write_full_paper(config, "source", "context")
        self.assertIn("multi round", paper)
        self.assertGreaterEqual(len(calls), 4)
        self.assertIn("program chair", calls[0])
        self.assertIn("section-contract planner", calls[1])
        self.assertIn("full-paper writing agent", calls[2])
        self.assertIn("reviewer agent", calls[3])

    def test_full_paper_writer_revises_until_reviewer_score_threshold(self) -> None:
        generated = "# Draft\n\n" + "\n\n".join(
            [
                "## Abstract " + "iterative " * 350,
                "## 1. Introduction " + "iterative " * 350,
                "## 2. Related Work " + "iterative " * 350,
                "## 3. Method " + "iterative " * 350,
                "## 4. Experiments and Results " + "iterative " * 350,
                "## 5. Limitations " + "iterative " * 350,
                "## 6. Conclusion " + "iterative " * 350,
                "## References " + "iterative " * 350,
            ]
        )
        scores = iter([72, 81, 87])
        calls: list[str] = []

        def fake_chat(config, *, model, messages, temperature=0.2, max_tokens=12000, timeout_s=900):
            del config, model, temperature, max_tokens, timeout_s
            system = messages[0]["content"]
            calls.append(system)
            if "reviewer agent" in system:
                return ChatResult(f'{{"score": {next(scores)}, "verdict": "revise"}}', {"choices": []})
            return ChatResult(generated, {"choices": []})

        with mock.patch.object(full_paper, "chat_completion", fake_chat):
            config = type("Config", (), {"writer_model": "writer", "reviewer_model": "reviewer"})()
            paper = full_paper._write_full_paper(config, "source", "context")
        self.assertIn("iterative", paper)
        self.assertEqual(sum("reviewer agent" in call for call in calls), 3)
        self.assertGreaterEqual(sum("internal revision agent" in call for call in calls), 2)

    def test_review_loop_revises_after_failed_round(self) -> None:
        initial = "# Draft\n\n" + "\n\n".join([
            "## Abstract " + "initial " * 350,
            "## 1. Introduction " + "initial " * 350,
            "## 2. Related Work " + "initial " * 350,
            "## 3. Method " + "initial " * 350,
            "## 4. Experiments and Results " + "initial " * 350,
            "## 5. Limitations " + "initial " * 350,
            "## 6. Conclusion " + "initial " * 350,
            "## References " + "initial " * 350,
        ])
        revised = "# Draft\n\n" + "\n\n".join([
            "## Abstract " + "revised " * 350,
            "## 1. Introduction " + "revised " * 350,
            "## 2. Related Work " + "revised " * 350,
            "## 3. Method\n- C1: The revised system handles reviewer issues. " + "revised " * 330,
            "## 4. Experiments and Results " + "revised " * 350,
            "## 5. Limitations " + "revised " * 350,
            "## 6. Conclusion " + "revised " * 350,
            "## References " + "revised " * 350,
        ])
        reviews = iter([
            {"verdict": "FAIL", "score": 5, "blocking_issues": ["missing details"]},
            {"verdict": "PASS", "score": 8, "blocking_issues": []},
        ])
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(full_paper, "extract_pdf_text") as extract:
            root = (Path(tempdir) / "workspace").resolve()
            source = root / ".paper-ai/SOURCE_TEXT.txt"
            extract.side_effect = lambda _pdf, _out: source
            source.parent.mkdir(parents=True)
            source.write_text("source pdf text", encoding="utf-8")
            with mock.patch.object(full_paper, "load_llm_config") as cfg, \
                 mock.patch.object(full_paper, "_write_full_paper", return_value=initial), \
                 mock.patch.object(full_paper, "review_full_paper", side_effect=lambda *_a, **_k: next(reviews)), \
                 mock.patch.object(full_paper, "revise_full_paper", return_value=revised):
                cfg.return_value = type("Config", (), {"writer_model": "writer", "reviewer_model": "reviewer"})()
                result = full_paper.generate_full_paper_from_pdf("paper.pdf", root, reviewer=True, max_review_rounds=2)
            self.assertTrue(result.ok, result.to_dict())
            self.assertTrue(result.section_ok, result.to_dict())
            self.assertEqual(result.reviewer_verdict, "PASS")
            self.assertIn("revised", (root / "paper/FULL_PAPER_DRAFT.md").read_text(encoding="utf-8"))


    def test_pass_with_required_revisions_gets_polished_when_rounds_remain(self) -> None:
        initial = "# Draft\n\n" + "\n\n".join([
            "## Abstract " + "initial " * 350,
            "## 1. Introduction " + "initial " * 350,
            "## 2. Related Work " + "initial " * 350,
            "## 3. Method " + "initial " * 350,
            "## 4. Experiments and Results " + "initial " * 350,
            "## 5. Limitations " + "initial " * 350,
            "## 6. Conclusion " + "initial " * 350,
            "## References " + "initial " * 350,
        ])
        polished = initial.replace("initial", "polished")
        reviews = iter([
            {"verdict": "PASS", "score": 9, "blocking_issues": [], "major_issues": ["needs context"], "required_revisions": ["add figure"]},
            {"verdict": "PASS", "score": 9, "blocking_issues": [], "major_issues": [], "required_revisions": []},
        ])
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(full_paper, "extract_pdf_text") as extract:
            root = (Path(tempdir) / "workspace").resolve()
            source = root / ".paper-ai/SOURCE_TEXT.txt"
            extract.side_effect = lambda _pdf, _out: source
            source.parent.mkdir(parents=True)
            source.write_text("source pdf text", encoding="utf-8")
            with mock.patch.object(full_paper, "load_llm_config") as cfg, \
                 mock.patch.object(full_paper, "_write_full_paper", return_value=initial), \
                 mock.patch.object(full_paper, "review_full_paper", side_effect=lambda *_a, **_k: next(reviews)), \
                 mock.patch.object(full_paper, "revise_full_paper", return_value=polished) as revise:
                cfg.return_value = type("Config", (), {"writer_model": "writer", "reviewer_model": "reviewer"})()
                result = full_paper.generate_full_paper_from_pdf("paper.pdf", root, reviewer=True, max_review_rounds=2)
            self.assertTrue(result.ok, result.to_dict())
            revise.assert_called_once()
            self.assertIn("polished", (root / "paper/FULL_PAPER_DRAFT.md").read_text(encoding="utf-8"))

    def test_pass_with_optional_suggestion_does_not_force_extra_round(self) -> None:
        review = {
            "verdict": "PASS",
            "score": 9,
            "blocking_issues": [],
            "major_issues": [],
            "required_revisions": ["None required, but consider adding dependency versions."],
        }
        self.assertFalse(full_paper._review_requests_revision(review))

    def test_sanitizer_softens_forbidden_overclaims(self) -> None:
        text = "robust evidence-key consistency improves accuracy over Standard RAG-based System"
        sanitized = full_paper._sanitize_overclaims(text)
        self.assertIn("known sensitivity limits", sanitized)
        self.assertIn("preserves source-reported accuracy", sanitized)
        self.assertIn("Proposed sliding-window retrieval baseline", sanitized)

    def test_result_not_ok_when_sections_fail_even_if_reviewer_passes(self) -> None:
        result = full_paper.FullPaperResult(
            workspace=Path("/tmp/w"),
            paper_path=Path("/tmp/w/paper.md"),
            review_path=None,
            trace_ok=True,
            section_ok=False,
            reviewer_verdict="PASS",
            reviewer_score=8,
        )
        self.assertFalse(result.ok)

    def test_local_section_gate_repairs_even_when_reviewer_passes(self) -> None:
        short = "# Draft\n\n## Abstract\nshort"
        complete = "# Draft\n\n" + "\n\n".join([
            "## Abstract " + "complete " * 350,
            "## 1. Introduction " + "complete " * 350,
            "## 2. Related Work " + "complete " * 350,
            "## 3. Method " + "complete " * 350,
            "## 4. Experiments and Results " + "complete " * 350,
            "## 5. Limitations " + "complete " * 350,
            "## 6. Conclusion " + "complete " * 350,
            "## References " + "complete " * 350,
        ])
        reviews = iter([
            {"verdict": "PASS", "score": 9, "blocking_issues": [], "major_issues": [], "required_revisions": []},
            {"verdict": "PASS", "score": 9, "blocking_issues": [], "major_issues": [], "required_revisions": []},
        ])
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(full_paper, "extract_pdf_text") as extract:
            root = (Path(tempdir) / "workspace").resolve()
            source = root / ".paper-ai/SOURCE_TEXT.txt"
            extract.side_effect = lambda _pdf, _out: source
            source.parent.mkdir(parents=True)
            source.write_text("source pdf text", encoding="utf-8")
            with mock.patch.object(full_paper, "load_llm_config") as cfg, \
                 mock.patch.object(full_paper, "_write_full_paper", return_value=short), \
                 mock.patch.object(full_paper, "complete_full_paper_text", return_value=complete) as repair, \
                 mock.patch.object(full_paper, "review_full_paper", side_effect=lambda *_a, **_k: next(reviews)):
                cfg.return_value = type("Config", (), {"writer_model": "writer", "reviewer_model": "reviewer"})()
                result = full_paper.generate_full_paper_from_pdf("paper.pdf", root, reviewer=True, max_review_rounds=2)
            self.assertTrue(result.ok, result.to_dict())
            repair.assert_called_once()


if __name__ == "__main__":
    unittest.main()
