"""Paper and explanation templates for the deterministic demo."""

from __future__ import annotations

def build_paper(material: str) -> str:
    thesis = (
        "现有强化学习评测若只报告平均 return，容易高估 agent 的真实可靠性；"
        "Policy-MME 通过层级能力、扰动压力测试和一致性评分揭示 PPO 类算法在稳定性、鲁棒性和决策忠实性上的瓶颈。"
    )
    return f"""# Policy-MME: A Diagnostic Benchmark for Robust and Faithful Policy Optimization

> Demo note: this paper is generated from `demo/input_material.md`. All numerical results are synthetic placeholders for demonstrating the oh my paper workflow; they are not empirical claims. The writing pattern is inspired by how PPO reports surrogate-objective comparisons, how ResNet turns an optimization pathology into an architectural reformulation, and how Video-MME-v2 frames benchmark saturation, hierarchy, quality control, and diagnostic analysis.

## Abstract

Recent reinforcement learning agents achieve strong average returns on standard control benchmarks, yet these scores often hide brittle optimization, seed-level instability, reward-specific shortcuts, and poor transfer under small environment shifts. This creates a gap between leaderboard-style performance and the reliability expected from deployable policy optimization systems. To address this gap, we introduce **Policy-MME**, a diagnostic benchmark for robust and faithful policy optimization. Policy-MME decomposes agent capability into three progressively harder levels: optimization stability, robustness and generalization, and decision faithfulness. Unlike conventional average-return reporting, Policy-MME uses grouped non-linear scoring that jointly evaluates nominal performance, seed consistency, perturbation robustness, and evidence-supported decision behavior. The benchmark is designed around auditable traces, fixed perturbation protocols, source-quality checks, and explicit failure labels, so that it exposes why a policy fails rather than merely ranking algorithms.

Using a synthetic demonstration based on PPO-style evaluation settings, we compare PPO, SAC, TD3, and an oracle/human reference under average return and grouped diagnostic scoring. PPO remains competitive under average return but loses substantial score when instability, perturbation sensitivity, and decision-faithfulness probes are counted jointly. Further analysis reveals a hierarchical bottleneck: Level-1 optimization collapse propagates to Level-2 robustness failures, which then undermines Level-3 faithful decision behavior. These results establish Policy-MME as a reproducible demonstration of how evaluation papers can turn a familiar algorithmic setting into a stricter, more explainable benchmark narrative.

## 1. Introduction

Policy-gradient algorithms such as Proximal Policy Optimization (PPO) have become default baselines for continuous control, game-like environments, robotics, and RLHF-style optimization. Their appeal is practical: PPO constrains policy updates through a clipped surrogate objective, supports multiple epochs of minibatch updates, and often strikes a useful balance among sample complexity, implementation simplicity, and wall-clock efficiency. Because of this balance, PPO is frequently used not only as an algorithm but also as a reference point for judging new reinforcement learning systems.

However, the popularity of PPO also highlights a broader evaluation problem. Standard reinforcement learning reports often compress each method into a mean return table. This convention is useful for quick comparison, but it can hide severe reliability failures. A method may achieve high average return by succeeding on favorable seeds, collapsing on difficult seeds, exploiting reward artifacts, or overfitting to narrow environment regularities. In these cases, the scalar score does not answer the question a skeptical reviewer actually cares about: whether the learned policy is stable, robust, and faithful to the intended task.

This paper treats that mismatch as an evaluation crisis. The goal is not to propose a new optimizer. Instead, we ask how to evaluate policy optimization methods when average return is no longer diagnostic enough. This shift mirrors a common pattern in mature machine learning fields: once standard benchmarks become easy to optimize, the next contribution is often a benchmark that measures deeper capability structure. In computer vision, ResNet made the degradation problem visible and then proposed residual learning as a response. In video understanding, Video-MME-v2 argues that saturated leaderboards require hierarchical and group-based evaluation. Policy-MME applies the same style of reasoning to reinforcement learning.

We propose **Policy-MME**, a benchmark wrapper that evaluates policy optimization through three capability levels. Level 1 measures optimization stability across seeds and update regimes. Level 2 measures robustness and generalization under reward noise, dynamics shift, delayed reward, and observation corruption. Level 3 measures decision faithfulness through counterfactual probes and action-support checks. The key design choice is that these levels are not independent checkboxes: higher-level reliability depends on lower-level stability.

Our central thesis is: **{thesis}** This thesis leads to three contributions. First, we define a capability hierarchy for policy optimization evaluation. Second, we introduce grouped non-linear scoring to penalize fragmented or shortcut-based success. Third, we provide a synthetic demonstration that shows how PPO can appear strong under average return while exhibiting diagnostic weaknesses under Policy-MME.

## 2. Background and Motivation

### 2.1 PPO as a practical policy optimization baseline

PPO belongs to the family of policy-gradient methods. It alternates between collecting trajectories through environment interaction and optimizing a surrogate objective. The clipped variant constrains the probability ratio between the new and old policies, discouraging updates that move too far from the behavior policy. This design inherits some intuition from trust-region methods while avoiding the implementation complexity of second-order optimization.

The practical significance of PPO is that it made a particular trade-off attractive: it is simple enough to implement widely, stable enough to serve as a baseline, and general enough to appear in many applied domains. A benchmark built around PPO therefore has pedagogical value. If even a widely trusted baseline can look different under average return and diagnostic scoring, then the evaluation issue is not a niche artifact.

### 2.2 Why average return is insufficient

Average return answers one question: how much reward did the policy obtain under a particular evaluation protocol? It does not directly answer whether the policy learned the intended behavior, whether training is repeatable, whether the result depends on lucky seeds, or whether the policy survives small shifts. In practice, these hidden dimensions often determine whether a policy is useful.

There are four common failure modes. First, **seed fragility** occurs when a method has high mean but high variance, making success difficult to reproduce. Second, **training collapse** occurs when policy updates destroy previously learned behavior. Third, **perturbation brittleness** occurs when small reward or dynamics changes sharply reduce performance. Fourth, **shortcut exploitation** occurs when the agent succeeds by exploiting spurious reward paths rather than solving the intended task.

A benchmark that does not expose these failures can overstate progress. Policy-MME is designed to make these failures first-class evaluation objects.

## 3. Policy-MME Benchmark Design

### 3.1 Design principles

Policy-MME follows four principles.

**Principle 1: Evaluate capabilities hierarchically.** Stable optimization is a prerequisite for robustness; robustness is a prerequisite for faithful decision behavior. Therefore, the benchmark should not treat all subtasks as a flat list.

**Principle 2: Score related evidence jointly.** A method that succeeds nominally but fails under controlled perturbations should not receive the same credit as a method that succeeds consistently.

**Principle 3: Preserve auditability.** Every score must be traceable to seeds, perturbation settings, training curves, and failure labels. This prevents polished prose from hiding unsupported claims.

**Principle 4: Separate demonstration from empirical claim.** Because this demo uses synthetic values, the paper shows how a real study would be written, not what PPO or SAC truly achieves.

### 3.2 Level 1: Optimization Stability

Level 1 measures whether training is stable across seeds and update regimes. It includes four checks: final-return variance, training-curve collapse, destructive-update frequency, and sensitivity to core optimizer hyperparameters. The motivation comes from the PPO paper's emphasis on comparing surrogate objectives and hyperparameters. If an algorithm only works for a narrow configuration, a single mean return table is not enough.

A method receives high Level-1 score when it has low seed variance, smooth learning curves, and few catastrophic drops. It receives low score when success depends on favorable initialization or when policy updates frequently erase progress.

### 3.3 Level 2: Robustness and Generalization

Level 2 measures whether a policy remains effective under controlled perturbations. The perturbations are chosen to be small enough that a robust policy should still solve the task, but meaningful enough to reveal overfitting. They include reward noise, delayed reward, observation masking, dynamics shifts, and altered termination conditions.

This level is inspired by benchmark papers that make distribution shift explicit rather than implicit. The purpose is not to punish every performance drop. The purpose is to distinguish graceful degradation from brittle collapse.

### 3.4 Level 3: Decision Faithfulness

Level 3 measures whether action choices are supported by task-relevant state information. It uses counterfactual probes, state-feature masking, action-attribution checks, and failure-case replay. A policy that succeeds by exploiting irrelevant shortcuts receives a lower score even if nominal return is high.

This level is deliberately conservative. It does not claim to fully interpret neural policies. Instead, it asks whether the most obvious shortcut explanations can be ruled out. If a policy changes behavior when irrelevant features are altered but ignores relevant state changes, the benchmark marks the decision as unfaithful.

## 4. Evaluation Protocol

### 4.1 Baseline metric: average return

Policy-MME reports average return because it remains useful and familiar. Removing it would make comparison harder. However, average return is treated as the baseline metric, not the final judgment.

### 4.2 Grouped non-linear score

Each evaluation group contains nominal return, seed stability, perturbation robustness, and decision-faithfulness checks. Let the normalized scores be \\(s_1, s_2, s_3, s_4\\). A simple group score can be written as:

\\[
G = \\bar{{s}} \\cdot (1 - \\lambda \\cdot \\mathrm{{Var}}(s_1, s_2, s_3, s_4)) \\cdot \\min_i(s_i)^{{\\gamma}}.
\\]

The exact formula can be changed in a real implementation, but the principle is fixed: unstable groups should receive less credit than consistently strong groups. The variance term penalizes fragmented success; the minimum term penalizes failure in a critical check.

### 4.3 Failure labels

Policy-MME attaches failure labels to low-scoring groups. The main labels are:

| Label | Meaning |
| --- | --- |
| `seed_fragility` | Large variance across seeds. |
| `collapse_after_update` | Sharp return drop after policy update. |
| `reward_noise_brittleness` | Performance collapses under reward noise. |
| `dynamics_overfit` | Policy fails under small transition shifts. |
| `observation_shortcut` | Policy depends on spurious observation features. |
| `unsupported_action` | Action choice is not supported by task-relevant state. |

These labels are important because a benchmark should produce insight, not only a score.

## 5. Dataset and Task Construction

A real Policy-MME release would include tasks from continuous control, sparse-reward navigation, manipulation, game-like environments, and RLHF-style preference optimization. For this demo, we specify the construction logic without claiming an actual released suite.

### 5.1 Task families

Policy-MME organizes tasks into four families.

1. **Control stability tasks** test locomotion and balancing under fixed dynamics.
2. **Robustness tasks** introduce reward noise, delayed reward, observation corruption, and dynamics shifts.
3. **Shortcut tasks** contain tempting but spurious reward features.
4. **Faithfulness tasks** use counterfactual probes to test whether actions track relevant state variables.

### 5.2 Seed protocol

Each method is evaluated across multiple seeds. A task is not considered solved if only one seed succeeds. This is the reinforcement-learning analogue of asking whether a benchmark answer is consistent across related questions.

### 5.3 Quality control

Policy-MME uses three quality checks. First, perturbations must preserve task semantics. Second, shortcut features must be documented and removable. Third, every synthetic or simulated task must provide a trace file containing seed, environment version, hyperparameters, and evaluation mode.

This section is modeled after high-quality benchmark papers: data construction is not a footnote; it is part of the contribution because poor data design can invalidate evaluation.

## 6. Synthetic Demonstration

### 6.1 Demonstration setup

This section illustrates reporting format with synthetic numbers. We compare PPO, SAC, TD3, and an oracle/human reference. Each method receives an average-return score and three level scores. The Policy-MME score is lower when the method is inconsistent across checks.

| Method | Average Return | Level 1 Stability | Level 2 Robustness | Level 3 Faithfulness | Policy-MME Score |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |
| SAC | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |
| TD3 | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |
| Oracle / Human reference | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |

### 6.2 Main observation

The main observation is not that SAC is better than PPO. These are synthetic values, so such a claim would be invalid. The real observation is structural: a method can look competitive under average return while losing diagnostic score under grouped evaluation. PPO's average return is only slightly below SAC, but its Policy-MME score is substantially lower because Level-2 and Level-3 checks expose brittleness.

### 6.3 Ablation-style reporting

A real paper should also compare scoring variants. For example, it should report average return, linear average of level scores, and grouped non-linear score. If the grouped score reveals failures hidden by the linear average, then the metric is doing diagnostic work. Without such a comparison, the new metric would look arbitrary.

### 6.4 Failure-mode table

| Method | Dominant synthetic failure label | Explanation |
| --- | --- | --- |
| PPO | `reward_noise_brittleness` | Clipped updates stabilize training but do not guarantee robustness to reward perturbation. |
| SAC | `observation_shortcut` | Higher robustness does not automatically imply faithful state use. |
| TD3 | `seed_fragility` | Performance is more sensitive to initialization and task variant. |
| Oracle / Human reference | none | Reference policy remains consistent across grouped checks. |

## 7. Analysis

### 7.1 Metric sensitivity

Average return rewards peak task success. Policy-MME rewards consistent evidence. This difference changes the interpretation of the same synthetic system. Under average return, PPO appears close to SAC. Under grouped scoring, the gap widens because robustness and faithfulness failures are no longer averaged away.

### 7.2 Hierarchical bottleneck

The level breakdown suggests a cascading bottleneck. If training is unstable at Level 1, the learned representation varies across seeds. This makes perturbation behavior unstable at Level 2. Once perturbation behavior is unstable, Level-3 decision-faithfulness probes become unreliable because the policy may not have learned a stable task representation in the first place.

This is why a benchmark needs hierarchy rather than a flat checklist. A low Level-3 score is not always a pure reasoning failure; it may originate from lower-level optimization instability.

### 7.3 Comparison with ResNet-style argumentation

ResNet's writing is powerful because it identifies a counterintuitive failure: deeper networks should be at least as good as shallower ones, yet plain deeper networks can have worse training error. That observation motivates residual learning. Policy-MME uses an analogous move: stronger average return should imply better policy quality, yet average return can coexist with brittle behavior. That contradiction motivates diagnostic scoring.

### 7.4 Comparison with Video-MME-v2-style benchmark writing

Video-MME-v2 is persuasive because the benchmark design, scoring protocol, data quality, and experiments all serve the same story. Policy-MME follows that structure. The three levels define the benchmark; grouped scoring operationalizes the reliability claim; synthetic experiments show what average return hides; limitations prevent overclaiming.

## 8. Practical Guidance for a Real Policy-MME Study

A real version of this paper should add four components.

First, it should implement the task suite with public seeds and environment versions. Second, it should release training curves, hyperparameters, and failure labels. Third, it should include ablations over perturbation strength and scoring formula. Fourth, it should compare at least one on-policy method, one off-policy method, and one reference policy.

The most important rule is that every main claim must be tied to a check. If the paper claims robustness, it needs perturbation results. If it claims faithfulness, it needs counterfactual probes. If it claims benchmark quality, it needs task validation and documentation.

## 9. Limitations

This demo is intentionally synthetic. It does not run MuJoCo, Atari, robotics, or RLHF environments. Therefore, the numbers should be read as a reporting example, not as evidence about PPO, SAC, or TD3. A real Policy-MME study would need fixed environments, public seeds, ablation protocols, human/oracle references, and released training logs.

Policy-MME also does not prove that a policy has human-like understanding. Decision-faithfulness probes can reduce shortcut success, but they remain approximations. Strong claims about mechanism require additional interpretability and causal analysis.

Finally, grouped scoring can be misused if the groups are poorly designed. If perturbations change task semantics, a lower score may reflect task invalidity rather than model weakness. For this reason, benchmark construction and quality control are as important as the scoring formula.

## 10. Conclusion

Policy-MME reframes policy optimization evaluation from average-return ranking to reliability diagnosis. By decomposing capability into stability, robustness, and decision faithfulness, and by scoring related checks jointly, the benchmark exposes failures that conventional scalar reporting can hide. The broader lesson is that future reinforcement learning evaluation should ask not only whether an agent wins, but whether it wins consistently, robustly, and for the right reasons.

## Appendix A: Input material used by the system

```markdown
{material.strip()}
```
"""


def build_explain() -> str:
    return """# 为什么要这么写：章节级中文解释

## 总体写作策略

这篇 demo 采用 benchmark / evaluation paper 的叙事，而不是普通算法论文叙事。原因是输入素材强调 PPO 和评测缺陷：平均 return 可能掩盖 seed variance、训练崩溃、reward hacking 和过拟合。因此论文主线不是“提出新算法”，而是“现有评测不足 → 设计诊断 benchmark → 用示例说明旧指标看不到的问题”。

系统参考了三篇论文的写作方式：PPO 提供“算法目标 + surrogate objective + ablation 实验”的结构；ResNet 提供“反直觉失败现象 → 方法重构”的论证方式；Video-MME-v2 提供“benchmark 饱和 → 层级能力 → group scoring → 质控 → 诊断发现”的完整 benchmark 叙事。demo 没有复制原文，而是把这些结构转化成可解释写作规则。

## Abstract

摘要按“背景进展 → 评测缺口 → 方案 → 设计机制 → 结果洞察 → 影响”组织。这样做的目的是让读者在一段内看到完整论证，而不是只看到“我们做了一个 benchmark”。摘要明确说明 synthetic numbers，避免把 demo 数字伪装成真实实验。

## Introduction

Introduction 先承认 PPO 的实用价值，再指出平均 return 不等于可靠学习。这个顺序能避免攻击前人，同时制造研究必要性。最后给出一句 thesis，把整篇文章压缩成一个可检查主张：旧评测高估真实可靠性，Policy-MME 用层级能力和组级评分揭示瓶颈。

## Background and Motivation

这一章解释 PPO 为什么适合作为 demo 素材：它是广泛使用的 baseline，有 clipped surrogate objective，也常被用作比较对象。然后拆解 average return 的四类盲点：seed fragility、training collapse、perturbation brittleness、shortcut exploitation。这样读者能理解为什么 benchmark 需要升级。

## Benchmark Design

设计部分使用三层能力结构：稳定性、鲁棒性、忠实性。这样比列任务清单更有理论感，也能为后文“错误层级传播”埋伏笔。每一层都回答一个具体问题：是否稳定学到、是否抗扰动、是否基于正确状态决策。

## Evaluation Protocol

协议部分解释为什么不能只用 average return。group-level non-linear scoring 的作用是惩罚“只在孤立条件下成功”。这和 Video-MME-v2 的逻辑一致：新 benchmark 不只是数据新，还要评价方式能揭示旧指标隐藏的问题。

## Dataset and Task Construction

这一章借鉴 benchmark 论文的数据质控写法。即使 demo 不真实发布任务，也要说明真实版本应如何构造 task families、seed protocol 和 quality control。这样可以避免“只写想法，没有可执行评测形态”。

## Synthetic Demonstration

演示实验明确标注 synthetic placeholders。这样既能展示论文该如何呈现表格和洞察，又不制造伪造实验。表格故意让 PPO average return 看起来不错，但 Policy-MME score 下降，用来说明新指标的诊断价值。

## Analysis

Analysis 不重复表格，而是提炼多条 insight：metric sensitivity、hierarchical propagation、ResNet-style contradiction、Video-MME-v2-style benchmark closure。这样实验部分从“排名”升级为“机制解释”，符合高质量 evaluation paper 的写法。

## Practical Guidance

这一章说明真实研究要补哪些东西：真实环境、公开 seeds、训练曲线、hyperparameters、failure labels、扰动强度 ablation 和 scoring formula ablation。它把 demo 和真实论文之间的距离说清楚，避免读者误解 demo 已经完成实证贡献。

## Limitations

Limitations 主动说明 demo 没有真实环境、不能对 PPO/SAC/TD3 做实证结论。这是诚信闸门：系统不能因为要写得像论文，就把演示内容写成真实发现。

## Conclusion

Conclusion 回收主线：从平均 return 排名转向可靠性诊断。它没有引入新概念，而是把稳定性、鲁棒性、忠实性和组级评分重新压缩成一句领域意义。

## 图为什么这样设计

Figure 1 是 pipeline overview，对应顶会论文常见的一图读懂：输入素材、层级能力、组级评分、论文输出。Figure 2 是 synthetic score comparison，用柱状图展示 average return 与 diagnostic score 的叙事落差。Figure 3 是 hierarchy figure，用来把“低层错误向上传播”的机制视觉化。真正的 AI 生图路径是正文 claim → figure intent → imagegen prompt → Codex imagegen → caption/audit；SVG 只保留为 deterministic preview，方便用户复现结构。
"""
