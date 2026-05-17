"""Templates for the section-based oh my paper demo."""

from __future__ import annotations

import hashlib
from pathlib import Path

PROJECT = "PolicyBench-Reliability"
TITLE = "PolicyBench-Reliability: An Iterative Evaluation Workflow for Reliable Policy Optimization"
SECTIONS = [
    (
        "01_sec_abstract.md",
        "Abstract",
        "Summarize the evaluation gap, selected idea, iterative workflow, synthetic evidence boundary, and reviewer-gated contribution.",
        "Recent reinforcement learning evaluations often compress policy quality into mean return, yet mean return can hide seed fragility, perturbation brittleness, and shortcut-driven behavior. This demo paper introduces PolicyBench-Reliability, a proposed evaluation workflow that turns user-provided PPO-oriented material into a reliability-focused benchmark narrative. The workflow first extracts multiple candidate paper ideas from the input, asks a reviewer model to select the most promising direction, and then writes each section through a repeated contract, draft, critique, and revision loop. Instead of treating the first generated paragraph as final, every section carries a reader question, claim IDs, evidence status, caveats, and a Chinese explanation of why the section is structured that way. A synthetic reporting example illustrates how an algorithm can appear competitive under average return while receiving lower diagnostic credit when stability, robustness, and decision support are considered jointly. All numbers in the demo are labeled illustrative rather than empirical. The resulting artifact demonstrates how oh my paper should coordinate Codex skills, reviewer agents, and image-generation prompts to produce long academic prose that remains auditable, revisable, and honest about evidence boundaries.",
    ),
    (
        "02_sec_introduction.md",
        "1. Introduction",
        "Explain why the user material becomes a reliability-evaluation paper rather than a new optimizer paper.",
        "Policy-gradient methods such as PPO are widely used because they combine implementation simplicity with comparatively stable updates. That popularity makes PPO a good seed material for a writing demo, but it also exposes a recurring evaluation problem: a method can achieve strong mean return without being reliable across seeds, perturbations, or decision probes. A paper that only reports the mean therefore risks answering the wrong reviewer question. The reviewer wants to know not only whether a policy wins, but whether the result is repeatable, robust, and supported by task-relevant state information.\n\nPolicyBench-Reliability is framed as a benchmark/evaluation paper because the input material is primarily about measurement failure. The workflow extracts candidate angles from the user material, rejects directions that would require unsupported real experiments, and selects a conservative thesis: average-return reporting should be complemented by reliability diagnostics. This choice is intentionally different from hard-coding a paper title in the prompt. In a live run, the idea-selection agent would propose several candidate papers, a Gemini-compatible reviewer endpoint would score them, and the orchestrator would select the highest-value direction before any long drafting begins.\n\nThe contribution is therefore procedural and methodological. First, the demo shows how to decompose a broad topic into a sectioned paper plan. Second, it demonstrates a multi-round writing loop in which every section is revised after critique. Third, it shows how reviewer scoring can drive further revision until an acceptance threshold is reached. Fourth, it separates deterministic previews from generated figures by preserving imagegen prompts and audit criteria.",
    ),
    (
        "03_sec_related_work.md",
        "2. Related Work",
        "Position the demo against RL evaluation practice, benchmark-writing logic, and iterative AI writing systems.",
        "The first related line is policy optimization evaluation. PPO-style reports often compare objectives, hyperparameters, and return curves, which is useful but incomplete when the paper claim concerns reliability. The demo borrows the habit of ablation-style reporting while refusing to invent real environment results. Any table in this demo is a format example unless a source artifact provides actual measurements.\n\nThe second line is benchmark and dataset writing. Mature benchmark papers are persuasive when the benchmark design, scoring rule, quality control, and analysis all support one story. This demo uses that pattern without reusing the prior project name or importing a fixed benchmark acronym. The design lesson is general: if a paper claims that old evaluation is saturated or misleading, its experiments must show what the old metric hides.\n\nThe third line is AI-assisted academic writing. A single LLM call can produce fluent prose, but fluency is not the same as evidence discipline. oh my paper therefore treats writing as a loop among owner skills: idea selection, writing, figures, review, and revision. Each role has a bounded responsibility, and the reviewer role is allowed to block the draft until the score reaches the configured threshold.",
    ),
    (
        "04_sec_method.md",
        "3. Method",
        "Describe the actual workflow: candidate extraction, reviewer selection, multi-agent section writing, and score-gated revision.",
        "The workflow begins with structured intake. The user material is converted into a compact input card containing topic, candidate claims, evidence status, forbidden overclaims, target venue style, and desired outputs. From this card, an idea agent proposes several paper directions. For the PPO-oriented demo, plausible directions include a reliability benchmark, a tutorial survey, a reproduction protocol, and a robustness checklist. A reviewer model then scores these directions for novelty, feasibility, evidence fit, and risk. The selected direction becomes the paper contract.\n\nAfter selection, the writing loop operates section by section. A planner produces a section contract with a reader question, section job, claim IDs, paragraph messages, required evidence, and caveats. A drafting agent writes the section from that contract. A critic agent audits unsupported claims, paragraph drift, weak transitions, and missing caveats. A revision agent rewrites the section. The loop can repeat until the reviewer score reaches the configured acceptance target, which is 85 in this demo protocol.\n\nThe reviewer is not merely a grammar checker. It returns a structured score with dimensions for problem framing, evidence discipline, method clarity, experiment credibility, figure usefulness, limitations, and overall readiness. If the score is below threshold, the orchestrator creates a revision brief and sends it back to the relevant owner skill. This makes the flow closer to a small research team than to a one-shot prompt.\n\nFigures follow a separate path. The figure agent reads the latest section claims and writes figure intent cards. Each card becomes a prompt for Codex imagegen. Deterministic SVG previews may exist for reproducibility, but generated paper figures should be produced through imagegen and then audited for text accuracy, unsupported values, and caption alignment.",
    ),
    (
        "05_sec_experiments.md",
        "4. Demonstration and Synthetic Results",
        "Show the reporting style while making clear that no real RL environment was run.",
        "This demo uses synthetic values only to show how a reliability paper would present results. The example compares a mean-return view with a diagnostic view. Under the mean-return view, PPO-like and off-policy baselines appear close. Under the diagnostic view, policies lose credit when performance varies across seeds, collapses under perturbation, or lacks support from task-relevant state features.\n\n| Method | Mean-return view | Stability check | Robustness check | Decision-support check | Diagnostic score |\n| --- | ---: | ---: | ---: | ---: | ---: |\n| PPO-style baseline | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |\n| Off-policy baseline | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |\n| Deterministic actor baseline | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |\n| Reference policy | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |\n\nThe intended lesson is structural rather than empirical. A real paper would need environment definitions, public seeds, perturbation settings, training curves, statistical intervals, and reproducible code. The demo table simply illustrates the kind of discrepancy that motivates diagnostic evaluation. The reviewer loop should penalize any draft that presents this table as a real PPO result.",
    ),
    (
        "06_sec_discussion.md",
        "5. Discussion",
        "Explain what the workflow teaches about reliable academic generation.",
        "The most important observation is that long academic writing needs governance. Without an explicit loop, the model can produce a polished but unsupported section. With a loop, each section must declare what question it answers, what evidence it has, and what remains uncertain. This is especially important for benchmark papers because benchmark claims often sound authoritative even when the dataset or protocol is only proposed.\n\nThe reviewer threshold also changes the behavior of the system. If the acceptance target is 85, the first draft is expected to fail unless it already has clear claims, evidence boundaries, figures, and limitations. Failure is not treated as a dead end; it becomes a revision brief. This mirrors software testing: a failing review identifies the next patch.\n\nFinally, image generation is separated from scientific evidence. The figure prompt can make the story easier to understand, but it cannot create evidence. The caption and audit must still point back to claims, tables, or protocols.",
    ),
    (
        "07_sec_limitations.md",
        "6. Limitations",
        "State what this demo does not prove and what a live API-backed run would add.",
        "This repository demo is deterministic and offline. It does not call a live Gemini endpoint during committed generation, does not run RL environments, and does not create final raster figures. Instead, it records the prompts and protocols that a live run should execute. This boundary is deliberate: committed demo outputs should be reproducible without secrets or network availability.\n\nA live run would add three elements. First, it would use the configured reviewer model to select among candidate paper ideas. Second, it would iterate section drafts until the reviewer score reaches the configured threshold or a maximum round limit is hit. Third, it would call Codex imagegen to produce bitmap figures and save them with an audit trail.\n\nThe demo also does not guarantee that an 85 score means publishability. It means the configured reviewer agent judged the draft acceptable according to the local rubric. Human supervision remains necessary for real claims, real citations, and real submission decisions.",
    ),
    (
        "08_sec_conclusion.md",
        "7. Conclusion",
        "Close the paper by returning to the workflow contribution.",
        "This demo reframes oh my paper as an iterative research-writing system rather than a single prompt that emits a paper. Starting from user material, the system should generate candidate directions, ask a reviewer model to choose the strongest one, write sections through multi-agent loops, produce imagegen prompts from final claims, and revise until the reviewer score reaches a target such as 85. The section-based output layout makes that process visible: every section has its own artifact, every figure has its own prompt, and every major writing decision has a Chinese explanation. The result is not just longer text, but a more inspectable and controllable academic workflow.",
    ),
]

EXPLANATIONS = {
    "01_sec_abstract.md": "摘要先压缩问题、方案、流程和诚信边界，因为评审最先判断论文是不是有完整故事。这里不写具体真实实验结论，避免把 synthetic demo 伪装成实证贡献。",
    "02_sec_introduction.md": "引言先承认 PPO 的价值，再指出平均 return 的评测缺口。这样避免攻击前人，同时把用户素材自然转成 evaluation paper，而不是硬写新算法。",
    "03_sec_related_work.md": "相关工作按功能分类：RL 评测、benchmark 写作、AI 写作系统。这样比罗列论文更适合 demo，因为它要说明这个系统为什么需要多角色协作。",
    "04_sec_method.md": "方法章写真实流程：候选选题、评审选择、多 agent 写作、85 分返修、imagegen 图像路径。它回应用户要求：不是硬编码 prompt，而是从素材出发再循环写作。",
    "05_sec_experiments.md": "实验章只展示 synthetic reporting style，并多次声明不是 PPO 真实结果。这样既能示范长文和表格，又不制造假实证。",
    "06_sec_discussion.md": "讨论章解释系统价值：长文需要治理、审稿分数驱动返修、图像不能替代证据。它把 demo 上升到设计哲学。",
    "07_sec_limitations.md": "局限章明确离线 demo 不调用真实 Gemini、不跑 RL、不生成最终位图。这个边界能防止用户误解，同时说明 live run 应补什么。",
    "08_sec_conclusion.md": "结论回收主线：从用户素材到候选选择、章节循环、图像提示词和审稿阈值。它不引入新概念，只总结工作流贡献。",
}

FIGURES = [
    (
        "fig_01_workflow_prompt.md",
        "Workflow overview",
        "Show the full loop: user material -> candidate ideas -> reviewer selection -> section writing agents -> reviewer score -> revision until >=85 -> imagegen figures.",
    ),
    (
        "fig_02_score_loop_prompt.md",
        "Reviewer score loop",
        "Show a revision trajectory from 72 to 81 to 87, with critique packets feeding back to writing agents.",
    ),
    (
        "fig_03_section_artifacts_prompt.md",
        "Section artifact layout",
        "Show files named 01_sec_abstract.md through 08_sec_conclusion.md plus fig_01 prompts and explanation files.",
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
    }
    for filename, title, role, body in SECTIONS:
        outputs[root / "sections" / filename] = section_file(title, role, body)
        outputs[root / "explain" / filename.replace("_sec_", "_why_")] = explanation_file(title, EXPLANATIONS[filename])
    for filename, title, intent in FIGURES:
        outputs[root / "figures" / filename] = figure_prompt(title, intent)
        outputs[root / "explain" / filename.replace("fig_", "why_fig_")] = explanation_file(title, figure_explanation(title))
    outputs[root / "sections" / "00_full_paper.md"] = full_paper()
    return outputs


def section_file(title: str, role: str, body: str) -> str:
    return f"""# {title}

## Section contract

- Reader question: {role}
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

{body}
"""


def explanation_file(title: str, text: str) -> str:
    return f"""# 为什么这样写：{title}

{text}

## 迭代说明

- 第一轮：确定本节回答的 reader question。
- 第二轮：检查是否有 unsupported claim。
- 第三轮：把批评转成修订或 caveat。
- 通过条件：本节不把 demo/synthetic 内容写成真实实证结论。
"""


def full_paper() -> str:
    joined = [f"# {TITLE}\n"]
    for _filename, title, _role, body in SECTIONS:
        joined.append(f"## {title}\n\n{body}\n")
    return "\n".join(joined)


def input_summary(material: str, digest: str) -> str:
    return f"""# Input summary

- Source file: `demo/input_material.md`
- SHA256: `{digest}`
- User intent interpreted by the demo: build a section-based academic writing workflow from PPO-oriented material.
- Forbidden behavior: do not hard-code a fixed benchmark acronym from prior examples; do not claim synthetic values are real experiments.

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
User: Score each candidate 0-100 for novelty, feasibility, evidence fit, risk, and expected paper clarity. Return JSON with selected_candidate, score, risk, and required caveats.
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
| Critic | Finds unsupported claims and weak logic. |
| Reviewer | Scores the paper/section and returns required revisions. |
| Figure planner | Converts final claims into imagegen prompts. |

## Loop

1. Write or revise a section.
2. Reviewer returns JSON: `score`, `verdict`, `blocking_issues`, `required_revisions`.
3. If `score < 85`, create a revision brief and return to the responsible section writer.
4. If any revision creates a new unsupported claim, send it back to critic before reviewer scoring.
5. Stop when score is at least 85 or max rounds is reached; if max rounds is reached, mark the artifact as not accepted.

## Example trajectory

```json
[
  {"round": 1, "score": 72, "verdict": "major_revision", "reason": "method loop unclear"},
  {"round": 2, "score": 81, "verdict": "minor_revision", "reason": "figure workflow under-specified"},
  {"round": 3, "score": 87, "verdict": "accept_demo", "reason": "claims, caveats, and workflow are aligned"}
]
```
"""


def figure_prompt(title: str, intent: str) -> str:
    return f"""# {title}

## Figure intent

{intent}

## Codex imagegen prompt

Use case: infographic-diagram
Asset type: academic paper figure
Primary request: Create a clean top-tier computer science paper figure titled "{title}".
Paper context: section-based oh my paper demo for iterative academic writing.
Required content: {intent}
Style: clean vector-like raster, restrained colors, high readability, white background, clear arrows and labels.
Text policy: use only short labels; avoid dense paragraphs inside the image.
Avoid: fake logos, watermark, unsupported numeric claims, decorative 3D clutter, unreadable tiny text.

## Audit checklist

- The takeaway is visible in 5 seconds.
- Text labels match the prompt.
- No unsupported empirical claim appears in the image.
- Caption can link the figure to a section claim.
"""


def figure_explanation(title: str) -> str:
    return f"{title} 的作用是降低读者理解流程的成本。它先由正文 claim 生成 figure intent，再变成 Codex imagegen prompt；demo 不用代码 SVG 冒充最终 AI 生图。"


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
demo/figures/fig_01_workflow_prompt.md
demo/explain/01_why_abstract.md
```

连续运行两次，在输入不变时输出应保持稳定。
"""


def imagegen_usage() -> str:
    return """# Imagegen usage

本 demo 只提交 imagegen prompt，不提交假装已经生成的位图。真实运行时：

1. 打开 `demo/figures/fig_01_workflow_prompt.md` 等文件。
2. 用 Codex `imagegen` skill 逐张生成 raster image。
3. 保存到 `demo/figures/generated/fig_01.png` 等路径。
4. 按每个 prompt 里的 audit checklist 检查。
"""


def readme() -> str:
    return """# oh my paper demo

这个 demo 展示新的目录形态：章节文件、图像提示词文件和解释文件分离。

- `sections/01_sec_abstract.md`：章节正文。
- `figures/fig_01_workflow_prompt.md`：图像生成提示词。
- `explain/01_why_abstract.md`：为什么这样写。
- `MODEL_SELECTION_PROTOCOL.md`：如何用配置的 reviewer/Gemini-compatible 模型选择论文方向。
- `REVIEW_LOOP_PROTOCOL.md`：如何审稿返修到 85 分。

所有内容是离线可复现 demo。真实运行时应调用配置的 LLM/API 和 Codex imagegen。
"""


def process_log(digest: str) -> str:
    return f"""# Process log

- Input hash: `{digest}`
- Output style: section files + figure prompts + Chinese explanations.
- Live API status: not run in committed demo.
- Selected direction: reliability evaluation workflow for policy optimization.
- Reviewer target score for live loop: 85.
- Figure generation: prompts only; use Codex imagegen in live run.
"""


def manifest(outputs: dict[Path, str], root: Path) -> str:
    rows = ["# Demo manifest", "", "| File | SHA256 |", "| --- | --- |"]
    for path in sorted(outputs):
        payload = path.read_text(encoding="utf-8") if path.exists() else outputs[path]
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        rows.append(f"| `{path.relative_to(root)}` | `{digest}` |")
    return "\n".join(rows) + "\n"
