---
name: paper-ai-idea
description: 将 AI 研究想法打磨成可投稿论文方向，包含问题定位、贡献假设、证据计划和新颖性风险；适合头脑风暴、选题、细化模糊想法或判断结果是否能写成论文。
---

# paper-ai-idea

## Use when

Use before drafting when the user needs topic selection, idea critique, research-question framing, or contribution hypotheses.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/IDEA_BRIEF.md`, research question, contribution hypothesis, evidence-needed list

## Workflow

1. Clarify audience, problem, gap, hypothesis, and evidence path.
2. Stress-test importance, novelty, feasibility, and falsifiability.
3. Convert vague directions into candidate paper claims.
4. List minimum publishable evidence and risks.

## Gate

Do not hand off to writing until the idea has audience, gap, and evidence path.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or curated case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/idea-playbook.md`
