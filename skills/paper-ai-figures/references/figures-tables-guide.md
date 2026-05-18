# Figures and tables guide

Figures and tables should reduce reviewer effort. Each visual needs one takeaway and a claim link.

## Visual planning table

| Visual | Type | Claim | Takeaway | Required data | Risk |
| --- | --- | --- | --- | --- | --- |

## Figure types

- Teaser: first impression and problem/method/result hook.
- Method diagram: components and information flow.
- Result plot: comparison, trend, or trade-off.
- Ablation figure/table: component contribution.
- Qualitative examples: failure/success cases with interpretation.
- Evidence map: claim -> source -> verification status.
- Workflow artifact map: files, owners, gates, and review loops.

## Scientific figure aesthetics

Treat the image prompt as a design brief, not a beauty request:

- **Purpose first:** one visual answers one reviewer question.
- **Hierarchy:** title/caption carries claim; panels carry structure; labels carry only necessary names.
- **Layout:** use an alignment grid, equal margins, consistent box widths, and a predictable reading path.
- **Color semantics:** use 2--3 muted colors with meaning; reserve accent color for the key mechanism or failure.
- **Typography:** large short labels; avoid tiny legends and paragraphs inside the bitmap.
- **Density:** prefer fewer stronger elements over many small decorative details.
- **Evidence honesty:** do not visualize unsupported numbers, fake curves, or invented screenshots.
- **Layering:** use nested panels, lanes, brackets, and small multiples to organize complexity without turning the figure into a poster.

This protocol follows public scientific-visualization guidance: adapt figures to the medium, keep labels readable and stand-alone, use consistent accessible colors, avoid dense overlapping text, and treat scientific figures as objective evidence carriers rather than decorative artwork.

## From paper content to figure

Before prompting an image model, extract:

| Paper element | Figure translation |
| --- | --- |
| Research gap | contrast panel or warning callout |
| Core mechanism | central layered schematic |
| Evaluation protocol | loop, gate, or score trajectory |
| Data / artifacts | grouped cards or table-like map |
| Failure mode | highlighted bottleneck, crossed shortcut, or red/amber badge |
| Contribution list | three-panel overview, not a bullet list |

For method/benchmark papers, a strong first figure often combines three layers:

1. **Problem layer:** what old evaluation misses.
2. **Design layer:** what the new workflow/benchmark changes.
3. **Evidence layer:** what output, score, or artifact verifies the change.

## Generated figure discipline

If the figure is meant to be an AI-generated bitmap, route through the article-content-to-imagegen workflow:

1. Extract the claim and takeaway from the written section.
2. Draft a figure intent card before any image prompt.
3. Convert the intent card into an imagegen prompt with exact labels and avoid-list.
4. Generate with Codex `imagegen` when available.
5. Audit the generated image against the claim, caption, and text labels.

Do not treat code-generated SVG as the default generated-figure path. SVG/Mermaid previews are acceptable as deterministic placeholders or tests, but the user-facing image-generation path should preserve the prompt, generated bitmap, and audit trail.

## First-page visual check

- One sentence takeaway is obvious.
- Labels readable at paper size.
- Caption tells the reader what to notice.
- Colors/markers are distinguishable and meaningful.
- The visual supports a central claim rather than decoration.
- It does not look like a marketing slide, cartoon, app UI mockup, or generic stock illustration.

## Caption pattern

What is shown → what comparison matters → what conclusion to draw → caveat/setting.

## Table-specific checks

- Comparable settings only.
- Metrics and directions clearly labeled.
- Bold/underline only when justified.
- Abbreviations explained.
- Caption states takeaway, not just contents.

## Common failures

- Beautiful but not evidential figure.
- Too many subplots without hierarchy.
- Tiny legends and axes.
- Caption repeats labels but not interpretation.
- Table implies unfair comparison.
- AI image contains pseudo-text, random symbols, or labels not requested.
- Prompt asks for a “paper figure” but gives no layout grammar, so the model invents clutter.

## Material-derived case cards

### Case 1: Visual hierarchy from writing tutorial

Source excerpt (rights-cleared tutorial):

> 合理地综合使用信息元素：图 > 曲线 > 表 > 正文 > 公式。

Imitation recipe:

- If the reader must understand a pipeline, use a diagram before prose.
- If the reader must compare trends, use a curve/plot before a table.
- If the reader needs exact values, use a table.
- Use equations only after intuition and visual structure are clear.

### Case 2: First-page figure as review signal

Source excerpt (rights-cleared internal meeting):

> 我看你这个图这么丑啊，我对你的印象分基本上...一定要把每一个细节做好。

Use this first-page figure audit:

| Item | Pass condition |
| --- | --- |
| Purpose | reader knows why the figure exists in 5 seconds |
| Takeaway | one sentence conclusion is visible from caption/title |
| Flow | arrows/order match method story |
| Readability | labels readable at final paper size |
| Evidence | figure supports a central claim, not decoration |

### Case 3: Pipeline sketch before writing

Source excerpt (rights-cleared writing template):

> 画一个清楚的 pipeline figure 的草图；梳理论文的 story，写 Introduction 的写作思路，并整理 comparison experiments 和 ablation studies。

Imitation recipe:

1. Sketch pipeline with boxes only.
2. Name the claim supported by each box.
3. Decide which boxes need ablations.
4. Only then beautify the figure.

### Case 4: Caption imitation

Bad caption:

> Overview of our method.

Good caption:

> Our method first builds an object-relation graph from the prompt, then uses graph-conditioned attention masks to reduce attribute binding errors. This figure highlights the mechanism evaluated in Table 2 and ablated in Fig. 4.
