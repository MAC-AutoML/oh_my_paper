---
name: paper-ai-material-intake
description: Ingest, classify, summarize, and fuse newly arriving paper-writing/review material into the local-only oh-my-paper knowledge cache without publishing raw sources. Use when the user provides new PDFs, repos, articles, screenshots, OCR text, meeting notes, or asks to update/fuse materials into the skill group.
---

# paper-ai-material-intake

## Use when

Use when new material arrives or existing local material must be categorized, summarized, fused into skills/evals, or kept private while informing future behavior.

## Do not use when

- The request belongs to a narrower `paper-ai-*` skill and no routing/handoff is needed.
- The user asks for unsupported scientific claims, fabricated experiments, or fake citations.
- The task would publish raw local-only/copyrighted material.

## Inputs

- Current user request and target venue/deadline if known.
- Relevant `.paper-ai/` and `paper/` artifacts.
- Local material category summaries, not raw local-only sources.

## Outputs

ignored `/materials/paper-ai/external/<id>/` entries, public-safe synthesis bullets, skill/eval change candidates

## Workflow

1. Run or recommend `uv run oh-my-paper intake-material <pdf> --material-id <id>` for text PDFs.
2. Classify material into research, writing, figure, review, rebuttal, layout, or infra categories.
3. Read local summaries/raw text only inside the private workspace.
4. Convert lessons into public-safe bullets and candidate skill/eval changes.
5. Commit only safe docs, skill instructions, synthetic fixtures, or code changes.

## Gate

Raw PDFs, screenshots, OCR text, private repo names, and verbatim proprietary material must remain untracked.

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

- `references/intake-loop.md`
