---
name: paper-ai-method-writing
description: Draft reader-centered AI-paper method sections with background, running examples, notation, algorithms, and component rationale. Use when writing methods, model architecture, algorithms, equations, or implementation details.
---

# paper-ai-method-writing

## Use when

Use for method section planning/drafting and for making technical descriptions understandable before formalism.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/METHOD_DRAFT.md`, notation table, running example, component rationale

## Workflow

1. Provide necessary background and assumptions before details.
2. Use a running example before equations when helpful.
3. Define notation and components in reader order.
4. Explain why each component exists and which claim it supports.

## Gate

Method is not ready if notation/components are introduced before the reader has context to understand them.

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

- `references/running-example.md`
