# oh my paper demo：多轮科研写作与图像提示词流程

本目录展示 oh my paper 如何把一段研究素材转成完整论文内容、章节级写作解释、可复现流程记录和 Codex imagegen 图像提示词。内容只用于演示系统能力，不声称真实投稿或真实实验结果。

## 输入素材

- `input_material.md`：基于 PPO 论文主题整理的公开知识型输入，不包含私有数据。
- `STRUCTURED_INPUT.yaml`：运行脚本后生成的结构化输入，记录论文类型、证据边界和输出要求。

## 输出内容

- `WORKFLOW_PLAN.md`：多轮写作计划，明确每个章节不能只调用一次。
- `ITERATION_LOG.md`：章节契约、段落计划、批评、修订和中文 rationale。
- `paper.md`：完整论文正文草稿。
- `explain/why_each_section.md`：逐章说明“为什么这么写”。
- `figures/figure_prompts.md`：可交给 Codex imagegen 的图像提示词。
- `figures/IMAGEGEN_PROCESS.md`：生图、保存和审查流程。
- `figures/figure*.svg`：确定性结构预览，不是默认最终生图路径。

## 重要声明

这是 demo，不是实证论文。所有分数和错误类型都是 synthetic placeholders，用来展示论文结构和可解释写作逻辑。真正生成论文图时，应使用 Codex imagegen，并保留 prompt 与 audit。
