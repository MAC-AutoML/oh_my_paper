# Section artifact layout

## Figure intent

- Figure type: Artifact map / file grid
- Reader takeaway: The workflow is auditable because every section, figure prompt, explanation, reference file, and optional package workspace is saved as a separate artifact.
- Required content: Show grouped artifact families only: section cards, figure prompt cards, explanation cards, a references card, and a LaTeX workspace card. Use only the allowed labels, not full filenames.
- Evidence boundary: workflow illustration only; do not invent empirical measurements.
- Layout grammar: Use a 2x3 grouped file-card grid: sections on the left, figures in the middle, explanations on the right, references and LaTeX workspace as bottom support cards.
- Allowed visible labels: "sections/", "01 Abstract", "02 Introduction", "03 Related Work", "figures/", "fig prompts", "explain/", "why files", "references.bib", "latex workspace"

## Codex imagegen prompt

Use case: infographic-diagram
Asset type: academic paper figure

Design brief:
Create a publication-ready Artifact map / file grid for a computer science / machine learning paper. Internal asset name: "Section artifact layout".

Reader takeaway:
The workflow is auditable because every section, figure prompt, explanation, reference file, and optional package workspace is saved as a separate artifact.

Paper context:
Section-based oh my paper demo for iterative academic writing, citation checking, reviewer scoring, image generation, and LaTeX packaging.

Layout grammar:
Use a 2x3 grouped file-card grid: sections on the left, figures in the middle, explanations on the right, references and LaTeX workspace as bottom support cards.
Use strict alignment, consistent margins, balanced whitespace, and a clear reading path. Keep the drawing flat and editorial, not cartoon-like.

Allowed visible labels:
Use only these exact labels: "sections/", "01 Abstract", "02 Introduction", "03 Related Work", "figures/", "fig prompts", "explain/", "why files", "references.bib", "latex workspace".
Do not render the internal asset name, style names, explanatory sentences, captions, or any other words inside the image.

Required visual elements:
Show grouped artifact families only: section cards, figure prompt cards, explanation cards, a references card, and a LaTeX workspace card. Use only the allowed labels, not full filenames.

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; minimalist editorial diagram; white background; muted slate-blue, teal, and warm gray palette; thin 1.5px-style strokes; simple rounded rectangles; subtle accent color only for the key feedback or threshold; no clipart; no 3D; no glossy gradients; no stock-photo look.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, filenames beyond the allowed labels, fake citations, tiny footnotes, or unsupported numbers inside the image. If a card needs more text than the allowed label, leave the card visually simple rather than inventing text.

Negative prompt:
Avoid fake logos, watermarks, decorative icons, busy background, oversaturated colors, marketing-slide style, cartoon mascots, fake axes, invented metrics, unsupported numeric claims, and any text not listed in the allowed labels.

Retry rule:
If any visible label differs from the allowed list, if pseudo-text appears, if the visual focal point is unclear in 5 seconds, or if it looks like a generic business infographic rather than an academic figure, regenerate or repair before using it.

## Audit checklist

- The takeaway is visible in 5 seconds: The workflow is auditable because every section, figure prompt, explanation, reference file, and optional package workspace is saved as a separate artifact.
- Text labels exactly match the allowed list.
- Layout follows the specified grammar.
- No unsupported empirical claim appears in the image.
- Caption can link the figure to a section claim.
- The result looks like a restrained academic paper figure, not a marketing image.
