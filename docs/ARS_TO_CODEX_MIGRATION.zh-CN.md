# ARS 到 Codex 迁移指南

本项目把面向 Claude 的 Academic Research Skills 工作流适配为 Codex 原生包。产品入口是 Codex skills、项目内 Codex subagents、可持久化论文 artifacts、本地 validators，以及 OpenAI-compatible API runtime。

## 运行模型

- 通过 Codex skills 安装和使用 `skills/paper-ai-*`。
- 用 `uv run oh-my-paper ...` 做本地 artifact 校验和 API 驱动流程。
- 模型访问使用 OpenAI-compatible endpoint：`OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`。
- Node tooling 只是浏览器自动化等可选能力需要。

## 旧 ARS 意图 / Codex 等价入口

旧的 slash 风格写法在这里表示“等价意图”。除非后续实现 literal command dispatch，不要把它理解为真实可执行命令。

| 旧 ARS 意图 | Codex owner skill | Mode |
| --- | --- | --- |
| `/ars-plan` | `paper-ai-idea` | academic-paper `plan` |
| `/ars-full` | `paper-ai-orchestrator` | academic-pipeline `pipeline` |
| `/ars-lit-review` | `paper-ai-research` | deep-research `lit-review` |
| `/ars-outline` | `paper-ai-writing` | academic-paper `outline-only` |
| `/ars-abstract` | `paper-ai-title-abstract` | academic-paper `abstract-only` |
| `/ars-revision` | `paper-ai-writing` | academic-paper `revision` |
| `/ars-revision-coach` | `paper-ai-reviewer` | academic-paper `revision-coach` |
| `/ars-citation-check` | `paper-ai-research` | academic-paper `citation-check` |
| `/ars-disclosure` | `paper-ai-layout` | academic-paper `disclosure` |
| `/ars-format-convert` | `paper-ai-layout` | academic-paper `format-convert` |

## Mode 覆盖

机器可读 registry 覆盖全部 25 个 ARS modes。每个 mode 都记录一个主 `owner_skill`、可选 `secondary_skills`、预期输出、gates、data access level、状态和下一步动作。

状态含义：

- `implemented`：已有 Codex-native route 或 artifact。
- `partial`：已有 route，但 contract 或 validator 还需要补齐。
- `advisory`：已有工作流建议， executable parity 后续推进。
- `deferred`：暂时不实现。

## 诚信与校验 artifacts

机器校验的兼容 artifacts 第一阶段使用 JSON：

- `paper/MATERIAL_PASSPORT.json`
- `paper/SPRINT_CONTRACT.json`
- `paper/CLAIM_AUDIT_REPORT.json`
- `paper/CITATION_ANCHOR_AUDIT.json`
- `paper/INTEGRITY_REPORT_STAGE_2_5.json`
- `paper/INTEGRITY_REPORT_FINAL.json`

Markdown 继续用于人类可读的 brief、draft、review 和 summary。
