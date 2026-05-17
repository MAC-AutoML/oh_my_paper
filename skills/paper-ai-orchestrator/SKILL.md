---
name: paper-ai-orchestrator
description: 统筹 AI 论文全流程，在选题、长文多轮写作、图表、排版、审稿模拟和 rebuttal 之间选择下一步；适合启动/恢复论文工作流或判断当前最该使用哪个论文技能。 / Routes the academic paper workflow across ideation, iterative writing, figures, review simulation, revision, and rebuttal.
---

# paper-ai-orchestrator

## Use when

Use to decide the next paper-natural skill and keep minimal state across idea, writing, figures, review, and rebuttal.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

minimal `.paper-ai/PAPER_AI_STATE.md`, next-skill route, handoff note

## Workflow

1. Inspect available paper artifacts and the user goal.
2. If the user asks for full-paper or long-section generation, require multi-round drafting rather than one-shot prose.
3. Choose exactly one natural next skill unless the user requests a multi-step plan.
4. Name missing evidence or human decisions.
5. Keep state minimal and avoid creating management artifacts that do not help the paper.

## Gate

The next paper step and blocking evidence gaps must be explicit.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or curated case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/workflow-router.md`
