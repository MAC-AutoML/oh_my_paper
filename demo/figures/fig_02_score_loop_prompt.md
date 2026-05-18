# Reviewer score loop

## Figure intent

- Figure type: Score trajectory with feedback packets
- Reader takeaway: The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.
- Required content: Show a revision trajectory from 72 to 81 to 87, with critique packets and citation gaps feeding a repair loop until the draft crosses the accept threshold.
- Evidence boundary: workflow illustration only; do not invent empirical measurements.
- Layout grammar: Create a CCF-A evaluation diagnostic figure with two labeled subpanels. Panel A: a clean stepped score trajectory from Draft v1 to Draft v3 with score markers 72, 81, 87 and an Accept threshold line. Panel B: a repair lane with Critique packet and Citation gaps feeding upward into the next draft; label the lane Repair loop. Do not add internal icon text, micro badges, or any extra words inside the packet cards.
- Layer stack: background grid -> grouped panels -> mechanism arrows -> evidence/revision callouts -> exact short labels.
- Allowed visible labels: "A", "B", "Draft v1", "72", "Critique packet", "Draft v2", "81", "Citation gaps", "Draft v3", "87", "Accept threshold", "Repair loop"

## Codex imagegen prompt

Use case: infographic-diagram
Asset type: academic paper figure

Design brief:
Create a publication-ready Score trajectory with feedback packets for a computer science / machine learning paper. Do not render a title inside the image; the paper caption will provide the title outside the bitmap.

Reader takeaway:
The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.

Paper context:
Section-based oh my paper demo for iterative academic writing, citation checking, reviewer scoring, image generation, and LaTeX packaging.

Style reference:
CCF-A/CVPR/NeurIPS benchmark Figure 1 style: information-dense but organized; left or top panels define structure, right or lower panels show diagnostic outputs or evidence artifacts. Use restrained pastel category colors, thin separators, small panel letters, compact evidence cards, and caption-ready composition. Avoid cartoon overview art.

Paper-content extraction:
- Entities: user material, candidate directions, writing agents, citation checks, reviewer score, revision loop, figure prompts, package artifacts.
- Relationships: evidence flows forward; critique and citation gaps flow backward into revision; generated figures and package outputs must remain auditable.
- Evidence status: workflow demonstration, not empirical experiment.
- Failure mode to avoid: a one-shot fluent draft that hides unsupported claims, fake citations, or unreviewed figures.

Layout grammar:
Create a CCF-A evaluation diagnostic figure with two labeled subpanels. Panel A: a clean stepped score trajectory from Draft v1 to Draft v3 with score markers 72, 81, 87 and an Accept threshold line. Panel B: a repair lane with Critique packet and Citation gaps feeding upward into the next draft; label the lane Repair loop. Do not add internal icon text, micro badges, or any extra words inside the packet cards.
Use strict alignment, consistent margins, balanced whitespace, grouped panels, and a clear reading path. Keep the drawing flat and editorial, not cartoon-like.

Layer stack:
1. Background: clean white or very light gray grid, no texture.
2. Major panels: grouped lanes or columns that carry the scientific story.
3. Mechanism flow: thin arrows and brackets showing dependency and feedback.
4. Evidence callouts: compact score, threshold, repair, or audit badges only when listed.
5. Text labels: exact short labels from the allowed list only.

Allowed visible labels:
Use only these exact labels: "A", "B", "Draft v1", "72", "Critique packet", "Draft v2", "81", "Citation gaps", "Draft v3", "87", "Accept threshold", "Repair loop".
Do not render the internal asset name, style names, explanatory sentences, captions, or any other words inside the image.
Forbidden visible labels:
Do not render these common hallucinated labels unless they are in the allowed list: "score", "audit", "overview", "workflow", "caption", "figure", "foundation", "evidence", "prompt", "support", "tax", "hair", "Figure 1", "academic paper", "publication-ready", "CCF-A", "CVPR", "NeurIPS".

Required visual elements:
Show a revision trajectory from 72 to 81 to 87, with critique packets and citation gaps feeding a repair loop until the draft crosses the accept threshold.

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; elegant editorial scientific schematic; white background; muted slate-blue, teal, warm gray, and one amber accent for revision/warning; thin 1.5px-style strokes; simple rounded rectangles; layered panel composition; small-multiple rhythm; generous whitespace; no clipart; no 3D; no glossy gradients; no stock-photo look.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, filenames beyond the allowed labels, fake citations, tiny footnotes, or unsupported numbers inside the image. Do not add helper words such as score, audit, overview, workflow, caption, figure, foundation, evidence, prompt, support, tax, hair, Figure 1, academic paper, publication-ready, CCF-A, CVPR, NeurIPS unless they appear in the allowed-label list. If a card needs more text than the allowed label, leave the card visually simple rather than inventing text.
Absolutely no caption, footer paragraph, explanatory sentence, or auto-generated figure description inside the image. Do not reserve a caption/footer band; crop the canvas to the figure content with balanced margins.
Layout words in the prompt are instructions only, not visible text.

Negative prompt:
Avoid fake logos, watermarks, decorative icons, busy background, oversaturated colors, marketing-slide style, cartoon mascots, comic-book style, isometric app illustration, fake axes, invented metrics, unsupported numeric claims, micro badges with text, thumbnail pseudo-text, and any text not listed in the allowed labels.

Retry rule:
If any visible label differs from the allowed list, if pseudo-text appears, if the visual focal point is unclear in 5 seconds, or if it looks like a generic business infographic rather than an academic figure, regenerate or repair before using it.

## Audit checklist

- The takeaway is visible in 5 seconds: The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.
- Text labels exactly match the allowed list.
- No forbidden helper label appears.
- Layout follows the specified grammar.
- No unsupported empirical claim appears in the image.
- Caption can link the figure to a section claim.
- The result looks like a restrained academic paper figure, not a marketing image.
