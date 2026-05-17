#!/usr/bin/env bash
set -euo pipefail
workspace="${1:-.}"
cd "$workspace"
if [[ ! -f main.tex ]]; then
  echo "main.tex not found in $workspace" >&2
  exit 2
fi
if command -v latexmk >/dev/null 2>&1; then
  latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
elif command -v xelatex >/dev/null 2>&1; then
  xelatex -interaction=nonstopmode -halt-on-error main.tex
  if command -v bibtex >/dev/null 2>&1 && [[ -f references.bib ]]; then
    bibtex main || true
  fi
  xelatex -interaction=nonstopmode -halt-on-error main.tex
  xelatex -interaction=nonstopmode -halt-on-error main.tex
else
  echo "No LaTeX compiler found. Install TeX Live/MacTeX with latexmk or xelatex." >&2
  exit 127
fi
