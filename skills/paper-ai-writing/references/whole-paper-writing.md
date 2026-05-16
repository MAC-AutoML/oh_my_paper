# Whole-paper writing principles

Use this when revising across sections or when a paper needs a coherent story before individual chapter work. The goal is reader-centered information flow, not merely elegant sentences.

## Three-layer audit

1. **Document surface**: section order, paragraph length, transitions, figures/tables, notation, citations.
2. **Information flow**: what the reader learns first, what context is missing, what each paragraph adds.
3. **Underlying thought**: problem, gap, hypothesis, method logic, evidence, limitations.

## Claim-grounded writing loop

1. Extract or create claim IDs in `paper/CLAIMS.md`.
2. Mark each claim as supported, partial, planned, unsupported, or removed.
3. Draft paragraphs around supported/partial claims.
4. Caveat partial claims and delete unsupported claims from final prose.
5. Send section-specific tasks to title/abstract, intro, related work, method, experiments, limitations, figures, or layout skills.

## Paragraph pattern

- Topic sentence: what this paragraph proves or explains.
- Support: evidence, mechanism, comparison, or citation.
- Connection: why it matters for the paper's argument.
- Transition: what the reader needs next.

## Common writing failures

- Author-process narration: describes what the authors did chronologically instead of what the reader needs.
- Generic motivation: “X is important and challenging” without concrete bottleneck.
- Contribution bullets that are implementation tasks rather than scientific claims.
- Paragraphs with multiple centers.
- Strong adjectives hiding weak evidence.

## Revision order

Fix story/evidence first, then section logic, then paragraph flow, then sentence polish, then formatting.

## Material-derived case cards

### Case 1: Reader-centered writing

Source excerpt (rights-cleared tutorial):

> 以作者为核心整理工作 → 以读者为核心阐述工作
>
> 全心全意为读者服务：信息的呈现符合读者的认知惯性；深入浅出，引人入胜，让读者快速找到想要的信息；尽量降低读者的理解难度；合理地综合使用信息元素：图 > 曲线 > 表 > 正文 > 公式。

Imitation recipe:

1. Rewrite every section outline from “what we did” to “what the reader needs to know next.”
2. Put visual/evidence elements before dense text when they reduce cognitive load.
3. Delay equations until intuition and examples exist.

Bad imitation:

> We first implemented module A, then tried module B, then found module C works.

Good imitation:

> The key difficulty is that local evidence conflicts with global constraints. We first show this failure mode, then introduce a constraint graph that makes the conflict explicit, and finally show how each module resolves one part of the graph.

### Case 2: One paragraph, one message

Source excerpt (rights-cleared writing template):

> 一段文字只讲一个Message，并表达清楚，不要把几个Messages杂糅在一起。一段文字开头第一句就要让读者知道这段在说什么。

Imitation recipe:

```markdown
Paragraph message: <one sentence>
Support 1: <evidence/mechanism>
Support 2: <comparison/caveat>
Transition: <why next paragraph follows>
```

Bad paragraph diagnosis:

- starts with background;
- introduces method and experiment in same paragraph;
- hides the claim in the last sentence.

Fix:

- move the claim to sentence one;
- split method and evidence into separate paragraphs;
- use the last sentence to prepare the next logical step.

### Case 3: Writing schedule from material

Source excerpt:

> 什么时候要开始写论文：一般情况下，至少要在截稿时间一个月前就开始写论文。

Use this as default schedule:

- T-30: story, claim ledger, pipeline sketch, experiment gaps.
- T-21: method + introduction draft while experiments continue.
- T-14: experiments section, figures/tables, related work.
- T-7: reviewer simulation and major fixes.
- T-3: abstract/title, layout, language, final proof.
