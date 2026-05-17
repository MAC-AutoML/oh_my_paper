# Imagegen figure workflow

Use this reference when the user wants Codex-generated paper visuals. The intended path is article content -> figure intent -> imagegen prompt -> generated raster image -> caption/audit.

## Workflow

1. Extract the figure's claim from the paper section.
2. Write a figure intent card:
   - supported claim ID;
   - one-sentence takeaway;
   - required visual elements;
   - exact text labels if any;
   - evidence or data source;
   - risks.
3. Convert the intent card into an `imagegen` prompt.
4. Use Codex `imagegen` skill for bitmap/raster generation when the environment exposes image generation.
5. Save generated project-bound assets under a workspace path such as `paper/figures/generated/` or `demo/figures/generated/`.
6. Audit text accuracy, visual hierarchy, evidence alignment, and caption consistency.
7. If image generation is unavailable, save the prompt and mark generation status as `not_run`; do not pretend the image was generated.

## Prompt schema for academic figures

```text
Use case: infographic-diagram
Asset type: academic paper figure
Primary request: <figure title and one-sentence purpose>
Paper context: <brief claim and section>
Required content: <boxes, arrows, charts, labels, data values if supported>
Style: top-tier computer science paper figure, clean vector-like raster, restrained colors, high readability
Text policy: use only these exact labels: <labels>; keep text large and legible
Avoid: fake logos, watermark, decorative clutter, unreadable tiny text, unsupported numbers
Output audit: generated image must make the takeaway obvious in 5 seconds
```

## Caption/audit pattern

```markdown
Caption: What is shown -> comparison/mechanism -> conclusion -> caveat.
Audit:
- Claim link:
- Evidence source:
- Text readable:
- No unsupported values:
- If generated image has text errors, regenerate or replace text in a deterministic editor.
```

## Deterministic placeholders

SVG, Mermaid, or table previews may be useful for reproducibility and tests, but they are placeholders/previews unless the user explicitly wants deterministic vector output. For user-facing generated visuals, route through imagegen and keep the prompt plus audit trail.
