"""Structured process artifacts for the deterministic demo."""

from __future__ import annotations

import hashlib
from pathlib import Path

def build_structured_input(material: str) -> str:
    escaped = material.replace("\n", "\n      ")
    return f"""# Stable structured input for the demo. It is generated from input_material.md.
project: Policy-MME demo
target_type: benchmark_evaluation_paper
language: english_paper_with_chinese_explanations
source_material:
  file: demo/input_material.md
  content: |
      {escaped}
constraints:
  - synthetic_numbers_must_be_labeled
  - no_real_empirical_claims_about_ppo_sac_td3
  - each_major_section_requires_multi_round_iteration
  - figure_generation_uses_imagegen_prompts_for_raster_outputs
paper_shape:
  thesis: average_return_can_overestimate_policy_reliability
  capability_levels:
    - optimization_stability
    - robustness_and_generalization
    - decision_faithfulness
  required_outputs:
    - paper.md
    - explain/why_each_section.md
    - WORKFLOW_PLAN.md
    - ITERATION_LOG.md
    - figures/figure_prompts.md
    - figures/IMAGEGEN_PROCESS.md
"""


def build_workflow_plan() -> str:
    return """# Multi-round workflow plan / 多轮写作流程规划

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
"""


def build_iteration_log() -> str:
    return """# Iteration log / 多轮迭代记录

This log is deterministic documentation of the writing process. It describes the rounds that a Codex skill should execute; it is not a transcript of hidden model thoughts.

## Global round

- **Contract:** write a benchmark/evaluation paper, not an algorithm paper.
- **Draft risk:** a one-shot draft may overclaim synthetic numbers as real RL findings.
- **Critique:** require explicit synthetic labels and limitations.
- **Revision:** every result table and figure prompt says demo values are illustrative.

## Abstract

- **Reader question:** What problem, benchmark, evidence, and impact does the paper claim?
- **Paragraph plan:** crisis -> benchmark -> scoring -> synthetic finding -> impact.
- **Critique:** avoid claiming actual PPO weakness.
- **Revision:** state that the synthetic comparison demonstrates reporting structure, not empirical truth.
- **Rationale:** 摘要要压缩完整故事，而不是只宣布“我们做了一个 benchmark”。

## Introduction

- **Reader question:** Why is average return no longer enough?
- **Paragraph plan:** PPO usefulness -> evaluation gap -> mature-field benchmark pattern -> Policy-MME design -> contributions.
- **Critique:** motivation must not sound like attacking PPO itself.
- **Revision:** frame PPO as a trusted baseline whose popularity makes the evaluation issue important.
- **Rationale:** 先承认进步，再指出评测矛盾，读者更容易接受新 benchmark 的必要性。

## Background and Motivation

- **Reader question:** What exactly does average return hide?
- **Paragraph plan:** PPO objective intuition -> scalar metric limitation -> four failure modes.
- **Critique:** failure modes need concrete names.
- **Revision:** add seed fragility, training collapse, perturbation brittleness, shortcut exploitation.
- **Rationale:** 把抽象“不可靠”拆成可检查 failure modes，后文才能评分。

## Benchmark Design

- **Reader question:** How does the benchmark operationalize reliability?
- **Paragraph plan:** principles -> Level 1 -> Level 2 -> Level 3.
- **Critique:** flat checklist would be weaker than hierarchy.
- **Revision:** emphasize that higher levels depend on lower levels.
- **Rationale:** 层级结构让实验分析能讲“错误向上传播”，形成闭环。

## Evaluation Protocol

- **Reader question:** Why is grouped scoring necessary?
- **Paragraph plan:** keep average return -> define group score -> define failure labels.
- **Critique:** formula may look arbitrary.
- **Revision:** explain variance/minimum terms as penalties for fragmented success.
- **Rationale:** 新指标必须解释直觉，否则像是在调分数。

## Dataset and Task Construction

- **Reader question:** What would a real benchmark need to release?
- **Paragraph plan:** task families -> seed protocol -> quality control.
- **Critique:** demo has no real environments.
- **Revision:** explicitly say this is construction logic, not a released suite.
- **Rationale:** benchmark 论文必须展示可执行形态，即使 demo 只演示写法。

## Synthetic Demonstration

- **Reader question:** What does the reporting format reveal?
- **Paragraph plan:** setup -> table -> observation -> ablation-style reporting -> failure labels.
- **Critique:** risk of fabricated empirical result.
- **Revision:** repeat synthetic placeholder boundary and focus on structural interpretation.
- **Rationale:** 让用户看到长文和表格如何写，但不制造假实验。

## Analysis

- **Reader question:** What insight does the benchmark produce beyond scores?
- **Paragraph plan:** metric sensitivity -> hierarchy bottleneck -> ResNet analogy -> Video-MME-v2 analogy.
- **Critique:** analogies could become decorative.
- **Revision:** tie each analogy to a writing function: contradiction and benchmark closure.
- **Rationale:** 好论文不是报分数，而是解释分数背后的机制。

## Figures

- **Reader question:** Which visual reduces reviewer effort?
- **Intent cards:** pipeline overview, score comparison, capability hierarchy.
- **Critique:** code SVG should not replace requested imagegen workflow.
- **Revision:** mark SVG as deterministic preview; provide prompts and imagegen process file.
- **Rationale:** 用户需要 Codex 生图流程，所以系统必须保存 prompt、caption 和 audit，而不是只画 SVG。
"""


def build_figure_prompts() -> str:
    return """# Figure prompts for image2 / imagegen

本 demo 的主图像生成路径是：文章 claim → figure intent → imagegen prompt → Codex imagegen 生成位图 → caption/audit。仓库中的 SVG 只是 deterministic preview，用于复现结构和测试，不是默认的最终生图方式。建议生成后人工核对文字，不要把无法辨认的 AI 文字直接放进论文。

## Figure 1: Pipeline overview

Use case: infographic-diagram
Asset type: academic paper overview figure
Primary request: Create a clean academic workflow diagram titled "Policy-MME Diagnostic Pipeline".
Scene/backdrop: white or very light slate background, flat vector infographic style.
Content: four connected blocks: Input Material, Capability Hierarchy, Grouped Scoring, Paper Output. Capability Hierarchy expands into L1 Optimization Stability, L2 Robustness and Generalization, L3 Decision Faithfulness. Use arrows to show progression from input to scoring to paper output.
Style: top-tier computer science paper overview figure, restrained colors, crisp lines, no decorative icons unless subtle.
Avoid: fake logos, watermark, tiny unreadable text, 3D clutter.

## Figure 2: Synthetic result comparison

Use case: infographic-diagram
Asset type: academic paper result figure
Primary request: Create a horizontal bar chart titled "Synthetic Policy-MME Score Comparison".
Data: PPO 52.4, SAC 58.2, TD3 49.7, Oracle/Human reference 88.9.
Annotation: Add a callout saying "Average return can hide robustness and faithfulness failures".
Style: clean vector chart, publication-ready, high contrast, minimal grid.
Avoid: implying these are real empirical numbers; include small note "demo synthetic values".

## Figure 3: Capability hierarchy

Use case: infographic-diagram
Asset type: academic paper methodology figure
Primary request: Create a three-level pyramid titled "Policy-MME Three-Level Capability Hierarchy".
Content: bottom layer Level 1 Optimization Stability, middle layer Level 2 Robustness and Generalization, top layer Level 3 Decision Faithfulness. Add arrows or small notes showing lower-level failures propagate upward.
Style: clean academic vector-like raster, restrained blue/green/amber palette, large readable labels.
Avoid: decorative 3D pyramid, fake data, unreadable tiny text, unsupported claims.
"""


def build_imagegen_process() -> str:
    return """# Imagegen process / Codex 生图流程

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
"""


def build_process_log(material: str) -> str:
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"""# Demo process log / 可复现过程记录

## 生成方式

Deterministic local generation. This log intentionally does not include wall-clock time so repeated runs can produce stable content.

## 输入

- 文件：`demo/input_material.md`
- SHA256：`{digest}`
- 主题：PPO 与强化学习评测
- 输入类型：公开知识型素材 + 用户指定的 demo 任务

## 操作步骤

1. 读取 `input_material.md`。
2. 识别论文类型：benchmark / evaluation paper。
3. 提取核心冲突：average return 可能高估真实 policy reliability。
4. 构造论文主张：Policy-MME 用层级能力和组级评分诊断 PPO 类算法。
5. 按章节执行契约、段落计划、草稿、批评、修订和 rationale 的多轮流程。
6. 生成 `paper.md` 的长文正文。
7. 生成 `explain/why_each_section.md`，逐章解释写作理由。
8. 生成 `WORKFLOW_PLAN.md` 和 `ITERATION_LOG.md`，记录稳定可复现的流程。
9. 从正文 claim 生成 `figures/figure_prompts.md` 和 `figures/IMAGEGEN_PROCESS.md`，供 Codex imagegen 生成位图。
10. 生成 SVG preview，仅作为确定性结构预览。
11. 写出 `MANIFEST.md`，记录所有输出文件哈希。

## 可复现命令

```bash
uv run python demo/run_demo.py
```

如果要验证可复现性，可以删除以下文件后重新运行：

```bash
rm -f demo/paper.md demo/PROCESS_LOG.md demo/MANIFEST.md
rm -f demo/explain/why_each_section.md
rm -f demo/figures/figure1_pipeline.svg demo/figures/figure2_results.svg demo/figures/figure_prompts.md
uv run python demo/run_demo.py
```

## 诚信边界

- 本 demo 不调用真实 RL 环境。
- 所有实验数值都是 synthetic placeholders。
- 图 2 是演示图，不是实验结果证明。
- SVG 是 deterministic preview，不是默认最终生图路径。
- 真正生图应使用 Codex imagegen，并保留 prompt 与 audit。
- 系统必须解释为什么这么写，不能只输出漂亮正文。
"""


def build_manifest(outputs: dict[Path, str], root: Path) -> str:
    rows = ["# Demo manifest", "", "| File | SHA256 |", "| --- | --- |"]
    for path in sorted(outputs):
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else hashlib.sha256(outputs[path].encode("utf-8")).hexdigest()
        rows.append(f"| `{path.relative_to(root)}` | `{digest}` |")
    return "\n".join(rows) + "\n"
