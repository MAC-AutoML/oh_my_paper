# Multi-round workflow plan / 多轮写作流程规划

本 demo 的目标不是证明 PPO、SAC 或 TD3 的真实性能，而是展示 oh my paper 如何稳定引导 Codex 生成一篇长论文。核心约束：**每个章节都不能只调用一次就结束**。

## 全局流程

1. **输入结构化**：把 `input_material.md` 转成 `STRUCTURED_INPUT.yaml`，明确论文类型、主张、证据边界和图像生成方式。
2. **全局 thesis**：确定论文主线：平均 return 可能高估 policy reliability。
3. **章节契约**：为每个章节写 reader question、section job、claim IDs、证据状态和 caveat。
4. **段落计划**：每段只承担一个 message，并说明它如何连接上下文。
5. **草稿生成**：按章节计划写正文，不允许把 unsupported claim 写成事实。
6. **内部批评**：检查过度主张、证据缺口、段落功能和章节闭环。
7. **修订**：将批评转化为删减、补 caveat、重排段落或增加解释。
8. **图像规划**：从最终正文 claim 提取 figure intent，再生成 imagegen prompt。
9. **解释输出**：用中文说明每章为什么这样写，保证系统可解释。

## 章节级 stop condition

每个章节只有满足以下条件才算完成：

- reader question 已回答；
- claim 有 ID；
- synthetic / proposed / supported 的边界清楚；
- critique 中的阻塞问题已修复或显式标为 limitation；
- 中文 rationale 已写出；
- 如果需要图，已生成 figure intent 和 imagegen prompt。

## 图像生成路径

文章内容先产生 figure intent，再产生 `figures/figure_prompts.md`。真正生成位图时，应调用 Codex `imagegen` skill。当前仓库保存 SVG 仅作为 deterministic preview，不把它作为最终生图路径。
