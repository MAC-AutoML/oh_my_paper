---
name: paper-ai-writing
description: 统筹整篇 AI 论文写作与跨章节修改，保持读者导向的叙事流、段落功能和 claim-evidence 绑定；适合多章节起草、论文故事线构建和全文一致性检查。
---

# paper-ai-writing

## Use when

Use for whole-paper story, section outline, paragraph flow, and cross-section consistency.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

paper story outline, section plan, claim-grounded rewrite notes

## Workflow

1. Audit document surface, information flow, and underlying argument.
2. Route section-specific work to title/abstract, introduction, related work, method, experiments, limitations, figures, or layout.
3. Keep claims tied to evidence status.
4. Revise from story to paragraphs to language.

## Gate

Important claims must be linked to evidence or explicitly caveated before final prose.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or curated case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/whole-paper-writing.md`
- `references/full-paper-narrative-flow.md` for paragraph-function audits, section-job mapping, and full-paper narrative closure.
