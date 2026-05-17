# 如何稳定复现这个 demo

## 1. 输入是什么？

主输入文件是：

```text
demo/input_material.md
```

它包含三类信息：

1. PPO 的基本背景：clipped surrogate objective、稳定训练、常见使用场景。
2. 评测问题：平均 return 可能掩盖 seed variance、collapse、reward hacking 和过拟合。
3. 目标论文形态：构造一个 benchmark / evaluation paper，而不是提出新算法。

运行后会派生出结构化输入：

```text
demo/STRUCTURED_INPUT.yaml
```

这个文件明确记录论文类型、证据边界、章节输出和 imagegen 图像路径。

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
5. 为长文生成 `WORKFLOW_PLAN.md`，规定每章不能一次性生成。
6. 为每章记录契约、段落计划、草稿风险、批评、修订和中文 rationale 到 `ITERATION_LOG.md`。
7. 写出完整论文内容 `paper.md`。
8. 写出中文解释 `explain/why_each_section.md`。
9. 从正文 claim 生成 imagegen 提示词和生图流程说明。
10. 生成 SVG preview，仅用于确定性结构预览。
11. 写出过程日志和 manifest。

## 3. 输出有哪些？

| 输出 | 作用 |
| --- | --- |
| `STRUCTURED_INPUT.yaml` | 记录稳定结构化输入。 |
| `WORKFLOW_PLAN.md` | 说明多轮写作流程和 stop condition。 |
| `ITERATION_LOG.md` | 记录章节级契约、批评、修订和中文 rationale。 |
| `paper.md` | 论文正文内容。 |
| `explain/why_each_section.md` | 每章为什么这么写的中文解释。 |
| `figures/figure_prompts.md` | 给 Codex imagegen 的位图生成提示词。 |
| `figures/IMAGEGEN_PROCESS.md` | 如何调用 imagegen、保存图片和审查图片。 |
| `figures/figure*.svg` | 确定性结构预览，不是默认最终生图路径。 |
| `PROCESS_LOG.md` | 输入哈希、操作步骤、诚信边界。 |
| `MANIFEST.md` | 输出文件哈希。 |

## 4. 如何从零复现？

```bash
rm -f demo/paper.md demo/PROCESS_LOG.md demo/MANIFEST.md
rm -f demo/STRUCTURED_INPUT.yaml demo/WORKFLOW_PLAN.md demo/ITERATION_LOG.md
rm -f demo/explain/why_each_section.md
rm -f demo/figures/figure1_pipeline.svg demo/figures/figure2_results.svg demo/figures/figure3_hierarchy.svg
rm -f demo/figures/figure_prompts.md demo/figures/IMAGEGEN_PROCESS.md
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

## 5. 图像如何生成？

本 demo 的主图像路径是：

```text
paper.md / claim → figure intent → figures/figure_prompts.md → Codex imagegen → generated PNG → caption/audit
```

仓库里的 SVG 是 deterministic preview，用于复现结构和测试。真正需要 AI 生成论文图时，请按 `figures/IMAGEGEN_PROCESS.md` 调用 Codex `imagegen` skill，并把选中的位图保存到 `demo/figures/generated/`。
