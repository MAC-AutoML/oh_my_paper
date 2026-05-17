# oh my paper demo

这个 demo 展示新的目录形态：章节文件、图像提示词文件、解释文件和参考文献分离。

- `sections/01_sec_abstract.md`：章节正文。
- `sections/09_sec_references.md`：15–20 条代表性参考文献说明。
- `figures/fig_01_workflow_prompt.md`：图像生成提示词。
- `figures/generated/*.jpg`：已由 `gemini-3.1-flash-image-preview` 生成的 demo 图。
- `explain/01_why_abstract.md`：为什么这样写。
- `MODEL_SELECTION_PROTOCOL.md`：如何用配置的 reviewer/Gemini-compatible 模型选择论文方向。
- `REVIEW_LOOP_PROTOCOL.md`：如何审稿返修到 85 分。

所有内容是离线可复现 demo。真实运行时应调用配置的 LLM/API、Codex imagegen 和 `paper-ai-latex`。
