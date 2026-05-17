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
| Codex Skills installer | Official `install-skill-from-github.py` path-based installer | Installs selected top-level and helper skill folders. |
| API endpoint | `.env` supports `OPENAI_API_KEY`; review/generation flows expect an OpenAI-compatible endpoint such as `https://automl.aiserverai.online/v1` when model calls are enabled | Powers full-paper generation, strict review, and revision loops. |
| LaTeX | Local `latexmk`, `xelatex`, and `bibtex` are available in this workspace | Optional PDF compilation for `paper-ai-latex` / `compile-latex`. |
| Semantic Scholar | `.env` supports `s2_api_key`; keyed mode sends it as `x-api-key` | Verifies citation existence and metadata with the official Graph API. |
| Node.js / npm | Local Node.js `v22.14.0`, npm `10.9.2` | Needed only for Node-based tooling such as Playwright-backed utilities. |
| npm package | Local `package.json` declares `playwright ^1.60.0` | Optional browser/automation dependency for local tooling. |

Python package metadata currently has no runtime third-party Python dependencies beyond the project package itself.

## Configure first

Start from the root template:

```bash
cp config.example.yaml config.yaml
uv run oh-my-paper config-status --config config.yaml
```

`config.yaml` is ignored by git. Configure OpenAI-compatible model fields there or through environment variables such as `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, and `OPENAI_REVIEWER_MODEL`. The example `.env` keeps the relay URL explicit: `https://automl.aiserverai.online/v1`.

Semantic Scholar citation verification supports four modes in `config.example.yaml`:

- `auto`: use `s2_api_key` when present, otherwise fall back to no-key mode.
- `api_key`: require the configured API key environment variable.
- `no_key`: call the public endpoint without a key; this is slower and should rely on cache reuse.
- `disabled`: skip live verification and mark checks honestly as skipped.

Semantic Scholar allows one request per second across endpoints. Keep `request_interval_seconds_api_key` at or above `1.1` unless you know you are fully cache-bound.

## Highlights

- 🧠 **4 user-facing top-level skills** and **15 helper skills** are available.
- 📚 **Material-derived references** inside each skill: case cards, source-derived examples, bad/good contrasts, and imitation recipes.
- 🧾 **Claim/Evidence artifacts**: `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl` keep claims, evidence, and workflow trace visible.
- 🔍 **Evidence gate**: unsupported or inconsistent claims are flagged before they become polished prose.
- 📝 **Full-paper generation from PDF**: `generate-paper` extracts a local PDF, drafts a complete paper, repairs structural incompleteness, and writes paper artifacts.
- 🧑‍⚖️ **Gemini-compatible strict reviewer gate**: `review-paper` and `generate-paper --max-review-rounds` use a hostile reviewer prompt through a local `.env` OpenAI-compatible endpoint.
- 🔁 **Reviewer-driven revision loop**: failed review JSON can trigger automatic revision, overclaim sanitization, and another review round.
- 🌐 **Injectable web/recent context**: pass recent related-work notes with `--related-context` while keeping raw collection local.
- 🔒 **Local-only material policy**: raw PDFs, private notes, credentials, and generated stress-test outputs stay ignored.
- 📦 **Official Codex skill-installer compatible packaging**: skill folders are installable by path through the official installer pattern.
- 🧾 **Built-in LaTeX export**: `paper-ai-latex` bundles an arXiv-style template, manages BibTeX, and compiles with XeLaTeX/BibTeX when local TeX tools are available.
- 🖼️ **Demo figures are generated**: `demo/figures/generated/*.jpg` contains Nano Banana 2 / `gemini-3.1-flash-image-preview` outputs created from the figure prompt cards.

## Skills

The public skill surface follows the paper lifecycle rather than many tiny management skills. Depth lives inside each skill as gates, references, checklists, handoffs, Codex subagent recipes, and eval discipline.

| Stage | Skill | Purpose |
| --- | --- | --- |
| 🧭 Research & evidence strategy | `deep-research` | Drive literature scoping, source grading, citation checks, and evidence passports. |
| ✍️ Core manuscript | `academic-paper` | Do end-to-end planning and whole-paper writing with section discipline. |
| 🧪 Reviewer simulation | `academic-paper-reviewer` | Run strict review, anti-sycophancy checks, and revision routing. |
| 🧭 Workflow orchestration | `academic-pipeline` | Orchestrate research → writing → review → integrity closure. |
| 🧾 LaTeX packaging | `paper-ai-latex` | Copy the built-in arXiv-style template, map sections, maintain BibTeX, and compile PDFs when TeX tools are installed. |

## Architecture

oh_my_paper has two compatible delivery modes:

1. 🖥️ **Local installed skills mode**
   - Install selected top-level and helper skills into the user's Codex skills directory.
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


Compile a LaTeX paper workspace with the bundled arXiv-style template:

```bash
# after preparing a LaTeX workspace from sections/references
uv run oh-my-paper compile-latex /tmp/ohmp-paper-run/latex
```

The LaTeX skill asset is adapted from `MAC-AutoML/Arxiv_Template`; the bundled copy excludes the removed university logo asset and header reference.

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
  --path skills/paper-ai-latex \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal
```

Install any subset of the top-level + helper skill surface depending on your workflow.

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
