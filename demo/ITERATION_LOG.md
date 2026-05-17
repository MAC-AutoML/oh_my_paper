# Iteration log / 多轮迭代记录

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
