# Materials Mapping

## 1. Policy

This file maps local materials to design decisions. It does not publish raw material content. Paths under `materials/` are local-only and ignored by git. This tracked document is public-safe: it names material categories and local index paths, but avoids listing private repository names. Maintain detailed private source names only inside ignored `materials/` indexes unless licensing and publication permission are confirmed.

## 2. Paper workflow materials

| Skill / subsystem | Local material sources | Usage |
| --- | --- | --- |
| `paper-ai-research-process` | `materials/paper-ai/categories/research-process.md`; `materials/paper-ai/external/learning-research/index.md`; `materials/paper-ai/external/cwmt14-tut/index.md` | Topic selection, problem framing, experiment planning, research-to-paper pipeline |
| `paper-ai-writing` | `materials/paper-ai/categories/writing.md`; local writing-guide family; awesome AI research writing; CWMT tutorial | Section drafting, reader-centered structure, claim/evidence discipline, polishing |
| `paper-ai-figures` | `materials/paper-ai/categories/figures.md`; local figure-guide family; awesome writing visual prompts; CWMT tutorial | Figure plans, chart choice, captions, visual hierarchy |
| `paper-ai-layout` | CWMT tutorial; writing/figures categories; future venue templates | Page budget, figure/table placement, final formatting checks |
| `paper-ai-reviewer` | `materials/paper-ai/categories/paper-checking.md`; `materials/paper-ai/categories/review-rating.md`; local paper-checking, peer-review, and paper-rating families | Reviewer simulation, scoring, risk prioritization |
| `paper-ai-rebuttal` | `materials/paper-ai/categories/rebuttal.md`; summarized Devi Parikh/Dhruv Batra/Stefan Lee article; learning-research rebuttal notes | Concern table, AC-facing response, tone/compression |
| `paper-ai-eval-loop` | `materials/architecture-references/README.md`; OpenAI cookbook improvement loop; OMX repos | Trace/eval flywheel, regression cases, human gates |

## 3. Architecture materials

| Design area | Local / official references | Usage |
| --- | --- | --- |
| Codex skills structure | Official Codex skills docs; `materials/architecture-references/repos/anthropics-skills/`; local Codex skill examples | Skill folder shape, progressive disclosure, plugin packaging direction |
| App Server mode | Official Codex App Server docs; OpenAI App Server article; `materials/architecture-references/repos/openai-codex/codex-rs/app-server*` | JSON-RPC, thread/turn/item mapping, approvals, client bindings |
| Agent handoffs/guardrails/tracing | `materials/architecture-references/repos/openai-openai-agents-python/docs/` | Handoff contracts, guardrail ideas, trace semantics |
| OMX-style orchestration | local oh-my-codex repos | Role separation, planning/execution/verification workflows, stateful skills |
| Research skill precedents | `AI-research-SKILLs`; `Research-Paper-Writing-Skills` | Skill naming and research-writing workflow precedents |


## 4. Continuous intake/fusion workflow

Use [`docs/MATERIAL_INTAKE_WORKFLOW.md`](MATERIAL_INTAKE_WORKFLOW.md) for newly arriving PDFs, repos, articles, screenshots, or OCR transcripts. The expected flow is:

1. ingest into ignored `/materials/paper-ai/external/<material-id>/`;
2. classify by category;
3. create local public-safe synthesis bullets;
4. map the bullets to skill instructions, gates/checklists, synthetic evals, or roadmap items;
5. commit only the resulting public-safe code/docs/tests.

Recent local-only fusion signals from review/title material:

- strengthen `paper-ai-writing` title/abstract/first-two-pages gates;
- strengthen `paper-ai-reviewer` first-impression and reviewer-time-pressure simulation;
- strengthen `paper-ai-figures` first-page figure readability checks;
- keep `paper-ai-rebuttal` conservative about score-changing promises.

## 5. Material-to-artifact trace rule

Future outputs should append a short `MATERIALS_USED.md` entry:

```markdown
## 2026-05-17 paper-ai-writing

- Used: materials/paper-ai/categories/writing.md
- Used: materials/paper-ai/external/cwmt14-tut/index.md
- Purpose: introduction flow and claim/evidence audit
- Copied raw text: no
```

## 6. Material risks

- Some local material may be private or copyrighted.
- Model-specific advice from prompt libraries can become outdated.
- OCR/rendered PDF material may contain recognition errors.
- Private/internal repositories should be treated as local reference only unless licensing is confirmed.

Mitigation: use materials for internal design extraction and cite categories, not raw private text, in public docs.
