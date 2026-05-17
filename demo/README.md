# oh my paper demo：从输入素材到可解释论文内容

本目录展示 oh my paper 如何把一段研究素材转成完整论文内容、章节级写作解释和图示资产。内容只用于演示系统能力，不声称真实投稿或真实实验结果。

## 输入素材

- `input_material.md`：基于 PPO 论文主题整理的公开知识型输入，不包含私有数据。

## 输出内容

- `paper.md`：完整论文正文草稿。
- `explain/why_each_section.md`：逐章说明“为什么这么写”。
- `figures/figure1_pipeline.svg`：方法/评测流水线图。
- `figures/figure2_results.svg`：模型与人类表现差距示意图。
- `figures/figure_prompts.md`：可交给 image2 / imagegen 的图像提示词。

## 重要声明

这是 demo，不是实证论文。所有分数和错误类型都是 synthetic placeholders，用来展示论文结构和可解释写作逻辑。
