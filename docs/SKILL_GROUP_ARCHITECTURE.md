# Skill Group Architecture

## 1. Architecture principles

1. **Artifact-first:** every phase reads and writes durable project files.
2. **Gate-before-generation:** drafting is blocked or labeled when evidence is missing.
3. **Progressive disclosure:** top-level skill files stay concise; detailed advice lives in references/scripts/assets.
4. **Separation of creator and critic:** writing/generation skills do not approve themselves.
5. **Same semantics across runtimes:** local skills and App Server mode share phase names, artifact schemas, gates, and eval fixtures.

## 2. Skill inventory

The skill group follows the natural paper lifecycle. It deliberately avoids exposing every internal gate as a separate user-facing skill. Richness lives inside each skill's `references/` as checklists, output formats, failure modes, and material-derived heuristics.

| Skill | Natural stage | Primary outputs | Main gate |
| --- | --- | --- | --- |
| `paper-ai-orchestrator` | Full workflow routing | minimal state, next-skill handoff | next paper step explicit |
| `paper-ai-idea` | Idea / research question | `IDEA_BRIEF.md`, contribution hypotheses | audience, gap, evidence path exist |
| `paper-ai-writing` | Whole-paper coherence | story outline, cross-section notes | claims linked to evidence |
| `paper-ai-title-abstract` | Title and abstract | title candidates, abstract, first-impression audit | no overclaim beyond evidence |
| `paper-ai-introduction` | Introduction | `INTRODUCTION_DRAFT.md`, contributions | contributions are evidence-linked |
| `paper-ai-related-work` | Related work | `RELATED_WORK_DRAFT.md`, contrast map | closest work and contrast axes named |
| `paper-ai-method` | Method | `METHOD_DRAFT.md`, notation/running example | reader context before formalism |
| `paper-ai-experiments` | Experiments/results | `EXPERIMENTS_DRAFT.md`, evidence table | no invented numbers/results |
| `paper-ai-figures` | Figures/tables | `FIGURE_PLAN.md`, `TABLE_PLAN.md`, captions | one takeaway and claim link per visual |
| `paper-ai-limitations` | Limitations/caveats | `LIMITATIONS.md`, caveated claims | validity-affecting limits visible |
| `paper-ai-layout` | Layout/polish | `LAYOUT_REPORT.md`, polish notes | polish preserves evidence limits |
| `paper-ai-reviewer` | Strict review | `REVIEW_SIMULATION.md`, `FIX_PLAN.md` | fatal blockers block ready verdict |
| `paper-ai-rebuttal` | Rebuttal/defense | `REBUTTAL_PLAN.md`, concern table, responses | every material concern addressed |


## 3. Standard workspace artifacts

```text
.paper-ai/
  PAPER_AI_STATE.md
  TRACE.jsonl
  MATERIALS_USED.md
  eval-notes/
paper/
  PAPER_BRIEF.md
  CLAIMS.md
  EVIDENCE_MAP.md
  EXPERIMENT_PLAN.md
  FIGURE_PLAN.md
  TABLE_PLAN.md
  LAYOUT_REPORT.md
  REVIEW_SIMULATION.md
  FIX_PLAN.md
  REBUTTAL_PLAN.md
  PROMISED_REVISIONS.md
```

### Artifact rules

- `CLAIMS.md` is the central ledger: each claim has status `supported`, `partial`, `planned`, `unsupported`, or `removed`.
- `EVIDENCE_MAP.md` links claims to experiments, tables, figures, citations, logs, or human notes.
- `TRACE.jsonl` records phase runs, model/tool decisions, gate outcomes, and eval verdicts.
- `MATERIALS_USED.md` records which local/public references informed the output without copying private content.

## 4. Handoff contracts

### Research process → Writing

Required inputs:

- paper goal and target audience
- contribution list
- baseline gap
- evidence map with missing evidence labels

Handoff output:

- section outline with claim IDs
- writing risks

### Writing → Figures

Required inputs:

- claims needing visual support
- result tables or experiment summaries
- target story for each visual

Handoff output:

- figure/table plan with claim IDs
- caption draft and visual audit checklist

### Writing/Figures/Layout → Reviewer

Required inputs:

- current draft or section bundle
- claims/evidence map
- figure/table plan
- venue constraints if known

Handoff output:

- reviewer reports
- score/risk rubric
- prioritized fix plan

### Reviewer → Rebuttal

Required inputs:

- submitted paper
- reviewer comments and scores
- extra evidence/experiments after submission
- fix plan

Handoff output:

- concern table
- AC summary
- reviewer-specific responses
- promised revisions

## 5. Stage gates

| Gate | Applies before | Block condition | Recovery |
| --- | --- | --- | --- |
| Evidence gate | full draft, rebuttal | claim has no evidence or caveat | ask for data, mark as limitation, remove claim |
| Visual gate | figure finalization | no single takeaway or unreadable labels | redesign figure or downgrade to appendix |
| Layout gate | final formatting | page budget/venue constraints unknown | request venue or run generic budget estimate |
| Reviewer gate | submission-ready label | fatal reviewer concerns unresolved | create fix plan, do not claim ready |
| Rebuttal gate | final response | concern unanswered or overpromised | revise answer/evidence/concession |
| Eval gate | skill update | no regression evidence | create fixture or document explicit waiver |

## 6. Skill folder pattern

Each skill should follow Codex skill conventions: a directory containing `SKILL.md`, with optional `scripts/`, `references/`, `assets/`, and `agents/`. Codex docs describe this as progressive disclosure: the initial context lists name/description/path, and the full `SKILL.md` is loaded only when selected.

Recommended pattern:

```text
skills/paper-ai-writing/
  SKILL.md
  references/
    section-patterns.md
    paragraph-audit.md
    claim-evidence-rules.md
  scripts/
    audit_claims.py
  assets/
    section-template.md
  evals/
    README.md          # optional examples pointing to canonical fixtures
```

## 7. Eval fixture ownership

Canonical executable eval fixtures live under `tests/fixtures/evals/` so one shared harness can run them across local and App Server adapters. Skill-local `evals/` folders may contain README files, examples, or links to canonical fixtures, but they are not the source of truth for regression tests.

## 8. Skill naming boundaries

Use `paper-ai-*` for installable skills to avoid conflict with existing generic writing/rebuttal skills.

- `paper-ai-orchestrator` owns routing and state, not detailed writing advice.
- `paper-ai-writing` drafts and revises, but does not approve submission readiness.
- `paper-ai-reviewer` criticizes and scores, but does not silently rewrite the paper.
- `paper-ai-rebuttal` answers reviews, but cannot invent results or promise experiments without evidence.
- `paper-ai-eval-loop` improves skills, but does not change raw material policy.

## 9. Human decision points

Ask or require approval when:

- A claim lacks evidence but the user wants to keep it.
- A rebuttal response promises new experiments, code release, or major revisions.
- A material source is private/copyrighted and might be copied into public docs.
- A target venue/template choice changes constraints materially.
- An App Server client would execute external side effects.
