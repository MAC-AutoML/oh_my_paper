# Milestone 3 — End-to-End Local MVP

Milestone 3 provides a deterministic local demo path for the `oh my paper` skill
chain. It does not call a model and does not claim to create a submission-ready
paper. Its purpose is to prove artifact routing, gate visibility, trace capture,
and eval-report generation across the full workflow.

## Command path

```bash
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
uv run oh-my-paper validate-artifacts /tmp/ohmp-demo
```

Use a temporary or copied workspace for demos so tracked examples stay clean.

## Workflow phases

`run-demo` executes these deterministic phases:

1. `research-process` validates the core workspace artifacts.
2. `writing` writes `paper/DEMO_DRAFT.md` while withholding unsupported claims.
3. `figures` writes claim-linked `FIGURE_PLAN.md` and `TABLE_PLAN.md`.
4. `layout` writes a generic page-budget warning in `LAYOUT_REPORT.md`.
5. `reviewer` writes `REVIEW_SIMULATION.md` and `FIX_PLAN.md`.
6. `rebuttal` writes `REBUTTAL_PLAN.md` and `PROMISED_REVISIONS.md` conservatively.
7. `eval-loop` writes `EVAL_REPORT.md` from phase gate statuses.

Every phase appends a `.paper-ai/TRACE.jsonl` event with phase, skill, inputs,
outputs, gate status, and human-decision visibility.

## Expected toy behavior

The default synthetic workspace includes unsupported claim `C3`. Therefore:

- artifact schema validation passes;
- the evidence gate fails on `C3`;
- writing withholds/caveats `C3` instead of drafting it as a result;
- reviewer and rebuttal phases keep human gates visible;
- the overall demo command exits successfully because the risky decision is
  surfaced rather than hidden.

## Verification summary

Maintainers should run the repository's internal validation suite and the local demo
flow before changing MVP workflow behavior. Public user workflows should use the
command path above.
