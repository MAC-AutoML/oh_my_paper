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
