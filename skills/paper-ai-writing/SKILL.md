---
name: paper-ai-writing
description: "Draft, revise, polish, and audit AI-paper sections while preserving claim-evidence grounding. Use when: Use for abstract, introduction, related work, method, experiments, limitation, or conclusion drafting and revision."
---

# paper-ai-writing

## Use when

Use for abstract, introduction, related work, method, experiments, limitation, or conclusion drafting and revision.

## Do not use when

- The user only asks a general academic-writing question with no paper workflow artifacts.
- The task belongs to another `paper-ai-*` phase and no handoff is needed.
- The requested action would publish private materials or unsupported scientific claims.

## Inputs

- Current user request.
- Relevant `.paper-ai/` state when present.
- Relevant `paper/` artifacts for this phase.
- Public-safe references listed below, loaded only when needed.

## Outputs

section drafts, updated `paper/CLAIMS.md`, writing risk notes

## Workflow

1. Load `PAPER_BRIEF.md`, `CLAIMS.md`, and `EVIDENCE_MAP.md` first.
2. Draft section text around claim IDs, not unsupported invention.
3. Run a paragraph-level clarity and evidence pass.
4. List unresolved claims and needed human decisions.

## Gate

Important claims must be linked to evidence, marked as partial/planned, or removed before final wording.

## Required artifacts

- Read existing `.paper-ai/PAPER_AI_STATE.md` when present.
- Prefer project artifacts under `paper/` over chat memory.
- Append material usage notes to `.paper-ai/MATERIALS_USED.md` without copying raw private sources.

## Safety rules

- Do not invent experiments, citations, reviewer scores, or results.
- Mark unsupported claims instead of polishing them into stronger claims.
- Ask for human approval before promising new experiments, releases, or major rebuttal commitments.
- Keep raw `materials/` local; reference only public-safe category names in outputs.

## Trace expectation

When this skill changes project artifacts, append a concise event to `.paper-ai/TRACE.jsonl` when tooling exists. Until Milestone 2 tooling exists, include a short trace note in the output.

## References to load as needed

- `references/section-patterns.md`
- `references/claim-grounding.md`
