---
name: paper-ai-reviewer
description: Simulate strict AI-paper reviewers and produce first-impression audits, technical reviews, score-risk analysis, and prioritized fix plans. Use before submission, after major revisions, or when acceptance risk must be assessed.
---

# paper-ai-reviewer

## Use when

Use for pre-submission review, score/risk assessment, reviewer simulation, and fix prioritization.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/REVIEW_SIMULATION.md`, `paper/FIX_PLAN.md`, first-impression audit

## Workflow

1. Run first-impression pass on title, abstract, first two pages, and first figure.
2. Review novelty, significance, correctness, empirical support, clarity, reproducibility, limitations, and presentation.
3. Separate evidence observed from reviewer inference.
4. Convert critique into fatal/major/minor/polish fixes.

## Gate

Do not mark submission-ready while fatal unsupported claims, missing baselines, or unreadable first visuals remain.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/reviewer-guide.md`
