---
name: paper-ai-literature-map
description: Organize related work into a literature map, contrast table, and positioning narrative for AI papers. Use when the user asks for related work structure, paper finding/reading synthesis, novelty positioning, or reviewer-facing comparison framing.
---

# paper-ai-literature-map

## Use when

Use for literature organization, contrast tables, related-work planning, and novelty positioning.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/LITERATURE_MAP.md`, contrast axes, related-work outline, missing-citation risks

## Workflow

1. Identify comparison axes rather than chronology only.
2. Group papers by problem, method, assumption, and evidence.
3. Map each group to the current paper's claimed difference.
4. Flag missing seminal or closest-work comparisons.

## Gate

Related work is not ready if closest competitors and contrast axes are unnamed.

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

- `references/contrast-axes.md`
