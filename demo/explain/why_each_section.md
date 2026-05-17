# 为什么要这么写：章节级中文解释

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
