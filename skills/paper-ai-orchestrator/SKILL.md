---
name: paper-ai-orchestrator
description: "Route full AI-paper workflows across planning, writing, figures, layout, review, rebuttal, and eval phases while maintaining durable artifacts and gates. Use when: Use when the user asks to start, resume, inspect, or decide the next step of an end-to-end paper workflow."
---

# paper-ai-orchestrator

## Use when

Use when the user asks to start, resume, inspect, or decide the next step of an end-to-end paper workflow.

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

`.paper-ai/PAPER_AI_STATE.md`, `.paper-ai/TRACE.jsonl`, `.paper-ai/MATERIALS_USED.md`, phase handoff notes

## Workflow

1. Inspect workspace artifacts before choosing a phase.
2. Update or create `.paper-ai/PAPER_AI_STATE.md` with current phase and blockers.
3. Route to exactly one specialist skill unless a review/eval gate is due.
4. Append a trace event for the routing decision.

## Gate

Current phase, missing artifacts, and next human decision are explicit before invoking a specialist skill.

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

- `references/workflow-map.md`
- `references/artifact-contract.md`
