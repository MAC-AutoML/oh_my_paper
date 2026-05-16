# oh_my_paper

`oh my paper` is a design-first project for a modular Codex skill group that supports the AI-paper lifecycle:

```text
idea/results → paper planning → writing → figures/tables → layout → reviewer simulation → fixes → rebuttal/defense → eval-driven improvement
```

The first milestone is **not** a UI product and not a magic one-click paper generator. It is an implementation-ready design package for two delivery modes:

1. **Local installed skills mode** — installable Codex skills running in a user workspace.
2. **Codex App Server mode** — a client/server integration that drives the same workflows through Codex App Server events, approvals, and thread state.

## Design package

Start here:

- [`docs/00_OVERVIEW.md`](docs/00_OVERVIEW.md) — design index and source-of-truth map.
- [`docs/PRD.md`](docs/PRD.md) — product requirements.
- [`docs/SKILL_GROUP_ARCHITECTURE.md`](docs/SKILL_GROUP_ARCHITECTURE.md) — skill boundaries, handoffs, artifacts, gates.
- [`docs/DUAL_MODE_TECH_DESIGN.md`](docs/DUAL_MODE_TECH_DESIGN.md) — local skills vs App Server runtime design.
- [`docs/HARNESS_EVAL_LOOP.md`](docs/HARNESS_EVAL_LOOP.md) — trace/eval/continuous-improvement loop.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — milestone order.
- [`docs/REPO_STRUCTURE_SPEC.md`](docs/REPO_STRUCTURE_SPEC.md) — future repository skeleton.
- [`docs/ACCEPTANCE_EVALS.md`](docs/ACCEPTANCE_EVALS.md) — acceptance checks and future eval fixture shapes.
- [`docs/MATERIALS_MAPPING.md`](docs/MATERIALS_MAPPING.md) — local material mapping without publishing raw materials.

Consensus handoff plan:

- `.omx/plans/ralplan-oh-my-paper-design.md` *(local OMX planning artifact, intentionally gitignored)*

## Local material policy

Raw references live under `materials/` and `temp/` and are intentionally excluded by `.gitignore`. Public commits should contain only curated design docs, source code, examples, and lightweight references that do not copy private or copyrighted material.

Continuous material updates use the local-only intake command documented in [`docs/MATERIAL_INTAKE_WORKFLOW.md`](docs/MATERIAL_INTAKE_WORKFLOW.md). New material is first extracted/classified into the ignored cache, then fused into public skill instructions or synthetic evals only after privacy-safe synthesis.

## Natural paper workflow skills

The installable skill group intentionally stays close to the paper lifecycle instead of exposing many management-style micro-skills. OMX-style depth is internalized as gates, references, checklists, and trace/eval discipline inside these natural skills.

| Stage | Skill |
| --- | --- |
| Full workflow routing | `paper-ai-orchestrator` |
| Idea / research question | `paper-ai-idea` |
| Whole-paper writing coherence | `paper-ai-writing` |
| Title and abstract | `paper-ai-title-abstract` |
| Introduction | `paper-ai-introduction` |
| Related work | `paper-ai-related-work` |
| Method | `paper-ai-method` |
| Experiments / results | `paper-ai-experiments` |
| Figures and tables | `paper-ai-figures` |
| Limitations / caveats | `paper-ai-limitations` |
| Layout and language polish | `paper-ai-layout` |
| Strict review simulation | `paper-ai-reviewer` |
| Rebuttal / defense | `paper-ai-rebuttal` |

Install metadata is generated from the official Codex skill folders under `skills/paper-ai-*`; use `uv run oh-my-paper packaging-status` to print the official `install-skill-from-github.py --repo ... --path ...` command.

## Milestone 1 skeleton

This repository includes the local-first skeleton for the skill group:

- `.codex-plugin/plugin.json` — local plugin metadata.
- `skills/paper-ai-*/` — 13 progressive-disclosure paper workflow skills.
- `examples/toy-paper-workspace/` — synthetic paper workspace for e2e tests.

## Milestone 2 validators and eval fixtures

Milestone 2 adds the first executable artifact checks:

- `src/oh_my_paper/artifacts/` — parsers and schema validators for `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl`.
- `src/oh_my_paper/gates/` — unsupported-claim evidence gate.
- `src/oh_my_paper/evals/` — synthetic JSONL fixture loader and evaluator dispatch.
- `tests/fixtures/evals/` — supported/unsupported claim and trace integrity fixtures.
- [`docs/MILESTONE2_ARTIFACTS.md`](docs/MILESTONE2_ARTIFACTS.md) — implementation notes and verification commands.

Run local checks with:

```bash
uv run oh-my-paper status
uv run oh-my-paper validate-artifacts examples/toy-paper-workspace
uv run oh-my-paper evidence-gate examples/toy-paper-workspace  # expected fail: synthetic C3 is unsupported
uv run oh-my-paper run-eval tests/fixtures/evals/unsupported_claim.jsonl
```

## Milestone 3 local MVP

Milestone 3 adds a deterministic end-to-end local demo path from workspace init to eval report:

```bash
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
```

See [`docs/MILESTONE3_LOCAL_MVP.md`](docs/MILESTONE3_LOCAL_MVP.md).

## Milestone 4 mocked App Server adapter

Milestone 4 adds a mocked App Server runtime boundary that reuses the same trace, gate, approval, and eval semantics:

```bash
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper mock-app-server /tmp/ohmp-demo tests/fixtures/evals/unsupported_claim.jsonl
```

See [`docs/MILESTONE4_APP_SERVER_ADAPTER.md`](docs/MILESTONE4_APP_SERVER_ADAPTER.md).

## Milestone 5 harness flywheel

Milestone 5 captures risky runs as fixtures and writes regression reports/changelog entries:

```bash
uv run oh-my-paper capture-fixture /tmp/ohmp-demo /tmp/captured.jsonl --fixture-id captured_c3 --purpose "capture C3 gate" --privacy redacted
uv run oh-my-paper eval-report /tmp/captured.jsonl --output /tmp/eval-report.md --changelog /tmp/HARNESS_CHANGELOG.md
```

See [`docs/MILESTONE5_HARNESS_FLYWHEEL.md`](docs/MILESTONE5_HARNESS_FLYWHEEL.md).

## Milestone 6 packaging

Milestone 6 aligns packaging with the official Codex `skill-installer` standard. Use the official installer with this repo's skill paths, and use the local CLI only to inspect packaging metadata:

```bash
uv run oh-my-paper packaging-status
# Official installer helper:
install-skill-from-github.py --repo MAC-AutoML/oh_my_paper --path skills/paper-ai-orchestrator --path skills/paper-ai-writing
```

See [`docs/MILESTONE6_PACKAGING.md`](docs/MILESTONE6_PACKAGING.md).
