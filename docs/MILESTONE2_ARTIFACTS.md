# Milestone 2 — Artifact Store, Gates, and Eval Fixtures

Milestone 2 turns the design package into executable local checks while keeping the
project local-first and material-safe.

## Implemented scope

- Artifact store resolver for a paper workspace.
- `CLAIMS.md` parser and schema validator.
- `EVIDENCE_MAP.md` parser and schema validator.
- `.paper-ai/TRACE.jsonl` parser and trace integrity validator.
- Evidence gate that blocks unsupported claims before writing/rebuttal outputs.
- Synthetic JSONL fixture loader and evaluator dispatch.
- CLI smoke commands:
  - `oh-my-paper status`
  - `oh-my-paper validate-artifacts <workspace>`
  - `oh-my-paper evidence-gate <workspace>`
  - `oh-my-paper run-eval <fixture.jsonl>`

## Tracked synthetic fixtures

- `tests/fixtures/evals/unsupported_claim.jsonl`
- `tests/fixtures/evals/supported_claim.jsonl`
- `tests/fixtures/evals/trace_integrity.jsonl`

All tracked fixtures are `privacy: synthetic`. Redacted/private real paper data must
stay under ignored local workspaces such as `materials/`, `temp/`, or untracked paper
project directories.

## Verification commands

```bash
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run python scripts/validate_m1_skeleton.py
uv run oh-my-paper validate-artifacts examples/toy-paper-workspace
uv run oh-my-paper evidence-gate examples/toy-paper-workspace  # expected exit 1 for C3
uv run oh-my-paper run-eval tests/fixtures/evals/unsupported_claim.jsonl
uv run oh-my-paper run-eval tests/fixtures/evals/supported_claim.jsonl
uv run oh-my-paper run-eval tests/fixtures/evals/trace_integrity.jsonl
```

The toy workspace is schema-valid but intentionally fails the evidence gate because
claim `C3` is unsupported. That failure is the first regression anchor for later
writing/rebuttal workflows.
