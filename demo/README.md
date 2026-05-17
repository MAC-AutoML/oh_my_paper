# oh my paper demo

这个 demo 展示新的目录形态：章节文件、图像提示词文件和解释文件分离。

- `sections/01_sec_abstract.md`：章节正文。
- `figures/fig_01_workflow_prompt.md`：图像生成提示词。
- `explain/01_why_abstract.md`：为什么这样写。
- `MODEL_SELECTION_PROTOCOL.md`：如何用配置的 reviewer/Gemini-compatible 模型选择论文方向。
- `REVIEW_LOOP_PROTOCOL.md`：如何审稿返修到 85 分。

所有内容是离线可复现 demo。真实运行时应调用配置的 LLM/API 和 Codex imagegen。
