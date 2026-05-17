# 1. Introduction

## Section contract

- Reader question: Explain why the user material becomes a reliability-evaluation paper rather than a new optimizer paper.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Citation status: representative references are included for field positioning; synthetic values remain non-empirical.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

Policy-gradient methods such as PPO are widely used because they combine implementation simplicity with comparatively stable updates [2,3]. That popularity makes PPO a good seed material for a writing demo, but it also exposes a recurring evaluation problem: a method can achieve strong mean return without being reliable across seeds, perturbations, or decision probes. Standardized environments such as ALE and Gym made progress measurable [5,7], yet later protocol work and reproducibility studies showed that score reporting can be sensitive to seeds, implementation choices, and statistical summarization [6,11,12]. A paper that only reports the mean therefore risks answering the wrong reviewer question. The reviewer wants to know not only whether a policy wins, but whether the result is repeatable, robust, and supported by task-relevant state information.

PolicyBench-Reliability is framed as a benchmark/evaluation paper because the input material is primarily about measurement failure. The workflow extracts candidate angles from the user material, rejects directions that would require unsupported real experiments, and selects a conservative thesis: average-return reporting should be complemented by reliability diagnostics. This choice is intentionally different from hard-coding a paper title in the prompt. In a live run, the idea-selection agent would propose several candidate papers, a Gemini-compatible reviewer endpoint would score them, and the orchestrator would select the highest-value direction before any long drafting begins.

The contribution is therefore procedural and methodological. First, the demo shows how to decompose a broad topic into a sectioned paper plan. Second, it demonstrates a multi-round writing loop in which every section is revised after critique. Third, it shows how reviewer scoring can drive further revision until an acceptance threshold is reached. Fourth, it separates deterministic previews from generated figures by preserving imagegen prompts and audit criteria. Fifth, it adds representative citation scaffolding and a LaTeX compilation skill so that the demo resembles a real paper pipeline rather than a prose-only mockup.
