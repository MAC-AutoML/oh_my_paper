---
name: paper-ai-related-work
description: Draft and revise AI-paper related work using contrast-based organization, closest-work positioning, and novelty-risk mitigation. Use for related work sections, literature positioning, and comparison narratives.
---

# paper-ai-related-work

## Use when

Use for related work prose, literature grouping, closest-work comparison, and novelty positioning.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/RELATED_WORK_DRAFT.md`, contrast map, citation-risk notes

## Workflow

1. Group papers by meaningful contrast axes.
2. Explain representative work fairly.
3. State limitations/gaps without strawman wording.
4. Write closest-work comparison directly.

## Gate

Novelty claims require closest work and contrast axes.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or adapted case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/related-work-guide.md`
