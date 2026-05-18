"""Templates for the section-based oh my paper demo."""

from __future__ import annotations

import hashlib
from pathlib import Path

PROJECT = 'PolicyBench-Reliability'
TITLE = 'PolicyBench-Reliability: An Iterative Evaluation Workflow for Reliable Policy Optimization'

BIBTEX = r"""@book{sutton2018reinforcement,
  title     = {Reinforcement Learning: An Introduction},
  author    = {Sutton, Richard S. and Barto, Andrew G.},
  edition   = {2},
  year      = {2018},
  publisher = {MIT Press}
}

@inproceedings{schulman2015trpo,
  title     = {Trust Region Policy Optimization},
  author    = {Schulman, John and Levine, Sergey and Abbeel, Pieter and Jordan, Michael and Moritz, Philipp},
  booktitle = {International Conference on Machine Learning},
  year      = {2015}
}

@article{schulman2017ppo,
  title   = {Proximal Policy Optimization Algorithms},
  author  = {Schulman, John and Wolski, Filip and Dhariwal, Prafulla and Radford, Alec and Klimov, Oleg},
  journal = {arXiv preprint arXiv:1707.06347},
  year    = {2017}
}

@article{mnih2015dqn,
  title   = {Human-level control through deep reinforcement learning},
  author  = {Mnih, Volodymyr and Kavukcuoglu, Koray and Silver, David and others},
  journal = {Nature},
  volume  = {518},
  number  = {7540},
  pages   = {529--533},
  year    = {2015}
}

@article{bellemare2013ale,
  title   = {The Arcade Learning Environment: An Evaluation Platform for General Agents},
  author  = {Bellemare, Marc G. and Naddaf, Yavar and Veness, Joel and Bowling, Michael},
  journal = {Journal of Artificial Intelligence Research},
  volume  = {47},
  pages   = {253--279},
  year    = {2013}
}

@article{machado2018ale,
  title   = {Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents},
  author  = {Machado, Marlos C. and Bellemare, Marc G. and Talvitie, Erik and Veness, Joel and Hausknecht, Matthew and Bowling, Michael},
  journal = {Journal of Artificial Intelligence Research},
  volume  = {61},
  pages   = {523--562},
  year    = {2018}
}

@article{brockman2016gym,
  title   = {{OpenAI Gym}},
  author  = {Brockman, Greg and Cheung, Vicki and Pettersson, Ludwig and Schneider, Jonas and Schulman, John and Tang, Jie and Zaremba, Wojciech},
  journal = {arXiv preprint arXiv:1606.01540},
  year    = {2016}
}

@inproceedings{lillicrap2016ddpg,
  title     = {Continuous control with deep reinforcement learning},
  author    = {Lillicrap, Timothy P. and Hunt, Jonathan J. and Pritzel, Alexander and others},
  booktitle = {International Conference on Learning Representations},
  year      = {2016}
}

@inproceedings{fujimoto2018td3,
  title     = {Addressing Function Approximation Error in Actor-Critic Methods},
  author    = {Fujimoto, Scott and van Hoof, Herke and Meger, David},
  booktitle = {International Conference on Machine Learning},
  year      = {2018}
}

@inproceedings{haarnoja2018sac,
  title     = {Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor},
  author    = {Haarnoja, Tuomas and Zhou, Aurick and Abbeel, Pieter and Levine, Sergey},
  booktitle = {International Conference on Machine Learning},
  year      = {2018}
}

@inproceedings{henderson2018reproducibility,
  title     = {Deep Reinforcement Learning that Matters},
  author    = {Henderson, Peter and Islam, Riashat and Bachman, Philip and Pineau, Joelle and Precup, Doina and Meger, David},
  booktitle = {AAAI Conference on Artificial Intelligence},
  year      = {2018}
}

@inproceedings{agarwal2021statistical,
  title     = {Deep Reinforcement Learning at the Edge of the Statistical Precipice},
  author    = {Agarwal, Rishabh and Schwarzer, Max and Castro, Pablo Samuel and Courville, Aaron C. and Bellemare, Marc G.},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2021}
}

@inproceedings{cobbe2019procgen,
  title     = {Leveraging Procedural Generation to Benchmark Reinforcement Learning},
  author    = {Cobbe, Karl and Hesse, Christopher and Hilton, Jacob and Schulman, John},
  booktitle = {International Conference on Machine Learning},
  year      = {2020}
}

@article{dulacarnold2021realworld,
  title   = {Challenges of real-world reinforcement learning: definitions, benchmarks and analysis},
  author  = {Dulac-Arnold, Gabriel and Levine, Nir and Mankowitz, Daniel J. and Li, Jerry and Paduraru, Cosmin and Gowal, Sven and Hester, Todd},
  journal = {Machine Learning},
  volume  = {110},
  pages   = {2419--2468},
  year    = {2021}
}

@article{amodei2016concrete,
  title   = {Concrete Problems in AI Safety},
  author  = {Amodei, Dario and Olah, Chris and Steinhardt, Jacob and Christiano, Paul and Schulman, John and Man{'e}, Dan},
  journal = {arXiv preprint arXiv:1606.06565},
  year    = {2016}
}

@inproceedings{christiano2017preferences,
  title     = {Deep Reinforcement Learning from Human Preferences},
  author    = {Christiano, Paul F. and Leike, Jan and Brown, Tom B. and Martic, Miljan and Legg, Shane and Amodei, Dario},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2017}
}

@inproceedings{ouyang2022instructgpt,
  title     = {Training language models to follow instructions with human feedback},
  author    = {Ouyang, Long and Wu, Jeff and Jiang, Xu and others},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2022}
}

@article{bai2022constitutional,
  title   = {Constitutional AI: Harmlessness from AI Feedback},
  author  = {Bai, Yuntao and Kadavath, Saurav and Kundu, Sandipan and others},
  journal = {arXiv preprint arXiv:2212.08073},
  year    = {2022}
}
"""

BIBLIOGRAPHY = ['Sutton and Barto (2018) define the reinforcement-learning problem and remain the standard background reference for value functions, policy optimization, and exploration.', 'Schulman et al. (2015) introduce trust-region policy optimization, motivating constrained policy updates before PPO.', 'Schulman et al. (2017) introduce proximal policy optimization, the PPO seed material for this demo.', 'Mnih et al. (2015) establish deep Q-learning on Atari and show how benchmark scores can drive rapid RL progress.', 'Bellemare et al. (2013) describe the Arcade Learning Environment, a canonical benchmark platform for RL evaluation.', 'Machado et al. (2018) revisit ALE evaluation protocols and motivate more careful benchmark methodology.', 'Brockman et al. (2016) introduce OpenAI Gym, making standardized environment APIs central to RL reporting.', 'Lillicrap et al. (2016) propose DDPG, a deterministic actor-critic baseline often compared with policy-gradient methods.', 'Fujimoto et al. (2018) propose TD3, showing how implementation and evaluation details affect continuous-control comparisons.', 'Haarnoja et al. (2018) introduce soft actor-critic, a strong off-policy baseline for stability-oriented discussions.', 'Henderson et al. (2018) show that deep RL results can be fragile across seeds, codebases, and hyperparameters.', 'Agarwal et al. (2021) argue that aggregate point estimates can be statistically misleading in deep RL benchmarks.', 'Cobbe et al. (2019) introduce Procgen to study generalization rather than memorized environment behavior.', 'Dulac-Arnold et al. (2021) summarize challenges for real-world RL, including robustness, safety, and deployment constraints.', 'Amodei et al. (2016) frame concrete AI safety problems that motivate robust and honest evaluation beyond reward maximization.', 'Christiano et al. (2017) connect reinforcement learning with human preferences, highlighting evaluation issues around learned objectives.', 'Ouyang et al. (2022) show instruction-following alignment with human feedback, a modern policy-optimization application context.', 'Bai et al. (2022) discuss constitutional AI and preference-based alignment, reinforcing why policy quality cannot be reduced to one scalar reward.']
SECTIONS = [('01_sec_abstract.md', 'Abstract', 'Summarize the evaluation gap, selected idea, iterative workflow, synthetic evidence boundary, and reviewer-gated contribution.', 'Recent reinforcement learning evaluations often compress policy quality into mean return, yet mean return can hide seed fragility, perturbation brittleness, and shortcut-driven behavior. This demo paper introduces PolicyBench-Reliability, a proposed evaluation workflow that turns user-provided PPO-oriented material into a reliability-focused benchmark narrative. PPO is a useful seed because it is widely adopted for stable policy-gradient updates, but the reproducibility literature shows that even familiar deep RL baselines require careful statistical treatment and protocol disclosure [2,3,11,12]. The workflow first extracts multiple candidate paper ideas from the input, asks a reviewer model to select the most promising direction, and then writes each section through a repeated contract, draft, critique, and revision loop. Instead of treating the first generated paragraph as final, every section carries a reader question, claim IDs, evidence status, caveats, and a Chinese explanation of why the section is structured that way. A synthetic reporting example illustrates how an algorithm can appear competitive under average return while receiving lower diagnostic credit when stability, robustness, and decision support are considered jointly. All numbers in the demo are labeled illustrative rather than empirical. The resulting artifact demonstrates how oh my paper should coordinate Codex skills, reviewer agents, citations, LaTeX packaging, and image-generation prompts to produce long academic prose that remains auditable, revisable, and honest about evidence boundaries.'), ('02_sec_introduction.md', '1. Introduction', 'Explain why the user material becomes a reliability-evaluation paper rather than a new optimizer paper.', 'Policy-gradient methods such as PPO are widely used because they combine implementation simplicity with comparatively stable updates [2,3]. That popularity makes PPO a good seed material for a writing demo, but it also exposes a recurring evaluation problem: a method can achieve strong mean return without being reliable across seeds, perturbations, or decision probes. Standardized environments such as ALE and Gym made progress measurable [5,7], yet later protocol work and reproducibility studies showed that score reporting can be sensitive to seeds, implementation choices, and statistical summarization [6,11,12]. A paper that only reports the mean therefore risks answering the wrong reviewer question. The reviewer wants to know not only whether a policy wins, but whether the result is repeatable, robust, and supported by task-relevant state information.\n\nPolicyBench-Reliability is framed as a benchmark/evaluation paper because the input material is primarily about measurement failure. The workflow extracts candidate angles from the user material, rejects directions that would require unsupported real experiments, and selects a conservative thesis: average-return reporting should be complemented by reliability diagnostics. This choice is intentionally different from hard-coding a paper title in the prompt. In a live run, the idea-selection agent would propose several candidate papers, a Gemini-compatible reviewer endpoint would score them, and the orchestrator would select the highest-value direction before any long drafting begins.\n\nThe contribution is therefore procedural and methodological. First, the demo shows how to decompose a broad topic into a sectioned paper plan. Second, it demonstrates a multi-round writing loop in which every section is revised after critique. Third, it shows how reviewer scoring can drive further revision until an acceptance threshold is reached. Fourth, it separates deterministic previews from generated figures by preserving imagegen prompts and audit criteria. Fifth, it adds representative citation scaffolding and a LaTeX compilation skill so that the demo resembles a real paper pipeline rather than a prose-only mockup.'), ('03_sec_related_work.md', '2. Related Work', 'Position the demo against RL evaluation practice, benchmark-writing logic, and iterative AI writing systems.', 'The first related line is policy optimization evaluation. PPO-style reports often compare objectives, hyperparameters, and return curves [2,3], while off-policy baselines such as DDPG, TD3, and SAC provide contrasting stability and sample-efficiency assumptions [8,9,10]. These comparisons are useful but incomplete when the paper claim concerns reliability. The demo borrows the habit of ablation-style reporting while refusing to invent real environment results. Any table in this demo is a format example unless a source artifact provides actual measurements.\n\nThe second line is benchmark and evaluation methodology. Atari, Gym, and Procgen illustrate how standardized environments shape research questions [5,7,13]. However, benchmark methodology papers also warn that environment choice, evaluation protocol, random seeds, and statistical summaries can change conclusions [6,11,12]. Mature benchmark papers are persuasive when the design, scoring rule, quality control, and analysis all support one story. This demo uses that pattern without reusing a prior benchmark acronym. The design lesson is general: if a paper claims that old evaluation is saturated or misleading, its experiments must show what the old metric hides.\n\nThe third line is reliability and alignment-oriented RL. Real-world RL and AI safety work emphasize robustness, deployment constraints, human preferences, and objective misspecification [14,15,16,17,18]. These references motivate why a policy should not be judged only by a scalar reward curve. They do not prove that the synthetic values in this demo are true; instead, they justify the kind of diagnostic questions a real paper would need to answer.\n\nThe fourth line is AI-assisted academic writing. A single LLM call can produce fluent prose, but fluency is not the same as evidence discipline. oh my paper therefore treats writing as a loop among owner skills: idea selection, writing, figures, review, revision, and LaTeX packaging. Each role has a bounded responsibility, and the reviewer role is allowed to block the draft until the score reaches the configured threshold.'), ('04_sec_method.md', '3. Method', 'Describe the actual workflow: candidate extraction, reviewer selection, multi-agent section writing, and score-gated revision.', 'The workflow begins with structured intake. The user material is converted into a compact input card containing topic, candidate claims, evidence status, forbidden overclaims, target venue style, and desired outputs. From this card, an idea agent proposes several paper directions. For the PPO-oriented demo, plausible directions include a reliability benchmark, a reproduction protocol for PPO-style experiments, a survey on RL evaluation failure modes, and a robustness checklist for policy updates. A reviewer model then scores these directions for novelty, feasibility, evidence fit, citation availability, and risk. The selected direction becomes the paper contract.\n\nAfter selection, the writing loop operates section by section. A planner produces a section contract with a reader question, section job, claim IDs, paragraph messages, required evidence, and caveats. A drafting agent writes the section from that contract. A citation-aware pass checks whether representative works are needed for the claim type. A critic agent audits unsupported claims, paragraph drift, weak transitions, and missing caveats. A revision agent rewrites the section. The loop can repeat until the reviewer score reaches the configured acceptance target, which is 85 in this demo protocol.\n\nThe reviewer is not merely a grammar checker. It returns a structured score with dimensions for problem framing, evidence discipline, method clarity, experiment credibility, citation coverage, figure usefulness, limitations, and overall readiness. If the score is below threshold, the orchestrator creates a revision brief and sends it back to the relevant owner skill. This makes the flow closer to a small research team than to a one-shot prompt.\n\nFigures and final packaging follow separate paths. The figure agent reads the latest section claims and writes figure intent cards. Each card becomes a prompt for Codex imagegen. The LaTeX skill then copies the built-in arXiv-style template, maps Markdown sections into `content/sec/*.tex`, carries over representative BibTeX entries, and compiles with XeLaTeX/BibTeX when local TeX tooling is available. Deterministic previews may exist for reproducibility, but generated paper figures should be produced through imagegen and then audited for text accuracy, unsupported values, and caption alignment.'), ('05_sec_experiments.md', '4. Demonstration and Synthetic Results', 'Show the reporting style while making clear that no real RL environment was run.', 'This demo uses synthetic values only to show how a reliability paper would present results. The example compares a mean-return view with a diagnostic view. Under the mean-return view, PPO-like and off-policy baselines appear close. Under the diagnostic view, policies lose credit when performance varies across seeds, collapses under perturbation, or lacks support from task-relevant state features. This reporting style is motivated by reproducibility and statistical-evaluation concerns in deep RL [11,12], but the values below are not copied from those works.\n\n| Method | Mean-return view | Stability check | Robustness check | Decision-support check | Diagnostic score |\n| --- | ---: | ---: | ---: | ---: | ---: |\n| PPO-style baseline | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |\n| Off-policy baseline | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |\n| Deterministic actor baseline | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |\n| Reference policy | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |\n\nThe intended lesson is structural rather than empirical. A real paper would need environment definitions, public seeds, perturbation settings, training curves, statistical intervals, and reproducible code. It would also need to compare against canonical baselines from both value-based and actor-critic traditions [4,8,9,10]. The demo table simply illustrates the kind of discrepancy that motivates diagnostic evaluation. The reviewer loop should penalize any draft that presents this table as a real PPO result.'), ('06_sec_discussion.md', '5. Discussion', 'Explain what the workflow teaches about reliable academic generation.', 'The most important observation is that long academic writing needs governance. Without an explicit loop, the model can produce a polished but unsupported section. With a loop, each section must declare what question it answers, what evidence it has, what citations are representative, and what remains uncertain. This is especially important for benchmark papers because benchmark claims often sound authoritative even when the dataset or protocol is only proposed.\n\nThe reviewer threshold also changes the behavior of the system. If the acceptance target is 85, the first draft is expected to fail unless it already has clear claims, evidence boundaries, citations, figures, and limitations. Failure is not treated as a dead end; it becomes a revision brief. This mirrors software testing: a failing review identifies the next patch.\n\nFinally, image generation and LaTeX compilation are separated from scientific evidence. A figure prompt can make the story easier to understand, and a template can make the paper look submission-ready, but neither creates evidence. Captions, citations, and audit notes must still point back to claims, tables, protocols, or source material.'), ('07_sec_limitations.md', '6. Limitations', 'State what this demo does not prove and what a live API-backed run would add.', 'This repository demo is deterministic and offline. It does not call a live Gemini endpoint during committed generation, does not run RL environments, does not verify every citation live at generation time, and does not create final raster figures. Instead, it records the prompts and protocols that a live run should execute. This boundary is deliberate: committed demo outputs should be reproducible without secrets or network availability.\n\nA live run would add four elements. First, it would use the configured reviewer model to select among candidate paper ideas. Second, it would iterate section drafts until the reviewer score reaches the configured threshold or a maximum round limit is hit. Third, it would call Codex imagegen to produce bitmap figures and save them with an audit trail. Fourth, it would use the LaTeX skill to create a compile-ready workspace, run XeLaTeX/BibTeX if available, and surface missing compiler or citation errors honestly.\n\nThe demo also does not guarantee that an 85 score means publishability. It means the configured reviewer agent judged the draft acceptable according to the local rubric. Human supervision remains necessary for real claims, real citations, real experiments, and real submission decisions.'), ('08_sec_conclusion.md', '7. Conclusion', 'Close the paper by returning to the workflow contribution.', 'This demo reframes oh my paper as an iterative research-writing system rather than a single prompt that emits a paper. Starting from user material, the system should generate candidate directions, ask a reviewer model to choose the strongest one, write sections through multi-agent loops, attach representative citations, produce imagegen prompts from final claims, package the draft in LaTeX, and revise until the reviewer score reaches a target such as 85. The section-based output layout makes that process visible: every section has its own artifact, every figure has its own prompt, every major writing decision has a Chinese explanation, and the references section shows the expected citation density. The result is not just longer text, but a more inspectable and controllable academic workflow.')]
EXPLANATIONS = {'01_sec_abstract.md': '摘要先压缩问题、方案、流程和诚信边界，因为评审最先判断论文是不是有完整故事。这里加入代表性引用的线索，但不把 synthetic demo 写成真实实证结论。', '02_sec_introduction.md': '引言先承认 PPO 的价值，再用 RL benchmark 与 reproducibility 文献指出平均 return 的评测缺口。这样避免攻击前人，同时把用户素材自然转成 evaluation paper。', '03_sec_related_work.md': '相关工作按功能分类：policy optimization、benchmark 方法、可靠性/对齐、AI 写作系统。这样比罗列论文更适合 demo，也让 15–20 条引用有结构。', '04_sec_method.md': '方法章写真实流程：候选选题、评审选择、多 agent 写作、引用 pass、85 分返修、imagegen 和 LaTeX 路径。它回应用户要求：不是硬编码 prompt，而是从素材出发再循环写作。', '05_sec_experiments.md': '实验章只展示 synthetic reporting style，并多次声明不是 PPO 真实结果。引用用于说明为什么这种报告方式重要，而不是冒充数据来源。', '06_sec_discussion.md': '讨论章解释系统价值：长文需要治理、审稿分数驱动返修、图像和排版不能替代证据。它把 demo 上升到设计哲学。', '07_sec_limitations.md': '局限章明确离线 demo 不调用真实 Gemini、不跑 RL、不逐条 live 核验引用、不生成最终位图。这个边界能防止用户误解，同时说明 live run 应补什么。', '08_sec_conclusion.md': '结论回收主线：从用户素材到候选选择、章节循环、引用、图像提示词、LaTeX 打包和审稿阈值。它不引入新概念，只总结工作流贡献。'}
FIGURES = [
    (
        'fig_01_workflow_prompt.md',
        'Workflow overview',
        'Pipeline / feedback loop',
        'A reliable academic draft emerges from repeated selection, writing, review, revision, figure generation, and packaging rather than from one prompt.',
        [
            'A',
            'B',
            'C',
            'One-shot prompt',
            'User material',
            'Candidate ideas',
            'Reviewer selection',
            'Section agents',
            'Citation check',
            'Review score',
            'Revise to 85+',
            'Citation gaps',
            'Critique packet',
            'Imagegen figures',
            'LaTeX package',
            'Auditable draft',
        ],
        'Create a CCF-A benchmark-paper Figure-1 composite with three labeled subpanels. Panel A: a small contrast card labeled One-shot prompt fading out. Panel B: the main left-to-right workflow from User material to LaTeX package with the Revise to 85+ feedback loop. Panel C: an output card labeled Auditable draft. Use panel grouping, thin separators, and a caption-ready layout, not a single flat row. Do not include score charts, axes, leaderboards, threshold lines, or numeric markers.',
        'Show that the paper is produced by layered selection, evidence checking, review, revision, figure generation, and packaging rather than a one-shot prompt.',
    ),
    (
        'fig_02_score_loop_prompt.md',
        'Reviewer score loop',
        'Score trajectory with feedback packets',
        'The reviewer does not merely grade; it creates targeted revision packets until the draft crosses the acceptance threshold.',
        [
            'A',
            'B',
            'Draft v1',
            '72',
            'Critique packet',
            'Draft v2',
            '81',
            'Citation gaps',
            'Draft v3',
            '87',
            'Accept threshold',
            'Repair loop',
        ],
        'Create a CCF-A evaluation diagnostic figure with two labeled subpanels. Panel A: a clean stepped score trajectory from Draft v1 to Draft v3 with score markers 72, 81, 87 and an Accept threshold line. Panel B: a repair lane with Critique packet and Citation gaps feeding upward into the next draft; label the lane Repair loop. Do not add internal icon text, micro badges, or any extra words inside the packet cards.',
        'Show a revision trajectory from 72 to 81 to 87, with critique packets and citation gaps feeding a repair loop until the draft crosses the accept threshold.',
    ),
    (
        'fig_03_section_artifacts_prompt.md',
        'Section artifact layout',
        'Artifact map / file grid',
        'The workflow is auditable because every section, figure prompt, explanation, reference file, and optional package workspace is saved as a separate artifact.',
        [
            'A',
            'B',
            'C',
            'sections/',
            '01 Abstract',
            '02 Introduction',
            '03 Related Work',
            '04 Method',
            'figures/',
            'explain/',
            'references.bib',
            'latex workspace',
            'audit trail',
        ],
        'Create a clean CCF-A appendix-style artifact map with three labeled subpanels. Panel A: sections/ as four stacked file cards. Panel B: figures/ and explain/ as two simple stacked card groups connected by arrows. Panel C: references.bib and latex workspace connected to audit trail. Use no tags, no badges, no header ribbons, no small helper labels, and no extra words.',
        'Show grouped artifact families only: section cards, figure cards, explanation cards, references, LaTeX workspace, and audit trail. Use only the allowed labels, not full filenames.',
    ),
]


def build_outputs(root: Path, material: str) -> dict[Path, str]:
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    outputs: dict[Path, str] = {
        root / "INPUT_SUMMARY.md": input_summary(material, digest),
        root / "MODEL_SELECTION_PROTOCOL.md": model_selection_protocol(),
        root / "REVIEW_LOOP_PROTOCOL.md": review_loop_protocol(),
        root / "HOW_TO_REPRODUCE.md": how_to_reproduce(),
        root / "IMAGEGEN_USAGE.md": imagegen_usage(),
        root / "README.md": readme(),
        root / "PROCESS_LOG.md": process_log(digest),
        root / "references.bib": BIBTEX,
    }
    for filename, title, role, body in SECTIONS:
        outputs[root / "sections" / filename] = section_file(title, role, body)
        outputs[root / "explain" / filename.replace("_sec_", "_why_")] = explanation_file(title, EXPLANATIONS[filename])
    outputs[root / "sections" / "09_sec_references.md"] = references_section()
    outputs[root / "explain" / "09_why_references.md"] = explanation_file(
        "References",
        "参考文献单独成节，确保 demo 不只是流畅长文，也具备真实论文需要的 citation density。这里选择 RL 优化、benchmark、reproducibility、安全/对齐方向的代表性文献，避免为了凑数加入无关引用。",
    )
    for filename, title, figure_type, takeaway, labels, layout, intent in FIGURES:
        outputs[root / "figures" / filename] = figure_prompt(
            title=title,
            figure_type=figure_type,
            takeaway=takeaway,
            labels=labels,
            layout=layout,
            intent=intent,
        )
        outputs[root / "explain" / filename.replace("fig_", "why_fig_")] = explanation_file(title, figure_explanation(title))
    outputs[root / "sections" / "00_full_paper.md"] = full_paper()
    return outputs


def section_file(title: str, role: str, body: str) -> str:
    return f"""# {title}

## Section contract

- Reader question: {role}
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Citation status: representative references are included for field positioning; synthetic values remain non-empirical.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

{body}
"""


def references_section() -> str:
    rows = ["# References", "", "Representative citation set for the demo paper:", ""]
    for index, item in enumerate(BIBLIOGRAPHY, 1):
        rows.append(f"{index}. {item}")
    rows.extend([
        "",
        "## Citation note",
        "",
        "These references are included to demonstrate expected citation coverage for a PPO/RL evaluation demo. A live paper run should verify metadata with the configured citation checker and replace representative placeholders with the exact works used by the author. The companion `demo/references.bib` file provides BibTeX scaffolding for these entries.",
    ])
    return "\n".join(rows) + "\n"


def explanation_file(title: str, text: str) -> str:
    return f"""# 为什么这样写：{title}

{text}

## 迭代说明

- 第一轮：确定本节回答的 reader question。
- 第二轮：检查是否有 unsupported claim。
- 第三轮：检查代表性引用是否服务于本节论证，而不是凑数量。
- 第四轮：把批评转成修订或 caveat。
- 通过条件：本节不把 demo/synthetic 内容写成真实实证结论。
"""


def full_paper() -> str:
    joined = [f"# {TITLE}\n"]
    for _filename, title, _role, body in SECTIONS:
        joined.append(f"## {title}\n\n{body}\n")
    joined.append(references_section())
    return "\n".join(joined)


def input_summary(material: str, digest: str) -> str:
    return f"""# Input summary

- Source file: `demo/input_material.md`
- SHA256: `{digest}`
- User intent interpreted by the demo: build a section-based academic writing workflow from PPO-oriented material.
- Forbidden behavior: do not hard-code a fixed benchmark acronym from prior examples; do not claim synthetic values are real experiments.
- Citation requirement: include representative references for RL optimization, benchmark methodology, reproducibility, and reliability.

## Raw input excerpt

```markdown
{material.strip()}
```
"""


def model_selection_protocol() -> str:
    return """# Model selection protocol

A live run should not hard-code the paper idea. It should perform this selection step before drafting.

## Candidate generation

The idea agent proposes 3-5 paper directions from the user's material, for example:

1. reliability benchmark for policy optimization;
2. reproduction protocol for PPO-style experiments;
3. survey/tutorial on RL evaluation failure modes;
4. robustness checklist for RLHF-style policy updates.

## Reviewer-model selection

Use the configured reviewer model. If the user config points to Gemini or a Gemini-compatible relay, this is the Gemini-backed selection step.

```text
System: You are a strict academic program chair. Select the best paper direction from user material.
User: Score each candidate 0-100 for novelty, feasibility, evidence fit, citation availability, risk, and expected paper clarity. Return JSON with selected_candidate, score, risk, required caveats, and citation gaps.
```

## Offline demo status

This committed demo records the protocol and uses a deterministic selected direction: reliability benchmark/workflow for policy optimization. It does not call live APIs during repository generation.
"""


def review_loop_protocol() -> str:
    return """# Reviewer loop protocol: revise until score >= 85

A live run should use multiple role agents or model calls:

| Role | Responsibility |
| --- | --- |
| Orchestrator | Maintains paper state and decides which section to revise. |
| Idea selector | Extracts candidate directions from user material. |
| Section writer | Writes one section from a contract and evidence map. |
| Citation auditor | Checks whether representative citations support the paper context. |
| Critic | Finds unsupported claims and weak logic. |
| Reviewer | Scores the paper/section and returns required revisions. |
| Figure planner | Converts final claims into imagegen prompts. |
| LaTeX packager | Copies the built-in template and compiles when TeX tools exist. |

## Loop

1. Write or revise a section.
2. Reviewer returns JSON: `score`, `verdict`, `blocking_issues`, `required_revisions`, `citation_gaps`.
3. If `score < 85`, create a revision brief and return to the responsible section writer.
4. If any revision creates a new unsupported claim, send it back to critic before reviewer scoring.
5. Stop when score is at least 85 or max rounds is reached; if max rounds is reached, mark the artifact as not accepted.

## Example trajectory

```json
[
  {"round": 1, "score": 72, "verdict": "major_revision", "reason": "method loop unclear and citations missing"},
  {"round": 2, "score": 81, "verdict": "minor_revision", "reason": "figure workflow under-specified"},
  {"round": 3, "score": 87, "verdict": "accept_demo", "reason": "claims, citations, caveats, and workflow are aligned"}
]
```
"""


def figure_prompt(
    title: str,
    figure_type: str,
    takeaway: str,
    labels: list[str],
    layout: str,
    intent: str,
) -> str:
    quoted_labels = ", ".join(f'"{label}"' for label in labels)
    helper_words = [
        "score",
        "threshold",
        "audit",
        "overview",
        "workflow",
        "caption",
        "figure",
        "foundation",
        "repair",
        "evidence",
        "prompt",
        "support",
        "tax",
        "hair",
    ]
    allowed_lower = " | ".join(labels).lower()
    forbidden = [label for label in helper_words if label.lower() not in allowed_lower]
    if "audit trail" in allowed_lower and "audit" not in forbidden:
        forbidden.append("audit")
    if "figures/" in labels and "figure" not in forbidden:
        forbidden.append("figure")
    forbidden.extend(["Figure 1", "academic paper", "publication-ready", "CCF-A", "CVPR", "NeurIPS"])
    # Preserve order while removing duplicates.
    forbidden = list(dict.fromkeys(forbidden))
    forbidden_examples = ", ".join(f'"{label}"' for label in forbidden)
    forbidden_line = (
        f"Do not render these common hallucinated labels unless they are in the allowed list: {forbidden_examples}."
        if forbidden
        else "No extra helper labels are allowed beyond the exact allowed-label list."
    )
    helper_word_line = (
        f"Do not add helper words such as {', '.join(forbidden)} unless they appear in the allowed-label list."
        if forbidden
        else "Do not add any helper words beyond the allowed-label list."
    )
    return f"""# {title}

## Figure intent

- Figure type: {figure_type}
- Reader takeaway: {takeaway}
- Required content: {intent}
- Evidence boundary: workflow illustration only; do not invent empirical measurements.
- Layout grammar: {layout}
- Layer stack: background grid -> grouped panels -> mechanism arrows -> evidence/revision callouts -> exact short labels.
- Allowed visible labels: {quoted_labels}

## Codex imagegen prompt

Use case: infographic-diagram
Asset type: academic paper figure

Design brief:
Create a publication-ready {figure_type} for a computer science / machine learning paper. Do not render a title inside the image; the paper caption will provide the title outside the bitmap.

Reader takeaway:
{takeaway}

Paper context:
Section-based oh my paper demo for iterative academic writing, citation checking, reviewer scoring, image generation, and LaTeX packaging.

Style reference:
CCF-A/CVPR/NeurIPS benchmark Figure 1 style: information-dense but organized; left or top panels define structure, right or lower panels show diagnostic outputs or evidence artifacts. Use restrained pastel category colors, thin separators, small panel letters, compact evidence cards, and caption-ready composition. Avoid cartoon overview art.

Paper-content extraction:
- Entities: user material, candidate directions, writing agents, citation checks, reviewer score, revision loop, figure prompts, package artifacts.
- Relationships: evidence flows forward; critique and citation gaps flow backward into revision; generated figures and package outputs must remain auditable.
- Evidence status: workflow demonstration, not empirical experiment.
- Failure mode to avoid: a one-shot fluent draft that hides unsupported claims, fake citations, or unreviewed figures.

Layout grammar:
{layout}
Use strict alignment, consistent margins, balanced whitespace, grouped panels, and a clear reading path. Keep the drawing flat and editorial, not cartoon-like.

Layer stack:
1. Background: clean white or very light gray grid, no texture.
2. Major panels: grouped lanes or columns that carry the scientific story.
3. Mechanism flow: thin arrows and brackets showing dependency and feedback.
4. Evidence callouts: compact score, threshold, repair, or audit badges only when listed.
5. Text labels: exact short labels from the allowed list only.

Allowed visible labels:
Use only these exact labels: {quoted_labels}.
Do not render the internal asset name, style names, explanatory sentences, captions, or any other words inside the image.
Forbidden visible labels:
{forbidden_line}

Required visual elements:
{intent}

Aesthetic contract:
NeurIPS / ICLR / Nature Methods style; elegant editorial scientific schematic; white background; muted slate-blue, teal, warm gray, and one amber accent for revision/warning; thin 1.5px-style strokes; simple rounded rectangles; layered panel composition; small-multiple rhythm; generous whitespace; no clipart; no 3D; no glossy gradients; no stock-photo look.

Text policy:
Short labels only. No title, subtitle, paragraphs, pseudo-text, random letters, filenames beyond the allowed labels, fake citations, tiny footnotes, or unsupported numbers inside the image. {helper_word_line} If a card needs more text than the allowed label, leave the card visually simple rather than inventing text.
Absolutely no caption, footer paragraph, explanatory sentence, or auto-generated figure description inside the image. Do not reserve a caption/footer band; crop the canvas to the figure content with balanced margins.
Layout words in the prompt are instructions only, not visible text.

Negative prompt:
Avoid fake logos, watermarks, decorative icons, busy background, oversaturated colors, marketing-slide style, cartoon mascots, comic-book style, isometric app illustration, fake axes, invented metrics, unsupported numeric claims, micro badges with text, thumbnail pseudo-text, and any text not listed in the allowed labels.

Retry rule:
If any visible label differs from the allowed list, if pseudo-text appears, if the visual focal point is unclear in 5 seconds, or if it looks like a generic business infographic rather than an academic figure, regenerate or repair before using it.

## Audit checklist

- The takeaway is visible in 5 seconds: {takeaway}
- Text labels exactly match the allowed list.
- No forbidden helper label appears.
- Layout follows the specified grammar.
- No unsupported empirical claim appears in the image.
- Caption can link the figure to a section claim.
- The result looks like a restrained academic paper figure, not a marketing image.
"""


def figure_explanation(title: str) -> str:
    return f"{title} 的作用是降低读者理解流程的成本。它先由正文 claim 生成 figure intent，再变成包含 takeaway、layout grammar、允许标签、负面约束和返修规则的 Codex imagegen prompt；demo 不用代码 SVG 冒充最终 AI 生图。"


def how_to_reproduce() -> str:
    return """# 如何复现这个 section-based demo

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
"""


def imagegen_usage() -> str:
    return """# Imagegen usage

本 demo 同时提交 imagegen prompt 和已生成的示例位图。真实运行时：

1. 打开 `demo/figures/fig_01_workflow_prompt.md` 等文件。
2. 用 Codex `imagegen` skill 逐张生成 raster image。
3. 保存到 `demo/figures/generated/fig_01_workflow.jpg` 等路径。
4. 按每个 prompt 里的 audit checklist 检查。

## 已生成图像 / Generated figures

本 demo 现在已经包含实际生成图像：

- `demo/figures/generated/fig_01_workflow.jpg`
- `demo/figures/generated/fig_02_score_loop.jpg`
- `demo/figures/generated/fig_03_section_artifacts.jpg`

生成模型：`gemini-3.1-flash-image-preview`。三张图使用结构化科研图 brief 重生成；重点是短标签、严格布局语法、细线箭头、留白、muted palette、无伪文本和审稿人可读性。
"""


def readme() -> str:
    return """# oh my paper demo

这个 demo 展示新的目录形态：章节文件、图像提示词文件、解释文件和参考文献分离。

- `sections/01_sec_abstract.md`：章节正文。
- `sections/09_sec_references.md`：15–20 条代表性参考文献说明。
- `figures/fig_01_workflow_prompt.md`：图像生成提示词。
- `figures/generated/*.jpg`：已由 `gemini-3.1-flash-image-preview` 生成的 demo 图。
- `explain/01_why_abstract.md`：为什么这样写。
- `MODEL_SELECTION_PROTOCOL.md`：如何用配置的 reviewer/Gemini-compatible 模型选择论文方向。
- `REVIEW_LOOP_PROTOCOL.md`：如何审稿返修到 85 分。

所有内容是离线可复现 demo。真实运行时应调用配置的 LLM/API、Codex imagegen 和 `paper-ai-latex`。
"""


def process_log(digest: str) -> str:
    return f"""# Process log

- Input hash: `{digest}`
- Output style: section files + figure prompts + Chinese explanations + representative references.
- Live API status: image-generation example figures were generated; reviewer/writer APIs are not run in committed demo.
- Selected direction: reliability evaluation workflow for policy optimization.
- Reviewer target score for live loop: 85.
- Figure generation: prompt cards plus generated example images; use Codex imagegen in live run.
- LaTeX packaging: use `paper-ai-latex` in live run.
"""


def manifest(outputs: dict[Path, str], root: Path) -> str:
    rows = ["# Demo manifest", "", "| File | SHA256 |", "| --- | --- |"]
    for path in sorted(outputs):
        payload = path.read_text(encoding="utf-8") if path.exists() else outputs[path]
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        rows.append(f"| `{path.relative_to(root)}` | `{digest}` |")
    return "\n".join(rows) + "\n"
