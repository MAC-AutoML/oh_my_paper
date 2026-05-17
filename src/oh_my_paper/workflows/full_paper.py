"""Generate and review full paper drafts from local source PDFs."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from oh_my_paper.artifacts.store import ArtifactStore
from oh_my_paper.llm.config import load_llm_config
from oh_my_paper.llm.openai_compatible import chat_completion
from oh_my_paper.review.prompts import STRICT_REVIEWER_PROMPT
from oh_my_paper.traces.events import validate_trace
from oh_my_paper.traces.recorder import TraceRecorder
from oh_my_paper.workflows.full_paper_iterations import write_full_paper_iterative

SECTION_MARKERS = [
    "# ",
    "# <descriptive paper title>",
    "## Abstract",
    "## 1. Introduction",
    "## 2. Related Work",
    "## 3. Method",
    "## 4. Experiments",
    "## 5. Limitations",
    "## 6. Conclusion",
    "## References",
]


@dataclass(frozen=True)
class FullPaperResult:
    workspace: Path
    paper_path: Path
    review_path: Path | None
    trace_ok: bool
    section_ok: bool
    reviewer_verdict: str | None = None
    reviewer_score: int | None = None

    @property
    def ok(self) -> bool:
        return self.trace_ok and self.section_ok and self.reviewer_verdict == "PASS"

    def to_dict(self) -> dict[str, object]:
        return {
            "workspace": str(self.workspace),
            "paper_path": str(self.paper_path),
            "review_path": str(self.review_path) if self.review_path else None,
            "trace_ok": self.trace_ok,
            "section_ok": self.section_ok,
            "reviewer_verdict": self.reviewer_verdict,
            "reviewer_score": self.reviewer_score,
            "ok": self.ok,
        }


def extract_pdf_text(pdf_path: str | Path, output_path: str | Path) -> Path:
    pdf = Path(pdf_path).resolve()
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(["pdftotext", "-layout", str(pdf), str(out)], text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {completed.stderr.strip()}")
    return out


def generate_full_paper_from_pdf(
    pdf_path: str | Path,
    workspace: str | Path,
    *,
    env_file: str | Path = ".env",
    related_context: str = "",
    reviewer: bool = True,
    max_review_rounds: int = 1,
) -> FullPaperResult:
    store = ArtifactStore.from_path(workspace)
    store.paper_dir.mkdir(parents=True, exist_ok=True)
    store.state_dir.mkdir(parents=True, exist_ok=True)
    source_text_path = extract_pdf_text(pdf_path, store.state_dir / "SOURCE_TEXT.txt")
    source_text = source_text_path.read_text(encoding="utf-8", errors="replace")
    config = load_llm_config(env_file)
    recorder = TraceRecorder(store.trace_path, project_id=store.root.name)
    recorder.record(
        phase="material-intake",
        skill="paper-ai-orchestrator",
        action="extract_pdf_text",
        inputs=[str(pdf_path)],
        outputs=[".paper-ai/SOURCE_TEXT.txt"],
        gate_name="pdf_extract",
        gate_status="pass",
        summary="Extracted source PDF text for full-paper generation.",
    )
    paper = _write_full_paper(config, source_text, related_context)
    paper_path = store.paper_dir / "FULL_PAPER_DRAFT.md"
    paper = _ensure_complete_paper(config, paper, source_text, related_context)
    paper_path.write_text(paper, encoding="utf-8")
    _write_claim_artifacts(store, paper)
    recorder.record(
        phase="full-paper-writing",
        skill="paper-ai-writing",
        action="generate_full_paper",
        inputs=[".paper-ai/SOURCE_TEXT.txt"],
        outputs=["paper/FULL_PAPER_DRAFT.md", "paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
        gate_name="section_completeness",
        gate_status="pass" if validate_paper_sections(paper) else "fail",
        human_required=not validate_paper_sections(paper),
        summary="Generated a complete paper draft from source material.",
    )
    review_path: Path | None = None
    verdict: str | None = None
    score: int | None = None
    if reviewer:
        rounds = max(1, max_review_rounds)
        for round_index in range(1, rounds + 1):
            review = review_full_paper(paper_path, env_file=env_file, related_context=related_context)
            review_path = store.paper_dir / f"GEMINI_REVIEW_ROUND_{round_index}.json"
            review_path.write_text(json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")
            verdict = str(review.get("verdict", "FAIL"))
            raw_score = review.get("score")
            score = raw_score if isinstance(raw_score, int) else None
            recorder.record(
                phase="gemini-review",
                skill="paper-ai-reviewer",
                action="strict_review_gate",
                inputs=["paper/FULL_PAPER_DRAFT.md"],
                outputs=[f"paper/GEMINI_REVIEW_ROUND_{round_index}.json"],
                gate_name="gemini_reviewer",
                gate_status="pass" if verdict == "PASS" else "fail",
                human_required=verdict != "PASS",
                summary=f"Gemini reviewer round {round_index} verdict: {verdict}; score: {score}.",
            )
            needs_local_repair = not validate_paper_sections(paper_path.read_text(encoding="utf-8"))
            if verdict == "PASS" and not needs_local_repair and (
                round_index == rounds or not _review_requests_revision(review)
            ):
                break
            if round_index == rounds:
                break
            if needs_local_repair and not _review_requests_revision(review):
                revised = complete_full_paper_text(
                    config,
                    paper_path.read_text(encoding="utf-8"),
                    source_text,
                    related_context,
                )
            else:
                revised = revise_full_paper(paper_path, review_path, env_file=env_file, related_context=related_context)
            revised = _ensure_complete_paper(config, revised, source_text, related_context)
            paper_path.write_text(revised, encoding="utf-8")
            _write_claim_artifacts(store, revised)
            recorder.record(
                phase="full-paper-revision",
                skill="paper-ai-writing",
                action="revise_against_gemini_review",
                inputs=["paper/FULL_PAPER_DRAFT.md", f"paper/GEMINI_REVIEW_ROUND_{round_index}.json"],
                outputs=["paper/FULL_PAPER_DRAFT.md", "paper/CLAIMS.md", "paper/EVIDENCE_MAP.md"],
                gate_name="revision",
                gate_status="pass" if validate_paper_sections(revised) else "fail",
                human_required=not validate_paper_sections(revised),
                summary="Revised full paper draft against strict Gemini review findings.",
            )
    final_paper = paper_path.read_text(encoding="utf-8")
    section_ok = validate_paper_sections(final_paper)
    trace_ok = validate_trace(store.trace_path).ok
    return FullPaperResult(store.root, paper_path, review_path, trace_ok, section_ok, verdict, score)



def _review_requests_revision(review: dict[str, object]) -> bool:
    if review.get("verdict") != "PASS":
        return True
    for key in ("required_revisions", "major_issues"):
        if _actionable_review_items(review.get(key, [])):
            return True
    return False


def _ensure_complete_paper(config, paper: str, source_text: str, related_context: str) -> str:
    current = paper
    for _ in range(2):
        if validate_paper_sections(current):
            break
        current = complete_full_paper_text(config, current, source_text, related_context)
    return current


def _actionable_review_items(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    items = [str(item).strip() for item in value if str(item).strip()]
    return [item for item in items if not _is_optional_or_empty_review_item(item)]


def _is_optional_or_empty_review_item(item: str) -> bool:
    lowered = item.casefold()
    empty_markers = (
        "none",
        "none required",
        "no required",
        "no mandatory",
        "not required",
        "n/a",
    )
    if lowered.strip(" .:-") in empty_markers:
        return True
    optional_markers = ("consider", "optional", "nice to have", "could", "may")
    return any(marker in lowered for marker in optional_markers)


def complete_full_paper_text(config, paper: str, source_text: str, related_context: str) -> str:
    result = chat_completion(
        config,
        model=config.writer_model,
        temperature=0.1,
        max_tokens=18000,
        messages=[
            {"role": "system", "content": _completion_system_prompt()},
            {"role": "user", "content": _completion_user_prompt(paper, source_text, related_context)},
        ],
    )
    return _sanitize_overclaims(_strip_fences(result.content))


def revise_full_paper(
    paper_path: str | Path,
    review_path: str | Path,
    *,
    env_file: str | Path = ".env",
    related_context: str = "",
) -> str:
    config = load_llm_config(env_file)
    paper = Path(paper_path).read_text(encoding="utf-8")
    review = Path(review_path).read_text(encoding="utf-8")
    result = chat_completion(
        config,
        model=config.writer_model,
        temperature=0.15,
        max_tokens=18000,
        messages=[
            {"role": "system", "content": _revision_system_prompt()},
            {"role": "user", "content": _revision_user_prompt(paper, review, related_context)},
        ],
    )
    return _sanitize_overclaims(_strip_fences(result.content))

def review_full_paper(
    paper_path: str | Path,
    *,
    env_file: str | Path = ".env",
    related_context: str = "",
) -> dict[str, object]:
    config = load_llm_config(env_file)
    paper = Path(paper_path).read_text(encoding="utf-8")
    result = chat_completion(
        config,
        model=config.reviewer_model,
        temperature=0,
        max_tokens=5000,
        messages=[
            {"role": "system", "content": STRICT_REVIEWER_PROMPT},
            {"role": "user", "content": _review_user_prompt(paper, related_context)},
        ],
    )
    return _parse_review_json(result.content)


def validate_paper_sections(paper: str) -> bool:
    required_patterns = [
        r"(?im)^#\s+(?!title\s*$).+",
        r"(?im)^#{2,3}\s+abstract\b",
        r"(?im)^##\s+1\.?\s+introduction\b",
        r"(?im)^##\s+2\.?\s+related work\b",
        r"(?im)^##\s+3\.?\s+method\b",
        r"(?im)^##\s+4\.?\s+experiments",
        r"(?im)^##\s+5\.?\s+limitations",
        r"(?im)^##\s+6\.?\s+conclusion\b",
        r"(?im)^##\s+references\b",
    ]
    return all(re.search(pattern, paper) for pattern in required_patterns) and len(paper.split()) >= 2500


def _write_full_paper(config, source_text: str, related_context: str) -> str:
    """Draft a full paper through explicit multi-round planning and revision."""

    paper = write_full_paper_iterative(config, source_text, related_context, chat=chat_completion)
    return _strip_fences(_sanitize_overclaims(paper))



def _completion_system_prompt() -> str:
    return """You are the oh_my_paper completeness repair agent.
Expand and restructure the draft into a complete markdown paper of at least 3000 words.
Use a descriptive top-level markdown title, not the literal text "# Title". Use these exact section headings after the title: ## Abstract, ## 1. Introduction, ## 2. Related Work, ## 3. Method, ## 4. Experiments and Results, ## 5. Limitations, ## 6. Conclusion, ## References.
Preserve conservative claim discipline: do not invent unsupported empirical results, do not claim accuracy gains over base experts, and caveat source-reported or proposed protocol values.
Return only the complete paper markdown.
"""


def _completion_user_prompt(paper: str, source_text: str, related_context: str) -> str:
    return f"""Current incomplete draft:
<<<DRAFT
{paper[:90000]}
DRAFT
>>>

Related/context notes:
{related_context or '(none)'}

Source text excerpt for grounding:
<<<SOURCE
{source_text[:80000]}
SOURCE
>>>"""


def _revision_system_prompt() -> str:
    return """You are the oh_my_paper revision agent.
Revise the full paper so it can pass a hostile top-tier ML reviewer.
You must directly address every blocking and major issue in the JSON review.
Keep the paper as a complete markdown paper of at least 3000 words, not a response letter, and use the exact required headings including ## 2. Related Work.
Add concrete tables, Mermaid diagrams when useful, explicit definitions, ablations, failure modes, and caveated claims where needed.
Do not invent unsupported empirical results; if a table uses source-derived values, say so; if a protocol is proposed, mark it as a protocol.
Remove or soften any claim that is not grounded in the source text or provided context.
Replace vague or strawman baselines with clearly defined source-reported baselines or proposed evaluation protocols without numeric superiority claims.
Return only the revised paper markdown.
"""


def _revision_user_prompt(paper: str, review: str, related_context: str) -> str:
    return f"""Strict reviewer JSON:
<<<REVIEW
{review}
REVIEW
>>>

Recent/context notes:
{related_context or '(none)'}

Current paper draft:
<<<PAPER
{paper[:120000]}
PAPER
>>>"""

def _writer_user_prompt(source_text: str, related_context: str) -> str:
    return f"""Generate a complete paper draft using this extracted PDF as the primary test material.

Additional recent/context notes, if any:
{related_context or '(none provided)'}

Source PDF text:
<<<SOURCE_TEXT
{source_text[:140000]}
SOURCE_TEXT
>>>"""


def _review_user_prompt(paper: str, related_context: str) -> str:
    return f"""Recent/context notes:
{related_context or '(none)'}

Generated paper to review:
<<<PAPER
{paper[:120000]}
PAPER
>>>"""


def _parse_review_json(content: str) -> dict[str, object]:
    cleaned = _strip_fences(content)
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if not match:
        return {"verdict": "FAIL", "score": 0, "blocking_issues": ["Reviewer returned non-JSON output."], "raw": content}
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        return {"verdict": "FAIL", "score": 0, "blocking_issues": [f"Invalid reviewer JSON: {exc}"], "raw": content}
    return parsed if isinstance(parsed, dict) else {"verdict": "FAIL", "score": 0, "blocking_issues": ["Reviewer JSON was not an object."]}


def _sanitize_overclaims(paper: str) -> str:
    replacements = {
        "robust evidence-key consistency": "verifiable exact evidence-key consistency with known sensitivity limits",
        "robust evidence key consistency": "verifiable exact evidence-key consistency with known sensitivity limits",
        "improves accuracy": "preserves source-reported accuracy while improving modularity/efficiency",
        "improved accuracy": "source-reported accuracy with improved modularity/efficiency",
        "outperforms the underlying expert": "does not claim to outperform the underlying expert without an explicit accuracy mechanism",
        "Standard RAG-based System": "Proposed sliding-window retrieval baseline",
    }
    sanitized = paper
    for old, new in replacements.items():
        sanitized = sanitized.replace(old, new)
    return sanitized


def _strip_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def _write_claim_artifacts(store: ArtifactStore, paper: str) -> None:
    claims = _extract_claim_rows(paper)
    store.claims_path.write_text(_claims_table(claims), encoding="utf-8")
    store.evidence_path.write_text(_evidence_table(claims), encoding="utf-8")


def _extract_claim_rows(paper: str) -> list[tuple[str, str]]:
    candidates = re.findall(r"(?im)^[-*]\s+\*?\*?\(?C?\d+\)?[^:：]*[:：]\s*(.+)$", paper)
    if not candidates:
        candidates = re.findall(r"(?im)^[-*]\s+(.{40,180})$", paper)
    rows = []
    for idx, claim in enumerate(candidates[:6], 1):
        clean = re.sub(r"\s+", " ", claim).strip(" -*`")
        if clean:
            rows.append((f"C{idx}", clean[:220]))
    if not rows:
        rows = [("C1", "Generated draft claims are grounded in the provided source PDF material.")]
    return rows


def _claims_table(claims: list[tuple[str, str]]) -> str:
    rows = ["# Claims", "", "| ID | Claim | Status | Evidence | Notes |", "| --- | --- | --- | --- | --- |"]
    for claim_id, claim in claims:
        rows.append(f"| {claim_id} | {claim} | partial | Source PDF text and generated section context | Requires human verification before submission. |")
    return "\n".join(rows) + "\n"


def _evidence_table(claims: list[tuple[str, str]]) -> str:
    rows = ["# Evidence Map", "", "| Claim ID | Evidence artifact | Evidence status | Caveat |", "| --- | --- | --- | --- |"]
    for claim_id, _claim in claims:
        rows.append(f"| {claim_id} | .paper-ai/SOURCE_TEXT.txt | partial | LLM-generated draft; verify against original PDF before real submission. |")
    return "\n".join(rows) + "\n"
