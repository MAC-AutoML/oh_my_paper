---
name: paper-ai-experiments
description: Plan, draft, and audit AI-paper experiment sections, result analysis, baselines, metrics, ablations, and empirical claim support without inventing data. Use for experiments and results chapters.
---

# paper-ai-experiments

## Use when

Use for experiment design, experiment prose, result interpretation, baseline/metric checks, and ablation narratives.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/EXPERIMENTS_DRAFT.md`, evidence coverage table, result-analysis paragraphs

## Workflow

1. Map claims to datasets, baselines, metrics, and artifacts.
2. Write question/setup/result/interpretation/caveat for each result.
3. Separate main results, ablations, diagnostics, and limitations.
4. Flag missing numbers or evidence instead of inventing them.

## Gate

No numeric result or empirical superiority claim may be written without provided evidence.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/experiments-guide.md`
