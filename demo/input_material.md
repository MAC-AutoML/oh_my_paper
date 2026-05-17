# 输入素材：PPO 与强化学习算法评测

Proximal Policy Optimization (PPO) 是强化学习中广泛使用的 policy-gradient 方法。它通过 clipped surrogate objective 限制单次策略更新幅度，从而在实现简单、样本效率和训练稳定性之间取得平衡。PPO 常被用于连续控制、游戏环境、机器人策略学习和 RLHF 等场景。

可围绕 PPO 构建一篇 evaluation / benchmark 风格论文：问题不是提出新算法，而是评估当前强化学习 agent 在“稳定学习、跨任务泛化、奖励噪声鲁棒性、超参数敏感性”上的真实能力。传统 benchmark 可能只报告平均 return，容易掩盖训练崩溃、seed variance、reward hacking 和环境特定过拟合。

演示论文可设计一个名为 Policy-MME 的诊断性评测框架，把 RL agent 能力分为三层：
1. optimization stability：训练曲线是否稳定，是否频繁 collapse；
2. robustness and generalization：面对 reward noise、dynamics shift、observation corruption 是否保持性能；
3. decision faithfulness：策略是否真正利用任务相关状态，而不是 exploit spurious reward 或环境漏洞。

演示实验可以比较 PPO、SAC、TD3 和一个 human reference / oracle policy。由于本 demo 不运行真实环境，所有实验数值必须明确标注为 synthetic，用来展示论文写法和系统解释能力。

## 源论文启发（来自 temp/papers 的本地阅读，不追踪原文）

### PPO 论文给 demo 的启发

PPO 的原文不是只说“我们提出一个算法”，而是先指出已有方法各有缺陷：vanilla policy gradient 数据效率和鲁棒性不足，TRPO 更复杂且不适合某些结构。然后它提出 clipped surrogate objective，并在实验中比较 no clipping、clipping、KL penalty 等不同 surrogate objectives。这个写法启发 demo：如果要写 Policy-MME，就不能只说“我们设计一个 benchmark”，还要说明旧评测为什么不够，并设计 ablation-style reporting 来证明新评分方式有意义。

### ResNet 论文给 demo 的启发

ResNet 的核心叙事是 degradation problem：理论上更深网络不应比浅网络训练误差更高，但实际 plain deep network 会变差。作者把这个反直觉现象转化为 residual learning 的必要性。这个写法启发 demo：平均 return 高不代表 policy 可靠，这也是一个反直觉矛盾。Policy-MME 要把这个矛盾转化为 benchmark 设计，而不是只做表格排名。

### Video-MME-v2 论文给 demo 的启发

Video-MME-v2 的摘要和正文都按“旧 benchmark 饱和 → 三层能力体系 → group-based nonlinear scoring → 严格数据质控 → 模型-人类差距 → 层级瓶颈分析”推进。这个写法启发 demo：Policy-MME 也应该有三层能力、组级评分、数据/任务质量控制和层级错误传播分析。尤其是 group-based scoring 的思想，可以迁移到 RL：同一任务组内 nominal return、seed stability、perturbation robustness、decision faithfulness 必须联合评价。
