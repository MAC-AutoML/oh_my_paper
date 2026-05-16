---
name: paper-ai-related-work
description: Draft and revise related work sections for AI papers using contrast-based organization and reviewer-aware positioning. Use when the user needs related work prose, taxonomy, closest-work discussion, or novelty-risk mitigation.
---

# paper-ai-related-work

## Use when

Use after or with `paper-ai-literature-map` to turn contrast axes into prose.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/RELATED_WORK_DRAFT.md`, closest-work paragraph, citation-risk notes

## Workflow

1. Load literature map or create a minimal one.
2. Organize paragraphs by conceptual contrast.
3. Explain closest work fairly before differentiating.
4. Avoid strawman claims and unsupported novelty.

## Gate

Do not claim novelty unless closest work and comparison basis are explicit.

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

- `references/related-work-patterns.md`
