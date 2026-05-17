# Milestone 4 — Mocked Codex App Server Adapter Prototype

Milestone 4 proves that `oh my paper` can map local workflow semantics to an
App Server-style runtime boundary without requiring a real Codex App Server or
API credentials yet.

## What is implemented

- Runtime-neutral protocol types in `src/oh_my_paper/runtime/protocol.py`:
  - `RunHandle`
  - `GateRequest` / `GateDecision`
  - `ArtifactChangeRequest` / `ChangeDecision`
  - `ToolRunRequest` / `ToolRunResult`
  - `RuntimeAdapter` protocol
- JSON-RPC-like message and thread models in `app_server_events.py`.
- `MockAppServerRuntimeAdapter` that:
  - starts a thread-like run;
  - maps paper trace events to `.paper-ai/TRACE.jsonl` with `runtime: app-server`;
  - maps human gates to approval request/resolution messages;
  - maps file-change and command approvals to explicit decisions;
  - runs the same synthetic eval fixtures used by local mode.
- CLI smoke command:

```bash
uv run oh-my-paper mock-app-server /tmp/ohmp-demo tests/fixtures/evals/unsupported_claim.jsonl
```

## Current non-goals

- No real Codex App Server process launch yet.
- No WebSocket transport; stdio/JSON-RPC remains the intended first real transport.
- No API keys or model credentials required for mocked tests.
- No App Server-specific logic in `skills/paper-ai-*` instructions.

## Credential/config policy for the future real adapter

When the real Codex/App Server or model API path is added, credentials should be
loaded from local, ignored files only:

- `.env` for secrets such as API tokens.
- `config.yaml` for non-secret adapter options such as transport mode, command,
  model/profile names, and timeouts.

Those files must remain untracked. The tracked repo should only contain templates
or documentation, not user credentials.

## Verification summary

Maintainers should run the repository's internal validation suite and the mocked
App Server probe before changing adapter behavior. No real App Server process or
API credentials are required for the mocked path.

Acceptance coverage:

- mocked JSON-RPC-like thread run maps events to `TRACE.jsonl`;
- file-change and command approval messages map to decision objects;
- human gate requests map to `GateDecision`;
- local and App Server adapter paths share eval fixtures;
- real WebSocket/App Server transport remains deferred.
