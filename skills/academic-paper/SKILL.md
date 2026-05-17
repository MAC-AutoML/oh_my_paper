---
name: academic-paper
description: 全流程论文写作（中英文） | End-to-end paper writing workflow with evidence-aware section sequencing.
---

# academic-paper

## Use when / 适用场景

- Use for outline, full-paper drafting, section flow, and bilingual abstract flow. / 用于大纲、全文草拟、章节结构与中英摘要流。
- Use after deep research has produced a stable evidence trail. / 在研究阶段已形成证据链后使用。

## Do not use when / 不适用场景

- Do not write unsupported factual claims. / 不得写入未支撑事实主张。
- Do not bypass section/claim validation before finalization. / 不得在章节与 claim 校验前直接定稿。

## Inputs / 输入

- Research/claim artifacts, `CLAIMS.md`, `EVIDENCE_MAP.md`, review constraints.
- Venue requirements and writing constraints.

## Outputs / 输出

Do not invent experiments, citations, reviewer scores, numeric results, or source claims. / 不得编造实验、引用、审稿分数、数字结果或来源主张.

- `paper/FULL_PAPER_DRAFT.md`
- `paper/EVIDENCE_MAP.md` updates and section-level handoff notes.
- Routed notes to section helpers: title/intro/related/method/experiments/figures/limitations/layout.

## Workflow / 流程

1. Route to helper writing/review skills for each section domain. / 按章节将任务下发到 helper。
2. Enforce claim-evidence links for each critical statement. / 强制关键命题与证据绑定。
3. Preserve bilingual safety constraints and reviewer-readiness.
4. Return to `academic-paper-reviewer` for strict pressure-testing.

## Gate / 质量门

- No final narrative handoff without `trace` / `integrity` continuity. / 没有 trace/完整性连续信息不交付。
- Overclaim suppression + transparent caveats required. / 需抑制过度承诺并保留保留态度。

## Team / Handoff / 团队映射

- Primary owner: `academic-paper`.
- Section helpers: `paper-ai-writing`, `paper-ai-title-abstract`, `paper-ai-introduction`, `paper-ai-related-work`, `paper-ai-method`, `paper-ai-experiments`, `paper-ai-figures`, `paper-ai-limitations`, `paper-ai-layout`.
- Typical route to: `academic-paper-reviewer`.

## Root config / 根配置

Start from root `config.example.yaml`, copy it to ignored local `config.yaml`, then set OpenAI-compatible model fields and Semantic Scholar mode. / 请从根目录 `config.example.yaml` 开始，复制为已忽略的本地 `config.yaml`，再配置 OpenAI-compatible 模型字段与 Semantic Scholar 模式。

## References to load as needed / 按需加载参考

- `references/four-team-writing-guide.md`
