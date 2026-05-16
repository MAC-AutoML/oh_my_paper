# Roadmap

## Milestone 0 — Design package

Goal: produce implementation-ready design docs.

Deliverables:

- PRD
- skill architecture
- dual-mode tech design
- harness/eval design
- repo structure spec
- acceptance/eval spec
- materials mapping
- consensus handoff plan

Exit criteria:

- docs are coherent and cross-linked;
- no raw materials are committed;
- next implementation plan can be derived without re-interviewing.

## Milestone 1 — Repository skeleton and local skill stubs

Goal: create installable local skill skeletons without deep automation.

Deliverables:

- `skills/paper-ai-*/SKILL.md` stubs
- `references/` summaries derived from public-safe material notes
- `.codex-plugin/plugin.json`
- `examples/toy-paper-workspace/`
- basic artifact templates

Exit criteria:

- skills are discoverable by Codex;
- each skill has trigger, inputs, outputs, and gates;
- no skill file exceeds maintainability target.

## Milestone 2 — Artifact store, validators, and local scripts

Goal: make the local workflow concrete and testable.

Deliverables:

- `src/oh_my_paper/artifacts/`
- `src/oh_my_paper/gates/`
- `src/oh_my_paper/evals/`
- `uv` project setup
- synthetic fixtures in `tests/fixtures/evals/*.jsonl`

First implementation slice:

1. Artifact schema validation for `CLAIMS.md`, `EVIDENCE_MAP.md`, and `.paper-ai/TRACE.jsonl`.
2. Unsupported-claim evidence gate with one failing and one passing fixture.
3. Trace integrity evaluator that confirms phase, skill, inputs, outputs, and gate status.

Exit criteria:

- `uv run pytest` passes;
- validators can detect missing artifacts and unsupported claims;
- toy workspace produces trace events.

## Milestone 3 — End-to-end local MVP

Goal: run a toy paper from brief to rebuttal outline.

Deliverables:

- orchestrator routing
- research-process → writing → reviewer → rebuttal demo
- figure/layout checklist flows
- eval report generation

Exit criteria:

- one documented demo command path works;
- every phase writes trace events;
- human gates are visible for risky decisions.

## Milestone 4 — App Server adapter prototype

Goal: prove the same workflow semantics can run through Codex App Server.

Deliverables:

- JSON-RPC client prototype
- mocked protocol tests
- thread/turn/item mapping
- approval/user-input gate mapping

Exit criteria:

- local adapter tests and mocked App Server adapter tests share fixture expectations;
- no App Server-specific logic leaks into skill instructions.

## Milestone 5 — Harness flywheel

Goal: turn failures into regression fixtures and skill improvements.

Deliverables:

- fixture capture command
- evaluator registry
- changelog/report generator
- privacy/redaction mode

Exit criteria:

- a failed run can be converted into a fixture;
- a skill change can be validated against the fixture;
- report shows before/after outcome.

## Milestone 6 — Packaging and documentation

Goal: make local installation and future server integration repeatable.

Deliverables:

- plugin packaging docs
- install/uninstall docs
- examples and demo recordings/screenshots if desired
- public-safe material attribution notes

Exit criteria:

- clean checkout can install and run local skills;
- docs explain limitations and non-goals clearly.
