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
