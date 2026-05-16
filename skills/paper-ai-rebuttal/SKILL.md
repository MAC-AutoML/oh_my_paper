---
name: paper-ai-rebuttal
description: "Build evidence-backed, AC-aware rebuttal plans and responses from reviewer comments and paper evidence. Use when: Use when reviews arrive or the user asks to draft, organize, compress, or audit an author response."
---

# paper-ai-rebuttal

## Use when

Use when reviews arrive or the user asks to draft, organize, compress, or audit an author response.

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

`paper/REBUTTAL_PLAN.md`, `paper/PROMISED_REVISIONS.md`, response drafts, concern table

## Workflow

1. Parse reviewer comments into atomic concerns.
2. Map each concern to evidence, limitation, or planned revision.
3. Draft reviewer-specific answers plus AC-facing summary.
4. Run tone, overpromise, and space-compression checks.

## Gate

Every reviewer concern must have an answer, evidence, concession, or approved revision promise before final response.

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

- `references/concern-table.md`
- `references/tone-and-compression.md`
- `references/ac-aware-rebuttal.md`
