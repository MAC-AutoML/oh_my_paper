# LaTeX compile guide

## Workspace shape

The built-in template expects this structure:

```text
main.tex
references.bib
template/*.cls
content/resources/*.tex
content/sec/0_abstract.tex
content/sec/1_intro.tex
content/sec/2_related.tex
content/sec/3_method.tex
content/sec/4_experiments.tex
content/sec/5_conclusion.tex
content/sec/append.tex
content/figures/
content/tables/
assets/branding/
assets/fonts/
```

## Preferred compilation

From the LaTeX workspace:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Fallback:

```bash
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## Template note

The bundled template falls back to Liberation Sans/Mono when Noto Sans families are unavailable, so a minimal TeX Live install can still compile the demo workspace.

## Common fixes

- `Undefined control sequence` near template font logic: use XeLaTeX, not pdfLaTeX.
- Missing citation output: run BibTeX between XeLaTeX passes and check `references.bib` keys.
- Missing image: copy files into `content/figures/` or update `\graphicspath`.
- Broken non-ASCII text: compile with XeLaTeX.
- Overfull boxes: shorten captions, break URLs, or move dense content to appendix.

## Citation discipline

Use `\citep{key}` / `\citet{key}` consistently. For demo papers, prefer representative and well-known references over obscure padding. Do not add a BibTeX entry unless the work is known, user-provided, or verified.
