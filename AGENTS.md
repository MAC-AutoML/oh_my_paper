# AGENTS.md — oh_my_paper

- Use `uv run` and `uv add` for Python work; do not introduce conda workflows.
- Keep implementation files generally under 500 lines; 550 lines is the tolerated upper bound.
- Prefer modular, decoupled packages and concise Codex skills with progressive disclosure.
- Do not commit raw `materials/`, `temp/`, `.omx/`, `.spec-workflow/`, `node_modules/`, or generated package-lock files.
- Do not promise magic one-click paper generation; keep evidence gates and human approvals explicit.
- Treat `tests/fixtures/evals/*.jsonl` as the canonical executable eval fixture location.
