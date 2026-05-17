# oh my paper 工作流指南

oh my paper 是一个独立的 Codex 原生科研写作与研究包。产品入口是 Codex skills、项目内 Codex subagents、可持久化论文 artifacts、本地 validators，以及 OpenAI-compatible API runtime。

## 运行模型

- 通过 Codex skills 安装和使用 `skills/paper-ai-*`。
- 用 `uv run oh-my-paper ...` 做本地 artifact 校验和 API 驱动流程。
- 模型访问使用 OpenAI-compatible endpoint：`OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`。
- Node tooling 只是浏览器自动化等可选能力需要。

## 论文流程意图与 Codex 入口

Slash 风格写法表示用户面对的论文意图。路由工作时使用表中的 owner skill 和 mode。

| 论文流程意图 | Codex owner skill | Mode |
| --- | --- | --- |
| `/paper-plan` | `paper-ai-idea` | academic-paper `plan` |
| `/paper-full` | `paper-ai-orchestrator` | academic-pipeline `pipeline` |
| `/paper-lit-review` | `paper-ai-research` | deep-research `lit-review` |
| `/paper-outline` | `paper-ai-writing` | academic-paper `outline-only` |
| `/paper-abstract` | `paper-ai-title-abstract` | academic-paper `abstract-only` |
| `/paper-revision` | `paper-ai-writing` | academic-paper `revision` |
| `/paper-revision-coach` | `paper-ai-reviewer` | academic-paper `revision-coach` |
| `/paper-citation-check` | `paper-ai-research` | academic-paper `citation-check` |
| `/paper-disclosure` | `paper-ai-layout` | academic-paper `disclosure` |
| `/paper-format-convert` | `paper-ai-layout` | academic-paper `format-convert` |

## Mode 覆盖

机器可读 registry 覆盖全部 25 个 oh my paper modes。每个 mode 都记录一个主 `owner_skill`、可选 `secondary_skills`、预期输出、gates、data access level、状态和下一步动作。

状态含义：

- `implemented`：已有 Codex native route 或 artifact。
- `partial`：已有 route，但 contract 或 validator 还需要补齐。
- `advisory`：已有工作流建议，可执行覆盖后续推进。
- `deferred`：暂时不实现。

## 诚信与校验 artifacts

机器校验的诚信 artifacts 优先使用 JSON：

- `paper/MATERIAL_PASSPORT.json`
- `paper/SPRINT_CONTRACT.json`
- `paper/CLAIM_AUDIT_REPORT.json`
- `paper/CITATION_ANCHOR_AUDIT.json`
- `paper/INTEGRITY_REPORT_STAGE_2_5.json`
- `paper/INTEGRITY_REPORT_FINAL.json`

Markdown 继续用于人类可读的 brief、draft、review 和 summary。
