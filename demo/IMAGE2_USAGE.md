# image2 / imagegen 使用说明

本 demo 已经提供确定性 SVG 图，适合复现和审计。如果你想让图更像顶会论文 overview figure，可以把 `figures/figure_prompts.md` 中的提示词复制给 Codex 的 image2 / imagegen skill。

推荐流程：

1. 先运行确定性 demo：

```bash
uv run python demo/run_demo.py
```

2. 打开提示词：

```bash
cat demo/figures/figure_prompts.md
```

3. 用 image2 / imagegen 生成位图版本。

4. 人工检查图中文字是否准确。如果 AI 位图中文字不清楚，保留 SVG 作为正式可审计版本。

## 为什么这样设计？

- SVG 图可复现，适合 demo 和测试。
- image2 位图更美观，但生成过程天然不保证字节级复现。
- oh my paper 的系统原则是：先保证论文逻辑和证据可审计，再用视觉生成增强表达。
