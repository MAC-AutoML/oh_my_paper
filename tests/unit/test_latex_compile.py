from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from oh_my_paper.latex.compile import compile_latex_workspace


class LatexCompileHelpersTest(unittest.TestCase):
    def test_missing_main_tex_reports_clear_error(self) -> None:
        with TemporaryDirectory() as tmp:
            result = compile_latex_workspace(Path(tmp))
        self.assertFalse(result.ok)
        self.assertEqual(result.error, "main.tex not found")
        self.assertIsNone(result.pdf)


if __name__ == "__main__":
    unittest.main()
