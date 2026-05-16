---
name: paper-ai-claim-evidence
description: Maintain the central claim/evidence ledger for AI-paper workflows and block unsupported claims before drafting, figures, review, or rebuttal. Use when claims, results, evidence maps, caveats, or unsupported statement audits are needed.
---

# paper-ai-claim-evidence

## Use when

Use whenever claims are introduced, strengthened, visualized, reviewed, or used in rebuttal.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

updated `paper/CLAIMS.md`, `paper/EVIDENCE_MAP.md`, unsupported-claim report

## Workflow

1. Extract atomic claims from draft/project notes.
2. Assign each claim a stable ID and evidence status.
3. Map evidence artifacts, caveats, and missing support.
4. Tell downstream skills which claims are safe, partial, planned, unsupported, or removed.

## Gate

Unsupported claims must be removed, caveated, or explicitly labeled before final wording.

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

- `references/status-rules.md`
