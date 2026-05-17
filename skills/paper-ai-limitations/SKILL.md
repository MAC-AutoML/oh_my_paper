---
name: paper-ai-limitations
description: 撰写和审查 AI 论文 limitations、scope caveats、validity threats、伦理/安全说明和 claim narrowing；适合限制、风险、诚实边界和过度主张收缩。
---

# paper-ai-limitations

## Use when

Use for limitation sections, claim caveats, threat-to-validity notes, and honest scope framing.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/LIMITATIONS.md`, caveated claim rewrites, limitation table

## Workflow

1. List scope, assumption, evidence, compute, reproducibility, and deployment limitations.
2. Link limitations to affected claims.
3. Rewrite overbroad claims with scope conditions.
4. Phrase limitations honestly without self-sabotage.

## Gate

Validity-affecting limitations must be visible before submission or rebuttal.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/limitations-guide.md`
