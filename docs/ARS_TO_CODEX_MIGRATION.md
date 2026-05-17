# ARS to Codex Migration Guide

This project adapts the Claude-oriented Academic Research Skills workflow into a Codex-native package. The product surface is Codex skills, repo-local Codex subagents, durable paper artifacts, local validators, and an OpenAI-compatible API runtime.

## Runtime model

- Install and use `skills/paper-ai-*` through Codex skills.
- Use `uv run oh-my-paper ...` for local artifact validation and API-backed workflows.
- Configure model access with an OpenAI-compatible endpoint: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `OPENAI_MODEL`.
- Optional Node tooling is only needed for browser automation utilities.

## Old ARS intent / Codex equivalent entry point

Old slash-style forms are documented as equivalent intents unless literal command dispatch is implemented.

| Old ARS intent | Codex owner skill | Mode |
| --- | --- | --- |
| `/ars-plan` | `paper-ai-idea` | academic-paper `plan` |
| `/ars-full` | `paper-ai-orchestrator` | academic-pipeline `pipeline` |
| `/ars-lit-review` | `paper-ai-research` | deep-research `lit-review` |
| `/ars-outline` | `paper-ai-writing` | academic-paper `outline-only` |
| `/ars-abstract` | `paper-ai-title-abstract` | academic-paper `abstract-only` |
| `/ars-revision` | `paper-ai-writing` | academic-paper `revision` |
| `/ars-revision-coach` | `paper-ai-reviewer` | academic-paper `revision-coach` |
| `/ars-citation-check` | `paper-ai-research` | academic-paper `citation-check` |
| `/ars-disclosure` | `paper-ai-layout` | academic-paper `disclosure` |
| `/ars-format-convert` | `paper-ai-layout` | academic-paper `format-convert` |

## Mode coverage

The machine-readable registry contains all 25 ARS modes. Each mode records one primary `owner_skill`, optional `secondary_skills`, expected outputs, gates, data access level, status, and next action.

Status meanings:

- `implemented`: a Codex-native route or artifact already exists.
- `partial`: a route exists but needs more contract or validator coverage.
- `advisory`: documented workflow guidance exists; executable parity is staged.
- `deferred`: intentionally not implemented yet.

## Integrity artifacts

Machine-validated compatibility artifacts use JSON first:

- `paper/MATERIAL_PASSPORT.json`
- `paper/SPRINT_CONTRACT.json`
- `paper/CLAIM_AUDIT_REPORT.json`
- `paper/CITATION_ANCHOR_AUDIT.json`
- `paper/INTEGRITY_REPORT_STAGE_2_5.json`
- `paper/INTEGRITY_REPORT_FINAL.json`

Markdown remains the human-facing format for briefs, drafts, reviews, and summaries.
