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

## 运行环境与依赖要求

安装或使用 skills 前，先确认这些运行依赖：

| 依赖 | 项目要求 / 当前本机版本 | 用途 |
| --- | --- | --- |
| Python | 项目要求 `>=3.11`；当前 uv 环境为 Python `3.13.7` | 运行本地 `oh-my-paper` CLI 与论文 workflow harness。 |
| uv | 当前版本 `0.9.28` | Python 环境与命令运行器。请使用 `uv run` / `uv add`，不要使用 conda-style setup。 |
| Codex CLI | 当前版本 `codex-cli 0.129.0` | 承载并调用 Codex skills。 |
| Codex Skills installer | 官方 `install-skill-from-github.py` path-based installer | 按路径安装选定的主技能与 helper skill 文件夹。 |
| API endpoint | `.env` 支持 `OPENAI_API_KEY`；启用模型调用时，生成、严格审稿和修订流程需要 OpenAI-compatible endpoint | 驱动 full-paper generation、strict review 和 revision loop。 |
| Node.js / npm | 当前 Node.js `v22.14.0`，npm `10.9.2` | 仅在使用 Playwright 等 Node-based tooling 时需要。 |
| npm package | 当前 `package.json` 声明 `playwright ^1.60.0` | 本地浏览器/自动化工具的可选依赖。 |

当前 Python package metadata 除项目自身外，没有声明额外 runtime third-party Python dependencies。

## 先配置

从根目录模板开始：

```bash
cp config.example.yaml config.yaml
uv run oh-my-paper config-status --config config.yaml
```

`config.yaml` 默认被 git 忽略。你可以在这里配置 OpenAI-compatible 模型字段，也可以通过 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`、`OPENAI_REVIEWER_MODEL` 等环境变量提供。

Semantic Scholar 引用核验在 `config.example.yaml` 中支持四种模式：

- `auto`：有 `SEMANTIC_SCHOLAR_API_KEY` 就用 key，否则自动走 no-key。
- `api_key`：要求配置的 API key 环境变量存在。
- `no_key`：无 key 调公共端点；速度较慢，建议依赖 cache。
- `disabled`：跳过 live verification，并诚实标记为 skipped。

## 当前能力

- 🧠 **4 个用户级主技能**与 **14 个 helper 技能**并存，适合不同粒度控制。
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

公开 skills 按论文生命周期组织，而不是拆成很多管理型 micro-skills。深度体现在每个 skill 内部的 gates、references、checklists、handoffs、Codex subagent recipes 和 eval discipline。

| 阶段 | Skill | 用途 |
| --- | --- | --- |
| 🧭 研究与证据策略 | `deep-research` | 文献范围、来源分级、引用核验和 evidence passport。 |
| ✍️ 论文正文 | `academic-paper` | 全文规划、章节写作、双语摘要与证据约束。 |
| 🧪 严格审稿 | `academic-paper-reviewer` | EIC/reviewer 模拟、反阿谀检查和修订路线图。 |
| 🧭 流水线编排 | `academic-pipeline` | 串联 research → writing → review → integrity closure。 |

## 架构

oh_my_paper 有两种兼容交付模式：

1. 🖥️ **本机 installed skills 模式**
   - 将选定主技能与 helper skills 安装到用户 Codex skills 目录。
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
install-skill-from-github.py \
  --repo MAC-AutoML/oh_my_paper \
  --path skills/deep-research \
  --path skills/academic-paper \
  --path skills/academic-paper-reviewer \
  --path skills/academic-pipeline \
  --path skills/paper-ai-orchestrator \
  --path skills/paper-ai-idea \
  --path skills/paper-ai-research \
  --path skills/paper-ai-writing \
  --path skills/paper-ai-title-abstract \
  --path skills/paper-ai-introduction \
  --path skills/paper-ai-related-work \
  --path skills/paper-ai-method \
  --path skills/paper-ai-experiments \
  --path skills/paper-ai-figures \
  --path skills/paper-ai-limitations \
  --path skills/paper-ai-layout \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal
```

可以按需求安装任意主技能与 helper 技能子集。

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
