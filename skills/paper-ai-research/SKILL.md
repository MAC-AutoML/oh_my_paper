---
name: paper-ai-research
description: 面向 AI 论文写作前置研究的 Codex skill，帮助澄清研究问题、制定文献检索策略、评估来源质量、综合证据并交接给写作/实验/related work；适合从模糊想法进入可写论文证据链。
---

# paper-ai-research

## Use when

Use before drafting when the user needs research-question scoping, literature search planning, source-quality screening, evidence synthesis, or a research handoff into the paper workflow.

## Do not use when

- The task is only generic chat and no paper artifact or research decision is involved.
- The user asks to fabricate citations, sources, experiments, reviewer opinions, or results.
- The user already has stable evidence and asks for a specific paper section; route to the narrower section skill.

## Inputs

- User's topic, vague idea, research question, target venue/field, or paper workspace.
- Existing notes, PDFs, citations, experiments, figures, reviews, or source lists.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/RESEARCH_BRIEF.md`, source-quality matrix, literature search plan, synthesis notes, paper handoff checklist

## Workflow

1. Scope the question: clarify audience, concepts, boundaries, answerability, and minimum publishable evidence.
2. Plan the search: define databases, keywords, inclusion/exclusion criteria, and freshness expectations.
3. Grade sources: separate primary evidence, systematic reviews, benchmarks, official docs, grey literature, and weak/unusable sources.
4. Synthesize evidence: map agreement, contradiction, gaps, and implications to claim IDs.
5. Handoff to paper skills: route to idea, related work, method, experiments, figures, or writing with explicit missing evidence.

## Gate

No claim may enter writing as supported unless it has traceable evidence, a source-quality judgment, and a stated scope condition.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across research, writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or curated case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/research-workflow-guide.md`
- `references/source-quality-guide.md`
- `references/socratic-scoping-guide.md`
