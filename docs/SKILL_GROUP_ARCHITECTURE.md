# Skill Group Architecture

## 1. Architecture principles

1. **Artifact-first:** every phase reads and writes durable project files.
2. **Gate-before-generation:** drafting is blocked or labeled when evidence is missing.
3. **Progressive disclosure:** top-level skill files stay concise; detailed advice lives in references/scripts/assets.
4. **Separation of creator and critic:** writing/generation skills do not approve themselves.
5. **Same semantics across runtimes:** local skills and App Server mode share phase names, artifact schemas, gates, and eval fixtures.

## 2. Skill inventory

The skill group uses a two-layer design:

1. **Coordinator skills** keep state, routing, material fusion, and eval loops explicit.
2. **Specialist skills** own narrow paper-work phases with their own gates and references.

### 2.1 Coordinator and lifecycle skills

| Skill | Trigger | Primary outputs | Main gate |
| --- | --- | --- | --- |
| `paper-ai-orchestrator` | Full workflow / next paper step | `PAPER_AI_STATE.md`, task routing | Current phase and required inputs identified |
| `paper-ai-material-intake` | New PDFs/repos/articles/screenshots/notes | ignored local material cache, public-safe synthesis | Raw sources remain untracked |
| `paper-ai-project-planner` | Project kickoff, deadline, roadmap | `PROJECT_PLAN.md`, phase plan | Claims/evidence artifacts stubbed before drafting |
| `paper-ai-eval-loop` | Improve skills from traces/failures | eval fixture, regression report | Failure reproduced or waived |
| `paper-ai-revision-plan` | Many findings need execution plan | `REVISION_PLAN.md` | Fixes linked to concerns/claims |
| `paper-ai-camera-ready` | Accepted/camera-ready work | `CAMERA_READY_PLAN.md` | Promises and venue instructions accounted for |

### 2.2 Research and evidence skills

| Skill | Trigger | Primary outputs | Main gate |
| --- | --- | --- | --- |
| `paper-ai-research-process` | Idea/project/contribution planning | `PAPER_BRIEF.md`, `EXPERIMENT_PLAN.md` | Claims and evidence needs explicit |
| `paper-ai-research-question` | Fuzzy topic, novelty/significance critique | `RESEARCH_QUESTION.md` | Audience, gap, and evidence path exist |
| `paper-ai-literature-map` | Literature organization and positioning | `LITERATURE_MAP.md` | Closest work and contrast axes named |
| `paper-ai-experiment-planner` | Baselines/metrics/ablations/evidence design | `EXPERIMENT_PLAN.md` | Strong claims have evidence path |
| `paper-ai-claim-evidence` | Claim ledger and evidence audit | `CLAIMS.md`, `EVIDENCE_MAP.md` | Unsupported claims removed/caveated/labeled |

### 2.3 Writing, visuals, and submission skills

| Skill | Trigger | Primary outputs | Main gate |
| --- | --- | --- | --- |
| `paper-ai-writing` | Mixed-section drafting/revision | section drafts, risk notes | Important claims linked to evidence |
| `paper-ai-title-abstract` | Title, abstract, first-page hook | title/abstract options | No overclaiming beyond claims ledger |
| `paper-ai-introduction` | Introduction/first-two-pages story | `INTRODUCTION_DRAFT.md` | Contributions link to claim IDs |
| `paper-ai-related-work` | Related-work prose | `RELATED_WORK_DRAFT.md` | Novelty claims grounded in closest work |
| `paper-ai-method-writing` | Method/algorithm/equation prose | `METHOD_DRAFT.md` | Reader context before formalism |
| `paper-ai-experiment-writing` | Experiment prose and analysis | `EXPERIMENTS_DRAFT.md` | No invented numbers/results |
| `paper-ai-limitations` | Limitations/scope/ethics caveats | `LIMITATIONS.md` | Validity-affecting limits visible |
| `paper-ai-language-polish` | Translation, compression, de-AI polish | polished prose | Meaning and evidence limits preserved |
| `paper-ai-figures` | Figures and captions | `FIGURE_PLAN.md` | Each visual has takeaway/claim link |
| `paper-ai-tables` | Tables and table captions | `TABLE_PLAN.md` | No unsupported comparison implied |
| `paper-ai-layout` | Page budget/template/camera-ready formatting | `LAYOUT_REPORT.md` | Venue/page constraints checked |
| `paper-ai-submission-check` | Final pre-submission QA | `SUBMISSION_CHECK.md` | Fatal blockers absent before ready verdict |

### 2.4 Review and defense skills

| Skill | Trigger | Primary outputs | Main gate |
| --- | --- | --- | --- |
| `paper-ai-reviewer` | Strict review/scoring/risk audit | `REVIEW_SIMULATION.md`, `FIX_PLAN.md` | Fatal/fixable gaps separated |
| `paper-ai-ac-simulator` | AC perspective and reviewer-discussion risk | `AC_SIMULATION.md` | Uncertainty and scenarios explicit |
| `paper-ai-rebuttal` | Author response needed | `REBUTTAL_PLAN.md`, responses | Every concern answered/evidenced/conceded |


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
