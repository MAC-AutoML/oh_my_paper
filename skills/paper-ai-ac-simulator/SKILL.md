---
name: paper-ai-ac-simulator
description: Simulate area-chair and reviewer-discussion perspectives for AI papers and rebuttals, focusing on score movement, consensus risks, and decision-maker evidence. Use after reviews arrive or before rebuttal finalization.
---

# paper-ai-ac-simulator

## Use when

Use when rebuttal strategy needs AC-facing prioritization or when reviewer disagreement/score movement must be reasoned about.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/AC_SIMULATION.md`, decision-risk summary, AC-facing rebuttal priorities

## Workflow

1. Summarize reviewer positions and likely AC concerns.
2. Identify consensus blockers and score-moving evidence.
3. Separate what can change minds from what only clarifies wording.
4. Recommend AC-facing response order and concise meta-narrative.

## Gate

Do not predict acceptance confidently; provide evidence-weighted scenarios and uncertainty.

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

- `references/ac-perspective.md`
