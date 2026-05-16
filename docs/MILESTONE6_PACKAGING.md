# Milestone 6 — Packaging and Installation

Milestone 6 makes local installation repeatable and documents the future real
App Server/model configuration boundary.

## Install local Codex skills

Install into the default Codex skills directory:

```bash
uv run oh-my-paper install-skills
uv run oh-my-paper list-skills
```

Install into an explicit directory for testing or custom `CODEX_HOME` layouts:

```bash
uv run oh-my-paper install-skills /tmp/codex-skills --overwrite
uv run oh-my-paper list-skills /tmp/codex-skills
uv run oh-my-paper uninstall-skills /tmp/codex-skills
```

The installer copies only `skills/paper-ai-*` directories. It does not copy raw
`materials/`, `temp/`, `.omx/`, `.spec-workflow/`, or generated local caches.

## Clean checkout verification

```bash
git clone https://github.com/MAC-AutoML/oh_my_paper.git
cd oh_my_paper
uv run oh-my-paper status
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
uv run oh-my-paper install-skills /tmp/ohmp-skills --overwrite
uv run oh-my-paper list-skills /tmp/ohmp-skills
```

## Future real adapter configuration

Tracked templates:

- `templates/env.example`
- `templates/config.example.yaml`

Local ignored files:

- `.env` for secrets such as API keys or tokens.
- `config.yaml` for non-secret runtime/model options.

Do not commit real credentials. The current mocked App Server adapter does not
need any model or Codex API credentials.

## Public-safe material attribution

The public package may cite category-level material influences and official docs,
but it must not include raw downloaded repositories, PDFs, OCR text, private paper
content, or copyrighted article excerpts. Those remain local under ignored paths.

## Limitations

- This is a local-first skill group and harness, not a UI product.
- It does not generate a paper in one click.
- App Server integration is mocked; real transport binding remains future work.
- Venue-specific formatting templates are intentionally out of scope for v1.
