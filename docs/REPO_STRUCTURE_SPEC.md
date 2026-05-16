# Repository Structure Specification

## 1. Current policy

Tracked repository should contain curated project docs and future implementation code. Raw research/material downloads stay local and ignored.

Ignored local directories:

- `.omx/`
- `.spec-workflow/`
- `materials/`
- `temp/`
- `node_modules/`
- package lock files created for local rendering/collection

## 2. Target skeleton

```text
oh_my_paper/
  README.md
  AGENTS.md
  pyproject.toml
  uv.lock
  .gitignore
  .codex-plugin/
    plugin.json
  docs/
    00_OVERVIEW.md
    PRD.md
    SKILL_GROUP_ARCHITECTURE.md
    DUAL_MODE_TECH_DESIGN.md
    HARNESS_EVAL_LOOP.md
    ROADMAP.md
    REPO_STRUCTURE_SPEC.md
    ACCEPTANCE_EVALS.md
    MATERIALS_MAPPING.md
    adr/
  skills/
    paper-ai-orchestrator/
      SKILL.md
      references/
      scripts/
      assets/
      evals/README.md       # examples/links only; canonical fixtures are in tests/fixtures/evals
    paper-ai-research-process/
    paper-ai-writing/
    paper-ai-figures/
    paper-ai-layout/
    paper-ai-reviewer/
    paper-ai-rebuttal/
    paper-ai-eval-loop/
  src/
    oh_my_paper/
      __init__.py
      artifacts/
      gates/
      router/
      runtime/
      evals/
      traces/
      cli/
  tests/
    unit/
    integration/
    fixtures/
      evals/                # canonical executable eval fixtures
  examples/
    toy-paper-workspace/
      paper/
      .paper-ai/
```

## 3. Python package boundaries

| Package | Responsibility |
| --- | --- |
| `artifacts` | Markdown/JSON artifact load/save, schema checks |
| `gates` | Evidence, visual, layout, reviewer, rebuttal, privacy gates |
| `router` | Phase detection and skill recommendation |
| `runtime` | `RuntimeAdapter`, local adapter, App Server adapter |
| `evals` | Fixture parser, evaluator registry, result reports |
| `traces` | Trace event schema and JSONL recorder |
| `cli` | `uv run oh-my-paper ...` commands |

## 4. File size rule

Implementation files should generally stay under 500 lines; 550 lines is the tolerated upper bound. Split by domain before adding large utility modules.

## 5. Skill file rule

Top-level `SKILL.md` files should be short and action-oriented:

- when to use / not use;
- required inputs;
- step sequence;
- output artifacts;
- gates;
- reference links.

Long rubrics belong in `references/`. Executable validators belong in `scripts/` or `src/`.

## 6. Example workspace rule

`examples/toy-paper-workspace/` should use synthetic content only. It is the default e2e fixture and must not include private research text.

## 7. Material cache rule

`materials/` may contain private repos, rendered PDFs, OCR output, and copyrighted summaries. It is a local design/reference cache, not a package asset. Public repo docs may point to local paths for maintainers but must not require them for normal user installation.

## 8. Future command surface

Possible CLI commands:

```bash
uv run oh-my-paper init
uv run oh-my-paper status
uv run oh-my-paper validate-artifacts
uv run oh-my-paper run-eval tests/fixtures/evals/unsupported_claim.jsonl
uv run oh-my-paper capture-fixture .paper-ai/TRACE.jsonl --event evt_123
```

## 9. Eval fixture location rule

The canonical executable fixture location is `tests/fixtures/evals/`. This keeps regression cases runnable by one shared harness and avoids copying fixture logic into each skill. Skill-local `evals/` folders may document relevant fixtures or contain non-authoritative examples only.

## 10. Packaging notes

- Use `uv` for dependency management.
- Keep optional App Server dependencies separated from core local validators if possible.
- Avoid new heavy dependencies until a script/eval requires them.
