# 如何稳定复现这个 demo

## 1. 输入是什么？

唯一输入文件是：

```text
demo/input_material.md
```

它包含三类信息：

1. PPO 的基本背景：clipped surrogate objective、稳定训练、常见使用场景。
2. 评测问题：平均 return 可能掩盖 seed variance、collapse、reward hacking 和过拟合。
3. 目标论文形态：构造一个 benchmark / evaluation paper，而不是提出新算法。

## 2. 系统怎么操作？

本 demo 使用确定性脚本：

```bash
uv run python demo/run_demo.py
```

脚本会执行以下步骤：

1. 读取输入素材。
2. 判断论文类型是 benchmark / evaluation paper。
3. 提取核心矛盾：平均 return 高，不代表 agent 可靠。
4. 生成论文主线：现有评测不足 → Policy-MME → 三层能力 → 组级评分 → synthetic demo → 局限。
5. 写出完整论文内容 `paper.md`。
6. 写出中文解释 `explain/why_each_section.md`。
7. 生成两张确定性 SVG 图。
8. 生成 image2 / imagegen 可用提示词。
9. 写出过程日志和 manifest。

## 3. 输出有哪些？

| 输出 | 作用 |
| --- | --- |
| `paper.md` | 论文正文内容。 |
| `explain/why_each_section.md` | 每章为什么这么写的中文解释。 |
| `figures/figure1_pipeline.svg` | 评测流程图。 |
| `figures/figure2_results.svg` | synthetic 结果对比图。 |
| `figures/figure_prompts.md` | 给 image2 / imagegen 的位图生成提示词。 |
| `PROCESS_LOG.md` | 输入哈希、操作步骤、诚信边界。 |
| `MANIFEST.md` | 输出文件哈希。 |

## 4. 如何从零复现？

```bash
rm -f demo/paper.md demo/PROCESS_LOG.md demo/MANIFEST.md
rm -f demo/explain/why_each_section.md
rm -f demo/figures/figure1_pipeline.svg demo/figures/figure2_results.svg demo/figures/figure_prompts.md
uv run python demo/run_demo.py
```

然后检查：

```bash
ls demo
ls demo/explain demo/figures
```

如果要检查内容稳定性，连续运行两次并比较 git diff：

```bash
uv run python demo/run_demo.py
git diff -- demo
uv run python demo/run_demo.py
git diff -- demo
```

在输入文件不变的情况下，第二次运行不应该产生新的 diff。

## 5. 为什么没有直接把 AI 生成位图作为唯一图？

为了稳定可复现，本 demo 默认提交 SVG 图。image2 / imagegen 适合生成更漂亮的位图，但每次生成可能不完全一致，所以本目录同时提供：

- 可复现 SVG：用于确定性 demo。
- image2 提示词：用于需要视觉美化时生成位图。

这符合 oh my paper 的设计原则：内容和证据要可解释，视觉资产可以增强表达，但不能替代可审计过程。
