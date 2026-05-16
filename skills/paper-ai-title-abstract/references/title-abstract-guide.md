# Title and abstract first-impression guide

Reviewers often form an early prior from the title, abstract, first two pages, and first important figure. Optimize for clarity, searchability, and believable scope before cleverness.

## Title checklist

- Names the problem area or task with searchable terms.
- Signals the main method, insight, or contribution when useful.
- Avoids universal or hype words unless evidence truly supports them.
- Does not depend on an obscure acronym to be understood.
- Can be remembered after a quick scan.
- Matches the actual claim ledger.

## Abstract structure

1. Problem and why it matters.
2. Concrete gap/challenge in existing work.
3. Core idea/method.
4. Key evidence, result type, or analysis.
5. Scope/implication without overclaiming.

## Title option types

- **Problem-method**: “Solving X with Y”.
- **Insight-first**: “X emerges from Y”.
- **Capability-first**: “Efficient/robust/faithful X under Y”.
- **Acronym-assisted**: use only when the expanded title remains clear.

## First-impression audit output

```markdown
| Candidate | Searchability | Specificity | Overclaim risk | Memorability | Verdict |
| --- | --- | --- | --- | --- | --- |
```

## Failure modes

- Clever but unsearchable title.
- Abstract hides the actual result until the last sentence.
- Method component list without problem/gap.
- “State-of-the-art” claim without evidence/caveat.
- Title promises a general solution while experiments cover a narrow setting.

## Material-derived case cards

### Case 1: Reviewers filter by title and abstract

Source excerpt (rights-cleared tutorial):

> 根据标题过滤50% ... 根据摘要再过滤20%

Source excerpt (rights-cleared internal meeting):

> 审稿人在读完你的题目、abstract 摘要，还有 figure 一二，看完之后基本的印象分就有了。

Imitation recipe:

- Title must communicate topic, problem, and often method.
- Abstract must let the reviewer know whether the paper is worth reading before method details.
- Never hide the main result/evidence until the end.

### Case 2: Title = problem + what we did

Source excerpt (rights-cleared tutorial example):

> Liang Huang. Forest Reranking: Discriminative Parsing with Non-Local Features. In ACL 2008.
>
> 问题是什么 / 我们做了什么

Imitation recipe:

```markdown
<Problem/object>: <method/action> with <key technique/insight>
```

Good pattern examples to imitate:

- `Forest Reranking: Discriminative Parsing with Non-Local Features`
- `Deep Residual Learning for Image Recognition`

Bad pattern:

- `A Unified Powerful Framework for Everything`

### Case 3: Searchability and acronym control

Source excerpt (rights-cleared internal meeting):

> 好的题目...切合主题...容易被人记住...容易检索...不要有生僻的单词...题目最好是要包含要解决的关键问题和采用的关键方法。

Imitation checklist:

| Check | Question |
| --- | --- |
| Theme fit | Can a reader infer the paper topic immediately? |
| Memory | Is it short enough or acronym-supported? |
| Search | Would common search terms find it? |
| Problem | Does it name the key problem/task? |
| Method | Does it name the key method/insight when useful? |

### Case 4: Overclaim warning

Source excerpt (rights-cleared internal meeting):

> 你一定不要在题目里面夸大你的贡献...不要去 overclaim...除非你的质量很好，你可以去另辟蹊径，不然就直接主题就行了。

Safe rewrite pattern:

- Overclaim: `All You Need for Robust Multimodal Reasoning`
- Safer: `Constraint-Guided Multimodal Reasoning under Compositional Layout Shifts`
