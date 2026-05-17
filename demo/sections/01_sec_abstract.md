# Abstract

## Section contract

- Reader question: Summarize the evaluation gap, selected idea, iterative workflow, synthetic evidence boundary, and reviewer-gated contribution.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

Recent reinforcement learning evaluations often compress policy quality into mean return, yet mean return can hide seed fragility, perturbation brittleness, and shortcut-driven behavior. This demo paper introduces PolicyBench-Reliability, a proposed evaluation workflow that turns user-provided PPO-oriented material into a reliability-focused benchmark narrative. The workflow first extracts multiple candidate paper ideas from the input, asks a reviewer model to select the most promising direction, and then writes each section through a repeated contract, draft, critique, and revision loop. Instead of treating the first generated paragraph as final, every section carries a reader question, claim IDs, evidence status, caveats, and a Chinese explanation of why the section is structured that way. A synthetic reporting example illustrates how an algorithm can appear competitive under average return while receiving lower diagnostic credit when stability, robustness, and decision support are considered jointly. All numbers in the demo are labeled illustrative rather than empirical. The resulting artifact demonstrates how oh my paper should coordinate Codex skills, reviewer agents, and image-generation prompts to produce long academic prose that remains auditable, revisable, and honest about evidence boundaries.
