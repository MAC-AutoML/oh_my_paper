---
name: deep-research
description: 深度文献调研研究（中英文） | Deep research for literature scoping, source grading, citation checks, and evidence passports.
---

# deep-research

## Use when / 适用场景

- Use for initial scoping, systematic evidence review, and research trail design. / 用于研究问题澄清、系统性文献检索与证据链启动。
- Use when a project needs citation grounding before writing. / 当需要在写作前建立可信证据基础时。

## Do not use when / 不适用场景

- Do not invent sources, citations, or experimental outcomes. / 不要伪造来源、引用或结果。
- Do not skip evidence grading / 不要跳过证据可信度分级。

## Inputs / 输入

- `workspace`, existing notes, and `paper-ai-research` handoff artifacts. / 工作区、现有笔记、`paper-ai-research` 交接产物。
- Research question, venue target, and search constraints. / 问题定义、目标 venue 与约束。
- Optional material cache references.

## Outputs / 输出

Do not invent experiments, citations, reviewer scores, numeric results, or source claims. / 不得编造实验、引用、审稿分数、数字结果或来源主张.

- `paper/RESEARCH_BRIEF.md`
- `paper/LITERATURE_CORPUS.json`
- `paper/CITATION_VERIFICATION_REPORT.json`
- Routed handoff note to `paper-ai-research` helpers.

## Workflow / 流程

1. Stabilize the problem scope and evidence scope. / 固定问题范围与证据范围。
2. Route detailed source work to helper skills (`paper-ai-idea`, `paper-ai-research`, `paper-ai-related-work`). / 将详细检索与来源分析交给 helper skills。
3. Track what is supported / ambiguous / missing in the citation layer. / 在证据层记录支持、模糊、缺失。
4. Produce claim-safe passport notes and pass explicit next-step gates.

## Gate / 质量门

- Cannot handoff writing without citation grounding and integrity status notes. / 未完成证据状态标记前不得交接写作。
- Must flag unsupported or ambiguous citations explicitly. / 必须显式标注不支持或待确认的引用。

## Team / Handoff / 团队映射

- Primary owner: `deep-research`.
- Secondary helpers: `paper-ai-idea`, `paper-ai-research`, `paper-ai-related-work`.
- Typical route to: `academic-paper`.

## Root config / 根配置

Start from root `config.example.yaml`, copy it to ignored local `config.yaml`, then set OpenAI-compatible model fields and Semantic Scholar mode. / 请从根目录 `config.example.yaml` 开始，复制为已忽略的本地 `config.yaml`，再配置 OpenAI-compatible 模型字段与 Semantic Scholar 模式。

## References to load as needed / 按需加载参考

- `references/four-team-research-guide.md`
