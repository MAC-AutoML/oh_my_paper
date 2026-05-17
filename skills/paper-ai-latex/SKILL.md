---
name: paper-ai-latex
description: LaTeX 论文模板与 PDF 编译（中英文） | Prepare an arXiv-style LaTeX paper workspace from oh my paper outputs, manage BibTeX references, and compile with XeLaTeX/latexmk when local TeX tools are available.
---

# paper-ai-latex

## Use when / 适用场景

- Use when the user wants to turn an oh my paper Markdown/section draft into a LaTeX workspace or PDF. / 当用户要把 oh my paper 的 Markdown/章节草稿转成 LaTeX 工作区或 PDF 时使用。
- Use for arXiv-style template setup, `references.bib` checks, section-to-`.tex` mapping, and compile troubleshooting. / 用于 arXiv 风格模板、BibTeX、章节映射和编译排错。

## Inputs / 输入

- Paper workspace or section files, e.g. `paper/FULL_PAPER_DRAFT.md`, `sections/*.md`, figures, tables, `references.bib`.
- Target mode: draft, arXiv preprint, camera-ready, anonymous submission, or local proof.

## Outputs / 输出

- A copied LaTeX workspace based on `assets/arxiv_template/`.
- Updated `main.tex`, `content/sec/*.tex`, `references.bib`, and optional `compile.log`.
- A PDF only if local TeX tools successfully compile it.

## Built-in template / 内置模板

The bundled template lives at `assets/arxiv_template/`. It is adapted from `MAC-AutoML/Arxiv_Template` and excludes the removed university logo asset and header reference.

## Workflow / 流程

1. Copy the bundled template into the target paper directory, never editing the skill asset in place.
2. Replace title, authors, affiliations, contact lines, and header logos in `main.tex` according to the user's paper.
3. Convert or paste sections into `content/sec/`:
   - abstract -> `0_abstract.tex`
   - introduction -> `1_intro.tex`
   - related work -> `2_related.tex`
   - method -> `3_method.tex`
   - experiments/results -> `4_experiments.tex`
   - conclusion -> `5_conclusion.tex`
   - appendix -> `append.tex`
4. Maintain `references.bib`; a demo paper should usually carry 15--20 representative references unless the user asks for a shorter citation set.
5. Compile with `scripts/compile_latex.sh <workspace>` or an equivalent XeLaTeX/BibTeX sequence.
6. If TeX is missing, do not claim success. Report missing tools and leave a reproducible workspace.

## Compile policy / 编译策略

Preferred local command:

```bash
bash skills/paper-ai-latex/scripts/compile_latex.sh /path/to/latex-workspace
```

The script tries `latexmk -xelatex` first, then falls back to `xelatex -> bibtex -> xelatex -> xelatex`. See `references/latex-compile-guide.md` when troubleshooting.

## Gates / 质量门

- Do not fabricate citations. Add BibTeX only for known representative works, user-provided sources, or verified sources.
- Do not present synthetic demo numbers as real experimental results.
- Keep source assets and generated PDFs separate from raw private material.
- The built-in template must not contain `UR.png` or removed university logo references.

## References to load as needed / 按需加载参考

- `references/latex-compile-guide.md` for compile commands, common errors, and section mapping.
