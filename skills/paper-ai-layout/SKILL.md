---
name: paper-ai-layout
description: "Check LaTeX/Word layout, page budget, section ordering, figure/table placement, and camera-ready formatting assumptions. Use when: Use when the user asks about formatting, page limits, venue template fit, camera-ready cleanup, or placement decisions."
---

# paper-ai-layout

## Use when

Use when the user asks about formatting, page limits, venue template fit, camera-ready cleanup, or placement decisions.

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

`paper/LAYOUT_REPORT.md`, page-budget notes, placement checklist

## Workflow

1. Collect venue/template/page-budget assumptions.
2. Map sections, figures, tables, and supplement items to page budget.
3. Flag overflow and placement risks.
4. Recommend minimal layout fixes before content rewrites.

## Gate

Do not claim venue compliance when the target template or page limit is unknown.

## Required artifacts

- Read existing `.paper-ai/PAPER_AI_STATE.md` when present.
- Prefer project artifacts under `paper/` over chat memory.
- Append material usage notes to `.paper-ai/MATERIALS_USED.md` without copying raw private sources.

## Safety rules

- Do not invent experiments, citations, reviewer scores, or results.
- Mark unsupported claims instead of polishing them into stronger claims.
- Ask for human approval before promising new experiments, releases, or major rebuttal commitments.
- Keep raw `materials/` local; reference only public-safe category names in outputs.

## Trace expectation

When this skill changes project artifacts, append a concise event to `.paper-ai/TRACE.jsonl` when tooling exists. Until Milestone 2 tooling exists, include a short trace note in the output.

## References to load as needed

- `references/layout-budget.md`
- `references/formatting-checklist.md`
