"""Compile an oh my paper LaTeX workspace when TeX tools are available."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from shutil import which


@dataclass(frozen=True)
class LatexCompileResult:
    workspace: str
    ok: bool
    pdf: str | None
    tool: str | None
    commands: list[list[str]] = field(default_factory=list)
    log: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "workspace": self.workspace,
            "ok": self.ok,
            "pdf": self.pdf,
            "tool": self.tool,
            "commands": self.commands,
            "log": self.log[-4000:],
            "error": self.error,
        }


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def compile_latex_workspace(workspace: str | Path) -> LatexCompileResult:
    root = Path(workspace).expanduser().resolve()
    main = root / "main.tex"
    if not main.exists():
        return LatexCompileResult(str(root), False, None, None, error="main.tex not found")

    log_parts: list[str] = []
    commands: list[list[str]] = []
    if which("latexmk"):
        commands = [
            ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        ]
        result = _run(commands[0], root)
        log_parts.append(result.stdout)
        ok = result.returncode == 0 and (root / "main.pdf").exists()
        return LatexCompileResult(
            str(root),
            ok,
            str(root / "main.pdf") if ok else None,
            "latexmk",
            commands,
            "\n".join(log_parts),
            None if ok else "latexmk failed",
        )

    if not which("xelatex"):
        return LatexCompileResult(
            str(root),
            False,
            None,
            None,
            error="No LaTeX compiler found. Install TeX Live/MacTeX with latexmk or xelatex.",
        )

    commands = [
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ["bibtex", "main"],
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ]
    for command in commands:
        if command[0] == "bibtex" and not which("bibtex"):
            log_parts.append("bibtex not found; skipping bibliography pass")
            continue
        result = _run(command, root)
        log_parts.append(result.stdout)
        if result.returncode != 0 and command[0] != "bibtex":
            return LatexCompileResult(
                str(root),
                False,
                None,
                "xelatex",
                commands,
                "\n".join(log_parts),
                f"{command[0]} failed",
            )
    ok = (root / "main.pdf").exists()
    return LatexCompileResult(
        str(root),
        ok,
        str(root / "main.pdf") if ok else None,
        "xelatex",
        commands,
        "\n".join(log_parts),
        None if ok else "PDF not produced",
    )
