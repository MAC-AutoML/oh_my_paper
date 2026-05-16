"""Local-only material intake and fusion helpers."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

CATEGORY_KEYWORDS = {
    "review-rating": ["审稿", "review", "reviewer", "评分", "分数", "meta review", "ac", "area chair"],
    "writing": ["abstract", "introduction", "写", "故事", "动机", "motivation", "前两页", "标题"],
    "figures": ["figure", "fig", "图", "caption", "可视化", "画图"],
    "paper-checking": ["漏洞", "细节", "印象分", "检查", "checklist", "consistency"],
    "rebuttal": ["rebuttal", "reply", "反馈", "改分", "反驳", "response"],
    "research-process": ["研究", "问题", "科学问题", "工程问题", "方法", "实验"],
    "workflow-infra": ["skill", "harness", "eval", "trace", "adapter", "workflow", "持续迭代"],
}

MATERIAL_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


@dataclass(frozen=True)
class MaterialIntakeResult:
    source: Path
    material_id: str
    text_path: Path
    summary_path: Path
    index_path: Path
    categories: list[str]
    sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "source": str(self.source),
            "material_id": self.material_id,
            "text_path": str(self.text_path),
            "summary_path": str(self.summary_path),
            "index_path": str(self.index_path),
            "categories": self.categories,
            "sha256": self.sha256,
        }


def intake_pdf(
    pdf_path: str | Path,
    material_id: str,
    materials_root: str | Path = "materials/paper-ai",
) -> MaterialIntakeResult:
    """Copy, extract, classify, and locally summarize one PDF material."""
    _validate_material_id(material_id)
    source = Path(pdf_path).resolve()
    if not source.exists():
        raise FileNotFoundError(source)

    root = Path(materials_root)
    target = root / "external" / material_id
    raw = target / "raw"
    raw.mkdir(parents=True, exist_ok=True)

    pdf_copy = raw / source.name
    if source != pdf_copy.resolve():
        shutil.copy2(source, pdf_copy)

    text_path = raw / "text.txt"
    _pdftotext(pdf_copy, text_path)
    text = text_path.read_text(encoding="utf-8", errors="ignore")
    categories = classify_text(text)
    digest = _sha256(pdf_copy)

    summary_path = target / "index.md"
    summary_path.write_text(
        build_summary(material_id, source.name, categories, digest, text),
        encoding="utf-8",
    )

    index_path = root / "intake-index.jsonl"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("a", encoding="utf-8") as handle:
        payload = {
            "id": material_id,
            "source_file": source.name,
            "categories": categories,
            "sha256": digest,
        }
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    return MaterialIntakeResult(source, material_id, text_path, summary_path, index_path, categories, digest)


def classify_text(text: str) -> list[str]:
    lowered = text.lower()
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(lowered.count(keyword.lower()) for keyword in keywords)
    ranked = [
        category
        for category, score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        if score > 0
    ]
    return ranked or ["workflow-infra"]


def build_summary(
    material_id: str,
    source_name: str,
    categories: list[str],
    digest: str,
    text: str,
) -> str:
    bullets = infer_public_safe_bullets(text)
    bullet_text = "\n".join(f"- {item}" for item in bullets)
    return f"""# {material_id}

Source file: `{source_name}`

Privacy: local/internal; do not publish raw text.

SHA256: `{digest}`

Categories: {", ".join(categories)}

## Public-safe synthesis

{bullet_text}

## Skill impact candidates

- `paper-ai-reviewer`: model reviewer time pressure and first-impression checks.
- `paper-ai-writing`: strengthen title/abstract/introduction gates.
- `paper-ai-rebuttal`: remind users rebuttal rarely fixes a weak first impression.
- `paper-ai-figures`: include first-page figure readability in reviewer simulation.
"""


def infer_public_safe_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    lowered = text.lower()
    if "rebuttal" in lowered:
        bullets.append("会议 rebuttal 应被视为有限纠偏机会，而不是主要翻盘手段；提交前质量更关键。")
    if "abstract" in lowered or "题" in text:
        bullets.append("标题、摘要、前两页和核心图会强烈影响审稿人的初始印象。")
    if "open review" in lowered or "openreview" in lowered:
        bullets.append("CMT/OpenReview/期刊流程差异会影响可见性、讨论方式和修回节奏。")
    if "期刊" in text:
        bullets.append("会议通常节奏快且 rebuttal 机会少；期刊可能多轮但周期长。")
    if "overclaim" in lowered or "夸" in text:
        bullets.append("标题应清晰可检索并避免过度宣称；质量不够时花哨标题会放大风险。")
    if "图" in text or "figure" in lowered:
        bullets.append("首屏图表质量会影响 reviewer 兴趣和信任，应进入 pre-review checklist。")
    return bullets or ["该材料已入库，需人工补充 public-safe synthesis。"]


def _validate_material_id(material_id: str) -> None:
    if not MATERIAL_ID_PATTERN.fullmatch(material_id):
        raise ValueError(
            "material_id must be 1-128 chars of letters, numbers, dots, underscores, or hyphens"
        )


def _pdftotext(pdf: Path, output: Path) -> None:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(output)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pdftotext failed")


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
