"""Deterministic oh my paper demo generator.

Run with:
    uv run python demo/run_demo.py

The script creates a section-by-section demo layout. Live model selection and
review loops are documented as prompts/protocols, while this committed demo uses
stable offline outputs for reproducibility.
"""

from __future__ import annotations

from pathlib import Path

from demo_templates import build_outputs, manifest

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input_material.md"


def _clean_old_outputs() -> None:
    keep = {
        "README.md",
        "HOW_TO_REPRODUCE.md",
        "IMAGEGEN_USAGE.md",
        "input_material.md",
        "run_demo.py",
        "demo_templates.py",
    }
    for path in ROOT.iterdir():
        if path.name in keep:
            continue
        if path.is_file() and path.suffix in {".md", ".yaml", ".json"}:
            path.unlink()
    for path in (ROOT / "sections").glob("*.md") if (ROOT / "sections").exists() else []:
        path.unlink()
    for path in (ROOT / "figures").glob("*") if (ROOT / "figures").exists() else []:
        if path.is_file():
            path.unlink()


def main() -> int:
    material = INPUT.read_text(encoding="utf-8")
    _clean_old_outputs()
    outputs = build_outputs(ROOT, material)
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    (ROOT / "MANIFEST.md").write_text(manifest(outputs, ROOT), encoding="utf-8")
    print(f"Generated section-based demo outputs under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
