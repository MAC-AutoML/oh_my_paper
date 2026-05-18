# Imagegen figure workflow

Use this reference when the user wants Codex-generated paper visuals. The intended path is article content -> figure intent -> scientific image brief -> imagegen prompt -> generated raster image -> caption/audit.

## Workflow

1. Extract the figure's claim from the paper section.
2. Write a figure intent card:
   - supported claim ID;
   - one-sentence takeaway;
   - paper-content extraction: entities, relations, evidence status, and failure mode;
   - figure type and layout grammar;
   - layer stack;
   - required visual elements;
   - exact text labels if any;
   - evidence or data source;
   - risks.
3. Convert the intent card into a structured scientific image brief, then an `imagegen` prompt.
4. Use Codex `imagegen` skill for bitmap/raster generation when the environment exposes image generation.
5. Save generated project-bound assets under a workspace path such as `paper/figures/generated/` or `demo/figures/generated/`.
6. Audit text accuracy, visual hierarchy, evidence alignment, caption consistency, and academic aesthetics.
7. If image generation is unavailable, save the prompt and mark generation status as `not_run`; do not pretend the image was generated.

## Prompt schema for scientific figures

```text
Use case: infographic-diagram
Asset type: academic paper figure
Design brief:
Create a publication-ready <figure type> for a computer science / machine learning paper.

Reader takeaway:
<one sentence claim; must be visible from layout, not paragraph text>

Layout grammar:
<horizontal pipeline | vertical evidence stack | 2x2 panel grid | score trajectory | taxonomy tree | comparison matrix>
Use strict alignment, consistent margins, and a clear reading path.

Paper-content extraction:
- Entities: <objects/modules/sections/models/datasets>
- Relationships: <causal flow, dependency, comparison, feedback, hierarchy>
- Evidence status: <real, synthetic, proposed, placeholder>
- Failure mode to avoid: <what old evaluation or weak figure hides>

Layer stack:
1. Background: clean white or very light grid, no texture.
2. Major panels: 2--4 grouped regions with clear boundaries.
3. Mechanism flow: arrows, brackets, or paths showing dependencies.
4. Evidence callouts: small tags or score markers only if supported.
5. Text labels: short labels from the allowed list only.

Allowed visible labels:
Use only these exact short labels: "<label 1>", "<label 2>", ...
Do not render the internal file name, prompt metadata, style names, title, subtitle, caption, or explanatory sentences inside the image unless explicitly listed here.

Forbidden visible labels:
List common hallucinated helper words that must not appear, e.g. "score", "threshold", "audit", "overview", "workflow", "caption", "figure", unless they are explicitly in the allowed-label list.
Also forbid prompt-meta words such as "Figure 1", "academic paper", "publication-ready", venue names, and any auto-generated caption text unless explicitly requested.
If a word is used only as a layout concept, such as "foundation", "support", "repair", "evidence", or "prompt", either put it in the allowed-label list or explicitly forbid it as visible text.

Required visual elements:
<boxes, arrows, panels, axes, callouts, data values only if supported>

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; editorial, minimalist, white background, muted slate-blue / teal / gray palette, thin strokes, generous whitespace, flat vector-like raster, no cartoon clipart, no 3D, no glossy gradients.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, tiny footnotes, filenames, style names, or fake citations inside the image.
Do not add helper labels beyond the allowed list.
Absolutely no caption, footer paragraph, or generated figure description inside the bitmap; captions belong outside the image. Do not reserve an empty caption/footer band.
Layout words in the prompt are instructions only, not visible text.

Negative prompt:
Avoid decorative icons, stock-photo look, over-saturated colors, busy backgrounds, fake logos, watermark, fake axes, unsupported numeric claims, micro badges with text, thumbnail pseudo-text, and any text not listed above.

Output audit:
The generated image must make the takeaway obvious in 5 seconds and all visible labels must match the allowed list.
```

## Figure-type patterns

- **Pipeline / method overview:** 4--7 aligned boxes, one arrow direction, optional feedback loop; no more than two nested levels.
- **Layered mechanism schematic:** three semantic layers: input/evidence at bottom or left, method loop in the middle, outputs/diagnostics at top or right.
- **Benchmark Figure 1 composite:** left taxonomy/hierarchy panel + right ranked result or diagnostic panel + bottom example/evidence strip.
- **Evidence-board example:** question card, highlighted answer, supporting evidence thumbnails/cards, and a timeline or grouping rail.
- **Score trajectory:** one clean line or stepped path, 3--5 labeled milestones, restrained callouts; no fake confidence intervals.
- **Artifact map:** file/card grid with grouped folders and ownership boundaries; use consistent icon-free cards.
- **Taxonomy / capability hierarchy:** tree or ladder; emphasize hierarchy with position and spacing, not rainbow colors.
- **Comparison matrix:** rows are methods/conditions, columns are criteria; use abstract checkmarks only when grounded.
- **Qualitative panel:** few examples with concise labels; avoid photorealistic claims unless source images are provided.

## Dense figure tactics

- Use panels, lanes, and grouped cards to carry density; avoid making a single crowded flowchart.
- Put detail in spatial structure, not paragraphs: nesting, brackets, badges, and repeated visual motifs.
- Use a restrained color system: neutral structure, one evidence color, one warning/revision color.
- Prefer consistent small multiples when showing repeated sections, agents, or iterations.
- If the figure needs many labels, split into subpanels A/B/C rather than shrinking text.
- Ask for “editorial scientific schematic” or “journal figure plate,” not “comic,” “cute,” “cartoon,” “3D render,” or “isometric app illustration.”

## Video-benchmark style prompt add-ons

Use these only when the paper is a benchmark/evaluation paper:

```text
Style reference:
CCF-A/CVPR/NeurIPS benchmark Figure 1 style: information-dense but organized; left panel defines capability hierarchy, right panel shows diagnostic ranking or score gap, bottom strip shows representative evidence cards. Use restrained pastel category colors, thin separators, small panel letters, and a caption-ready layout. Avoid cartoon illustration and avoid decorative icons.
```

For video or multimodal papers, prefer evidence strips, timeline rails, taxonomy wheels/trees, radar/bar diagnostics, and side-by-side “old metric vs new metric” comparisons.

## Caption/audit pattern

```markdown
Caption: What is shown -> comparison/mechanism -> conclusion -> caveat.
Audit:
- Claim link:
- Evidence source:
- Text readable:
- No unsupported values:
- No pseudo-text:
- Academic aesthetic:
- If generated image has text errors, regenerate or replace text in a deterministic editor.
```

## Retry policy

Retry or repair the figure when any of these occur:

- visible text differs from the allowed labels;
- forbidden helper labels appear;
- decorative art dominates the claim;
- the reader cannot infer the takeaway in 5 seconds;
- arrows or panel order contradict the paper section;
- colors imply a metric ranking that is not supported;
- the figure contains pseudo-text, fake logos, fake charts, or invented numbers.

## Deterministic placeholders

SVG, Mermaid, or table previews may be useful for reproducibility and tests, but they are placeholders/previews unless the user explicitly wants deterministic vector output. For user-facing generated visuals, route through imagegen and keep the prompt plus audit trail.
