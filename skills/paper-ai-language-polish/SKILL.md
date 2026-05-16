---
name: paper-ai-language-polish
description: Polish, translate, shorten, expand, and de-AI academic prose for AI papers while preserving LaTeX, claim meaning, and evidence limits. Use for Chinese-English academic translation, grammar/style polishing, compression, expansion, or removing AI-like phrasing.
---

# paper-ai-language-polish

## Use when

Use for final language improvement after claim/evidence and section structure are stable.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

polished prose, change notes, preserved-meaning warnings

## Workflow

1. Identify target language, style, length, and file format constraints.
2. Preserve LaTeX commands, citations, math, claim IDs, and technical terms.
3. Improve clarity, sentence force, and flow without strengthening unsupported claims.
4. Report meaning-changing edits and remaining issues.

## Gate

Do not polish unsupported claims into more confident language.

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

- `references/polish-modes.md`
