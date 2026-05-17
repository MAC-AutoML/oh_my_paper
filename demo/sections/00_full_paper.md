# PolicyBench-Reliability: An Iterative Evaluation Workflow for Reliable Policy Optimization

## Abstract

Recent reinforcement learning evaluations often compress policy quality into mean return, yet mean return can hide seed fragility, perturbation brittleness, and shortcut-driven behavior. This demo paper introduces PolicyBench-Reliability, a proposed evaluation workflow that turns user-provided PPO-oriented material into a reliability-focused benchmark narrative. The workflow first extracts multiple candidate paper ideas from the input, asks a reviewer model to select the most promising direction, and then writes each section through a repeated contract, draft, critique, and revision loop. Instead of treating the first generated paragraph as final, every section carries a reader question, claim IDs, evidence status, caveats, and a Chinese explanation of why the section is structured that way. A synthetic reporting example illustrates how an algorithm can appear competitive under average return while receiving lower diagnostic credit when stability, robustness, and decision support are considered jointly. All numbers in the demo are labeled illustrative rather than empirical. The resulting artifact demonstrates how oh my paper should coordinate Codex skills, reviewer agents, and image-generation prompts to produce long academic prose that remains auditable, revisable, and honest about evidence boundaries.

## 1. Introduction

Policy-gradient methods such as PPO are widely used because they combine implementation simplicity with comparatively stable updates. That popularity makes PPO a good seed material for a writing demo, but it also exposes a recurring evaluation problem: a method can achieve strong mean return without being reliable across seeds, perturbations, or decision probes. A paper that only reports the mean therefore risks answering the wrong reviewer question. The reviewer wants to know not only whether a policy wins, but whether the result is repeatable, robust, and supported by task-relevant state information.

PolicyBench-Reliability is framed as a benchmark/evaluation paper because the input material is primarily about measurement failure. The workflow extracts candidate angles from the user material, rejects directions that would require unsupported real experiments, and selects a conservative thesis: average-return reporting should be complemented by reliability diagnostics. This choice is intentionally different from hard-coding a paper title in the prompt. In a live run, the idea-selection agent would propose several candidate papers, a Gemini-compatible reviewer endpoint would score them, and the orchestrator would select the highest-value direction before any long drafting begins.

The contribution is therefore procedural and methodological. First, the demo shows how to decompose a broad topic into a sectioned paper plan. Second, it demonstrates a multi-round writing loop in which every section is revised after critique. Third, it shows how reviewer scoring can drive further revision until an acceptance threshold is reached. Fourth, it separates deterministic previews from generated figures by preserving imagegen prompts and audit criteria.

## 2. Related Work

The first related line is policy optimization evaluation. PPO-style reports often compare objectives, hyperparameters, and return curves, which is useful but incomplete when the paper claim concerns reliability. The demo borrows the habit of ablation-style reporting while refusing to invent real environment results. Any table in this demo is a format example unless a source artifact provides actual measurements.

The second line is benchmark and dataset writing. Mature benchmark papers are persuasive when the benchmark design, scoring rule, quality control, and analysis all support one story. This demo uses that pattern without reusing the prior project name or importing a fixed benchmark acronym. The design lesson is general: if a paper claims that old evaluation is saturated or misleading, its experiments must show what the old metric hides.

The third line is AI-assisted academic writing. A single LLM call can produce fluent prose, but fluency is not the same as evidence discipline. oh my paper therefore treats writing as a loop among owner skills: idea selection, writing, figures, review, and revision. Each role has a bounded responsibility, and the reviewer role is allowed to block the draft until the score reaches the configured threshold.

## 3. Method

The workflow begins with structured intake. The user material is converted into a compact input card containing topic, candidate claims, evidence status, forbidden overclaims, target venue style, and desired outputs. From this card, an idea agent proposes several paper directions. For the PPO-oriented demo, plausible directions include a reliability benchmark, a tutorial survey, a reproduction protocol, and a robustness checklist. A reviewer model then scores these directions for novelty, feasibility, evidence fit, and risk. The selected direction becomes the paper contract.

After selection, the writing loop operates section by section. A planner produces a section contract with a reader question, section job, claim IDs, paragraph messages, required evidence, and caveats. A drafting agent writes the section from that contract. A critic agent audits unsupported claims, paragraph drift, weak transitions, and missing caveats. A revision agent rewrites the section. The loop can repeat until the reviewer score reaches the configured acceptance target, which is 85 in this demo protocol.

The reviewer is not merely a grammar checker. It returns a structured score with dimensions for problem framing, evidence discipline, method clarity, experiment credibility, figure usefulness, limitations, and overall readiness. If the score is below threshold, the orchestrator creates a revision brief and sends it back to the relevant owner skill. This makes the flow closer to a small research team than to a one-shot prompt.

Figures follow a separate path. The figure agent reads the latest section claims and writes figure intent cards. Each card becomes a prompt for Codex imagegen. Deterministic SVG previews may exist for reproducibility, but generated paper figures should be produced through imagegen and then audited for text accuracy, unsupported values, and caption alignment.

## 4. Demonstration and Synthetic Results

This demo uses synthetic values only to show how a reliability paper would present results. The example compares a mean-return view with a diagnostic view. Under the mean-return view, PPO-like and off-policy baselines appear close. Under the diagnostic view, policies lose credit when performance varies across seeds, collapses under perturbation, or lacks support from task-relevant state features.

| Method | Mean-return view | Stability check | Robustness check | Decision-support check | Diagnostic score |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO-style baseline | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |
| Off-policy baseline | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |
| Deterministic actor baseline | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |
| Reference policy | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |

The intended lesson is structural rather than empirical. A real paper would need environment definitions, public seeds, perturbation settings, training curves, statistical intervals, and reproducible code. The demo table simply illustrates the kind of discrepancy that motivates diagnostic evaluation. The reviewer loop should penalize any draft that presents this table as a real PPO result.

## 5. Discussion

The most important observation is that long academic writing needs governance. Without an explicit loop, the model can produce a polished but unsupported section. With a loop, each section must declare what question it answers, what evidence it has, and what remains uncertain. This is especially important for benchmark papers because benchmark claims often sound authoritative even when the dataset or protocol is only proposed.

The reviewer threshold also changes the behavior of the system. If the acceptance target is 85, the first draft is expected to fail unless it already has clear claims, evidence boundaries, figures, and limitations. Failure is not treated as a dead end; it becomes a revision brief. This mirrors software testing: a failing review identifies the next patch.

Finally, image generation is separated from scientific evidence. The figure prompt can make the story easier to understand, but it cannot create evidence. The caption and audit must still point back to claims, tables, or protocols.

## 6. Limitations

This repository demo is deterministic and offline. It does not call a live Gemini endpoint during committed generation, does not run RL environments, and does not create final raster figures. Instead, it records the prompts and protocols that a live run should execute. This boundary is deliberate: committed demo outputs should be reproducible without secrets or network availability.

A live run would add three elements. First, it would use the configured reviewer model to select among candidate paper ideas. Second, it would iterate section drafts until the reviewer score reaches the configured threshold or a maximum round limit is hit. Third, it would call Codex imagegen to produce bitmap figures and save them with an audit trail.

The demo also does not guarantee that an 85 score means publishability. It means the configured reviewer agent judged the draft acceptable according to the local rubric. Human supervision remains necessary for real claims, real citations, and real submission decisions.

## 7. Conclusion

This demo reframes oh my paper as an iterative research-writing system rather than a single prompt that emits a paper. Starting from user material, the system should generate candidate directions, ask a reviewer model to choose the strongest one, write sections through multi-agent loops, produce imagegen prompts from final claims, and revise until the reviewer score reaches a target such as 85. The section-based output layout makes that process visible: every section has its own artifact, every figure has its own prompt, and every major writing decision has a Chinese explanation. The result is not just longer text, but a more inspectable and controllable academic workflow.
