---
name: paper-ai-submission-check
description: Run pre-submission AI-paper QA across story, claims, experiments, figures, tables, layout, reproducibility, and reviewer first impression. Use before deadline, arXiv, conference submission, or when the user asks if the paper is ready.
---

# paper-ai-submission-check

## Use when

Use for final pre-submission checks and readiness assessment.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/SUBMISSION_CHECK.md`, readiness verdict, blocker list, final fix queue

## Workflow

1. Check title/abstract/first two pages/first figure first.
2. Run claim/evidence, experiment, figure/table, related work, layout, and reproducibility passes.
3. Rank blockers by fatal/major/minor/polish.
4. Return a readiness verdict with evidence.

## Gate

Do not say submission-ready while fatal unsupported claims, missing core baselines, or unreadable first-page visuals remain.

## Artifact protocol

- Inspect `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md` when present.
- Prefer workspace artifacts over chat memory.
- Append or request a `.paper-ai/MATERIALS_USED.md` note using category names only.
- Keep outputs as editable markdown artifacts under `paper/` or `.paper-ai/`.

## Safety rules

- Do not invent experiments, citations, reviewer scores, or results.
- Mark unsupported claims instead of polishing them into stronger claims.
- Ask for human approval before promising new experiments, code releases, or major rebuttal commitments.
- Keep raw `/materials` and `/temp` local; never copy private text into public outputs.

## Trace expectation

When tooling exists, append a concise event to `.paper-ai/TRACE.jsonl`. Otherwise include a short trace note with phase, inputs, outputs, and gate result.

## References to load as needed

- `references/submission-rubric.md`
