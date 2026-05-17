# Input summary

- Source file: `demo/input_material.md`
- SHA256: `5added71fdfdf86ebb4d146f7424179e8d761425db7fe5ea690d6965afe84c52`
- User intent interpreted by the demo: build a section-based academic writing workflow from PPO-oriented material.
- Forbidden behavior: do not hard-code a fixed benchmark acronym from prior examples; do not claim synthetic values are real experiments.
- Citation requirement: include representative references for RL optimization, benchmark methodology, reproducibility, and reliability.

## Raw input excerpt

```markdown
# 输入素材：PPO 与强化学习算法评测

Proximal Policy Optimization (PPO) 是强化学习中广泛使用的 policy-gradient 方法。它通过 clipped surrogate objective 限制单次策略更新幅度，从而在实现简单、样本效率和训练稳定性之间取得平衡。PPO 常被用于连续控制、游戏环境、机器人策略学习和 RLHF 等场景。

用户希望系统围绕这类素材自动生成一篇 academic evaluation / benchmark 风格论文，但不能提前把论文题目和 benchmark 名称写死。系统应先从输入素材中抽取多个候选论文方向，再让配置的 reviewer / Gemini-compatible 模型选择最合适的方向，然后进入写作循环。

可选研究方向示例：

1. 可靠性评测：平均 return 可能掩盖 seed variance、训练 collapse、reward hacking、环境特定过拟合和扰动脆弱性。
2. 复现实验协议：把 PPO 类算法的 seeds、hyperparameters、training curves、环境版本和 ablation 设置组织成可审计 protocol。
3. 鲁棒性 checklist：面向 RLHF 或连续控制场景，检查 reward noise、dynamics shift、observation corruption、delayed reward 等压力测试。
4. 教程/综述：解释为什么 policy optimization 论文不能只报告单一平均分数。

系统应该原创地选择其中一个方向，并保留选择理由。若使用 live API，应调用配置的 reviewer model 评分候选方向；如果 reviewer model 是 Gemini 或 Gemini-compatible relay，则由该模型完成选择。

长文写作必须是多轮过程：每个章节先有 section contract 和 paragraph plan，然后由写作 agent 起草，再由 critic/reviewer agent 评分与指出问题，最后返修。若 reviewer score 低于 85，应继续返修，直到达到阈值或达到最大轮数。所有 synthetic numbers 必须明确标注为示例，不得写成真实 PPO/SAC/TD3 实验结果。

图像生成也必须从正文 claim 出发：先生成 figure intent，再生成 Codex imagegen prompt，最后由 imagegen 生成位图并审查。demo 可以保存 prompt 和 audit，不应把代码生成 SVG 当作默认最终图像。
```
