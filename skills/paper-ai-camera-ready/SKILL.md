---
name: paper-ai-camera-ready
description: Plan camera-ready revisions for accepted AI papers, including promised changes, reviewer-visible fixes, formatting, acknowledgments, artifact links, and final consistency checks. Use after acceptance or conditional acceptance.
---

# paper-ai-camera-ready

## Use when

Use after acceptance/camera-ready instructions arrive or when promised rebuttal revisions must be fulfilled.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/CAMERA_READY_PLAN.md`, promised-revision checklist, final consistency report

## Workflow

1. Collect accepted-paper instructions and promised revisions.
2. Map every promise to an implemented change or documented reason.
3. Check formatting, references, artifacts, acknowledgments, and appendix boundaries.
4. Produce final consistency and release checklist.

## Gate

Do not mark camera-ready complete until rebuttal promises and venue instructions are accounted for.

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

- `references/camera-ready-checks.md`
