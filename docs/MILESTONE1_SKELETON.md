# Milestone 1 Skeleton Notes

Milestone 1 creates installable local skill stubs and public-safe examples. It intentionally does not implement the artifact store, gates, runtime adapters, or eval harness; those begin in Milestone 2.

## Created surfaces

- `.codex-plugin/plugin.json` for local plugin metadata.
- `skills/paper-ai-*/SKILL.md` for eight discoverable skill stubs.
- `skills/paper-ai-*/references/` for public-safe progressive disclosure notes.
- `examples/toy-paper-workspace/` with synthetic `.paper-ai/` and `paper/` artifacts.
- `tests/fixtures/evals/README.md` as the future canonical eval fixture location.
- `src/oh_my_paper/` package skeleton for future `uv` implementation.

## Validation boundary

Current validation checks structure, public-safety policy, and installability of the placeholder package. Behavioral eval fixtures and harness execution are deferred to Milestone 2.
