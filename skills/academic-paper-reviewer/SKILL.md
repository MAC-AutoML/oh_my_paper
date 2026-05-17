---
name: academic-paper-reviewer
description: 严格审稿与辩驳规划（中英文） | Strict reviewer simulation, anti-sycophancy checks, and revision planning.
---

# academic-paper-reviewer

## Use when / 适用场景

- Use for EIC/reviewer simulation, anti-sycophancy stress review, and revision roadmap. / 用于 AC/审稿人压力测试、反阿谀校验与修订路线图。
- Use before final `pipeline` handoff.

## Do not use when / 不适用场景

- Do not grant guarantees unsupported by evidence. / 不得用不支持的内容作承诺。
- Do not replace author intent without trace evidence. / 不得在缺失证据下替代作者决策。

## Inputs / 输入

- Candidate draft and evidence artifacts.
- Previous review rounds and rejection risk notes.

## Outputs / 输出

Do not invent experiments, citations, reviewer scores, numeric results, or source claims. / 不得编造实验、引用、审稿分数、数字结果或来源主张.

- `paper/REVIEW_SIMULATION.md` or `paper/GEMINI_REVIEW_ROUND_*.json`
- Revision priority list and explicit blocking issues.

## Workflow / 流程

1. Run structured scoring and regression checks.
2. Detect unsupported claims, weak baselines, evidence gaps.
3. Route for specific fixes to `paper-ai-reviewer` / `paper-ai-rebuttal` helpers.
4. Return clear block/fix matrix to `academic-paper`.

## Gate / 质量门

- Review failures, score regressions, and weak evidence must block pass path. / 评分退化和证据弱化必须阻塞通过。
- Optional suggestions should not force extra mandatory loops without blocking issues.

## Team / Handoff / 团队映射

- Primary owner: `academic-paper-reviewer`.
- Secondary helpers: `paper-ai-reviewer`, `paper-ai-rebuttal`.
- Typical route: `academic-pipeline` for final consolidation.

## Root config / 根配置

Start from root `config.example.yaml`, copy it to ignored local `config.yaml`, then set OpenAI-compatible model fields and Semantic Scholar mode. / 请从根目录 `config.example.yaml` 开始，复制为已忽略的本地 `config.yaml`，再配置 OpenAI-compatible 模型字段与 Semantic Scholar 模式。

## References to load as needed / 按需加载参考

- `references/four-team-reviewer-guide.md`
