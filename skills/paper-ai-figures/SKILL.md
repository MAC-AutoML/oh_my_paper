---
name: paper-ai-figures
description: 设计和审查 AI 论文图、结果图、方法示意图、表格、caption 和首页视觉，使每个视觉服务一个 takeaway 和 claim；适合画图规划、表格规划、视觉层级和 caption。
---

# paper-ai-figures

## Use when

Use for paper figures, architecture diagrams, result plots, tables, captions, visual readability, and first-page visual checks.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/FIGURE_PLAN.md`, `paper/TABLE_PLAN.md`, captions, visual audit

## Workflow

1. Identify the claim each visual supports.
2. Choose figure/table type based on the takeaway.
3. Design labels, hierarchy, caption, and caveats.
4. Check first-page visual impact and readability.

## Gate

Every visual must have one takeaway and a claim/evidence link.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or curated case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/figures-tables-guide.md`
