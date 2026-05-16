# oh my paper Design Overview

## Status

- Product name: `oh my paper`.
- Current phase: design-first planning package.
- Source requirement artifact: `.omx/specs/deep-interview-oh-my-paper-skill-group.md`.
- Local material cache: `materials/` *(gitignored; do not publish raw contents)*.
- Planning target: ready for implementation planning via `$ralplan`, `$ralph`, `$team`, or `$ultragoal` after review.

## Problem statement

AI-paper work is not one task. It is a chain of research judgment, evidence management, writing, visual design, formatting, reviewer modeling, revision, rebuttal, and continuous learning. Current prompts tend to be isolated: one prompt writes an abstract, another checks grammar, another drafts a rebuttal. `oh my paper` should instead provide a **skill group** that keeps state, artifacts, evidence, gates, and evaluations across the full lifecycle.

## Product principle

The system should be useful because it is **stage-gated and evidence-aware**, not because it pretends to generate a publishable paper in one click.

## Design deliverables

| Deliverable | File | Purpose |
| --- | --- | --- |
| PRD | `docs/PRD.md` | Product goal, users, scenarios, non-goals, requirements |
| Skill architecture | `docs/SKILL_GROUP_ARCHITECTURE.md` | Skill names, responsibilities, handoffs, artifact contracts |
| Dual-mode design | `docs/DUAL_MODE_TECH_DESIGN.md` | Local installed skills and Codex App Server modes |
| Harness/eval loop | `docs/HARNESS_EVAL_LOOP.md` | Trace schema, eval fixtures, regression loop, human gates |
| Roadmap | `docs/ROADMAP.md` | Milestones from design package to implementation |
| Repo skeleton | `docs/REPO_STRUCTURE_SPEC.md` | Future tracked files/directories and ignored local caches |
| Acceptance/evals | `docs/ACCEPTANCE_EVALS.md` | Testable acceptance criteria and future eval shapes |
| Materials mapping | `docs/MATERIALS_MAPPING.md` | Which local materials inform each skill |
| Milestone 2 artifacts | `docs/MILESTONE2_ARTIFACTS.md` | Executable artifact validators, gates, fixture runner, and CLI checks |
| Milestone 3 local MVP | `docs/MILESTONE3_LOCAL_MVP.md` | Deterministic init/run-demo path across writing, figures, layout, reviewer, rebuttal, and eval-loop |
| Milestone 4 App Server adapter | `docs/MILESTONE4_APP_SERVER_ADAPTER.md` | Mocked JSON-RPC/thread/approval mapping that reuses local artifacts, traces, gates, and eval fixtures |
| Milestone 5 harness flywheel | `docs/MILESTONE5_HARNESS_FLYWHEEL.md` | Capture failed/risky runs into fixtures, run regression reports, and append changelog notes with privacy guards |
| Milestone 6 packaging | `docs/MILESTONE6_PACKAGING.md` | Local skill install/uninstall commands, clean checkout verification, safe config templates, and public material policy |
| ADR | `docs/adr/ADR-0001-design-first-dual-mode.md` | Design decision record |

## Authoritative references

### User-supplied local requirements

- `.omx/specs/deep-interview-oh-my-paper-skill-group.md`
- `materials/paper-ai/README.md`
- `materials/paper-ai/categories/*.md`
- `materials/architecture-references/README.md`
- `materials/architecture-references/paper-ai-skill-group-sketch.md`

### OpenAI/Codex references

- Codex skills docs: <https://developers.openai.com/codex/skills>
- Codex App Server docs: <https://developers.openai.com/codex/app-server>
- Codex harness article: <https://openai.com/index/unlocking-the-codex-harness/>
- Local OpenAI repo cache: `materials/architecture-references/repos/openai-codex/`
- Local Agents SDK docs: `materials/architecture-references/repos/openai-openai-agents-python/docs/`

## Non-goals for this package

- No UI or standalone visual product build.
- No public upload or embedding of the raw `materials/` corpus.
- No claim that the system can produce a high-quality complete paper without human evidence, review, and revision.
- No exhaustive support for all venue templates in v1.

## Stop condition for this phase

This design package is complete when it is actionable for implementation, covers the full workflow, separates local/App Server modes, maps to materials, states risks/non-goals, and defines executable future evals.
