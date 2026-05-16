# Material Intake and Fusion Workflow

## Purpose

`oh my paper` is designed to keep improving as new writing, figure, review, and rebuttal material arrives. The material loop must absorb private or copyrighted sources without publishing them. Raw sources and extracted text stay in ignored local folders; only safe process documentation, synthetic tests, and skill/eval changes are committed.

## Local-only storage contract

- Put newly collected files in `/temp/` or another local staging path.
- Ingested material is copied under `/materials/paper-ai/external/<material-id>/`.
- `/temp/` and `/materials/` are ignored by git.
- Do not commit PDFs, screenshots, OCR text, private repo names, or verbatim proprietary summaries.
- Commit only:
  - general workflow docs;
  - synthetic tests and fixtures;
  - public-safe synthesis;
  - skill changes derived from the synthesis;
  - eval cases that use synthetic or redacted content.

## Intake command

For a PDF with embedded text:

```bash
uv run oh-my-paper intake-material \
  'temp/new-material.pdf' \
  --material-id short-stable-id
```

Optional root override:

```bash
uv run oh-my-paper intake-material 'temp/new-material.pdf' \
  --material-id short-stable-id \
  --materials-root materials/paper-ai
```

The command writes:

- `materials/paper-ai/external/<material-id>/raw/<source>.pdf`
- `materials/paper-ai/external/<material-id>/raw/text.txt`
- `materials/paper-ai/external/<material-id>/index.md`
- `materials/paper-ai/intake-index.jsonl`

The generated `index.md` is a local working note, not a publication artifact.

## Classification categories

Material is routed into the current skill group categories:

| Category | Typical skill impact |
| --- | --- |
| `research-process` | topic selection, problem framing, experiments |
| `writing` | title, abstract, introduction, claim/evidence drafting |
| `figures` / `paper-checking` | visual clarity, first-page impression, checklist gates |
| `review-rating` | reviewer simulation, score-risk triage, AC-facing risk |
| `rebuttal` | response strategy, evidence table, promise control |
| `workflow-infra` | harness, trace, packaging, adapter behavior |

## Fusion/update loop

After each intake:

1. Read the local `index.md` and raw text only inside the private workspace.
2. Convert lessons into public-safe bullets: no long quotes, no private names, no raw reviewer text.
3. Map each bullet to one of four change types:
   - skill instruction update;
   - gate/checklist update;
   - synthetic regression fixture;
   - roadmap backlog item.
4. Update tracked docs only at the abstraction level needed to guide implementation.
5. If behavior changes, add or update tests before claiming the material is fused.
6. Run the validation commands listed in the README.

## Example: internal review/title meeting intake

A local meeting PDF about review flow and title writing was ingested under a private material ID. Its public-safe impact is category-level only:

- reviewer simulation should model time pressure and first-impression effects;
- title, abstract, first two pages, and first figure should be explicit writing gates;
- rebuttal should be treated as limited correction, not a replacement for submission quality;
- figure readability should be checked before reviewer simulation.

No raw transcript or PDF text is tracked.

## OCR and screenshot fallback

The current command uses local `pdftotext -layout` and is best for text PDFs. For scanned PDFs or slide decks where extraction is poor:

1. render pages or screenshots locally under `/temp/`;
2. use OCR/vision tooling to create a private transcript under `/materials/`;
3. write only public-safe synthesis into tracked docs or synthetic evals;
4. mark OCR uncertainty in the local material index.

Do not add OCR dependencies until a concrete scanned-material case requires them.
