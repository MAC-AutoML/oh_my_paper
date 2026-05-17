# 为什么这样写：Workflow overview

Workflow overview 的作用是降低读者理解流程的成本。它先由正文 claim 生成 figure intent，再变成 Codex imagegen prompt；demo 不用代码 SVG 冒充最终 AI 生图。

## 迭代说明

- 第一轮：确定本节回答的 reader question。
- 第二轮：检查是否有 unsupported claim。
- 第三轮：把批评转成修订或 caveat。
- 通过条件：本节不把 demo/synthetic 内容写成真实实证结论。
