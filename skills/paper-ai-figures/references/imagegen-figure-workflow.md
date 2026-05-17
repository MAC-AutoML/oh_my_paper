# Imagegen figure workflow

Use this reference when the user wants Codex-generated paper visuals. The intended path is article content -> figure intent -> scientific image brief -> imagegen prompt -> generated raster image -> caption/audit.

## Workflow

1. Extract the figure's claim from the paper section.
2. Write a figure intent card:
   - supported claim ID;
   - one-sentence takeaway;
   - figure type and layout grammar;
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

Allowed visible labels:
Use only these exact short labels: "<label 1>", "<label 2>", ...
Do not render the internal file name, prompt metadata, style names, title, subtitle, caption, or explanatory sentences inside the image unless explicitly listed here.

Required visual elements:
<boxes, arrows, panels, axes, callouts, data values only if supported>

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; editorial, minimalist, white background, muted slate-blue / teal / gray palette, thin strokes, generous whitespace, flat vector-like raster, no cartoon clipart, no 3D, no glossy gradients.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, tiny footnotes, filenames, style names, or fake citations inside the image.

Negative prompt:
Avoid decorative icons, stock-photo look, over-saturated colors, busy backgrounds, fake logos, watermark, fake axes, unsupported numeric claims, and any text not listed above.

Output audit:
The generated image must make the takeaway obvious in 5 seconds and all visible labels must match the allowed list.
```

## Figure-type patterns

- **Pipeline / method overview:** 4--7 aligned boxes, one arrow direction, optional feedback loop; no more than two nested levels.
- **Score trajectory:** one clean line or stepped path, 3--5 labeled milestones, restrained callouts; no fake confidence intervals.
- **Artifact map:** file/card grid with grouped folders and ownership boundaries; use consistent icon-free cards.
- **Taxonomy / capability hierarchy:** tree or ladder; emphasize hierarchy with position and spacing, not rainbow colors.
- **Comparison matrix:** rows are methods/conditions, columns are criteria; use abstract checkmarks only when grounded.
- **Qualitative panel:** few examples with concise labels; avoid photorealistic claims unless source images are provided.

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
- decorative art dominates the claim;
- the reader cannot infer the takeaway in 5 seconds;
- arrows or panel order contradict the paper section;
- colors imply a metric ranking that is not supported;
- the figure contains pseudo-text, fake logos, fake charts, or invented numbers.

## Deterministic placeholders

SVG, Mermaid, or table previews may be useful for reproducibility and tests, but they are placeholders/previews unless the user explicitly wants deterministic vector output. For user-facing generated visuals, route through imagegen and keep the prompt plus audit trail.
