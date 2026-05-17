# 如何复现这个 section-based demo

```bash
uv run python demo/run_demo.py
```

输出结构：

```text
demo/sections/01_sec_abstract.md
demo/sections/02_sec_introduction.md
...
demo/figures/fig_01_workflow_prompt.md
demo/explain/01_why_abstract.md
```

连续运行两次，在输入不变时输出应保持稳定。
