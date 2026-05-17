# Imagegen usage

本 demo 同时提交 imagegen prompt 和已生成的示例位图。真实运行时：

1. 打开 `demo/figures/fig_01_workflow_prompt.md` 等文件。
2. 用 Codex `imagegen` skill 逐张生成 raster image。
3. 保存到 `demo/figures/generated/fig_01_workflow.jpg` 等路径。
4. 按每个 prompt 里的 audit checklist 检查。

## 已生成图像 / Generated figures

本 demo 现在已经包含实际生成图像：

- `demo/figures/generated/fig_01_workflow.jpg`
- `demo/figures/generated/fig_02_score_loop.jpg`
- `demo/figures/generated/fig_03_section_artifacts.jpg`

生成模型：`gemini-3.1-flash-image-preview`。三张图使用结构化科研图 brief 重生成；重点是短标签、严格布局语法、细线箭头、留白、muted palette、无伪文本和审稿人可读性。
