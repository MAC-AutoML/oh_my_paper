# Dual-Mode Technical Design

## 1. Goal

Support two delivery modes without duplicating workflow semantics:

1. **Local installed skills mode:** Codex discovers and runs skills from the user machine.
2. **Codex App Server mode:** an application launches or connects to Codex App Server and drives the same workflow through thread, turn, item, approval, and tool events.

## 2. Shared domain model

```text
PaperProject
  ├── ProjectState
  ├── ArtifactStore
  ├── SkillRouter
  ├── GateRegistry
  ├── TraceRecorder
  ├── EvalHarness
  └── RuntimeAdapter
       ├── LocalSkillRuntimeAdapter
       └── AppServerRuntimeAdapter
```

### Core abstractions

| Abstraction | Responsibility |
| --- | --- |
| `PaperProject` | Workspace root, metadata, target venue, language, active phase |
| `ProjectState` | Phase status, required artifacts, blockers, next actions |
| `ArtifactStore` | Own artifact schemas, canonical paths, validation, and Markdown/JSON read/write semantics |
| `SkillRouter` | Choose skill based on user intent, state, and missing artifacts |
| `GateRegistry` | Run evidence/reviewer/layout/rebuttal/eval gates |
| `TraceRecorder` | Append normalized events to `TRACE.jsonl` |
| `EvalHarness` | Run fixture-based checks and summarize pass/fail |
| `RuntimeAdapter` | Own execution context, event emission, approvals, and transport-specific behavior |

### Boundary rule

`ArtifactStore` is the only layer that defines artifact names, paths, schemas, and read/write validation. `RuntimeAdapter` must not redefine artifact semantics. The local adapter can let `ArtifactStore` write directly to disk; the App Server adapter can request or observe approved file changes, but it still calls through the same `ArtifactStore` contract. This prevents local skills and App Server mode from drifting into separate paper-project formats.

## 3. Local installed skills mode

### Intended use

Fast local adoption: users install `paper-ai-*` skills into their Codex skills directory and use them inside paper workspaces.

### Execution model

- Codex skill selection loads `SKILL.md` only for relevant skills.
- Skills operate on project files in the current workspace.
- Scripts run through `uv run` when Python is needed.
- State is file-based under `.paper-ai/` and `paper/`.
- Human gates are natural Codex questions or explicit checklist blocks.

### Installation target

Future plugin layout should support copying skills to a local skill directory and optionally packaging as a Codex plugin.

```text
.codex-plugin/plugin.json
skills/paper-ai-orchestrator/SKILL.md
skills/paper-ai-writing/SKILL.md
...
```

### Local strengths

- Works without server/client development.
- Easy to inspect and modify.
- Keeps private paper material on the user machine.
- Best for first MVP.

### Local limitations

- No rich external UI by default.
- Long-running state is file-based and convention-driven.
- Multi-agent concurrency depends on Codex-native subagent support and explicit artifact handoff contracts.

## 4. Codex App Server mode

### Intended use

Future integration mode for richer orchestration, app clients, persistent event streams, approvals, and continuous-evolution infrastructure.

### OpenAI App Server facts to design around

Official Codex App Server docs describe bidirectional JSON-RPC messages over stdio by default, with WebSocket listed as experimental. The harness exposes thread/session state and supports server-initiated approval and user-input requests. The Codex harness article also frames App Server as the shared interface that lets multiple clients drive the same Codex core loop.

### Execution model

- A client starts/resumes a Codex thread for a paper workspace.
- The App Server emits turn/item lifecycle events.
- The paper workflow maps phase runs to thread turns and normalized trace events.
- Approvals are surfaced for file changes, commands, dynamic tools, and high-stakes paper gates.
- The App Server client stores enough thread IDs and project metadata to reconnect.

### Event mapping

| Paper concept | App Server concept | Notes |
| --- | --- | --- |
| Paper project | thread metadata + workspace cwd | Keep project ID in client metadata/artifacts |
| Skill invocation | user turn + selected skill | Record skill name in trace |
| Artifact edit | file change item | May require approval depending settings |
| Human gate | server request / user input / approval | Gate must pause completion until resolved |
| Eval run | command/tool item + eval summary artifact | Prefer deterministic scripts where possible |
| Reconnect | thread resume/read/list | Client can rebuild status from thread + artifacts |

### App Server strengths

- Rich event stream for UI and automation.
- Thread lifecycle, resume/fork/archive primitives.
- Stable protocol boundary for clients.
- Good fit for long-running paper workflows and dashboards later.

### App Server limitations

- Requires client binding and version management.
- Protocol evolves; integration should pin/test server versions.
- WebSocket transport is experimental per current docs; stdio should be the first implementation target.

## 5. Adapter interface sketch

Future Python interface:

```python
class RuntimeAdapter(Protocol):
    def start_run(self, phase: str, intent: str) -> RunHandle: ...
    def emit_event(self, event: TraceEvent) -> None: ...
    def request_human_gate(self, gate: GateRequest) -> GateDecision: ...
    def request_file_change(self, change: ArtifactChangeRequest) -> ChangeDecision: ...
    def run_tool_or_command(self, request: ToolRunRequest) -> ToolRunResult: ...
    def run_eval(self, fixture: EvalFixture) -> EvalResult: ...
```

Local adapter implements these as filesystem-visible actions, Codex prompts, and `uv run` commands. App Server adapter maps them to thread/turn/item events, file-change approvals, command approvals, and client-visible gate prompts. Artifact path/schema handling remains in `ArtifactStore`; adapter methods only request execution or approval around those changes.

## 6. Data boundaries

- Raw `materials/` are not part of either runtime package.
- Project papers may contain unpublished research; default to local storage and explicit approval before export.
- Traces may contain sensitive claims, reviews, or paper text; eval export must support redaction.

## 7. Implementation sequencing

1. Build local file/artifact semantics first.
2. Add deterministic validators and eval fixtures.
3. Wrap the same semantics in `RuntimeAdapter`.
4. Implement App Server client prototype once local semantics stabilize.
5. Add server-mode tests with mocked JSON-RPC events before real client release.

## 8. App Server source and version policy

- Treat official Codex App Server docs and the local `openai-codex` repo schema as the implementation source of truth.
- Pin the tested Codex CLI/App Server version for any generated TypeScript or JSON Schema bundle because generated schemas are version-specific.
- Prefer stdio/JSONL transport first. WebSocket is experimental/unsupported in current docs and must not be exposed remotely without explicit authentication and risk review.
- Keep App Server integration tests mocked until the local artifact/gate/eval semantics are stable.
