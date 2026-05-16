from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from oh_my_paper.llm.openai_compatible import ChatResult
from oh_my_paper.workflows import full_paper


class Milestone7FullPaperWorkflowTest(unittest.TestCase):
    def test_section_validator_requires_complete_long_paper(self) -> None:
        paper = "# Title\n\n" + "\n\n".join(
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
        self.assertFalse(full_paper.validate_paper_sections("## Abstract\nshort"))

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
            self.assertTrue((root / "paper/FULL_PAPER_DRAFT.md").exists())
            self.assertTrue((root / "paper/CLAIMS.md").exists())
            self.assertTrue((root / "paper/EVIDENCE_MAP.md").exists())


if __name__ == "__main__":
    unittest.main()
