# 2. Related Work

## Section contract

- Reader question: Position the demo against RL evaluation practice, benchmark-writing logic, and iterative AI writing systems.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

The first related line is policy optimization evaluation. PPO-style reports often compare objectives, hyperparameters, and return curves, which is useful but incomplete when the paper claim concerns reliability. The demo borrows the habit of ablation-style reporting while refusing to invent real environment results. Any table in this demo is a format example unless a source artifact provides actual measurements.

The second line is benchmark and dataset writing. Mature benchmark papers are persuasive when the benchmark design, scoring rule, quality control, and analysis all support one story. This demo uses that pattern without reusing the prior project name or importing a fixed benchmark acronym. The design lesson is general: if a paper claims that old evaluation is saturated or misleading, its experiments must show what the old metric hides.

The third line is AI-assisted academic writing. A single LLM call can produce fluent prose, but fluency is not the same as evidence discipline. oh my paper therefore treats writing as a loop among owner skills: idea selection, writing, figures, review, and revision. Each role has a bounded responsibility, and the reviewer role is allowed to block the draft until the score reaches the configured threshold.
