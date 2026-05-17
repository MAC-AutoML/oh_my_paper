# Workflow overview

## Figure intent

- Figure type: Pipeline / feedback loop
- Reader takeaway: A reliable academic draft emerges from repeated selection, writing, review, revision, figure generation, and packaging rather than from one prompt.
- Required content: Show the full loop: user material -> candidate ideas -> reviewer selection -> citation-aware section writing agents -> reviewer score -> revision until >=85 -> imagegen figures -> LaTeX packaging.
- Evidence boundary: workflow illustration only; do not invent empirical measurements.
- Layout grammar: Use a left-to-right pipeline with a single curved feedback arrow from Review score back to Section agents; place Imagegen figures and LaTeX package as the final two output cards.
- Allowed visible labels: "User material", "Candidate ideas", "Reviewer selection", "Section agents", "Citation check", "Review score", "Revise to 85+", "Imagegen figures", "LaTeX package"

## Codex imagegen prompt

Use case: infographic-diagram
Asset type: academic paper figure

Design brief:
Create a publication-ready Pipeline / feedback loop for a computer science / machine learning paper. Internal asset name: "Workflow overview".

Reader takeaway:
A reliable academic draft emerges from repeated selection, writing, review, revision, figure generation, and packaging rather than from one prompt.

Paper context:
Section-based oh my paper demo for iterative academic writing, citation checking, reviewer scoring, image generation, and LaTeX packaging.

Layout grammar:
Use a left-to-right pipeline with a single curved feedback arrow from Review score back to Section agents; place Imagegen figures and LaTeX package as the final two output cards.
Use strict alignment, consistent margins, balanced whitespace, and a clear reading path. Keep the drawing flat and editorial, not cartoon-like.

Allowed visible labels:
Use only these exact labels: "User material", "Candidate ideas", "Reviewer selection", "Section agents", "Citation check", "Review score", "Revise to 85+", "Imagegen figures", "LaTeX package".
Do not render the internal asset name, style names, explanatory sentences, captions, or any other words inside the image.

Required visual elements:
Show the full loop: user material -> candidate ideas -> reviewer selection -> citation-aware section writing agents -> reviewer score -> revision until >=85 -> imagegen figures -> LaTeX packaging.

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; minimalist editorial diagram; white background; muted slate-blue, teal, and warm gray palette; thin 1.5px-style strokes; simple rounded rectangles; subtle accent color only for the key feedback or threshold; no clipart; no 3D; no glossy gradients; no stock-photo look.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, filenames beyond the allowed labels, fake citations, tiny footnotes, or unsupported numbers inside the image. If a card needs more text than the allowed label, leave the card visually simple rather than inventing text.

Negative prompt:
Avoid fake logos, watermarks, decorative icons, busy background, oversaturated colors, marketing-slide style, cartoon mascots, fake axes, invented metrics, unsupported numeric claims, and any text not listed in the allowed labels.

Retry rule:
If any visible label differs from the allowed list, if pseudo-text appears, if the visual focal point is unclear in 5 seconds, or if it looks like a generic business infographic rather than an academic figure, regenerate or repair before using it.

## Audit checklist

- The takeaway is visible in 5 seconds: A reliable academic draft emerges from repeated selection, writing, review, revision, figure generation, and packaging rather than from one prompt.
- Text labels exactly match the allowed list.
- Layout follows the specified grammar.
- No unsupported empirical claim appears in the image.
- Caption can link the figure to a section claim.
- The result looks like a restrained academic paper figure, not a marketing image.
