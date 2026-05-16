---
name: paper-ai-eval-loop
description: "Convert weak workflow outputs into trace-backed eval fixtures and regression checks for continuous skill improvement. Use when: Use when a workflow failed, a user corrected an output, or a skill/reference change needs regression evidence."
---

# paper-ai-eval-loop

## Use when

Use when a workflow failed, a user corrected an output, or a skill/reference change needs regression evidence.

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

`tests/fixtures/evals/*.jsonl`, eval report, skill improvement notes

## Workflow

1. Find the smallest trace/artifact slice that shows the failure.
2. Create or update a synthetic/redacted fixture under `tests/fixtures/evals/`.
3. Define pass/fail expectations and privacy mode.
4. Record what skill/reference/script change the fixture protects.

## Gate

Do not mark a skill behavior fixed unless a fixture reproduces the failure or a waiver is documented.

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

- `references/fixture-schema.md`
- `references/privacy-modes.md`
