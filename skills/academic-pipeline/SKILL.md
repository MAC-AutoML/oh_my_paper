---
name: academic-pipeline
description: 论文流程编排与工艺收口（中英文） | Paper workflow orchestration from research to integrity-complete publishable package.
---

# academic-pipeline

## Use when / 适用场景

- Use as the primary workflow starter for full oh my paper papers. / 用于完整论文流程启动与串联。
- Use to resume, summarize, and finalize after section and review loops.

## Do not use when / 不适用场景

- Do not bypass phase gates or omit required artifact checks. / 不得跳过阶段门控或缺少必需 artifacts。

## Inputs / 输入

- Workspace path and selected quality targets.
- Claims/evidence artifacts, existing review rounds, config status.

## Outputs / 输出

Do not invent experiments, citations, reviewer scores, numeric results, or source claims. / 不得编造实验、引用、审稿分数、数字结果或来源主张.

- `paper/INTEGRITY_REPORT_STAGE_2_5.json`
- `paper/INTEGRITY_REPORT_FINAL.json`
- `paper/PIPELINE_SUMMARY.md`
- `paper/REPRO_LOCK.json`
- `paper/CLAIMS.md`, `paper/EVIDENCE_MAP.md` (updated through pipeline ownership).

## Workflow / 流程

1. Route to research (`deep-research`) and writing (`academic-paper`) phases.
2. Trigger reviewer loop (`academic-paper-reviewer`) with revision tracking.
3. Resolve gates (stage 2.5 / 4.5) and finalize with evidence/disclosure readiness.
4. Emit reproducibility summary and package-safe metadata.

## Gate / 质量门

- Required integrity artifacts must exist or pipeline remains incomplete. / 必需完整性 artifacts 不存在则不允许完成。
- No final success without config visibility, trace continuity, and explicit override notes.

## Team / Handoff / 团队映射

- Primary owner: `academic-pipeline`.
- Secondary helpers: `paper-ai-orchestrator` and all helpers via staged handoff.
- Terminal route target: closed `paper` deliverable and review-ready package.

## Root config / 根配置

Start from root `config.example.yaml`, copy it to ignored local `config.yaml`, then set OpenAI-compatible model fields and Semantic Scholar mode. / 请从根目录 `config.example.yaml` 开始，复制为已忽略的本地 `config.yaml`，再配置 OpenAI-compatible 模型字段与 Semantic Scholar 模式。

## References to load as needed / 按需加载参考

- `references/four-team-pipeline-guide.md`
