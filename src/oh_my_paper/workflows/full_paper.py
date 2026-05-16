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

SECTION_MARKERS = [
    "# ",
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
    reviewer_verdict: str | None = None
    reviewer_score: int | None = None

    @property
    def ok(self) -> bool:
        return self.trace_ok and self.reviewer_verdict == "PASS"

    def to_dict(self) -> dict[str, object]:
        return {
            "workspace": str(self.workspace),
            "paper_path": str(self.paper_path),
            "review_path": str(self.review_path) if self.review_path else None,
            "trace_ok": self.trace_ok,
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
        review = review_full_paper(paper_path, env_file=env_file, related_context=related_context)
        review_path = store.paper_dir / "GEMINI_REVIEW.json"
        review_path.write_text(json.dumps(review, indent=2, ensure_ascii=False), encoding="utf-8")
        verdict = str(review.get("verdict", "FAIL"))
        raw_score = review.get("score")
        score = raw_score if isinstance(raw_score, int) else None
        recorder.record(
            phase="gemini-review",
            skill="paper-ai-reviewer",
            action="strict_review_gate",
            inputs=["paper/FULL_PAPER_DRAFT.md"],
            outputs=["paper/GEMINI_REVIEW.json"],
            gate_name="gemini_reviewer",
            gate_status="pass" if verdict == "PASS" else "fail",
            human_required=verdict != "PASS",
            summary=f"Gemini reviewer verdict: {verdict}; score: {score}.",
        )
    trace_ok = validate_trace(store.trace_path).ok
    return FullPaperResult(store.root, paper_path, review_path, trace_ok, verdict, score)


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
    normalized = paper.lower()
    required = ["abstract", "introduction", "related work", "method", "experiment", "limitation", "conclusion", "references"]
    return all(term in normalized for term in required) and len(paper.split()) >= 2500


def _write_full_paper(config, source_text: str, related_context: str) -> str:
    result = chat_completion(
        config,
        model=config.writer_model,
        temperature=0.25,
        max_tokens=16000,
        messages=[
            {"role": "system", "content": _writer_system_prompt()},
            {"role": "user", "content": _writer_user_prompt(source_text, related_context)},
        ],
    )
    return _strip_fences(result.content)


def _writer_system_prompt() -> str:
    return """You are the oh_my_paper full-paper writing agent.
Write a coherent complete ML paper draft in markdown from provided source material.
Use the source as test input, but do not merely copy it; reorganize it into a cleaner paper with consistent terminology.
Preserve factual numbers only when supported by the source. If a claim is not directly supported, mark it as proposed or future work.
Required markdown sections: title, Abstract, 1. Introduction, 2. Related Work, 3. Method, 4. Experiments and Results, 5. Limitations, 6. Conclusion, References.
Also include concise Figure/Table plans inline where relevant.
"""


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
