# 🚀 oh_my_paper

**oh my paper** is a local-first Codex skill group for building better AI research papers with evidence, iteration, and review pressure built in.

It is **not** a magic one-click paper generator. It is a practical workflow system for moving from idea to paper sections, figures/tables, layout polish, reviewer simulation, and rebuttal defense — with a harness-style loop that can keep improving as new writing/review materials arrive.

```text
💡 idea/results
  → 🧭 paper plan + claims/evidence map
  → ✍️ section writing
  → 📊 figures/tables
  → 🧩 layout + polish
  → 🧑‍⚖️ reviewer simulation
  → 🛠️ fix plan
  → 🛡️ rebuttal/defense
  → 🔁 eval-driven skill evolution
```

## ✨ What is in this repo now

- 🧠 **13 natural paper workflow skills** under `skills/paper-ai-*`.
- 📚 **Material-derived references** inside each skill: case cards, examples, bad/good contrasts, and imitation recipes distilled from the local material library.
- 🔒 **Local-only material intake**: raw PDFs/repos/notes stay under ignored `materials/` and `temp/`.
- ✅ **Executable validators and gates** for claims, evidence maps, trace integrity, packaging status, and synthetic eval fixtures.
- 🔁 **Harness flywheel prototype** for capturing risky runs into future regression fixtures.
- 🧱 **Dual-mode design** for both local installed Codex skills and future Codex App Server integration.

## 🧭 Skill map

The skill group intentionally follows the natural paper lifecycle instead of exposing too many management-style micro-skills. OMX-style depth is internalized as gates, references, checklists, and trace/eval discipline inside each stage.

| Stage | Skill | Purpose |
| --- | --- | --- |
| 🧭 Full workflow routing | `paper-ai-orchestrator` | Choose the right paper workflow path and hand off between skills. |
| 💡 Idea / research question | `paper-ai-idea` | Sharpen idea, contribution, novelty, and evidence pressure. |
| ✍️ Whole-paper coherence | `paper-ai-writing` | Keep claims, story, sections, and evidence aligned. |
| 🏷️ Title + abstract | `paper-ai-title-abstract` | Optimize first impression, searchability, and claim discipline. |
| 🚪 Introduction | `paper-ai-introduction` | Build motivation, gap, contribution, and reader momentum. |
| 🧾 Related work | `paper-ai-related-work` | Position against prior work without turning into a literature dump. |
| ⚙️ Method | `paper-ai-method` | Explain the method from intuition to formal detail. |
| 🧪 Experiments / results | `paper-ai-experiments` | Design evidence, ablations, comparisons, and result narrative. |
| 📊 Figures and tables | `paper-ai-figures` | Make visuals claim-linked, readable, and reviewer-friendly. |
| ⚠️ Limitations / caveats | `paper-ai-limitations` | State boundaries without weakening the contribution. |
| 🧩 Layout + language polish | `paper-ai-layout` | Improve page budget, flow, readability, and final polish. |
| 🧑‍⚖️ Strict review simulation | `paper-ai-reviewer` | Stress-test the paper from reviewer/AC perspective. |
| 🛡️ Rebuttal / defense | `paper-ai-rebuttal` | Draft grounded rebuttals and safe revision promises. |

## 🏗️ Architecture at a glance

Two delivery modes share the same skill knowledge, artifacts, gates, and eval loop:

1. 🖥️ **Local installed skills mode**
   - Skills are installed into the user's Codex skill directory.
   - The user works inside a paper workspace with local artifacts such as `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl`.
   - The CLI provides deterministic checks and toy demos.

2. 🌐 **Codex App Server mode**
   - A future adapter drives the same workflows through App Server events, approvals, and thread state.
   - The current repo includes a mocked App Server boundary so the event/gate/eval semantics can be tested before real integration.

## 📚 Design docs

Start here:

- [`docs/00_OVERVIEW.md`](docs/00_OVERVIEW.md) — design index and source-of-truth map.
- [`docs/PRD.md`](docs/PRD.md) — product requirements.
- [`docs/SKILL_GROUP_ARCHITECTURE.md`](docs/SKILL_GROUP_ARCHITECTURE.md) — skill boundaries, handoffs, artifacts, gates.
- [`docs/DUAL_MODE_TECH_DESIGN.md`](docs/DUAL_MODE_TECH_DESIGN.md) — local skills vs App Server runtime design.
- [`docs/HARNESS_EVAL_LOOP.md`](docs/HARNESS_EVAL_LOOP.md) — trace/eval/continuous-improvement loop.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — milestone order.
- [`docs/REPO_STRUCTURE_SPEC.md`](docs/REPO_STRUCTURE_SPEC.md) — repository structure contract.
- [`docs/ACCEPTANCE_EVALS.md`](docs/ACCEPTANCE_EVALS.md) — acceptance checks and future eval fixture shapes.
- [`docs/MATERIALS_MAPPING.md`](docs/MATERIALS_MAPPING.md) — local material mapping without publishing raw materials.
- [`docs/MATERIAL_INTAKE_WORKFLOW.md`](docs/MATERIAL_INTAKE_WORKFLOW.md) — how new PDFs/repos/notes get fused into skills.
- [`docs/LOCAL_PUSH_NOTES.md`](docs/LOCAL_PUSH_NOTES.md) — local push workflow notes for this development environment.

Local OMX planning artifacts such as `.omx/plans/ralplan-oh-my-paper-design.md` are intentionally gitignored.

## 🔒 Material policy

Raw references live under ignored local folders:

- `materials/`
- `temp/`

Public commits should contain only curated design docs, source code, examples, eval fixtures, and selected skill references that are safe to publish. New material should follow this loop:

1. 📥 place/download source material into `temp/` or `materials/`;
2. 🔎 extract/classify it locally;
3. 🧠 fuse the lessons into skill references, case cards, checklists, or eval fixtures;
4. ✅ validate skills and tests;
5. 🚫 keep raw materials out of git.

## ⚡ Quick start

This project uses **uv** for Python management.

```bash
uv run oh-my-paper status
uv run oh-my-paper packaging-status
```

Run the deterministic toy workflow:

```bash
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
```

Validate the toy workspace artifacts:

```bash
uv run oh-my-paper validate-artifacts examples/toy-paper-workspace
uv run oh-my-paper evidence-gate examples/toy-paper-workspace  # expected fail: synthetic C3 is unsupported
uv run oh-my-paper run-eval tests/fixtures/evals/unsupported_claim.jsonl
```

## 📦 Installing skills

Packaging follows the official Codex `skill-installer` standard. Use the repo's skill folders as install paths:

```bash
uv run oh-my-paper packaging-status

# Example official installer usage:
install-skill-from-github.py \
  --repo MAC-AutoML/oh_my_paper \
  --path skills/paper-ai-orchestrator \
  --path skills/paper-ai-writing \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal
```

Install any subset of `skills/paper-ai-*` depending on the workflow surface you want.

## 🧪 Milestones implemented

| Milestone | Status | Highlights |
| --- | --- | --- |
| ✅ M1 Skeleton | Done | Plugin metadata, 13 skill folders, toy workspace. |
| ✅ M2 Validators | Done | `CLAIMS.md`, `EVIDENCE_MAP.md`, trace validation, evidence gate, eval fixtures. |
| ✅ M3 Local MVP | Done | Deterministic `init` and `run-demo` workflow. |
| ✅ M4 Mock App Server | Done | Mock adapter using the same trace/gate/eval semantics. |
| ✅ M5 Harness flywheel | Done | Fixture capture, eval reports, harness changelog. |
| ✅ M6 Packaging | Done | Official Codex skill-installer-compatible packaging metadata. |

Relevant milestone notes:

- [`docs/MILESTONE1_SKELETON.md`](docs/MILESTONE1_SKELETON.md)
- [`docs/MILESTONE2_ARTIFACTS.md`](docs/MILESTONE2_ARTIFACTS.md)
- [`docs/MILESTONE3_LOCAL_MVP.md`](docs/MILESTONE3_LOCAL_MVP.md)
- [`docs/MILESTONE4_APP_SERVER_ADAPTER.md`](docs/MILESTONE4_APP_SERVER_ADAPTER.md)
- [`docs/MILESTONE5_HARNESS_FLYWHEEL.md`](docs/MILESTONE5_HARNESS_FLYWHEEL.md)
- [`docs/MILESTONE6_PACKAGING.md`](docs/MILESTONE6_PACKAGING.md)

## ✅ Development checks

```bash
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run python scripts/validate_m1_skeleton.py
uv run --with pyyaml python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/paper-ai-orchestrator
```

Before pushing, also confirm ignored local material is not tracked:

```bash
git ls-files materials temp .omx .spec-workflow node_modules package-lock.json package.json .venv .env config.yaml
```

Expected output: empty.
