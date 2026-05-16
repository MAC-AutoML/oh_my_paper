# Milestone 5 — Harness Flywheel

Milestone 5 turns workflow failures and risky gate decisions into regression
fixtures that can be replayed after skill or script changes.

## Implemented commands

Capture a risky run as a fixture:

```bash
uv run oh-my-paper capture-fixture /tmp/ohmp-demo /tmp/captured.jsonl \
  --fixture-id captured_c3_regression \
  --purpose "capture unsupported claim gate" \
  --privacy redacted
```

Run fixture sets and write reports/changelog entries:

```bash
uv run oh-my-paper eval-report tests/fixtures/evals/unsupported_claim.jsonl \
  --output /tmp/eval-report.md \
  --changelog /tmp/HARNESS_CHANGELOG.md \
  --note "verified unsupported-claim regression"
```

## Privacy policy

- `synthetic`: safe for tracked fixtures.
- `redacted`: allowed for local/private reports; content is passed through simple
  email/token/secret redaction before fixture writing.
- `private`: allowed only outside tracked fixture directories.

The tracked canonical fixture directory remains `tests/fixtures/evals/`, and it
must contain only synthetic fixtures. Real paper or review text should be stored
outside the repo or in ignored local workspaces.

## Flywheel loop

1. Run local or mocked App Server workflow.
2. Detect failed/warn gate or human-required decision in `.paper-ai/TRACE.jsonl`.
3. Capture minimal artifacts into a fixture.
4. Run `eval-report` on the fixture set.
5. Patch skill/reference/script behavior.
6. Re-run the report and append a changelog entry.

## Current evaluator registry

The registry is intentionally small and dependency-free:

- evidence grounding fixtures via `must_flag_claim_ids`;
- trace integrity fixtures via `trace_integrity`;
- artifact completeness fixtures via `artifact_completeness`.

Future milestones can add writing-structure, figure-readability, reviewer, and
rebuttal-safety evaluators without changing the fixture file location.
