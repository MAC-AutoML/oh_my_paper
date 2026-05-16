---
name: paper-ai-experiment-writing
description: Write AI-paper experiment sections from grounded results, baselines, metrics, ablations, and analysis without inventing data. Use when drafting experiments, result analysis, ablations, or empirical claims.
---

# paper-ai-experiment-writing

## Use when

Use to convert result tables/logs into experiment prose and to audit empirical support.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/EXPERIMENTS_DRAFT.md`, result-analysis paragraphs, empirical caveats

## Workflow

1. For each experiment, state question, setup, result, interpretation, and caveat.
2. Tie results to claims and figures/tables.
3. Separate main results, ablations, diagnostics, and limitations.
4. Flag missing numbers instead of filling them in.

## Gate

Never write numeric results or superiority claims that are absent from provided evidence.

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

- `references/result-paragraph.md`
