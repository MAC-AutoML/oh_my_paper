---
name: paper-ai-method
description: 撰写和修改 AI 论文 Method，覆盖问题设定、假设、running example、符号、算法、组件动机和实现细节；适合方法、模型、算法或公式写作。
---

# paper-ai-method

## Use when

Use for method section planning, technical explanation, notation, and component rationale.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/METHOD_DRAFT.md`, notation table, running example, component rationale

## Workflow

1. Give setup and assumptions before formal details.
2. Use a running example for complex methods.
3. Introduce notation and components in reader order.
4. Link components to claims and ablations.

## Gate

Reader must understand context and notation before equations/components become dense.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/method-guide.md`
