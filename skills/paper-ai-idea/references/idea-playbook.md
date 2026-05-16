# Idea and research question playbook

Use this reference before writing begins. A good idea skill does not merely brainstorm catchy topics; it converts vague interest into a publishable, testable research question.

## Core questions

1. **Audience**: Who must care? Domain experts, method builders, application users, benchmark maintainers, or reviewers from a specific venue?
2. **Problem**: What bottleneck, failure mode, or missing capability is the paper about?
3. **Gap**: Why do existing methods, datasets, or explanations fail to address it?
4. **Hypothesis**: What is the central claim that could be true or false?
5. **Evidence path**: What experiment, proof, analysis, or case study could convince a skeptical reviewer?
6. **Risk**: What result would make the idea not worth a paper?

## Output pattern

```markdown
## Idea brief
- Working title:
- Target audience:
- Problem:
- Existing gap:
- Core hypothesis:
- Proposed approach:
- Evidence needed:
- Closest-work risk:
- Minimum publishable result:
- Stretch result:
```

## Idea quality rubric

- **Importance**: solves a real scientific/engineering bottleneck, not just a cosmetic variant.
- **Specificity**: names a concrete setting and failure mode.
- **Novelty**: has a plausible distinction from closest prior work.
- **Testability**: can be evaluated with available or planned evidence.
- **Narrative fit**: can become title, abstract, intro, experiments, and rebuttal consistently.

## Common failure modes

- Method-first idea with no problem: “we use X” but no reason readers need X.
- Trend-only idea: follows a hot topic but lacks a precise contribution.
- Experiment-only idea: has numbers but no generalizable insight.
- Overbroad idea: tries to solve all settings and becomes indefensible.
- Unfalsifiable idea: no experiment could clearly support or refute it.

## Material trace

Internalized from research-process materials: direction → problem → idea → method → experiments → writing → submission, plus emphasis on roadmap, experiment discipline, and writing as part of research training.

## Material-derived case cards

### Case 1: Publication pipeline as idea scaffold

Source excerpt (rights-cleared teaching material):

> 确定方向：统计机器翻译 → 确定问题：利用句法对长距离调序建模 → 确定思路：将树到串对泛化为树到串模板 → 确定方法：规则抽取，搜索算法 → 实验验证：数据集、基线系统、评价指标 → 撰写论文：投稿ACL

Imitation recipe:

```markdown
Direction: <broad field>
Problem: <specific bottleneck/failure mode>
Idea: <conceptual move that changes the formulation>
Method: <concrete algorithm/model/system>
Evidence: <dataset + baseline + metric>
Paper target: <venue/audience>
```

Bad imitation:

> Direction: diffusion models. Idea: use a better network. Evidence: run experiments.

Good imitation:

> Direction: text-to-image controllability. Problem: layouts drift when prompts contain multiple objects. Idea: represent object relations as an explicit constraint graph before denoising. Method: graph-conditioned attention masks plus a consistency loss. Evidence: compositional layout benchmark, strong layout-control baselines, spatial accuracy and human preference metrics. Target: CVPR/ICLR audience interested in controllable generation.

### Case 2: Idea ownership and discussion

Source excerpt (rights-cleared internal meeting):

> 科研是一个 idea 碰撞的过程，不是说自己一个人就能把所有东西想明白。

Imitation recipe:

- Ask for at least three candidate framings.
- For each framing, list why a skeptical collaborator might reject it.
- Convert collaborator objections into fast validation experiments or literature checks.

### Case 3: Problem-first instead of method-first

Material pattern: idea ability is framed as “choose a good problem, then solve it.”

Use this transformation:

```markdown
Method-first note: We use <technique> for <task>.
Problem-first rewrite: In <task>, current systems fail when <condition>. This matters because <impact>. We test whether <technique/insight> can address <failure mode>.
```
