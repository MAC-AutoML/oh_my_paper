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

## Verification summary

Maintainers should run the repository's internal validation suite before changing
artifact, gate, or eval-fixture behavior. Public user workflows should use the
CLI commands listed above rather than the maintainer-only checks.

The toy workspace is schema-valid but intentionally fails the evidence gate because
claim `C3` is unsupported. That failure is the first regression anchor for later
writing/rebuttal workflows.
