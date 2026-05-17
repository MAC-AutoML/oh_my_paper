# Reviewer score loop

## Figure intent

- Figure type: Score trajectory with feedback packets
- Reader takeaway: The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.
- Required content: Show a revision trajectory from 72 to 81 to 87, with critique packets feeding back to writing agents and citation gaps tracked separately.
- Evidence boundary: workflow illustration only; do not invent empirical measurements.
- Layout grammar: Use a clean stepped trajectory from left to right with three draft cards and three score markers; put critique and citation-gap packets as small callouts feeding into the next draft.
- Allowed visible labels: "Draft v1", "72", "Critique packet", "Draft v2", "81", "Citation gaps", "Draft v3", "87", "Accept threshold"

## Codex imagegen prompt

Use case: infographic-diagram
Asset type: academic paper figure

Design brief:
Create a publication-ready Score trajectory with feedback packets for a computer science / machine learning paper. Internal asset name: "Reviewer score loop".

Reader takeaway:
The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.

Paper context:
Section-based oh my paper demo for iterative academic writing, citation checking, reviewer scoring, image generation, and LaTeX packaging.

Layout grammar:
Use a clean stepped trajectory from left to right with three draft cards and three score markers; put critique and citation-gap packets as small callouts feeding into the next draft.
Use strict alignment, consistent margins, balanced whitespace, and a clear reading path. Keep the drawing flat and editorial, not cartoon-like.

Allowed visible labels:
Use only these exact labels: "Draft v1", "72", "Critique packet", "Draft v2", "81", "Citation gaps", "Draft v3", "87", "Accept threshold".
Do not render the internal asset name, style names, explanatory sentences, captions, or any other words inside the image.

Required visual elements:
Show a revision trajectory from 72 to 81 to 87, with critique packets feeding back to writing agents and citation gaps tracked separately.

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; minimalist editorial diagram; white background; muted slate-blue, teal, and warm gray palette; thin 1.5px-style strokes; simple rounded rectangles; subtle accent color only for the key feedback or threshold; no clipart; no 3D; no glossy gradients; no stock-photo look.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, filenames beyond the allowed labels, fake citations, tiny footnotes, or unsupported numbers inside the image. If a card needs more text than the allowed label, leave the card visually simple rather than inventing text.

Negative prompt:
Avoid fake logos, watermarks, decorative icons, busy background, oversaturated colors, marketing-slide style, cartoon mascots, fake axes, invented metrics, unsupported numeric claims, and any text not listed in the allowed labels.

Retry rule:
If any visible label differs from the allowed list, if pseudo-text appears, if the visual focal point is unclear in 5 seconds, or if it looks like a generic business infographic rather than an academic figure, regenerate or repair before using it.

## Audit checklist

- The takeaway is visible in 5 seconds: The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.
- Text labels exactly match the allowed list.
- Layout follows the specified grammar.
- No unsupported empirical claim appears in the image.
- Caption can link the figure to a section claim.
- The result looks like a restrained academic paper figure, not a marketing image.
