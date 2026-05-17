# 🚀 oh_my_paper

> 中文：一个面向 AI / ML 论文全流程的 Codex skills 群与本地写作系统。它从想 idea、组织论文、写各章节、做图表、版面润色，到严格审稿模拟和 rebuttal 防守，形成一个可持续迭代的“写作—审稿—修订”闭环。
>
> English: A local-first Codex skill group and writing system for the full AI/ML paper lifecycle: idea shaping, paper planning, section writing, figures/tables, layout polish, strict reviewer simulation, rebuttal defense, and continuous eval-driven improvement.

**oh_my_paper is not a magic one-click paper generator.** It is a structured agent workflow that helps a long-context Codex-style assistant keep paper context consistent, enforce evidence discipline, and revise under reviewer pressure.

**oh_my_paper 不是“无脑一键发论文”。** 它更像一个论文写作 harness：把长上下文写作、材料内化、claim/evidence 管理、严格审稿、失败反馈和系统演化连成一套可执行流程。

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

## ✨ 当前系统能力 / Current system

- 🧠 **13 个自然论文流程 skills / 13 natural paper workflow skills** under `skills/paper-ai-*`.
- 📚 **材料内化 references / material-derived references**: each skill carries case cards, source-derived examples, bad/good contrasts, and imitation recipes.
- 🧾 **Claim/Evidence artifacts**: `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl` keep claims, evidence, and workflow trace visible.
- 🔍 **Evidence gate**: unsupported or inconsistent claims are flagged before they become polished prose.
- 📝 **Full-paper generation from PDF**: `generate-paper` extracts a local PDF, drafts a complete paper, repairs structural incompleteness, and writes paper artifacts.
- 🧑‍⚖️ **Gemini-compatible strict reviewer gate**: `review-paper` and the `generate-paper --max-review-rounds` loop use a hostile reviewer prompt through the local `.env` OpenAI-compatible endpoint.
- 🔁 **Reviewer-driven revision loop**: failed review JSON can trigger automatic revision, overclaim sanitization, and another review round.
- 🌐 **联网上下文可接入 / web context can be injected**: recent related-work notes can be passed with `--related-context` while raw collection stays local.
- 🔒 **Local-only material policy**: raw PDFs, private notes, credentials, and generated stress-test outputs stay under ignored folders such as `materials/`, `temp/`, and `.env`.
- 📦 **Official Codex skill-installer compatible packaging**: skill folders are installable by path through the official installer pattern.

## 🧭 Skills / 技能地图

The public skill surface follows the paper lifecycle rather than many tiny management skills. The OMX-like depth lives inside each skill as gates, references, checklists, handoffs, and eval discipline.

| Stage / 阶段 | Skill | Purpose / 用途 |
| --- | --- | --- |
| 🧭 全流程路由 | `paper-ai-orchestrator` | Route the writing task and coordinate handoffs between skills. |
| 💡 Idea / 选题 | `paper-ai-idea` | Sharpen research question, contribution, novelty, and evidence pressure. |
| ✍️ Whole-paper writing / 全文一致性 | `paper-ai-writing` | Keep story, claims, sections, and evidence aligned. |
| 🏷️ Title + Abstract / 标题摘要 | `paper-ai-title-abstract` | Optimize first impression, searchability, and claim discipline. |
| 🚪 Introduction / 引言 | `paper-ai-introduction` | Build motivation, gap, contribution, and reader momentum. |
| 🧾 Related Work / 相关工作 | `paper-ai-related-work` | Position against prior work without becoming a literature dump. |
| ⚙️ Method / 方法 | `paper-ai-method` | Explain the method from intuition to formal detail. |
| 🧪 Experiments / 实验 | `paper-ai-experiments` | Design evidence, ablations, comparisons, and result narrative. |
| 📊 Figures + Tables / 图表 | `paper-ai-figures` | Make visuals claim-linked, readable, and reviewer-friendly. |
| ⚠️ Limitations / 局限性 | `paper-ai-limitations` | State boundaries without destroying the contribution. |
| 🧩 Layout + Polish / 排版润色 | `paper-ai-layout` | Improve page budget, flow, readability, and final polish. |
| 🧑‍⚖️ Reviewer / 审稿模拟 | `paper-ai-reviewer` | Stress-test the paper from reviewer/AC perspective. |
| 🛡️ Rebuttal / 辩护 | `paper-ai-rebuttal` | Draft grounded rebuttals and safe revision promises. |

## 🏗️ Architecture / 架构

oh_my_paper has two compatible delivery modes:

1. 🖥️ **Local installed skills mode / 本机 skills 模式**
   - Install selected `skills/paper-ai-*` into the user's Codex skills directory.
   - Work inside a local paper workspace.
   - Keep artifacts such as `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl` close to the draft.

2. 🌐 **Codex App Server mode / Codex App Server 模式**
   - The same skill logic, trace semantics, gates, and approvals can be driven by an App Server adapter.
   - The repo includes a mocked adapter boundary so event/gate behavior can be tested before real deployment.

The current CLI provides the executable local harness: artifact validation, evidence gates, toy demos, full-paper PDF drafting, Gemini-compatible review, reviewer-conditioned revision, fixture capture, and eval reports.

## ⚡ Quick start / 快速开始

This project uses **uv**. Use `uv run`, not conda-style commands.

```bash
uv run oh-my-paper status
uv run oh-my-paper packaging-status
```

Run a deterministic toy workflow:

```bash
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
```

Validate paper workspace artifacts:

```bash
uv run oh-my-paper validate-artifacts examples/toy-paper-workspace
uv run oh-my-paper evidence-gate examples/toy-paper-workspace  # expected fail: synthetic C3 is unsupported
uv run oh-my-paper run-eval tests/fixtures/evals/unsupported_claim.jsonl
```

Generate and review a full paper from a local PDF:

```bash
uv run oh-my-paper generate-paper \
  /path/to/source-paper.pdf \
  /tmp/ohmp-paper-run \
  --env-file /root/wirting_skills/.env \
  --related-context /tmp/related_context.md \
  --max-review-rounds 4
```

Review or revise an existing draft:

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

## 🧑‍⚖️ Reviewer-pressure loop / 审稿压力闭环

The strict review loop is intentionally harsh:

- requires all paper sections to exist;
- rejects unsupported empirical claims;
- flags vague baselines, missing ablations, weak latency accounting, fragile evidence keys, and overclaims;
- produces structured JSON review output;
- can feed that review back into the revision agent;
- only accepts the run when local structure checks, trace checks, artifact checks, and reviewer verdict align.

The system has already been stress-tested on a full PDF input under this loop. A successful run must produce `ok: true` with:

```json
{
  "trace_ok": true,
  "section_ok": true,
  "reviewer_verdict": "PASS",
  "reviewer_score": 8,
  "ok": true
}
```

## 🔒 Materials and privacy / 材料与隐私

Raw references and generated stress-test outputs are local-only by default:

- `materials/`
- `temp/`
- `.env`
- `config.yaml`
- `.omx/`
- `.spec-workflow/`

New material should follow this loop:

1. 📥 put/download source material into `temp/` or `materials/`;
2. 🔎 extract and classify locally;
3. 🧠 fuse lessons into skill references, case cards, checklists, prompts, or eval fixtures;
4. ✅ validate skills and tests;
5. 🚫 keep raw local material and credentials out of git.

## 📦 Installing skills / 安装 skills

Packaging follows the official Codex `skill-installer` standard. Use this repo's skill folders as install paths:

```bash
uv run oh-my-paper packaging-status

install-skill-from-github.py \
  --repo MAC-AutoML/oh_my_paper \
  --path skills/paper-ai-orchestrator \
  --path skills/paper-ai-writing \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal
```

Install any subset of `skills/paper-ai-*` depending on the workflow surface you want.

## 📚 Docs / 文档

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

## ✅ Development checks / 开发检查

```bash
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run python scripts/validate_m1_skeleton.py
uv run --with pyyaml python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/paper-ai-orchestrator
uv run oh-my-paper packaging-status
```

Before pushing, confirm ignored local material is not tracked:

```bash
git ls-files materials temp .omx .spec-workflow node_modules package-lock.json package.json .venv .env config.yaml
```

Expected output: empty.
