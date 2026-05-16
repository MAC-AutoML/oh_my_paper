# Eval fixtures

Milestone 2 introduces small synthetic JSONL fixtures for local evaluator development.

- `unsupported_claim.jsonl`: unsupported claim must fail the evidence gate.
- `supported_claim.jsonl`: supported claim should pass the evidence gate.
- `trace_integrity.jsonl`: complete trace event should pass trace validation.

Only `privacy: synthetic` fixtures are allowed in this tracked directory. Redacted or private paper/review text belongs in ignored local workspaces, never in git.
