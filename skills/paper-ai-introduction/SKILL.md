---
name: paper-ai-introduction
description: Build reader-centered AI-paper introductions from problem motivation to gap, method idea, contributions, and evidence preview. Use when drafting or revising introductions, first two pages, story framing, or contribution lists.
---

# paper-ai-introduction

## Use when

Use for Introduction structure, first-two-pages flow, motivation, gap statements, and contribution paragraphs.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/INTRODUCTION_DRAFT.md`, contribution list, reader-flow audit

## Workflow

1. Start with reader problem and task context, not author chronology.
2. Explain prior work enough to reveal the gap/challenge.
3. Introduce the method idea and why it addresses the gap.
4. End with evidence-backed contributions and preview.

## Gate

Every contribution must link to a claim ID and evidence status.

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

- `references/intro-flow.md`
