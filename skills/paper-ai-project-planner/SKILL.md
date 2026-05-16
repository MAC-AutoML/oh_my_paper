---
name: paper-ai-project-planner
description: Plan the end-to-end AI-paper project from direction to submission with OMX-style phases, gates, risks, and artifacts. Use when the user has a project idea, partial results, a deadline, or asks how to organize the whole paper workflow.
---

# paper-ai-project-planner

## Use when

Use for project kickoff, milestone planning, deadline planning, phase sequencing, and deciding what the paper workflow should do next.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/PROJECT_PLAN.md`, phase roadmap, risk register, next-action queue

## Workflow

1. Define target venue/deadline assumptions.
2. Split work into idea, evidence, writing, visuals, review, rebuttal, and eval lanes.
3. Name blockers and human decisions.
4. Produce the next three concrete actions and gates.

## Gate

Do not start drafting until target claim/evidence artifacts are at least stubbed.

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

- `references/phase-map.md`
