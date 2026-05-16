# ADR-0001: Design-first dual-mode skill group

## Status

Accepted for v1 planning.

## Context

The project goal is a full-process AI-paper skill group inspired by oh-my-codex orchestration and Codex harness/App Server ideas. User clarification selected a design-first MVP and required PRD, skill architecture, dual-mode design, harness/eval loop, roadmap, repo structure, and acceptance/eval specs.

## Decision

Build `oh my paper` as a modular `paper-ai-*` skill group with shared workflow semantics and two runtime adapters:

1. local installed Codex skills mode;
2. Codex App Server mode.

Implement local skills first, while designing adapter boundaries early enough that App Server integration can reuse artifacts, gates, traces, and eval fixtures.

## Drivers

- The full paper workflow needs durable artifacts and gates, not isolated prompts.
- Local skills are the fastest path to adoption.
- App Server gives a richer future event/approval/thread model.
- Raw materials must remain private/local.
- Continuous improvement requires traces and eval fixtures.

## Alternatives considered

### Local-only skills

Pros: fastest and simplest.

Rejected because it risks creating workflow semantics that do not map cleanly to future App Server integration.

### App Server-first product

Pros: richer orchestration and event model from day one.

Rejected for v1 because user explicitly excluded UI/product build, and server integration would delay usable local skills.

### One monolithic paper skill

Pros: simpler installation and discovery.

Rejected because the lifecycle is too broad; monolith would bloat context and mix generation, critique, layout, and rebuttal responsibilities.

### One-click full-paper generator

Pros: superficially attractive.

Rejected because it conflicts with research integrity, evidence requirements, and the user's explicit non-goal.

## Consequences

- More upfront design work and schemas.
- More directories than a simple prompt pack.
- Clearer boundaries for future parallel work.
- Local MVP can ship before App Server implementation.
- Evals and traces become first-class rather than afterthoughts.

## Follow-ups

- Create skill stubs and plugin metadata.
- Implement artifact/gate/eval core with `uv`.
- Add toy paper examples and synthetic fixtures.
- Prototype App Server adapter with mocked JSON-RPC before real client.
