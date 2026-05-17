# PolicyBench-Reliability: An Iterative Evaluation Workflow for Reliable Policy Optimization

## Abstract

Recent reinforcement learning evaluations often compress policy quality into mean return, yet mean return can hide seed fragility, perturbation brittleness, and shortcut-driven behavior. This demo paper introduces PolicyBench-Reliability, a proposed evaluation workflow that turns user-provided PPO-oriented material into a reliability-focused benchmark narrative. PPO is a useful seed because it is widely adopted for stable policy-gradient updates, but the reproducibility literature shows that even familiar deep RL baselines require careful statistical treatment and protocol disclosure [2,3,11,12]. The workflow first extracts multiple candidate paper ideas from the input, asks a reviewer model to select the most promising direction, and then writes each section through a repeated contract, draft, critique, and revision loop. Instead of treating the first generated paragraph as final, every section carries a reader question, claim IDs, evidence status, caveats, and a Chinese explanation of why the section is structured that way. A synthetic reporting example illustrates how an algorithm can appear competitive under average return while receiving lower diagnostic credit when stability, robustness, and decision support are considered jointly. All numbers in the demo are labeled illustrative rather than empirical. The resulting artifact demonstrates how oh my paper should coordinate Codex skills, reviewer agents, citations, LaTeX packaging, and image-generation prompts to produce long academic prose that remains auditable, revisable, and honest about evidence boundaries.

## 1. Introduction

Policy-gradient methods such as PPO are widely used because they combine implementation simplicity with comparatively stable updates [2,3]. That popularity makes PPO a good seed material for a writing demo, but it also exposes a recurring evaluation problem: a method can achieve strong mean return without being reliable across seeds, perturbations, or decision probes. Standardized environments such as ALE and Gym made progress measurable [5,7], yet later protocol work and reproducibility studies showed that score reporting can be sensitive to seeds, implementation choices, and statistical summarization [6,11,12]. A paper that only reports the mean therefore risks answering the wrong reviewer question. The reviewer wants to know not only whether a policy wins, but whether the result is repeatable, robust, and supported by task-relevant state information.

PolicyBench-Reliability is framed as a benchmark/evaluation paper because the input material is primarily about measurement failure. The workflow extracts candidate angles from the user material, rejects directions that would require unsupported real experiments, and selects a conservative thesis: average-return reporting should be complemented by reliability diagnostics. This choice is intentionally different from hard-coding a paper title in the prompt. In a live run, the idea-selection agent would propose several candidate papers, a Gemini-compatible reviewer endpoint would score them, and the orchestrator would select the highest-value direction before any long drafting begins.

The contribution is therefore procedural and methodological. First, the demo shows how to decompose a broad topic into a sectioned paper plan. Second, it demonstrates a multi-round writing loop in which every section is revised after critique. Third, it shows how reviewer scoring can drive further revision until an acceptance threshold is reached. Fourth, it separates deterministic previews from generated figures by preserving imagegen prompts and audit criteria. Fifth, it adds representative citation scaffolding and a LaTeX compilation skill so that the demo resembles a real paper pipeline rather than a prose-only mockup.

## 2. Related Work

The first related line is policy optimization evaluation. PPO-style reports often compare objectives, hyperparameters, and return curves [2,3], while off-policy baselines such as DDPG, TD3, and SAC provide contrasting stability and sample-efficiency assumptions [8,9,10]. These comparisons are useful but incomplete when the paper claim concerns reliability. The demo borrows the habit of ablation-style reporting while refusing to invent real environment results. Any table in this demo is a format example unless a source artifact provides actual measurements.

The second line is benchmark and evaluation methodology. Atari, Gym, and Procgen illustrate how standardized environments shape research questions [5,7,13]. However, benchmark methodology papers also warn that environment choice, evaluation protocol, random seeds, and statistical summaries can change conclusions [6,11,12]. Mature benchmark papers are persuasive when the design, scoring rule, quality control, and analysis all support one story. This demo uses that pattern without reusing a prior benchmark acronym. The design lesson is general: if a paper claims that old evaluation is saturated or misleading, its experiments must show what the old metric hides.

The third line is reliability and alignment-oriented RL. Real-world RL and AI safety work emphasize robustness, deployment constraints, human preferences, and objective misspecification [14,15,16,17,18]. These references motivate why a policy should not be judged only by a scalar reward curve. They do not prove that the synthetic values in this demo are true; instead, they justify the kind of diagnostic questions a real paper would need to answer.

The fourth line is AI-assisted academic writing. A single LLM call can produce fluent prose, but fluency is not the same as evidence discipline. oh my paper therefore treats writing as a loop among owner skills: idea selection, writing, figures, review, revision, and LaTeX packaging. Each role has a bounded responsibility, and the reviewer role is allowed to block the draft until the score reaches the configured threshold.

## 3. Method

The workflow begins with structured intake. The user material is converted into a compact input card containing topic, candidate claims, evidence status, forbidden overclaims, target venue style, and desired outputs. From this card, an idea agent proposes several paper directions. For the PPO-oriented demo, plausible directions include a reliability benchmark, a reproduction protocol for PPO-style experiments, a survey on RL evaluation failure modes, and a robustness checklist for policy updates. A reviewer model then scores these directions for novelty, feasibility, evidence fit, citation availability, and risk. The selected direction becomes the paper contract.

After selection, the writing loop operates section by section. A planner produces a section contract with a reader question, section job, claim IDs, paragraph messages, required evidence, and caveats. A drafting agent writes the section from that contract. A citation-aware pass checks whether representative works are needed for the claim type. A critic agent audits unsupported claims, paragraph drift, weak transitions, and missing caveats. A revision agent rewrites the section. The loop can repeat until the reviewer score reaches the configured acceptance target, which is 85 in this demo protocol.

The reviewer is not merely a grammar checker. It returns a structured score with dimensions for problem framing, evidence discipline, method clarity, experiment credibility, citation coverage, figure usefulness, limitations, and overall readiness. If the score is below threshold, the orchestrator creates a revision brief and sends it back to the relevant owner skill. This makes the flow closer to a small research team than to a one-shot prompt.

Figures and final packaging follow separate paths. The figure agent reads the latest section claims and writes figure intent cards. Each card becomes a prompt for Codex imagegen. The LaTeX skill then copies the built-in arXiv-style template, maps Markdown sections into `content/sec/*.tex`, carries over representative BibTeX entries, and compiles with XeLaTeX/BibTeX when local TeX tooling is available. Deterministic previews may exist for reproducibility, but generated paper figures should be produced through imagegen and then audited for text accuracy, unsupported values, and caption alignment.

## 4. Demonstration and Synthetic Results

This demo uses synthetic values only to show how a reliability paper would present results. The example compares a mean-return view with a diagnostic view. Under the mean-return view, PPO-like and off-policy baselines appear close. Under the diagnostic view, policies lose credit when performance varies across seeds, collapses under perturbation, or lacks support from task-relevant state features. This reporting style is motivated by reproducibility and statistical-evaluation concerns in deep RL [11,12], but the values below are not copied from those works.

| Method | Mean-return view | Stability check | Robustness check | Decision-support check | Diagnostic score |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO-style baseline | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |
| Off-policy baseline | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |
| Deterministic actor baseline | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |
| Reference policy | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |

The intended lesson is structural rather than empirical. A real paper would need environment definitions, public seeds, perturbation settings, training curves, statistical intervals, and reproducible code. It would also need to compare against canonical baselines from both value-based and actor-critic traditions [4,8,9,10]. The demo table simply illustrates the kind of discrepancy that motivates diagnostic evaluation. The reviewer loop should penalize any draft that presents this table as a real PPO result.

## 5. Discussion

The most important observation is that long academic writing needs governance. Without an explicit loop, the model can produce a polished but unsupported section. With a loop, each section must declare what question it answers, what evidence it has, what citations are representative, and what remains uncertain. This is especially important for benchmark papers because benchmark claims often sound authoritative even when the dataset or protocol is only proposed.

The reviewer threshold also changes the behavior of the system. If the acceptance target is 85, the first draft is expected to fail unless it already has clear claims, evidence boundaries, citations, figures, and limitations. Failure is not treated as a dead end; it becomes a revision brief. This mirrors software testing: a failing review identifies the next patch.

Finally, image generation and LaTeX compilation are separated from scientific evidence. A figure prompt can make the story easier to understand, and a template can make the paper look submission-ready, but neither creates evidence. Captions, citations, and audit notes must still point back to claims, tables, protocols, or source material.

## 6. Limitations

This repository demo is deterministic and offline. It does not call a live Gemini endpoint during committed generation, does not run RL environments, does not verify every citation live at generation time, and does not create final raster figures. Instead, it records the prompts and protocols that a live run should execute. This boundary is deliberate: committed demo outputs should be reproducible without secrets or network availability.

A live run would add four elements. First, it would use the configured reviewer model to select among candidate paper ideas. Second, it would iterate section drafts until the reviewer score reaches the configured threshold or a maximum round limit is hit. Third, it would call Codex imagegen to produce bitmap figures and save them with an audit trail. Fourth, it would use the LaTeX skill to create a compile-ready workspace, run XeLaTeX/BibTeX if available, and surface missing compiler or citation errors honestly.

The demo also does not guarantee that an 85 score means publishability. It means the configured reviewer agent judged the draft acceptable according to the local rubric. Human supervision remains necessary for real claims, real citations, real experiments, and real submission decisions.

## 7. Conclusion

This demo reframes oh my paper as an iterative research-writing system rather than a single prompt that emits a paper. Starting from user material, the system should generate candidate directions, ask a reviewer model to choose the strongest one, write sections through multi-agent loops, attach representative citations, produce imagegen prompts from final claims, package the draft in LaTeX, and revise until the reviewer score reaches a target such as 85. The section-based output layout makes that process visible: every section has its own artifact, every figure has its own prompt, every major writing decision has a Chinese explanation, and the references section shows the expected citation density. The result is not just longer text, but a more inspectable and controllable academic workflow.

# References

Representative citation set for the demo paper:

1. Sutton and Barto (2018) define the reinforcement-learning problem and remain the standard background reference for value functions, policy optimization, and exploration.
2. Schulman et al. (2015) introduce trust-region policy optimization, motivating constrained policy updates before PPO.
3. Schulman et al. (2017) introduce proximal policy optimization, the PPO seed material for this demo.
4. Mnih et al. (2015) establish deep Q-learning on Atari and show how benchmark scores can drive rapid RL progress.
5. Bellemare et al. (2013) describe the Arcade Learning Environment, a canonical benchmark platform for RL evaluation.
6. Machado et al. (2018) revisit ALE evaluation protocols and motivate more careful benchmark methodology.
7. Brockman et al. (2016) introduce OpenAI Gym, making standardized environment APIs central to RL reporting.
8. Lillicrap et al. (2016) propose DDPG, a deterministic actor-critic baseline often compared with policy-gradient methods.
9. Fujimoto et al. (2018) propose TD3, showing how implementation and evaluation details affect continuous-control comparisons.
10. Haarnoja et al. (2018) introduce soft actor-critic, a strong off-policy baseline for stability-oriented discussions.
11. Henderson et al. (2018) show that deep RL results can be fragile across seeds, codebases, and hyperparameters.
12. Agarwal et al. (2021) argue that aggregate point estimates can be statistically misleading in deep RL benchmarks.
13. Cobbe et al. (2019) introduce Procgen to study generalization rather than memorized environment behavior.
14. Dulac-Arnold et al. (2021) summarize challenges for real-world RL, including robustness, safety, and deployment constraints.
15. Amodei et al. (2016) frame concrete AI safety problems that motivate robust and honest evaluation beyond reward maximization.
16. Christiano et al. (2017) connect reinforcement learning with human preferences, highlighting evaluation issues around learned objectives.
17. Ouyang et al. (2022) show instruction-following alignment with human feedback, a modern policy-optimization application context.
18. Bai et al. (2022) discuss constitutional AI and preference-based alignment, reinforcing why policy quality cannot be reduced to one scalar reward.

## Citation note

These references are included to demonstrate expected citation coverage for a PPO/RL evaluation demo. A live paper run should verify metadata with the configured citation checker and replace representative placeholders with the exact works used by the author. The companion `demo/references.bib` file provides BibTeX scaffolding for these entries.
