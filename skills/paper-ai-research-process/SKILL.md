---
name: paper-ai-research-process
description: "Turn research ideas, project notes, and experiment summaries into paper briefs, claims, evidence maps, and experiment plans. Use when: Use when the user has an idea, project direction, preliminary results, baseline gap, or unclear contribution story."
---

# paper-ai-research-process

## Use when

Use when the user has an idea, project direction, preliminary results, baseline gap, or unclear contribution story.

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

`paper/PAPER_BRIEF.md`, `paper/CLAIMS.md`, `paper/EVIDENCE_MAP.md`, `paper/EXPERIMENT_PLAN.md`

## Workflow

1. Separate goal, problem, method, evidence, and missing evidence.
2. Create or update claim IDs in `CLAIMS.md`.
3. Map available and planned evidence in `EVIDENCE_MAP.md`.
4. Produce a writing-ready paper brief and experiment-risk list.

## Gate

No drafting handoff until each main claim has an evidence status and missing experiments are explicit.

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

- `references/research-brief.md`
- `references/claim-evidence-map.md`
