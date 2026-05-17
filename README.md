<p align="center">
  <h1 align="center">🚀 oh_my_paper</h1>
  <p align="center">
    A Codex-native skill group and local harness for writing, reviewing, revising, and defending AI/ML papers under evidence and reviewer pressure.
  </p>
  <p align="center">
    <a href="README.zh-CN.md">中文 README</a> ·
    <a href="#quick-start">Quick Start</a> ·
    <a href="#skills">Skills</a> ·
    <a href="#reviewer-pressure-loop">Reviewer Loop</a>
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

**oh_my_paper** is a local-first system for the full AI/ML paper lifecycle: idea shaping, paper planning, section writing, figures/tables, layout polish, strict reviewer simulation, rebuttal defense, and continuous eval-driven improvement.

It is **not** a magic one-click paper generator. It is a structured agent workflow that helps a long-context Codex-style assistant keep paper context consistent, enforce evidence discipline, and revise under reviewer pressure.

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

## Runtime and dependency requirements

Put the runtime dependencies in place before installing or using the skills:

| Dependency | Required / observed in this workspace | Purpose |
| --- | --- | --- |
| Python | Project requires `>=3.11`; local uv environment uses Python `3.13.7` | Runs the local `oh-my-paper` CLI and paper workflow harness. |
| uv | Local version `0.9.28` | Python environment and command runner. Use `uv run` / `uv add`; do not use conda-style setup. |
| Codex CLI | Local version `codex-cli 0.129.0` | Hosts and invokes Codex skills. |
| Codex Skills installer | Official `install-skill-from-github.py` path-based installer | Installs selected `skills/paper-ai-*` folders. |
| API endpoint | `.env` supports `OPENAI_API_KEY`; review/generation flows expect an OpenAI-compatible endpoint when model calls are enabled | Powers full-paper generation, strict review, and revision loops. |
| Node.js / npm | Local Node.js `v22.14.0`, npm `10.9.2` | Needed only for Node-based tooling such as Playwright-backed utilities. |
| npm package | Local `package.json` declares `playwright ^1.60.0` | Optional browser/automation dependency for local tooling. |
| oh-my-codex | Local version `v0.17.3` | Optional OMX/Codex orchestration environment used by this workspace. |

Python package metadata currently has no runtime third-party Python dependencies beyond the project package itself.

## Highlights

- 🧠 **13 natural paper workflow skills** under `skills/paper-ai-*`.
- 📚 **Material-derived references** inside each skill: case cards, source-derived examples, bad/good contrasts, and imitation recipes.
- 🧾 **Claim/Evidence artifacts**: `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl` keep claims, evidence, and workflow trace visible.
- 🔍 **Evidence gate**: unsupported or inconsistent claims are flagged before they become polished prose.
- 📝 **Full-paper generation from PDF**: `generate-paper` extracts a local PDF, drafts a complete paper, repairs structural incompleteness, and writes paper artifacts.
- 🧑‍⚖️ **Gemini-compatible strict reviewer gate**: `review-paper` and `generate-paper --max-review-rounds` use a hostile reviewer prompt through a local `.env` OpenAI-compatible endpoint.
- 🔁 **Reviewer-driven revision loop**: failed review JSON can trigger automatic revision, overclaim sanitization, and another review round.
- 🌐 **Injectable web/recent context**: pass recent related-work notes with `--related-context` while keeping raw collection local.
- 🔒 **Local-only material policy**: raw PDFs, private notes, credentials, and generated stress-test outputs stay ignored.
- 📦 **Official Codex skill-installer compatible packaging**: skill folders are installable by path through the official installer pattern.

## Skills

The public skill surface follows the paper lifecycle rather than many tiny management skills. The OMX-like depth lives inside each skill as gates, references, checklists, handoffs, and eval discipline.

| Stage | Skill | Purpose |
| --- | --- | --- |
| 🧭 Workflow routing | `paper-ai-orchestrator` | Route the writing task and coordinate handoffs between skills. |
| 💡 Idea | `paper-ai-idea` | Sharpen research question, contribution, novelty, and evidence pressure. |
| ✍️ Whole-paper writing | `paper-ai-writing` | Keep story, claims, sections, and evidence aligned. |
| 🏷️ Title + Abstract | `paper-ai-title-abstract` | Optimize first impression, searchability, and claim discipline. |
| 🚪 Introduction | `paper-ai-introduction` | Build motivation, gap, contribution, and reader momentum. |
| 🧾 Related Work | `paper-ai-related-work` | Position against prior work without becoming a literature dump. |
| ⚙️ Method | `paper-ai-method` | Explain the method from intuition to formal detail. |
| 🧪 Experiments | `paper-ai-experiments` | Design evidence, ablations, comparisons, and result narrative. |
| 📊 Figures + Tables | `paper-ai-figures` | Make visuals claim-linked, readable, and reviewer-friendly. |
| ⚠️ Limitations | `paper-ai-limitations` | State boundaries without destroying the contribution. |
| 🧩 Layout + Polish | `paper-ai-layout` | Improve page budget, flow, readability, and final polish. |
| 🧑‍⚖️ Reviewer | `paper-ai-reviewer` | Stress-test the paper from reviewer/AC perspective. |
| 🛡️ Rebuttal | `paper-ai-rebuttal` | Draft grounded rebuttals and safe revision promises. |

## Architecture

oh_my_paper has two compatible delivery modes:

1. 🖥️ **Local installed skills mode**
   - Install selected `skills/paper-ai-*` into the user's Codex skills directory.
   - Work inside a local paper workspace.
   - Keep artifacts such as `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl` close to the draft.

2. 🌐 **Codex App Server mode**
   - The same skill logic, trace semantics, gates, and approvals can be driven by an App Server adapter.
   - The repo includes a mocked adapter boundary so event/gate behavior can be tested before real deployment.

The current CLI provides the executable local harness: artifact validation, evidence gates, toy demos, full-paper PDF drafting, Gemini-compatible review, reviewer-conditioned revision, fixture capture, and eval reports.

## Quick Start

This project uses **uv**. Use `uv run`, not conda-style commands.

```bash
uv run oh-my-paper status
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

## Reviewer-pressure loop

The strict review loop is intentionally harsh:

- requires all paper sections to exist;
- rejects unsupported empirical claims;
- flags vague baselines, missing ablations, weak latency accounting, fragile evidence keys, and overclaims;
- produces structured JSON review output;
- can feed that review back into the revision agent;
- only accepts the run when local structure checks, trace checks, artifact checks, and reviewer verdict align.

A successful run must produce `ok: true` with evidence similar to:

```json
{
  "trace_ok": true,
  "section_ok": true,
  "reviewer_verdict": "PASS",
  "reviewer_score": 8,
  "ok": true
}
```

## Materials and privacy

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

## Installing skills

Packaging follows the official Codex `skill-installer` standard. Use this repo's skill folders as install paths:

```bash
install-skill-from-github.py \
  --repo MAC-AutoML/oh_my_paper \
  --path skills/paper-ai-orchestrator \
  --path skills/paper-ai-writing \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal
```

Install any subset of `skills/paper-ai-*` depending on the workflow surface you want.

## Docs

- [`README.zh-CN.md`](README.zh-CN.md) — Chinese README.
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
