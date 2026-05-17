"""Deterministic oh my paper demo generator.

Run with:
    uv run python demo/run_demo.py

The script intentionally uses only stdlib and synthetic numbers so the demo is
stable, explainable, and safe to commit.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input_material.md"
PAPER = ROOT / "paper.md"
EXPLAIN_DIR = ROOT / "explain"
FIG_DIR = ROOT / "figures"
PROCESS = ROOT / "PROCESS_LOG.md"
MANIFEST = ROOT / "MANIFEST.md"


def main() -> int:
    material = INPUT.read_text(encoding="utf-8")
    EXPLAIN_DIR.mkdir(exist_ok=True)
    FIG_DIR.mkdir(exist_ok=True)
    outputs = {
        PAPER: build_paper(material),
        EXPLAIN_DIR / "why_each_section.md": build_explain(),
        FIG_DIR / "figure1_pipeline.svg": figure_pipeline(),
        FIG_DIR / "figure2_results.svg": figure_results(),
        FIG_DIR / "figure_prompts.md": build_figure_prompts(),
        PROCESS: build_process_log(material),
    }
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    MANIFEST.write_text(build_manifest(outputs), encoding="utf-8")
    print(f"Generated demo outputs under {ROOT}")
    return 0


def build_paper(material: str) -> str:
    thesis = (
        "现有强化学习评测若只报告平均 return，容易高估 agent 的真实可靠性；"
        "Policy-MME 通过层级能力、扰动压力测试和一致性评分揭示 PPO 类算法在稳定性、鲁棒性和决策忠实性上的瓶颈。"
    )
    return f"""# Policy-MME: A Diagnostic Benchmark for Robust and Faithful Policy Optimization

> Demo note: this paper is generated from `demo/input_material.md`. All numerical results are synthetic placeholders for demonstrating the oh my paper workflow; they are not empirical claims.

## Abstract

Recent reinforcement learning agents achieve strong average returns on standard control benchmarks, yet these scores often hide brittle optimization, seed-level instability, and reward-specific shortcuts. To address this evaluation gap, we introduce **Policy-MME**, a diagnostic benchmark for policy optimization methods. Policy-MME decomposes agent capability into three progressively harder levels: optimization stability, robustness and generalization, and decision faithfulness. Unlike conventional average-return reporting, the benchmark uses grouped non-linear scoring that penalizes unstable seeds, inconsistent perturbation behavior, and unsupported decision rationales. Built around auditable traces, fixed perturbation protocols, and explicit failure labels, Policy-MME is designed to make failure modes visible rather than merely rank algorithms. In a synthetic demonstration comparing PPO, SAC, TD3, and an oracle policy, PPO obtains competitive average returns but loses substantial score under group-level robustness evaluation. The analysis suggests that reliable policy optimization requires not only high peak performance, but also stable learning dynamics, perturbation robustness, and faithful state-dependent decisions.

## 1. Introduction

Policy-gradient algorithms such as Proximal Policy Optimization (PPO) have become default baselines for continuous control, game-like environments, robotics, and RLHF-style optimization. Their appeal is clear: PPO is comparatively simple to implement, clips destructive policy updates, and often works well across a broad range of tasks. However, this practical success has also made PPO a common reference point in papers where benchmark tables emphasize mean return over deeper reliability properties.

The problem is that average return is not the same as trustworthy policy learning. A method may achieve a high mean by succeeding on easy seeds, collapsing on harder seeds, exploiting reward artifacts, or overfitting environment-specific dynamics. When evaluation focuses on a single scalar, the leaderboard can look saturated even while agents remain fragile under small distribution shifts.

This paper proposes **Policy-MME**, a diagnostic benchmark designed around the following thesis: **{thesis}** The benchmark is not intended to replace environment suites; instead, it wraps existing tasks with capability levels, perturbation protocols, and group-level scoring so that evaluation reflects robustness and faithfulness rather than isolated success.

Our contributions are threefold. First, we define a three-level capability hierarchy for policy optimization evaluation. Second, we introduce grouped non-linear scoring that downweights fragmented success and unstable seed-level behavior. Third, we provide a synthetic demonstration showing how PPO can look strong under average return while appearing more limited under diagnostic scoring.

## 2. Related Work

PPO introduced a clipped surrogate objective to constrain policy updates and improve training stability without the complexity of second-order trust-region methods. This made it a widely used baseline in reinforcement learning and a practical reference algorithm for many applied systems.

Benchmarking in reinforcement learning has traditionally emphasized environment returns, sample efficiency, and comparisons across standard suites. These metrics are useful but incomplete. A method can be sample efficient on nominal environments while remaining sensitive to reward noise, observation corruption, dynamics shifts, or seed variance.

Recent discussions of reliable evaluation increasingly emphasize robustness, reproducibility, and failure analysis. Policy-MME follows this line: it treats performance as a capability profile, not a single number. The benchmark asks whether an algorithm learns stably, generalizes under controlled perturbations, and makes decisions supported by task-relevant observations.

## 3. Benchmark Design

Policy-MME organizes policy optimization evaluation into three levels.

**Level 1: Optimization Stability.** This level measures whether training remains stable across seeds. It tracks learning-curve collapse, variance across seeds, catastrophic drops after policy updates, and sensitivity to clipping or entropy settings. A method passes this level only when success is repeatable rather than seed-selective.

**Level 2: Robustness and Generalization.** Building on stable optimization, this level tests whether the learned policy survives controlled perturbations. Perturbations include reward noise, observation masking, dynamics shifts, and delayed rewards. This level distinguishes policies that learn general task structure from policies that rely on narrow environment regularities.

**Level 3: Decision Faithfulness.** The highest level asks whether policy behavior is supported by task-relevant state information. It uses counterfactual state probes and action-attribution checks to detect spurious reward exploitation. A policy that succeeds while ignoring relevant state variables receives a lower score, because the success is not faithful to the intended task.

## 4. Evaluation Protocol

Conventional evaluation reports average return across tasks and seeds. Policy-MME keeps this number as a baseline, but adds group-level diagnostic scoring. Each task group contains related checks: nominal performance, seed stability, perturbation robustness, and decision-faithfulness probes.

The group score is non-linear. If an algorithm performs well on nominal tasks but fails under perturbation, its score is suppressed. If it succeeds in late-stage probes only after failing earlier evidence checks, the later success is not fully credited. This design follows a simple principle: robust policy learning should be consistent across related evidence, not a collection of isolated wins.

## 5. Synthetic Demonstration

Because this demo does not run real environments, all numbers in this section are synthetic placeholders. They illustrate how the benchmark would be reported.

| Method | Average Return | Level 1 Stability | Level 2 Robustness | Level 3 Faithfulness | Policy-MME Score |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |
| SAC | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |
| TD3 | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |
| Oracle / Human reference | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |

The synthetic results show why a diagnostic benchmark is useful. PPO appears competitive under average return, only slightly below SAC. However, its Policy-MME score drops because performance is less stable under perturbations and decision-faithfulness probes. The gap between average return and grouped score is the main diagnostic signal.

## 6. Analysis

The first finding is metric sensitivity. Average return rewards peak success, while Policy-MME rewards consistent success. This difference matters because policy optimization failures are often conditional: they appear under particular seeds, perturbations, or reward variants.

The second finding is hierarchical propagation. Instability at Level 1 limits robustness at Level 2; robustness failures then undermine decision faithfulness at Level 3. In other words, high-level decision failures are not always caused by weak reasoning alone. They can originate in unstable optimization dynamics.

The third finding is that PPO's clipped objective is helpful but not sufficient. Clipping reduces destructive updates, yet it does not guarantee robustness to observation corruption or reward shifts. A benchmark that only measures nominal return cannot expose this limitation.

## 7. Limitations

This demo is intentionally synthetic. It does not run MuJoCo, Atari, robotics, or RLHF environments. Therefore, the numbers should be read as a reporting example, not as evidence about PPO, SAC, or TD3. A real Policy-MME study would need fixed environments, public seeds, ablation protocols, human/oracle references, and released training logs.

Policy-MME also does not prove that a policy has human-like understanding. Its decision-faithfulness probes can reduce shortcut success, but they remain approximations. Strong claims about mechanism require additional interpretability and causal analysis.

## 8. Conclusion

Policy-MME reframes policy optimization evaluation from average-return ranking to reliability diagnosis. By decomposing capability into stability, robustness, and decision faithfulness, and by scoring related checks jointly, the benchmark exposes failures that conventional scalar reporting can hide. The broader lesson is that future reinforcement learning evaluation should ask not only whether an agent wins, but whether it wins consistently, robustly, and for the right reasons.

## Input material used by the system

```markdown
{material.strip()}
```
"""


def build_explain() -> str:
    return """# 为什么要这么写：章节级中文解释

## 总体写作策略

这篇 demo 采用 benchmark / evaluation paper 的叙事，而不是普通算法论文叙事。原因是输入素材强调 PPO 和评测缺陷：平均 return 可能掩盖 seed variance、训练崩溃、reward hacking 和过拟合。因此论文主线不是“提出新算法”，而是“现有评测不足 → 设计诊断 benchmark → 用示例说明旧指标看不到的问题”。

## Abstract

摘要按“背景进展 → 评测缺口 → 方案 → 设计机制 → 结果洞察 → 影响”组织。这样做的目的是让读者在一段内看到完整论证，而不是只看到“我们做了一个 benchmark”。摘要明确说明 synthetic numbers，避免把 demo 数字伪装成真实实验。

## Introduction

Introduction 先承认 PPO 的实用价值，再指出平均 return 不等于可靠学习。这个顺序能避免攻击前人，同时制造研究必要性。最后给出一句 thesis，把整篇文章压缩成一个可检查主张：旧评测高估真实可靠性，Policy-MME 用层级能力和组级评分揭示瓶颈。

## Related Work

Related Work 不堆论文名，而是按功能定位：PPO 是实践基线；传统 RL benchmark 有用但不完整；可靠评测需要鲁棒性、可复现性和失败分析。这样写能服务主线，而不是变成文献流水账。

## Benchmark Design

设计部分使用三层能力结构：稳定性、鲁棒性、忠实性。这样比列任务清单更有理论感，也能为后文“错误层级传播”埋伏笔。每一层都回答一个具体问题：是否稳定学到、是否抗扰动、是否基于正确状态决策。

## Evaluation Protocol

协议部分解释为什么不能只用 average return。group-level non-linear scoring 的作用是惩罚“只在孤立条件下成功”。这和用户给的范文逻辑一致：新 benchmark 不只是数据新，还要评价方式能揭示旧指标隐藏的问题。

## Synthetic Demonstration

演示实验明确标注 synthetic placeholders。这样既能展示论文该如何呈现表格和洞察，又不制造伪造实验。表格故意让 PPO average return 看起来不错，但 Policy-MME score 下降，用来说明新指标的诊断价值。

## Analysis

Analysis 不重复表格，而是提炼三条 insight：metric sensitivity、hierarchical propagation、clipping helps but is insufficient。这样实验部分从“排名”升级为“机制解释”，符合高质量 evaluation paper 的写法。

## Limitations

Limitations 主动说明 demo 没有真实环境、不能对 PPO/SAC/TD3 做实证结论。这是诚信闸门：系统不能因为要写得像论文，就把演示内容写成真实发现。

## Conclusion

Conclusion 回收主线：从平均 return 排名转向可靠性诊断。它没有引入新概念，而是把稳定性、鲁棒性、忠实性和组级评分重新压缩成一句领域意义。
"""


def figure_pipeline() -> str:
    return """<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"520\" viewBox=\"0 0 1200 520\">
  <rect width=\"1200\" height=\"520\" fill=\"#f8fafc\"/>
  <text x=\"60\" y=\"60\" font-size=\"32\" font-family=\"Arial\" font-weight=\"700\" fill=\"#0f172a\">Policy-MME Diagnostic Pipeline</text>
  <g font-family=\"Arial\" font-size=\"18\">
    <rect x=\"70\" y=\"110\" width=\"220\" height=\"110\" rx=\"18\" fill=\"#dbeafe\" stroke=\"#2563eb\" stroke-width=\"3\"/>
    <text x=\"95\" y=\"150\" fill=\"#1e3a8a\" font-weight=\"700\">Input Material</text>
    <text x=\"95\" y=\"180\" fill=\"#1e40af\">PPO + RL evaluation</text>
    <text x=\"95\" y=\"205\" fill=\"#1e40af\">problem statement</text>

    <rect x=\"370\" y=\"110\" width=\"240\" height=\"110\" rx=\"18\" fill=\"#dcfce7\" stroke=\"#16a34a\" stroke-width=\"3\"/>
    <text x=\"395\" y=\"145\" fill=\"#14532d\" font-weight=\"700\">Capability Hierarchy</text>
    <text x=\"395\" y=\"175\" fill=\"#166534\">L1 stability</text>
    <text x=\"395\" y=\"200\" fill=\"#166534\">L2 robustness · L3 faithfulness</text>

    <rect x=\"700\" y=\"110\" width=\"240\" height=\"110\" rx=\"18\" fill=\"#fef3c7\" stroke=\"#d97706\" stroke-width=\"3\"/>
    <text x=\"725\" y=\"145\" fill=\"#78350f\" font-weight=\"700\">Grouped Scoring</text>
    <text x=\"725\" y=\"175\" fill=\"#92400e\">penalize fragmented wins</text>
    <text x=\"725\" y=\"200\" fill=\"#92400e\">reward consistent evidence</text>

    <rect x=\"430\" y=\"320\" width=\"340\" height=\"110\" rx=\"18\" fill=\"#ede9fe\" stroke=\"#7c3aed\" stroke-width=\"3\"/>
    <text x=\"460\" y=\"360\" fill=\"#4c1d95\" font-weight=\"700\">Paper Output</text>
    <text x=\"460\" y=\"390\" fill=\"#5b21b6\">claim-grounded sections</text>
    <text x=\"460\" y=\"415\" fill=\"#5b21b6\">explainable writing rationale</text>

    <path d=\"M295 165 L360 165\" stroke=\"#334155\" stroke-width=\"4\" marker-end=\"url(#arrow)\"/>
    <path d=\"M615 165 L690 165\" stroke=\"#334155\" stroke-width=\"4\" marker-end=\"url(#arrow)\"/>
    <path d=\"M820 230 C790 300 720 325 650 330\" stroke=\"#334155\" stroke-width=\"4\" fill=\"none\" marker-end=\"url(#arrow)\"/>
    <path d=\"M495 230 C500 285 525 310 565 330\" stroke=\"#334155\" stroke-width=\"4\" fill=\"none\" marker-end=\"url(#arrow)\"/>
  </g>
  <defs><marker id=\"arrow\" markerWidth=\"10\" markerHeight=\"10\" refX=\"8\" refY=\"3\" orient=\"auto\"><path d=\"M0,0 L0,6 L9,3 z\" fill=\"#334155\"/></marker></defs>
</svg>
"""


def figure_results() -> str:
    bars = [("PPO", 52.4, "#2563eb"), ("SAC", 58.2, "#16a34a"), ("TD3", 49.7, "#f97316"), ("Oracle", 88.9, "#7c3aed")]
    parts = ["<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"620\" viewBox=\"0 0 1200 620\">", "<rect width=\"1200\" height=\"620\" fill=\"#ffffff\"/>", "<text x=\"70\" y=\"60\" font-size=\"32\" font-family=\"Arial\" font-weight=\"700\" fill=\"#111827\">Synthetic Policy-MME Score Comparison</text>", "<text x=\"70\" y=\"95\" font-size=\"18\" font-family=\"Arial\" fill=\"#6b7280\">Demo numbers only: illustrate diagnostic reporting, not empirical claims.</text>"]
    x0, y0, width, maxv = 150, 500, 780, 100
    for i, (name, score, color) in enumerate(bars):
        y = y0 - i * 90
        bar_w = width * score / maxv
        parts.append(f"<text x=\"70\" y=\"{y-8}\" font-size=\"22\" font-family=\"Arial\" font-weight=\"700\" fill=\"#111827\">{name}</text>")
        parts.append(f"<rect x=\"{x0}\" y=\"{y-38}\" width=\"{bar_w:.1f}\" height=\"42\" rx=\"10\" fill=\"{color}\"/>")
        parts.append(f"<text x=\"{x0+bar_w+18:.1f}\" y=\"{y-10}\" font-size=\"22\" font-family=\"Arial\" fill=\"#111827\">{score}</text>")
    parts.append("<line x1=\"150\" y1=\"520\" x2=\"930\" y2=\"520\" stroke=\"#d1d5db\" stroke-width=\"2\"/>")
    parts.append("<text x=\"150\" y=\"560\" font-size=\"16\" font-family=\"Arial\" fill=\"#6b7280\">0</text><text x=\"910\" y=\"560\" font-size=\"16\" font-family=\"Arial\" fill=\"#6b7280\">100</text>")
    parts.append("<rect x=\"975\" y=\"155\" width=\"150\" height=\"170\" rx=\"16\" fill=\"#f3f4f6\" stroke=\"#d1d5db\"/>")
    parts.append("<text x=\"995\" y=\"195\" font-size=\"18\" font-family=\"Arial\" font-weight=\"700\" fill=\"#111827\">Takeaway</text>")
    parts.append("<text x=\"995\" y=\"230\" font-size=\"15\" font-family=\"Arial\" fill=\"#374151\">Average return can</text>")
    parts.append("<text x=\"995\" y=\"255\" font-size=\"15\" font-family=\"Arial\" fill=\"#374151\">hide robustness and</text>")
    parts.append("<text x=\"995\" y=\"280\" font-size=\"15\" font-family=\"Arial\" fill=\"#374151\">faithfulness failures.</text>")
    parts.append("</svg>\n")
    return "".join(parts)


def build_figure_prompts() -> str:
    return """# Figure prompts for image2 / imagegen

本 demo 中已提交可复现 SVG 图。若要用 image2 / imagegen 生成更像论文插图的位图，可使用以下提示词。建议生成后人工核对文字，不要把无法辨认的 AI 文字直接放进论文。

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
5. 生成 `paper.md` 的 8 个章节。
6. 生成 `explain/why_each_section.md`，逐章解释写作理由。
7. 生成两张可复现 SVG 图：pipeline overview 和 synthetic score comparison。
8. 生成 `figures/figure_prompts.md`，供 image2 / imagegen 生成位图版本。
9. 写出 `MANIFEST.md`，记录所有输出文件哈希。

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
- 系统必须解释为什么这么写，不能只输出漂亮正文。
"""


def build_manifest(outputs: dict[Path, str]) -> str:
    rows = ["# Demo manifest", "", "| File | SHA256 |", "| --- | --- |"]
    for path in sorted(outputs):
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else hashlib.sha256(outputs[path].encode("utf-8")).hexdigest()
        rows.append(f"| `{path.relative_to(ROOT)}` | `{digest}` |")
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
