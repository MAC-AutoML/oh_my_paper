---
name: paper-ai-figures
description: 设计和审查 AI 论文图、结果图、方法示意图、表格、caption 和首页视觉，使每个视觉服务一个 takeaway 和 claim；适合画图规划、imagegen 图像提示词、表格规划、视觉层级和 caption。 / Designs academic figures, tables, captions, visual hierarchy, and imagegen prompts from paper claims.
---

# paper-ai-figures

## Use when

Use for paper figures, architecture diagrams, result plots, tables, captions, visual readability, and first-page visual checks.

## Do not use when

- The task is only generic chat and no paper artifact or paper-writing decision is involved.
- The user asks to fabricate evidence, citations, reviewer opinions, or results.
- The request should be handled by a narrower chapter/figure/rebuttal skill already named by the user.

## Inputs

- User request and target venue/deadline if known.
- Existing paper draft, notes, figures, tables, reviews, or workspace artifacts.
- Local material summaries and selected rights-cleared excerpts when useful.

## Outputs

`paper/FIGURE_PLAN.md`, `paper/TABLE_PLAN.md`, captions, visual audit

## Workflow

1. Identify the claim each visual supports.
2. Choose figure/table type based on the takeaway.
3. For generated bitmap figures, convert article content into a figure intent card, then into a structured scientific image brief.
4. Design labels, hierarchy, caption, caveats, and retry criteria.
5. Check first-page visual impact, text fidelity, and reviewer-style readability.

## Scientific image prompt protocol

For imagegen figures, do not prompt with “make it beautiful.” Write a compact design brief:

- **Claim/takeaway:** the one sentence the reader should learn in 5 seconds.
- **Paper-content extraction:** list entities, relationships, evidence status, failure modes, and section dependencies before drawing.
- **Figure type:** pipeline, taxonomy, score trajectory, ablation plot, evidence map, comparison matrix, or qualitative panel.
- **Layout grammar:** reading direction, panel structure, alignment grid, arrows, grouping, and focal point.
- **Layer stack:** background grid -> major panels -> mechanism flow -> evidence callouts -> minimal text labels.
- **Allowed visible labels:** exact short labels only; quote labels when the image model must render them.
- **Title policy:** do not ask the image model to render titles, subtitles, captions, style names, or internal file names unless they are in the allowed-label list.
- **Aesthetic contract:** conference-paper style, white background, muted accessible palette, thin strokes, generous whitespace, no clipart.
- **Evidence boundary:** supported values only; synthetic or illustrative values must be marked as such in caption/prompt.
- **Negative prompt:** no pseudo-text, logos, watermarks, glossy 3D, decorative icons, dense paragraphs, fake axes, or unsupported numbers.
- **Retry rule:** regenerate or repair if labels drift, pseudo-text appears, the focal claim is not obvious, or the figure looks like marketing art.

## Layered / dense figure mode

For complex paper figures, request a multi-panel academic schematic instead of one flat row of boxes:

1. Panel A: problem or input evidence.
2. Panel B: method/mechanism with 2--3 semantic layers.
3. Panel C: diagnostic output, score, or artifact map.
4. Use thin connectors and one accent color to show the main causal path.
5. Keep dense information in grouped panels, not in long in-image sentences.

For benchmark/evaluation papers, prefer a CCF-A Figure-1 composite: taxonomy/hierarchy panel + diagnostic ranking/score panel + representative evidence strip. Keep it information-dense but organized; do not make it a cartoon overview.

## Image generation rule

When the desired output is a generated raster image, use the Codex `imagegen` skill if available. Do not replace imagegen with code-generated SVG unless the user explicitly wants deterministic vector output. If image generation is unavailable, save the imagegen prompt and mark the image status as `not_run`.

## Gate

Every visual must have one takeaway and a claim/evidence link.

## Shared rules

- Work from project artifacts when present: `.paper-ai/PAPER_AI_STATE.md`, `paper/CLAIMS.md`, and `paper/EVIDENCE_MAP.md`.
- Preserve claim IDs across writing, figures, review, and rebuttal.
- Do not invent experiments, citations, reviewer scores, numeric results, or code releases.
- Mark unsupported claims as unsupported instead of polishing them into confident prose.
- Keep `/materials` and `/temp` as raw-source caches; include only selected rights-cleared excerpts or curated case cards inside skills.
- If you change a durable paper artifact, include a short trace note: phase, inputs, outputs, gate result.

## References to load as needed

- `references/figures-tables-guide.md`
- `references/imagegen-figure-workflow.md` for article-content-to-imagegen prompts, generated figure audits, and fallback status.
