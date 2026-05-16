---
name: paper-ai-reviewer
description: "Simulate strict academic reviewers and convert weaknesses into severity-ranked fix plans. Use when: Use before submission, after major draft changes, or whenever the user asks for review, scoring, or acceptance-risk assessment."
---

# paper-ai-reviewer

## Use when

Use before submission, after major draft changes, or whenever the user asks for review, scoring, or acceptance-risk assessment.

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

`paper/REVIEW_SIMULATION.md`, `paper/FIX_PLAN.md`, score/risk rubric

## Workflow

1. Review as skeptical specialists, not copyeditors only.
2. Separate fatal, major, minor, and wording issues.
3. Map each issue to claim/evidence artifacts.
4. Create a fix plan that prioritizes scientific risk before polish.

## Gate

Submission-ready status is blocked while fatal unsupported claims, missing baselines, or reproducibility gaps remain.

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

- `references/review-rubric.md`
- `references/fix-plan.md`
- `references/first-impression-review.md`
