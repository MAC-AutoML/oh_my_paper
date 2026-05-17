# Figure prompts for image2 / imagegen

本 demo 中已提交可复现 SVG 图。若要用 image2 / imagegen 生成更像论文插图的位图，可使用以下提示词。建议生成后人工核对文字，不要把无法辨认的 AI 文字直接放进论文。

## Figure 1: Pipeline overview

Use case: infographic-diagram
Asset type: academic paper overview figure
Primary request: Create a clean academic workflow diagram titled "Policy-MME Diagnostic Pipeline".
Scene/backdrop: white or very light slate background, flat vector infographic style.
Content: four connected blocks: Input Material, Capability Hierarchy, Grouped Scoring, Paper Output. Capability Hierarchy expands into L1 Optimization Stability, L2 Robustness and Generalization, L3 Decision Faithfulness. Use arrows to show progression from input to scoring to paper output.
Style: top-tier computer science paper overview figure, restrained colors, crisp lines, no decorative icons unless subtle.
Avoid: fake logos, watermark, tiny unreadable text, 3D clutter.

## Figure 2: Synthetic result comparison

Use case: infographic-diagram
Asset type: academic paper result figure
Primary request: Create a horizontal bar chart titled "Synthetic Policy-MME Score Comparison".
Data: PPO 52.4, SAC 58.2, TD3 49.7, Oracle/Human reference 88.9.
Annotation: Add a callout saying "Average return can hide robustness and faithfulness failures".
Style: clean vector chart, publication-ready, high contrast, minimal grid.
Avoid: implying these are real empirical numbers; include small note "demo synthetic values".
