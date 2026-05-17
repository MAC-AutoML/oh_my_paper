---
name: paper-ai-rebuttal
description: 基于审稿意见撰写和审查 AI 会议/期刊 rebuttal，包含 concern table、证据映射、AC-aware 优先级、语气控制和承诺边界；适合收到 reviews 后规划、写作、压缩或批判 author response。
---

# paper-ai-rebuttal

## Use when

Use after reviews arrive or when drafting, organizing, compressing, or auditing a rebuttal/author response.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/REBUTTAL_PLAN.md`, concern table, response draft, promised revisions

## Workflow

1. Parse reviewer comments into atomic concerns.
2. Map each concern to evidence, concession, or approved revision.
3. Draft direct reviewer-facing and AC-aware answers.
4. Compress while preserving decision-relevant evidence and respectful tone.

## Gate

Every material concern must have an answer, evidence, concession, or approved revision promise.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/rebuttal-guide.md`
