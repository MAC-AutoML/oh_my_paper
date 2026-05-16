---
name: paper-ai-tables
description: Design and audit AI-paper result tables, ablation tables, comparison matrices, and table captions around claims and reader expectations. Use when creating or revising tables, table titles, captions, or result presentation.
---

# paper-ai-tables

## Use when

Use for table planning, readability, captioning, and claim-linked result presentation.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/TABLE_PLAN.md`, table schema, caption/title options, readability audit

## Workflow

1. Identify the claim the table supports.
2. Choose rows/columns around the comparison readers need.
3. Mark best/second-best and statistical caveats only when supported.
4. Draft title/caption that states the takeaway.

## Gate

Each table must have one takeaway and must not imply unsupported comparisons.

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

- `references/table-checklist.md`
