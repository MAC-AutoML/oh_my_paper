---
name: paper-ai-research-question
description: Sharpen AI research directions into important, testable research questions and contribution hypotheses. Use when the user has vague ideas, needs topic selection, wants novelty/significance critique, or must connect a project to a long-term research roadmap.
---

# paper-ai-research-question

## Use when

Use before experiments or writing when the problem, motivation, novelty, or target audience is still fuzzy.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/RESEARCH_QUESTION.md`, problem framing, hypothesis list, novelty/significance risks

## Workflow

1. Separate field direction, problem, gap, hypothesis, and contribution.
2. Stress-test importance, feasibility, and audience relevance.
3. Turn fuzzy ideas into testable questions.
4. List evidence needed to make the question publishable.

## Gate

A research question is not ready if it lacks audience, gap, and falsifiable evidence path.

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

- `references/question-rubric.md`
