---
name: paper-ai-experiment-planner
description: Design experiment plans, ablations, baselines, metrics, debugging records, and evidence coverage for AI papers. Use when claims need empirical support, experiments are failing, baselines/metrics are unclear, or a paper needs an experiment roadmap.
---

# paper-ai-experiment-planner

## Use when

Use when the paper needs evidence design before writing or when reviewers would question experimental rigor.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/EXPERIMENT_PLAN.md`, baseline matrix, metric plan, ablation/debug checklist

## Workflow

1. Map each claim to experiment evidence.
2. Choose datasets, baselines, metrics, ablations, and significance checks.
3. Separate main experiments from diagnostics and appendix evidence.
4. List failure/debug hypotheses and record-keeping needs.

## Gate

No strong empirical claim unless required dataset/baseline/metric evidence is available or explicitly planned.

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

- `references/experiment-rigor.md`
