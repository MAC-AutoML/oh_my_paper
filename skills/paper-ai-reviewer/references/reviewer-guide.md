# Reviewer first-impression and full-review guide

Start with title, abstract, first two pages, and first figure before deep technical review. Reviewers under time pressure may anchor on these surfaces; a bad first impression amplifies later small holes.

## First-impression pass

1. **Title**: clear problem, searchable terms, believable scope, non-gimmicky acronym.
2. **Abstract**: problem, gap, method, evidence, implication; no unsupported result claims.
3. **First two pages**: problem → gap → challenge → idea → contributions; no broad boilerplate drag.
4. **First visual**: readable, one takeaway, claim-linked, not decorative.
5. **Trust prior**: note what the reviewer is likely to believe before reading details.

## Full review rubric

| Dimension | Strong signal | Weak signal |
| --- | --- | --- |
| Novelty | clear distinction from closest work | closest work hidden |
| Significance | important bottleneck | cosmetic/incremental motivation |
| Correctness | assumptions and logic explicit | hidden assumptions |
| Empirical support | baselines/metrics/ablations match claims | missing core evidence |
| Clarity | reader-centered flow | author-process narration |
| Reproducibility | enough setup detail | missing hyperparams/data/code plan |
| Limitations | honest scope | overbroad claims |

## Critique format

```markdown
- Issue:
- Evidence observed:
- Reviewer inference:
- Severity: fatal / major / minor / polish
- Fix:
```

## Submission-ready blockers

- Unsupported main claim.
- Missing closest baseline or comparison.
- Method cannot be understood from notation/example.
- Main result visual is unreadable or misleading.
- Limitations materially change the claim but are hidden.

## Material-derived case cards

### Case 1: Actual reviewer behavior

Source excerpt (rights-cleared tutorial):

> 审稿人实际上往往是这样审稿的：他不一定是专家，一直忙于其他事，在deadline到来之前一天要完成n篇。审稿时他往往先看题目、摘要，扫一下introduction（知道你做什么），然后直接翻到最后找核心实验结果（做得好不好），然后基本确定录还是不录（也许只用5分钟！）。

Imitation recipe for review simulation:

1. Spend first pass only on title, abstract, intro skim, first figure, and main result.
2. Write the likely prior: accept-leaning, borderline, reject-leaning.
3. Only then inspect method/experiments for reasons supporting or overturning that prior.

### Case 2: Internal meeting first-impression warning

Source excerpt (rights-cleared internal meeting):

> 审稿人在读完你的题目、abstract 摘要，还有 figure 一二，看完之后基本的印象分就有了...如果故事都没讲明白，审稿人这个时候基本就没法耐心了。

Use this output:

```markdown
## 5-minute reviewer prior
- Prior:
- What created it:
- What the reviewer will inspect next:
- What small issue could be amplified:
```

### Case 3: Rebuttal rarely rescues weak first impression

Source excerpt (rights-cleared internal meeting):

> 至少90%以上的文章很难在 rebuttal 阶段改分...大部分审稿人可能甚至都不看你的 reply。

Review implication:

- Pre-submission review must be adversarial.
- Do not defer known clarity/evidence problems to rebuttal.
- Treat rebuttal as correction of misunderstandings, not primary quality control.

### Case 4: Detail amplification

Source excerpt:

> 如果印象不太好，抓住一个漏洞，他就可以直接把你判死。

Imitation recipe:

When first impression is weak, classify every small inconsistency as potentially major until fixed: unsupported claim, sloppy caption, notation mismatch, missing baseline, vague limitation.

## Benchmark/evaluation paper review checklist

When reviewing benchmark, dataset, or evaluation papers, ask whether the paper proves a real evaluation gap rather than merely adding data.

Fatal or major risks:

- Starts with “we introduce a dataset” but never shows why existing evaluation is failing.
- Claims benchmark authority using adjectives instead of annotation/review/leakage evidence.
- Uses a flat list of question types where a capability hierarchy or diagnostic taxonomy is needed.
- Reports only average leaderboard scores without model-human gap, capability breakdown, or error analysis.
- Proposes a new metric but does not compare it with conventional accuracy.
- Says “valid reasoning” without a verifiable way to judge reasoning support.
- Uses impressive annotation numbers in the abstract that are not supported in the method/appendix.

Reviewer questions:

```markdown
1. What real evaluation crisis does this benchmark solve?
2. What capability does it measure that prior benchmarks miss?
3. Is the benchmark systematically designed or just larger/more diverse?
4. Is the scoring protocol justified and ablated?
5. Are annotation and QA claims concrete enough to trust?
6. Do experiments reveal a bottleneck, or only rank models?
7. Are impact claims restrained and evidence-backed?
```

Score-up signals:

- Clear contradiction such as inflated leaderboard scores vs. real-world capability.
- Capability hierarchy that structures both data construction and analysis.
- Group/consistency-based evaluation that exposes shortcut correctness.
- Human expert comparison or strong diagnostic baseline.
- Error propagation analysis showing why models fail.
- Honest condition-specific findings: X helps under condition A but fails under condition B.

## Narrative-flow review pass

In addition to technical correctness, review paragraph function and story flow.

Ask:

1. Can I state the paper's hidden spine in one sentence?
2. Does every section have a distinct job?
3. Does every paragraph have a road-sign first sentence?
4. Do method designs answer earlier gaps?
5. Do experiments close loops opened by the method?
6. Are subsection titles takeaways or neutral labels?
7. Does every major number receive interpretation?
8. Does the conclusion recover the same story rather than introducing new claims?

Flag as major clarity risk if the paper has strong components but no visible `Problem → Gap → Design → Evidence → Insight → Impact` progression.

## oh my paper reviewer-panel contract

The reviewer panel maps paper-review responsibilities to repo-local Codex subagents where available:

- field analyst: infer field and rubric.
- editor-in-chief: synthesize decision and priorities.
- methodology reviewer: pressure-test design and evidence.
- domain reviewer: evaluate field fit and related work.
- perspective reviewer: test generality and interdisciplinary clarity.
- devil's advocate reviewer: preserve attack intensity.
- editorial synthesizer: merge without softening fatal concerns.

Reviewer outputs must stay read-only over the draft: produce critique, decision, and fix plan rather than silently rewriting claims.
