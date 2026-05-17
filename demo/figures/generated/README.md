# Generated demo figures

These raster figures were generated from the prompt cards in `demo/figures/`.

| Figure | Prompt card | Model | Notes |
| --- | --- | --- | --- |
| `fig_01_workflow.jpg` | `../fig_01_workflow_prompt.md` | `gemini-3.1-flash-image-preview` | Workflow loop overview. |
| `fig_02_score_loop.jpg` | `../fig_02_score_loop_prompt.md` | `gemini-3.1-flash-image-preview` | Reviewer score trajectory. |
| `fig_03_section_artifacts.jpg` | `../fig_03_section_artifacts_prompt.md` | `gemini-3.1-flash-image-preview` | Regenerated after visual audit to avoid pseudo-text. |

The API response was served through an OpenAI-compatible relay using the Nano Banana 2 image model. If regeneration fails, retry up to three times and prefer shorter visible labels; image models often hallucinate long file names or dense in-figure text.
