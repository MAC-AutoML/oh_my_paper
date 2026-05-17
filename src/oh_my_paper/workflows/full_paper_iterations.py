"""Multi-round drafting prompts for full paper generation."""

from __future__ import annotations

from typing import Protocol

from oh_my_paper.llm.config import LLMConfig
from oh_my_paper.llm.openai_compatible import ChatResult, chat_completion


class ChatFn(Protocol):
    def __call__(
        self,
        config: LLMConfig,
        *,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 12000,
        timeout_s: int = 900,
    ) -> ChatResult: ...


def write_full_paper_iterative(
    config,
    source_text: str,
    related_context: str,
    *,
    chat: ChatFn = chat_completion,
) -> str:
    """Write a complete paper using plan, draft, critique, and revision calls."""

    selection = select_paper_direction(config, source_text, related_context, chat=chat)
    plan = draft_section_plan(config, source_text, related_context, selection=selection, chat=chat)
    paper = draft_from_plan(config, plan, source_text, related_context, chat=chat)
    for _round_index in range(3):
        review = score_draft(config, paper, plan, source_text, related_context, chat=chat)
        if _review_score(review) >= 85:
            return paper
        critique = critique_draft(config, paper, plan, source_text, related_context, review=review, chat=chat)
        paper = revise_from_internal_critique(config, paper, critique, plan, source_text, related_context, chat=chat)
    return paper


def select_paper_direction(config, source_text: str, related_context: str, *, chat: ChatFn = chat_completion) -> str:
    result = chat(
        config,
        model=config.reviewer_model,
        temperature=0.1,
        max_tokens=5000,
        messages=[
            {"role": "system", "content": _selection_system_prompt()},
            {"role": "user", "content": _source_user_prompt(source_text, related_context)},
        ],
    )
    return _strip_fences(result.content)


def draft_section_plan(
    config,
    source_text: str,
    related_context: str,
    *,
    selection: str = "",
    chat: ChatFn = chat_completion,
) -> str:
    result = chat(
        config,
        model=config.writer_model,
        temperature=0.15,
        max_tokens=6000,
        messages=[
            {"role": "system", "content": _section_plan_system_prompt()},
            {"role": "user", "content": _planning_user_prompt(source_text, related_context, selection)},
        ],
    )
    return _strip_fences(result.content)


def draft_from_plan(
    config,
    plan: str,
    source_text: str,
    related_context: str,
    *,
    chat: ChatFn = chat_completion,
) -> str:
    result = chat(
        config,
        model=config.writer_model,
        temperature=0.25,
        max_tokens=18000,
        messages=[
            {"role": "system", "content": _writer_system_prompt()},
            {"role": "user", "content": _draft_user_prompt(plan, source_text, related_context)},
        ],
    )
    return _strip_fences(result.content)


def score_draft(
    config,
    draft: str,
    plan: str,
    source_text: str,
    related_context: str,
    *,
    chat: ChatFn = chat_completion,
) -> str:
    result = chat(
        config,
        model=config.reviewer_model,
        temperature=0,
        max_tokens=5000,
        messages=[
            {"role": "system", "content": _score_system_prompt()},
            {"role": "user", "content": _review_round_user_prompt(draft, plan, source_text, related_context)},
        ],
    )
    return _strip_fences(result.content)


def critique_draft(
    config,
    draft: str,
    plan: str,
    source_text: str,
    related_context: str,
    *,
    review: str = "",
    chat: ChatFn = chat_completion,
) -> str:
    result = chat(
        config,
        model=config.writer_model,
        temperature=0.1,
        max_tokens=7000,
        messages=[
            {"role": "system", "content": _internal_critique_system_prompt()},
            {"role": "user", "content": _internal_critique_user_prompt(draft, plan, source_text, related_context, review)},
        ],
    )
    return _strip_fences(result.content)


def revise_from_internal_critique(
    config,
    draft: str,
    critique: str,
    plan: str,
    source_text: str,
    related_context: str,
    *,
    chat: ChatFn = chat_completion,
) -> str:
    result = chat(
        config,
        model=config.writer_model,
        temperature=0.15,
        max_tokens=18000,
        messages=[
            {"role": "system", "content": _internal_revision_system_prompt()},
            {"role": "user", "content": _internal_revision_user_prompt(draft, critique, plan, source_text, related_context)},
        ],
    )
    return _strip_fences(result.content)


def _review_score(review: str) -> int:
    import json
    import re

    match = re.search(r"\{.*\}", review, flags=re.DOTALL)
    if match:
        try:
            value = json.loads(match.group(0)).get("score", 0)
            return int(value) if isinstance(value, int | float | str) and str(value).isdigit() else 0
        except Exception:
            pass
    match = re.search(r"score[^0-9]{0,12}([0-9]{1,3})", review, flags=re.IGNORECASE)
    return int(match.group(1)) if match else 0


def _selection_system_prompt() -> str:
    return """You are a strict academic program chair.
From the user's material, propose and score 3-5 original paper directions before any drafting.
Do not reuse a fixed project name from examples. Select the best direction by novelty, feasibility, evidence fit, and risk.
Return concise JSON or markdown with selected_candidate, score, rationale, risks, and required caveats.
"""


def _section_plan_system_prompt() -> str:
    return """You are the oh_my_paper section-contract planner.
Do not draft prose yet. Create a complete writing contract for a long ML paper.
For each required section, specify: reader question, section claim, paragraph plan, claim IDs, evidence status, caveats, and figure/table needs.
Required sections: Abstract; 1. Introduction; 2. Related Work; 3. Method; 4. Experiments and Results; 5. Limitations; 6. Conclusion; References.
Every claim must be labeled supported, partial, proposed, or unsupported. Unsupported claims must be removed or converted to future work in the later draft.
"""


def _writer_system_prompt() -> str:
    return """You are the oh_my_paper full-paper writing agent.
Write from the supplied section contract, not as a one-shot stream. For every section, follow this loop internally: section contract -> paragraph plan -> draft -> self-check -> revised section.
Write a coherent complete ML paper draft in markdown from provided source material.
Use the source as test input, but do not merely copy it; reorganize it into a cleaner paper with consistent terminology.
Preserve factual numbers only when supported by the source. If a claim is not directly supported, mark it as proposed or future work.
Use a descriptive top-level markdown title, not the literal text "# Title". Required exact section headings after the title: ## Abstract, ## 1. Introduction, ## 2. Related Work, ## 3. Method, ## 4. Experiments and Results, ## 5. Limitations, ## 6. Conclusion, ## References. The draft must be at least 3000 words.
Do not use placeholder figures. Include concrete Markdown tables and Mermaid diagrams/plots when the output is markdown, and describe which figure should later be generated with an image-generation skill.
Treat this as a source-derived design/reproduction draft: be conservative, and only report mechanisms, baselines, datasets, or numbers that are present in the source or explicitly labeled as proposed follow-up evaluation.
When reporting source benchmark numbers, state they are source-reported and should be independently reproduced.
Define every baseline concretely. If a baseline is illustrative rather than source-reported, mark it as a proposed protocol and avoid numeric superiority claims.
Include reliability checks, ablations, failure modes, and validity threats that are appropriate to the source paper's domain.
If the source paper is a reinforcement-learning paper, include objective definitions, optimization details, ablations, and evaluation protocol caveats grounded in the source.
"""


def _score_system_prompt() -> str:
    return """You are the oh_my_paper reviewer agent.
Score the draft from 0 to 100. Be strict: below 85 means another revision is required.
Evaluate problem framing, originality from user material, evidence discipline, method clarity, experiment credibility, figure readiness, limitations, and overall paper flow.
Return JSON with score, verdict, blocking_issues, required_revisions, and satisfied_items.
"""


def _internal_critique_system_prompt() -> str:
    return """You are the oh_my_paper internal writing critic.
Audit the draft before external review. Return a concise but strict markdown report, not revised prose.
Check: section completeness, paragraph function, claim/evidence alignment, unsupported numbers, missing caveats, figure/table needs, and whether each section answers its reader question.
For every required section, list one must-fix item or say CLEAR.
"""


def _internal_revision_system_prompt() -> str:
    return """You are the oh_my_paper internal revision agent.
Revise the complete markdown paper using the section contract and internal critique.
Keep all required headings and at least 3000 words.
Fix unsupported claims by grounding, caveating, converting to proposed work, or deleting.
Preserve a reader-centered top-tier paper flow: problem -> gap -> design -> evidence -> insight -> impact.
Return only the revised complete paper markdown.
"""


def _planning_user_prompt(source_text: str, related_context: str, selection: str) -> str:
    return f"""Reviewer-selected paper direction:
<<<SELECTION
{selection[:30000] or '(not provided)'}
SELECTION
>>>

{_source_user_prompt(source_text, related_context)}"""


def _source_user_prompt(source_text: str, related_context: str) -> str:
    return f"""Additional recent/context notes, if any:
{related_context or '(none provided)'}

Source PDF text:
<<<SOURCE_TEXT
{source_text[:140000]}
SOURCE_TEXT
>>>"""


def _draft_user_prompt(plan: str, source_text: str, related_context: str) -> str:
    return f"""Section contract to follow:
<<<SECTION_CONTRACT
{plan[:50000]}
SECTION_CONTRACT
>>>

Generate the full paper draft using the extracted PDF as the primary test material.

{_source_user_prompt(source_text[:120000], related_context)}"""


def _review_round_user_prompt(draft: str, plan: str, source_text: str, related_context: str) -> str:
    return f"""Section contract:
<<<SECTION_CONTRACT
{plan[:30000]}
SECTION_CONTRACT
>>>

{_source_user_prompt(source_text[:30000], related_context)}

Draft to score:
<<<DRAFT
{draft[:100000]}
DRAFT
>>>"""


def _internal_critique_user_prompt(
    draft: str,
    plan: str,
    source_text: str,
    related_context: str,
    review: str = "",
) -> str:
    return f"""Reviewer score packet:
<<<REVIEW
{review[:30000] or '(not provided)'}
REVIEW
>>>

Section contract:
<<<SECTION_CONTRACT
{plan[:40000]}
SECTION_CONTRACT
>>>

{_source_user_prompt(source_text[:50000], related_context)}

Draft to audit:
<<<DRAFT
{draft[:100000]}
DRAFT
>>>"""


def _internal_revision_user_prompt(
    draft: str,
    critique: str,
    plan: str,
    source_text: str,
    related_context: str,
) -> str:
    return f"""Internal critique to address:
<<<CRITIQUE
{critique[:30000]}
CRITIQUE
>>>

Section contract:
<<<SECTION_CONTRACT
{plan[:40000]}
SECTION_CONTRACT
>>>

{_source_user_prompt(source_text[:50000], related_context)}

Draft to revise:
<<<DRAFT
{draft[:110000]}
DRAFT
>>>"""


def _strip_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        import re

        stripped = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()
