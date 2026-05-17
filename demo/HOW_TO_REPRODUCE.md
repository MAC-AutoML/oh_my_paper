# 如何复现这个 section-based demo

```bash
uv run python demo/run_demo.py
```

输出结构：

```text
demo/sections/01_sec_abstract.md
demo/sections/02_sec_introduction.md
...
demo/sections/09_sec_references.md
demo/figures/fig_01_workflow_prompt.md
demo/explain/01_why_abstract.md
```

连续运行两次，在输入不变时输出应保持稳定。

## LaTeX packaging

真实运行时可用 `paper-ai-latex` skill 将章节与 references 转入内置 arXiv-style LaTeX 模板，并在本地 TeX 工具存在时编译 PDF。这个 committed demo 只保留稳定 Markdown 产物。
