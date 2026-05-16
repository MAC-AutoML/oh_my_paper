# PRD: oh my paper

## 1. Summary

`oh my paper` is a modular Codex skill group for AI researchers writing papers. It guides a project from idea/results through paper planning, writing, figures/tables, layout, reviewer simulation, revision, rebuttal, and eval-driven improvement.

The first milestone is an implementation-ready design package and then a local-skills MVP. App Server integration is designed early so the local workflow does not become a dead end.

## 2. Target users

1. **AI PhD student / researcher** who has experiments or a project direction and needs to turn it into a coherent paper.
2. **Research engineer** who owns results, ablations, figures, and reproducibility notes.
3. **Advisor / senior collaborator** who wants structured review artifacts instead of free-form drafts.
4. **Rebuttal-phase author** who needs grounded, concise, non-combative responses under deadline.

## 3. Core user journeys

### Journey A — Idea/results to paper plan

Input: research notes, experiment summaries, baseline comparisons, rough claims.

Output:

- `PAPER_BRIEF.md`
- `CLAIMS.md`
- `EVIDENCE_MAP.md`
- `EXPERIMENT_PLAN.md`
- section outline with known evidence gaps

Gate: no full draft until claims have evidence status and missing experiments are explicit.

### Journey B — Draft writing and revision

Input: paper brief, claims, evidence map, target venue constraints, section outline.

Output:

- section drafts
- paragraph-level revision notes
- terminology table
- limitation/framing notes

Gate: each important claim must link to evidence, a figure/table, or a planned caveat.

### Journey C — Figures, tables, and layout

Input: results, diagrams, target story, page budget.

Output:

- figure plan
- table plan
- caption drafts
- plot/readability checklist
- layout budget report

Gate: each visual must have a single takeaway and must support a claim in `CLAIMS.md`.

### Journey D — Reviewer simulation and fix planning

Input: draft, evidence map, figures, supplementary notes.

Output:

- strict reviewer reports
- score/risk rubric
- fatal-vs-fixable gap list
- prioritized fix plan

Gate: fatal unsupported claims or missing baselines block “submission-ready” status.

### Journey E — Rebuttal and defense

Input: submitted paper, reviewer comments, scores, evidence, extra experiments.

Output:

- reviewer concern table
- evidence-backed reply plan
- AC-facing summary
- compressed final rebuttal
- promised revision list

Gate: no rebuttal finalization until every reviewer concern is mapped to an answer, evidence, limitation, or explicit concession.

### Journey F — Continuous improvement

Input: traces, weak outputs, user corrections, review outcomes.

Output:

- eval fixtures
- regression cases
- updated references/scripts
- changelog entries explaining behavior changes

Gate: a skill change should include a before/after fixture or documented reason why not.

## 4. Functional requirements

| ID | Requirement | Acceptance signal |
| --- | --- | --- |
| FR-1 | Provide a top-level orchestrator skill that routes lifecycle phases. | Given a workspace, it can identify current phase and next artifact. |
| FR-2 | Maintain explicit artifacts rather than relying on chat memory. | Required artifact files are created/updated per phase. |
| FR-3 | Support local installed skills mode. | Skills can be copied/installed into a Codex skill directory and used without server code. |
| FR-4 | Support Codex App Server mode by design. | Runtime abstraction maps phases to thread/turn/item events and approvals. |
| FR-5 | Preserve human gates for claims, evidence, experiments, and rebuttal promises. | The workflow blocks or labels risky unsupported outputs. |
| FR-6 | Use material references through progressive disclosure. | `SKILL.md` files remain concise and point to references/scripts. |
| FR-7 | Provide eval fixtures and trace format for later automation. | `tests/fixtures/evals/*.jsonl` schema is defined. |
| FR-8 | Keep raw materials private/local. | `.gitignore` excludes `materials/` and public docs summarize only. |

## 5. Non-functional requirements

- **Modularity:** each skill owns one phase and small artifact contracts.
- **Maintainability:** future Python source files should stay under 500 lines when practical, 550 max tolerance.
- **UV-first Python:** use `uv run` and `uv add`; avoid conda instructions.
- **Traceability:** design decisions should cite local material category or official Codex/App Server docs.
- **Safety:** high-stakes claims, rebuttal promises, and reviewer-facing statements require evidence or human approval.
- **Portability:** local skills should not require App Server; App Server should reuse the same workflow semantics.

## 6. Explicit non-goals

- Build no UI product in v1.
- Publish no raw local materials.
- Promise no magic one-click full paper.
- Support no exhaustive all-venue template matrix in v1.

## 7. Success metrics

### Design-phase metrics

- All required docs exist and cross-reference each other.
- Every lifecycle phase has a skill owner, artifact inputs, outputs, and gates.
- Local and App Server modes are separated by adapter boundaries.
- Eval fixture shapes are specific enough for later implementation.

### MVP implementation metrics

- A toy paper workspace can run from brief → claims → draft section → reviewer simulation → rebuttal outline.
- At least one regression fixture exists for each major phase.
- Human gates trigger for unsupported claims and rebuttal overpromises.
- Installation docs work in a clean local checkout.

## 8. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Scope explodes into all paper tasks at once. | Large unfinished system. | Stage roadmap; local skills MVP first. |
| Skill prompts become huge. | Poor context efficiency. | Progressive disclosure: `SKILL.md` + references + scripts. |
| App Server integration blocks local value. | Slow adoption. | Adapter-first design, local runtime first. |
| Private/copyrighted material leaks. | Legal/privacy issue. | Keep `materials/` ignored; public docs only summarize. |
| AI produces unsupported scientific claims. | Research integrity issue. | Evidence map and human gates. |
| Rebuttal tone overpromises or antagonizes reviewers. | Review outcome risk. | Concern table, evidence tags, tone/compression critic. |
