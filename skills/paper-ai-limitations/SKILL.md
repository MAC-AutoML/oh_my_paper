---
name: paper-ai-limitations
description: Identify, phrase, and strategically place limitations, threats to validity, ethics notes, and scope caveats in AI papers and rebuttals. Use when the user asks for limitation sections, caveats, weakness framing, or honest scope control.
---

# paper-ai-limitations

## Use when

Use when claims need caveats or when reviewer trust depends on honest limitation framing.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

`paper/LIMITATIONS.md`, threat model, caveated claim rewrites

## Workflow

1. List technical, empirical, data, compute, deployment, and ethical limitations.
2. Distinguish fatal weaknesses from honest scope boundaries.
3. Rewrite overbroad claims with scope conditions.
4. Place limitations where they improve trust without self-sabotage.

## Gate

Do not hide limitations that affect claim validity or reviewer interpretation.

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

- `references/limitation-types.md`
