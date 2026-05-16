---
name: paper-ai-figures
description: "Plan paper figures, experiment charts, tables, titles, and captions around single takeaways and claim support. Use when: Use for teaser, method, pipeline, architecture, result chart, table, caption, or visual-readability work."
---

# paper-ai-figures

## Use when

Use for teaser, method, pipeline, architecture, result chart, table, caption, or visual-readability work.

## Do not use when

- The user only asks a general academic-writing question with no paper workflow artifacts.
- The task belongs to another `paper-ai-*` phase and no handoff is needed.
- The requested action would publish private materials or unsupported scientific claims.

## Inputs

- Current user request.
- Relevant `.paper-ai/` state when present.
- Relevant `paper/` artifacts for this phase.
- Public-safe references listed below, loaded only when needed.

## Outputs

`paper/FIGURE_PLAN.md`, `paper/TABLE_PLAN.md`, captions, visual audit notes

## Workflow

1. Identify the claim each visual must support.
2. Choose figure/table type based on the comparison or mechanism.
3. Draft title/caption and readability checklist.
4. Flag missing data, crowded layout, or unclear visual hierarchy.

## Gate

Every proposed visual must name one takeaway and link to at least one claim or reviewer concern.

## Required artifacts

- Read existing `.paper-ai/PAPER_AI_STATE.md` when present.
- Prefer project artifacts under `paper/` over chat memory.
- Append material usage notes to `.paper-ai/MATERIALS_USED.md` without copying raw local-only sources.

## Safety rules

- Do not invent experiments, citations, reviewer scores, or results.
- Mark unsupported claims instead of polishing them into stronger claims.
- Ask for human approval before promising new experiments, releases, or major rebuttal commitments.
- Keep raw `materials/` local; reference only public-safe category names in outputs.

## Trace expectation

When this skill changes project artifacts, append a concise event to `.paper-ai/TRACE.jsonl` when tooling exists. Until Milestone 2 tooling exists, include a short trace note in the output.

## References to load as needed

- `references/visual-takeaway-checklist.md`
- `references/caption-patterns.md`
- `references/first-page-figure.md`
