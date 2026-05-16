# Introduction guide

The introduction is the paper's first argument. It should move the reader from a known problem to a specific gap, then to the paper's idea and evidence.

## Recommended flow

1. **Task/problem context**: make the reader care quickly.
2. **Current bottleneck**: what fails, is costly, is unclear, or is missing.
3. **Prior work and gap**: enough context to make the gap credible.
4. **Key challenge**: why the gap is nontrivial.
5. **Our idea**: the central mechanism or insight.
6. **Evidence preview**: what experiments/analysis support it.
7. **Contributions**: claim-linked bullets, not vague effort descriptions.

## Contribution bullet rules

Each contribution should be:

- specific enough to be falsifiable;
- linked to evidence or clearly marked as conceptual/tooling;
- different from implementation steps;
- scoped to the evaluated setting.

## First-two-pages check

- Can a tired reviewer state the problem and contribution after two pages?
- Is the closest-work risk visible early enough?
- Does the first figure/table reduce cognitive load?
- Are terms and notation delayed until needed?

## Common failures

- Starts too broad and burns reviewer patience.
- Lists prior work without explaining the challenge.
- Announces a method before the reader understands why it exists.
- Contributions repeat the abstract without claim/evidence discipline.
- Hides limitations that affect interpretation.

## Material-derived case cards

### Case 1: First two pages decide patience

Source excerpt (rights-cleared internal meeting):

> 前两页的内容，尤其是第一页的内容，一定非常重要...如果故事都没讲明白，审稿人这个时候基本就没法耐心了。

Imitation recipe:

- Page 1 must answer: What problem? Why hard? Why current work fails? What is the idea?
- Page 2 must answer: What evidence and contributions make this paper credible?

### Case 2: Reader-centered introduction

Source pattern (rights-cleared tutorial):

> 信息的呈现符合读者的认知惯性...让读者快速找到想要的信息。

Use this introduction skeleton:

```markdown
P1 Problem: In <setting>, <failure/bottleneck> prevents <goal>.
P2 Gap: Existing <families of work> handle <case>, but fail under <condition>.
P3 Challenge: The difficulty is <specific technical conflict>.
P4 Idea: We propose <central idea> that <mechanism>.
P5 Evidence preview: On <datasets/tasks>, we compare against <baselines> and show <type of result>.
P6 Contributions: C1/C2/C3 with evidence links.
```

### Case 3: Bad→good contribution bullets

Bad:

- We propose a new framework.
- We conduct extensive experiments.
- We show good performance.

Good:

- We formulate <specific failure mode> as <technical problem>, enabling direct evaluation of <claim C1>.
- We introduce <method component> to address <challenge>, with ablations isolating its effect <C2>.
- We provide <dataset/analysis/tool> showing <scoped evidence>, not a universal claim <C3>.
