# Policy-MME: A Diagnostic Benchmark for Robust and Faithful Policy Optimization

> Demo note: this paper is generated from `demo/input_material.md`. All numerical results are synthetic placeholders for demonstrating the oh my paper workflow; they are not empirical claims.

## Abstract

Recent reinforcement learning agents achieve strong average returns on standard control benchmarks, yet these scores often hide brittle optimization, seed-level instability, and reward-specific shortcuts. To address this evaluation gap, we introduce **Policy-MME**, a diagnostic benchmark for policy optimization methods. Policy-MME decomposes agent capability into three progressively harder levels: optimization stability, robustness and generalization, and decision faithfulness. Unlike conventional average-return reporting, the benchmark uses grouped non-linear scoring that penalizes unstable seeds, inconsistent perturbation behavior, and unsupported decision rationales. Built around auditable traces, fixed perturbation protocols, and explicit failure labels, Policy-MME is designed to make failure modes visible rather than merely rank algorithms. In a synthetic demonstration comparing PPO, SAC, TD3, and an oracle policy, PPO obtains competitive average returns but loses substantial score under group-level robustness evaluation. The analysis suggests that reliable policy optimization requires not only high peak performance, but also stable learning dynamics, perturbation robustness, and faithful state-dependent decisions.

## 1. Introduction

Policy-gradient algorithms such as Proximal Policy Optimization (PPO) have become default baselines for continuous control, game-like environments, robotics, and RLHF-style optimization. Their appeal is clear: PPO is comparatively simple to implement, clips destructive policy updates, and often works well across a broad range of tasks. However, this practical success has also made PPO a common reference point in papers where benchmark tables emphasize mean return over deeper reliability properties.

The problem is that average return is not the same as trustworthy policy learning. A method may achieve a high mean by succeeding on easy seeds, collapsing on harder seeds, exploiting reward artifacts, or overfitting environment-specific dynamics. When evaluation focuses on a single scalar, the leaderboard can look saturated even while agents remain fragile under small distribution shifts.

This paper proposes **Policy-MME**, a diagnostic benchmark designed around the following thesis: **现有强化学习评测若只报告平均 return，容易高估 agent 的真实可靠性；Policy-MME 通过层级能力、扰动压力测试和一致性评分揭示 PPO 类算法在稳定性、鲁棒性和决策忠实性上的瓶颈。** The benchmark is not intended to replace environment suites; instead, it wraps existing tasks with capability levels, perturbation protocols, and group-level scoring so that evaluation reflects robustness and faithfulness rather than isolated success.

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
# 输入素材：PPO 与强化学习算法评测

Proximal Policy Optimization (PPO) 是强化学习中广泛使用的 policy-gradient 方法。它通过 clipped surrogate objective 限制单次策略更新幅度，从而在实现简单、样本效率和训练稳定性之间取得平衡。PPO 常被用于连续控制、游戏环境、机器人策略学习和 RLHF 等场景。

可围绕 PPO 构建一篇 evaluation / benchmark 风格论文：问题不是提出新算法，而是评估当前强化学习 agent 在“稳定学习、跨任务泛化、奖励噪声鲁棒性、超参数敏感性”上的真实能力。传统 benchmark 可能只报告平均 return，容易掩盖训练崩溃、seed variance、reward hacking 和环境特定过拟合。

演示论文可设计一个名为 Policy-MME 的诊断性评测框架，把 RL agent 能力分为三层：
1. optimization stability：训练曲线是否稳定，是否频繁 collapse；
2. robustness and generalization：面对 reward noise、dynamics shift、observation corruption 是否保持性能；
3. decision faithfulness：策略是否真正利用任务相关状态，而不是 exploit spurious reward 或环境漏洞。

演示实验可以比较 PPO、SAC、TD3 和一个 human reference / oracle policy。由于本 demo 不运行真实环境，所有实验数值必须明确标注为 synthetic，用来展示论文写法和系统解释能力。
```
