# Milestone 6 — Packaging and Installation

Milestone 6 makes local installation repeatable while following the official
Codex skills installer standard. This repository provides skill folders and
installer-compatible paths; it does **not** replace Codex's system
`skill-installer`.

## Official installation path

Use Codex's system `skill-installer` skill / helper script:

```bash
install-skill-from-github.py --repo MAC-AutoML/oh_my_paper \
  --path skills/paper-ai-orchestrator \
  --path skills/paper-ai-research-process \
  --path skills/paper-ai-writing \
  --path skills/paper-ai-figures \
  --path skills/paper-ai-layout \
  --path skills/paper-ai-reviewer \
  --path skills/paper-ai-rebuttal \
  --path skills/paper-ai-eval-loop
```

The official installer installs into `$CODEX_HOME/skills/<skill-name>` and
aborts if a destination skill already exists unless the official helper options
say otherwise. Restart Codex after installing skills.

## Packaging metadata helper

This project includes a metadata-only helper so maintainers can verify the paths
that should be passed to the official installer:

```bash
uv run oh-my-paper packaging-status
```

This command prints the official repo/path command and checks each skill folder
has a required `SKILL.md`. It is not a competing installer.

## Clean checkout verification

```bash
git clone https://github.com/MAC-AutoML/oh_my_paper.git
cd oh_my_paper
uv run oh-my-paper status
uv run oh-my-paper packaging-status
uv run python -m unittest discover -s tests -p 'test_*.py' -v
uv run oh-my-paper init /tmp/ohmp-demo
uv run oh-my-paper run-demo /tmp/ohmp-demo
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
