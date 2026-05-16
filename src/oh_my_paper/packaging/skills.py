"""Install, list, and uninstall local Codex skills."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

SKILL_PREFIX = "paper-ai-"


@dataclass(frozen=True)
class SkillInstallResult:
    target_dir: Path
    installed: list[str]
    skipped: list[str]
    removed: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "target_dir": str(self.target_dir),
            "installed": self.installed,
            "skipped": self.skipped,
            "removed": self.removed,
        }


def default_skills_dir(home: Path | None = None) -> Path:
    root = home or Path.home()
    return root / ".codex" / "skills"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def source_skills_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "skills"


def discover_source_skills(root: Path | None = None) -> list[Path]:
    base = source_skills_dir(root)
    return sorted(path for path in base.glob(f"{SKILL_PREFIX}*") if (path / "SKILL.md").exists())


def list_installed_skills(target_dir: str | Path | None = None) -> list[str]:
    target = Path(target_dir) if target_dir is not None else default_skills_dir()
    if not target.exists():
        return []
    return sorted(path.name for path in target.glob(f"{SKILL_PREFIX}*") if (path / "SKILL.md").exists())


def install_skills(target_dir: str | Path | None = None, *, overwrite: bool = False, root: Path | None = None) -> SkillInstallResult:
    target = Path(target_dir) if target_dir is not None else default_skills_dir()
    target.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    skipped: list[str] = []
    for skill in discover_source_skills(root):
        destination = target / skill.name
        if destination.exists():
            if not overwrite:
                skipped.append(skill.name)
                continue
            shutil.rmtree(destination)
        shutil.copytree(skill, destination, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
        installed.append(skill.name)
    return SkillInstallResult(target, installed, skipped, [])


def uninstall_skills(target_dir: str | Path | None = None) -> SkillInstallResult:
    target = Path(target_dir) if target_dir is not None else default_skills_dir()
    removed: list[str] = []
    if target.exists():
        for path in sorted(target.glob(f"{SKILL_PREFIX}*")):
            if path.is_dir():
                shutil.rmtree(path)
                removed.append(path.name)
    return SkillInstallResult(target, [], [], removed)
