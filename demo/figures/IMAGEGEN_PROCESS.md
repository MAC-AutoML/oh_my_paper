# Imagegen process / Codex 生图流程

本文件说明如何把正文内容转成 Codex `imagegen` 可执行的生图任务。当前环境如果没有直接暴露图像生成工具，就保留 prompt 和状态；不要声称图片已经生成。

## 输入

- 论文正文：`demo/paper.md`
- 图像意图和提示词：`demo/figures/figure_prompts.md`
- 图像用途：论文 overview / result / capability hierarchy

## 推荐操作

1. 打开 `demo/figures/figure_prompts.md`。
2. 对每个 figure prompt 调用 Codex `imagegen` skill。
3. 若生成结果保存在 Codex 默认生成目录，将选中的位图复制到：

```text
demo/figures/generated/figure1_pipeline.png
demo/figures/generated/figure2_results.png
demo/figures/generated/figure3_hierarchy.png
```

4. 对每张图执行 audit：
   - 标题和标签是否准确；
   - 是否包含 unsupported number；
   - 是否 5 秒内能看出 takeaway；
   - caption 是否与正文 claim 对齐；
   - 若文字错误，重新生成或用确定性编辑方式修正。

## 当前状态

```yaml
imagegen_status: not_run_in_this_deterministic_demo
reason: repository demo must be reproducible without assuming image generation tool availability
svg_preview_status: available_as_structure_preview_only
```

## 重要边界

SVG preview 用来稳定展示结构；真正面向用户的 AI 生图，应以 imagegen 生成的 raster asset、prompt 和 audit 记录为准。
