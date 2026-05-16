---
name: paper-ai-title-abstract
description: Create and audit AI-paper titles and abstracts for clarity, searchability, first impression, claim support, and reviewer expectations. Use when drafting titles, abstracts, contribution summaries, acronyms, or first-page hooks.
---

# paper-ai-title-abstract

## Use when

Use for title candidates, abstract drafts, acronym decisions, searchability checks, and first-impression audits.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

title candidates, abstract draft, first-impression audit, searchability notes

## Workflow

1. Identify problem, method/insight, evidence, and target audience.
2. Generate clear/searchable title options and avoid overclaiming.
3. Draft abstract with problem, gap, method, evidence, implication.
4. Audit first impression against reviewer time pressure.

## Gate

Reject titles/abstracts that overclaim beyond `CLAIMS.md` or hide the core problem.

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

- `references/first-impression.md`
