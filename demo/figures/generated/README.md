# Generated demo figures

These raster figures were generated from the prompt cards in `demo/figures/`.

| Figure | Prompt card | Model | Notes |
| --- | --- | --- | --- |
| `fig_01_workflow.jpg` | `../fig_01_workflow_prompt.md` | `gemini-3.1-flash-image-preview` | Minimalist workflow loop generated from a structured scientific image brief. |
| `fig_02_score_loop.jpg` | `../fig_02_score_loop_prompt.md` | `gemini-3.1-flash-image-preview` | Sparse score trajectory generated from exact-label and threshold constraints. |
| `fig_03_section_artifacts.jpg` | `../fig_03_section_artifacts_prompt.md` | `gemini-3.1-flash-image-preview` | Restrained artifact-card layout generated with title/text suppression rules. |

The API response was served through an OpenAI-compatible relay using the configured Gemini image model. If regeneration fails, retry up to three times and prefer shorter visible labels, explicit layout grammar, thin strokes, generous whitespace, and muted palettes; image models often hallucinate long file names or dense in-figure text.
