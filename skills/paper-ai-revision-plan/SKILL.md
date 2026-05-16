---
name: paper-ai-revision-plan
description: Convert reviewer, self-review, or submission-check findings into a prioritized revision plan with owners, artifacts, evidence, and risk gates. Use after reviewer simulation, real reviews, or any audit that produces many fixes.
---

# paper-ai-revision-plan

## Use when

Use to turn critique into an actionable fix plan rather than ad hoc edits.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/REVISION_PLAN.md`, prioritized tasks, gate checklist, promised revisions

## Workflow

1. Deduplicate findings across reviewers/checks.
2. Rank fixes by decision impact and effort.
3. Map each fix to artifact files and required evidence.
4. Separate do-now, if-time, appendix, and no-action-with-rationale items.

## Gate

Major revisions must link to the concern or claim they resolve.

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

- `references/fix-priority.md`
