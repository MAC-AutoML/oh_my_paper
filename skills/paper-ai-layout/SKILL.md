---
name: paper-ai-layout
description: 检查 AI 论文版式、页数预算、venue/template 假设、格式、语言润色、翻译、压缩和最终 PDF 可读性；适合页限、LaTeX/Word 排版、camera-ready 清理和稳定文本 polish。
---

# paper-ai-layout

## Use when

Use after story/evidence are stable for page budget, formatting, language polish, compression, translation, and final readability.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/LAYOUT_REPORT.md`, polish notes, formatting checklist

## Workflow

1. Check venue/page/template constraints.
2. Inspect figure/table placement and first-page readability.
3. Polish language without changing claim strength.
4. Flag formatting/PDF issues and remaining risks.

## Gate

Do not polish or compress away evidence caveats or unsupported-claim warnings.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/layout-polish-guide.md`
