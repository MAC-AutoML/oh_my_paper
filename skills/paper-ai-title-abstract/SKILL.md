---
name: paper-ai-title-abstract
description: Draft and audit AI-paper titles and abstracts for first impression, clarity, searchability, contribution accuracy, and evidence-safe scope. Use for title options, abstracts, acronyms, contribution summaries, and first-page hooks.
---

# paper-ai-title-abstract

## Use when

Use for title candidates, abstract drafts, acronym decisions, and first-impression checks.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

title candidates, abstract draft, first-impression audit

## Workflow

1. Identify problem, method/insight, evidence, and audience.
2. Generate clear/searchable title options.
3. Draft abstract with problem, gap, method, evidence, implication.
4. Reject overclaiming and unclear first impressions.

## Gate

Title and abstract must not claim beyond the evidence ledger.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/title-abstract-guide.md`
