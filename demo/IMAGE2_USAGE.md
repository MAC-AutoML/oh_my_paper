# Codex imagegen 使用说明

本 demo 不把代码生成 SVG 当作默认最终图像。SVG 只是稳定预览；真正的 AI 生图流程是使用 Codex `imagegen` skill。

## 推荐流程

1. 先运行确定性 demo：

```bash
uv run python demo/run_demo.py
```

2. 打开提示词：

```bash
cat demo/figures/figure_prompts.md
```

3. 对每张图调用 Codex `imagegen` skill。每个 prompt 已包含：用途、论文 claim、必要元素、风格、避免事项和审查重点。

4. 将选中的生成图保存到：

```text
demo/figures/generated/figure1_pipeline.png
demo/figures/generated/figure2_results.png
demo/figures/generated/figure3_hierarchy.png
```

5. 按 `demo/figures/IMAGEGEN_PROCESS.md` 做 audit：文字是否正确、是否有 unsupported number、5 秒内是否能看出 takeaway、caption 是否匹配正文。

## 为什么仍然保留 SVG？

- SVG 可复现，适合 demo、测试和结构预览。
- imagegen 位图更像论文插图，但每次生成不保证字节级一致。
- oh my paper 的原则是：稳定记录输入、prompt、audit 和证据边界；视觉生成用于增强表达，不能替代可审计写作流程。
