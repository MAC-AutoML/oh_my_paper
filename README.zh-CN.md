<p align="center">
  <h1 align="center">🚀 oh_my_paper</h1>
  <p align="center">
    面向 AI / ML 论文全流程的 Codex skills 群与本地写作 harness：写作、审稿、修订、rebuttal、持续进化。
  </p>
  <p align="center">
    <a href="README.md">English README</a> ·
    <a href="#快速开始">快速开始</a> ·
    <a href="#技能地图">技能地图</a> ·
    <a href="#审稿压力闭环">审稿压力闭环</a>
  </p>
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB.svg?logo=python&logoColor=white">
    <img alt="uv" src="https://img.shields.io/badge/Package%20Manager-uv-654FF0.svg">
    <img alt="Codex Skills" src="https://img.shields.io/badge/Codex-Skills-111827.svg">
    <img alt="Paper AI" src="https://img.shields.io/badge/Paper-AI-2ECC71.svg">
    <img alt="Reviewer Gate" src="https://img.shields.io/badge/Reviewer--Gate-Gemini--Compatible-F39C12.svg">
    <img alt="Privacy" src="https://img.shields.io/badge/Raw%20Materials-Local--Only-E74C3C.svg">
  </p>
</p>

---

**oh_my_paper** 是一个本地优先的论文写作系统，覆盖 AI / ML 论文从 idea、planning、分章节写作、图表、排版润色，到严格审稿模拟、rebuttal 防守和 eval 驱动持续改进的完整链路。

它不是“无脑一键发论文”。它更像一个论文写作 harness：帮助长上下文 Codex-style agent 保持论文上下文一致，强制 claim/evidence 纪律，并在 reviewer pressure 下持续修订。

```text
💡 idea / research question
  → 🧭 paper plan + claims/evidence map
  → ✍️ section-by-section writing
  → 📊 figures, tables, experiments, layout
  → 🧑‍⚖️ strict reviewer simulation
  → 🛠️ revision under reviewer pressure
  → 🛡️ rebuttal / defense
  → 🔁 captured failures become future evals and skill improvements
```

## 当前能力

- 🧠 **13 个自然论文流程 skills**，位于 `skills/paper-ai-*`。
- 📚 **材料内化 references**：每个 skill 内置 case card、原材料启发案例、bad/good 对照、模仿配方。
- 🧾 **Claim/Evidence artifacts**：`CLAIMS.md`、`EVIDENCE_MAP.md`、`.paper-ai/TRACE.jsonl` 显式记录 claim、证据和流程轨迹。
- 🔍 **Evidence gate**：在 unsupported / inconsistent claims 被写成漂亮废话之前拦截。
- 📝 **PDF 生成完整论文**：`generate-paper` 可抽取本地 PDF，生成完整论文，修补结构不完整，并写出 paper artifacts。
- 🧑‍⚖️ **Gemini-compatible strict reviewer gate**：通过本地 `.env` 里的 OpenAI-compatible endpoint 调用严格 reviewer prompt。
- 🔁 **Reviewer-driven revision loop**：失败的 review JSON 会反向驱动自动修订、overclaim sanitizer 和下一轮审稿。
- 🌐 **可注入联网/新近上下文**：通过 `--related-context` 注入 recent related-work notes，原始收集材料仍保持本地。
- 🔒 **本地材料隐私策略**：原始 PDF、私有笔记、密钥、生成测试输出都默认 gitignored。
- 📦 **兼容官方 Codex skill-installer**：按 repo path 安装 skill folders。

## 技能地图

公开 skills 按论文生命周期组织，而不是拆成很多管理型 micro-skills。OMX-like 深度体现在每个 skill 内部的 gates、references、checklists、handoffs 和 eval discipline。

| 阶段 | Skill | 用途 |
| --- | --- | --- |
| 🧭 全流程路由 | `paper-ai-orchestrator` | 路由写作任务，协调 skill handoff。 |
| 💡 选题 / Idea | `paper-ai-idea` | 打磨 research question、contribution、novelty 和 evidence pressure。 |
| ✍️ 全文写作 | `paper-ai-writing` | 保持 story、claims、sections、evidence 一致。 |
| 🏷️ 标题摘要 | `paper-ai-title-abstract` | 优化第一印象、可检索性和 claim discipline。 |
| 🚪 引言 | `paper-ai-introduction` | 建立 motivation、gap、contribution 和阅读推进。 |
| 🧾 相关工作 | `paper-ai-related-work` | 定位 prior work，避免 literature dump。 |
| ⚙️ 方法 | `paper-ai-method` | 从直觉到形式化细节解释方法。 |
| 🧪 实验 | `paper-ai-experiments` | 设计 evidence、ablation、comparison 和 result narrative。 |
| 📊 图表 | `paper-ai-figures` | 让图表 claim-linked、readable、reviewer-friendly。 |
| ⚠️ 局限性 | `paper-ai-limitations` | 说明边界但不摧毁贡献。 |
| 🧩 排版润色 | `paper-ai-layout` | 改善页数预算、flow、readability 和 final polish。 |
| 🧑‍⚖️ 审稿模拟 | `paper-ai-reviewer` | 从 reviewer / AC 视角压力测试论文。 |
| 🛡️ Rebuttal | `paper-ai-rebuttal` | 起草 grounded rebuttal 和安全 revision promises。 |

## 架构

oh_my_paper 有两种兼容交付模式：

1. 🖥️ **本机 installed skills 模式**
   - 将 `skills/paper-ai-*` 安装到用户 Codex skills 目录。
   - 在本地 paper workspace 中工作。
   - `CLAIMS.md`、`EVIDENCE_MAP.md`、`.paper-ai/TRACE.jsonl` 与草稿一起维护。

2. 🌐 **Codex App Server 模式**
   - 同一套 skill logic、trace semantics、gates 和 approvals 可以由 App Server adapter 驱动。
   - 当前 repo 包含 mocked adapter boundary，用于先验证 event/gate behavior。

当前 CLI 是可执行的本地 harness：artifact validation、evidence gate、toy demo、PDF full-paper drafting、Gemini-compatible review、reviewer-conditioned revision、fixture capture 和 eval report。

## 快速开始

项目使用 **uv**。请使用 `uv run`，不要用 conda-style 命令。

```bash
uv run oh-my-paper status
uv run oh-my-paper packaging-status
```

运行 deterministic toy workflow：

```bash
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
```

验证 paper workspace artifacts：

```bash
uv run oh-my-paper validate-artifacts examples/toy-paper-workspace
uv run oh-my-paper evidence-gate examples/toy-paper-workspace  # expected fail: synthetic C3 is unsupported
uv run oh-my-paper run-eval tests/fixtures/evals/unsupported_claim.jsonl
```

从本地 PDF 生成并审稿：

```bash
uv run oh-my-paper generate-paper \
  /path/to/source-paper.pdf \
  /tmp/ohmp-paper-run \
  --env-file /root/wirting_skills/.env \
  --related-context /tmp/related_context.md \
  --max-review-rounds 4
```

审稿或修订已有草稿：

```bash
uv run oh-my-paper review-paper /tmp/ohmp-paper-run/paper/FULL_PAPER_DRAFT.md \
  --env-file /root/wirting_skills/.env \
  --output /tmp/ohmp-paper-run/paper/GEMINI_REVIEW.json

uv run oh-my-paper revise-paper \
  /tmp/ohmp-paper-run/paper/FULL_PAPER_DRAFT.md \
  /tmp/ohmp-paper-run/paper/GEMINI_REVIEW.json \
  /tmp/ohmp-paper-run/paper/FULL_PAPER_DRAFT_REVISED.md \
  --env-file /root/wirting_skills/.env
```

## 审稿压力闭环

严格审稿 loop 会：

- 要求论文 section 完整；
- 拒绝 unsupported empirical claims；
- 标记 vague baselines、missing ablations、weak latency accounting、fragile evidence keys 和 overclaims；
- 输出结构化 JSON review；
- 将 review 反喂给 revision agent；
- 只有 local structure checks、trace checks、artifact checks 和 reviewer verdict 同时通过时才接受。

成功运行应产生类似结果：

```json
{
  "trace_ok": true,
  "section_ok": true,
  "reviewer_verdict": "PASS",
  "reviewer_score": 8,
  "ok": true
}
```

## 材料与隐私

原始材料和生成的压力测试输出默认只保存在本地：

- `materials/`
- `temp/`
- `.env`
- `config.yaml`
- `.omx/`
- `.spec-workflow/`

新材料建议流程：

1. 📥 放入或下载到 `temp/` / `materials/`；
2. 🔎 本地抽取和分类；
3. 🧠 融合进 skill references、case cards、checklists、prompts 或 eval fixtures；
4. ✅ 运行 skills/tests 验证；
5. 🚫 不把原始本地材料和 credentials 提交到 git。

## 安装 skills

遵循官方 Codex `skill-installer` 标准，使用 repo skill folders 作为安装 path：

```bash
uv run oh-my-paper packaging-status

install-skill-from-github.py \
  --repo MAC-AutoML/oh_my_paper \
  --path skills/paper-ai-orchestrator \
  --path skills/paper-ai-writing \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal
```

可以按需求安装任意 `skills/paper-ai-*` 子集。

## 文档

- [`README.md`](README.md) — English README.
- [`docs/00_OVERVIEW.md`](docs/00_OVERVIEW.md) — design index and source-of-truth map.
- [`docs/PRD.md`](docs/PRD.md) — product requirements.
- [`docs/SKILL_GROUP_ARCHITECTURE.md`](docs/SKILL_GROUP_ARCHITECTURE.md) — skill boundaries, handoffs, artifacts, gates.
- [`docs/DUAL_MODE_TECH_DESIGN.md`](docs/DUAL_MODE_TECH_DESIGN.md) — local skills vs App Server runtime design.
- [`docs/HARNESS_EVAL_LOOP.md`](docs/HARNESS_EVAL_LOOP.md) — trace/eval/continuous-improvement loop.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — roadmap and sequencing.
- [`docs/REPO_STRUCTURE_SPEC.md`](docs/REPO_STRUCTURE_SPEC.md) — repository structure contract.
- [`docs/ACCEPTANCE_EVALS.md`](docs/ACCEPTANCE_EVALS.md) — acceptance checks and future eval fixture shapes.
- [`docs/MATERIALS_MAPPING.md`](docs/MATERIALS_MAPPING.md) — local material mapping without publishing raw materials.
- [`docs/MATERIAL_INTAKE_WORKFLOW.md`](docs/MATERIAL_INTAKE_WORKFLOW.md) — how new PDFs/repos/notes get fused into skills.
- [`docs/LOCAL_PUSH_NOTES.md`](docs/LOCAL_PUSH_NOTES.md) — local push workflow notes for this development environment.

## 开发检查

```bash
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run python scripts/validate_m1_skeleton.py
uv run --with pyyaml python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/paper-ai-orchestrator
uv run oh-my-paper packaging-status
```

推送前确认本地材料没有被追踪：

```bash
git ls-files materials temp .omx .spec-workflow node_modules package-lock.json package.json .venv .env config.yaml
```

期望输出为空。
