from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from oh_my_paper.materials import intake


class MaterialIntakeTest(unittest.TestCase):
    def test_classify_text_routes_review_title_rebuttal_material(self) -> None:
        text = (
            "reviewer and area chair discuss review scores. "
            "标题 abstract 前两页 figure 图 shape first impression. "
            "rebuttal reply should avoid overclaim and focus on evidence. "
            "研究 问题 方法 实验 need a workflow eval loop."
        )
        categories = intake.classify_text(text)
        self.assertIn("review-rating", categories)
        self.assertIn("writing", categories)
        self.assertIn("figures", categories)
        self.assertIn("rebuttal", categories)
        self.assertIn("research-process", categories)
        self.assertIn("workflow-infra", categories)

    def test_build_summary_is_local_only_and_public_safe(self) -> None:
        summary = intake.build_summary(
            "meeting-review-title",
            "private.pdf",
            ["writing", "rebuttal"],
            "abc123",
            "rebuttal abstract 标题 OpenReview 期刊 overclaim 图",
        )
        self.assertIn("Privacy: local/internal", summary)
        self.assertIn("do not publish raw text", summary)
        self.assertIn("Categories: writing, rebuttal", summary)
        self.assertIn("rebuttal 应被视为有限纠偏机会", summary)
        self.assertIn("标题、摘要、前两页", summary)
        self.assertNotIn("private transcript", summary)

    def test_intake_pdf_writes_ignored_cache_shape_without_real_pdftotext(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            source = root / "source.pdf"
            source.write_bytes(b"%PDF synthetic")
            materials_root = root / "materials" / "paper-ai"

            def fake_pdftotext(_pdf: Path, output: Path) -> None:
                output.write_text("reviewer rebuttal 标题 figure 研究", encoding="utf-8")

            with patch.object(intake, "_pdftotext", side_effect=fake_pdftotext):
                result = intake.intake_pdf(source, "synthetic-review-title", materials_root)

            self.assertEqual(result.material_id, "synthetic-review-title")
            self.assertTrue(result.text_path.exists())
            self.assertTrue(result.summary_path.exists())
            self.assertTrue(result.index_path.exists())
            self.assertIn("review-rating", result.categories)
            self.assertIn("rebuttal", result.categories)

            index_entry = json.loads(result.index_path.read_text(encoding="utf-8").strip())
            self.assertEqual(index_entry["id"], "synthetic-review-title")
            self.assertEqual(index_entry["source_file"], "source.pdf")
            self.assertEqual(index_entry["sha256"], result.sha256)

    def test_material_id_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            source = Path(tempdir) / "source.pdf"
            source.write_bytes(b"%PDF synthetic")
            with self.assertRaises(ValueError):
                intake.intake_pdf(source, "../escape", Path(tempdir) / "materials")


if __name__ == "__main__":
    unittest.main()
