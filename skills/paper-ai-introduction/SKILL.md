---
name: paper-ai-introduction
description: 撰写和修改 AI 论文 Introduction、前两页、研究动机、gap framing、贡献列表和读者导向故事线；适合引言写作和首页审稿印象优化。
---

# paper-ai-introduction

## Use when

Use for introduction, motivation, first-two-pages flow, gap statements, and contribution bullets.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/INTRODUCTION_DRAFT.md`, contribution list, flow audit

## Workflow

1. Start from reader problem and concrete bottleneck.
2. Explain prior work enough to reveal the gap.
3. Introduce the method idea and evidence preview.
4. Write claim-linked contribution bullets.

## Gate

Each contribution must be specific and evidence-linked or caveated.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/introduction-guide.md`
