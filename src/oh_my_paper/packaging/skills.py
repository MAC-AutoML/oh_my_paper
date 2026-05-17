"""Codex official skill-installer compatibility helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

HELPER_SKILL_PREFIX = "paper-ai-"
TOP_LEVEL_SKILLS = ("deep-research", "academic-paper", "academic-paper-reviewer", "academic-pipeline")
REPO = "MAC-AutoML/oh_my_paper"
OFFICIAL_INSTALLER = "install-skill-from-github.py"


@dataclass(frozen=True)
class SkillPackageInfo:
    name: str
    path: str
    has_skill_md: bool
    has_agents_metadata: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "path": self.path,
            "has_skill_md": self.has_skill_md,
            "has_agents_metadata": self.has_agents_metadata,
        }


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def source_skills_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "skills"


def discover_source_skills(root: Path | None = None) -> list[Path]:
    base = source_skills_dir(root)
    helpers = [path for path in base.glob(f"{HELPER_SKILL_PREFIX}*") if path.is_dir()]
    top_level = [base / name for name in TOP_LEVEL_SKILLS if (base / name).is_dir()]
    return sorted([*top_level, *helpers], key=lambda path: path.name)


def skill_package_info(root: Path | None = None) -> list[SkillPackageInfo]:
    repo = root or repo_root()
    infos: list[SkillPackageInfo] = []
    for path in discover_source_skills(repo):
        relative = path.relative_to(repo).as_posix()
        infos.append(
            SkillPackageInfo(
                name=path.name,
                path=relative,
                has_skill_md=(path / "SKILL.md").exists(),
                has_agents_metadata=(path / "agents" / "openai.yaml").exists(),
            )
        )
    return infos


def official_install_command(*, repo: str = REPO, root: Path | None = None, ref: str | None = None) -> list[str]:
    """Return the official skill-installer helper command for this repo.

    The actual installer lives in Codex's system `skill-installer` skill. This
    project only emits the command/paths expected by that installer; it does not
    implement a competing installer.
    """

    command = [OFFICIAL_INSTALLER, "--repo", repo]
    if ref:
        command.extend(["--ref", ref])
    for info in skill_package_info(root):
        command.extend(["--path", info.path])
    return command


def packaging_status(root: Path | None = None) -> dict[str, object]:
    infos = skill_package_info(root)
    return {
        "repo": REPO,
        "installer": "Codex system skill-installer",
        "official_command": official_install_command(root=root),
        "skills": [info.to_dict() for info in infos],
        "ok": bool(infos) and all(info.has_skill_md for info in infos),
    }
