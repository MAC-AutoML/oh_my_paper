# oh my paper arXiv LaTeX template

This is the built-in LaTeX template used by the `paper-ai-latex` skill. It is adapted from `MAC-AutoML/Arxiv_Template` for oh my paper workflows. The removed university logo asset and header reference have been removed.

## Structure

- `main.tex`: entrypoint; set this as the Overleaf main file.
- `references.bib`: BibTeX database.
- `template/`: class files and shared template macros.
- `content/sec/`: paper sections.
- `content/resources/`: local packages and math macros.
- `content/figures/`: paper figures.
- `content/tables/`: table sources.
- `assets/branding/`: reusable paper or group logos.
- `assets/fonts/`: fonts required by the template.

## Compile

Use XeLaTeX and BibTeX:

```bash
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

If `latexmk` is available:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

## Edit points

Update title, authors, affiliations, contact, links, section files, figures, and `references.bib`. Keep generated PDFs and build intermediates out of the skill asset.
