# Full-paper narrative flow and paragraph-function pattern

Use this reference when a draft feels choppy even if the sentences are grammatical. A fluent top-tier paper is usually fluent because every paragraph has a clear function and every section advances the same argument.

## Hidden spine

Strong papers repeatedly instantiate:

```text
Problem → Gap → Design → Evidence → Insight → Impact
```

For benchmark/evaluation papers this often becomes:

```text
Old evaluation saturates
→ introduce a stronger benchmark
→ define difficulty through a capability hierarchy
→ redefine scoring through group/consistency evaluation
→ prove data quality through annotation and QA
→ show models still fail far below humans
→ explain bottlenecks and future model directions
```

## Section jobs

| Section | Primary job | Reader question answered |
| --- | --- | --- |
| Abstract | Compress the full argument | Why does this paper matter in one paragraph? |
| Introduction | Manufacture necessity | Why must this work exist now? |
| Related Work | Position the gap | What did prior work solve and what remains? |
| Design/Method | Justify design choices | How exactly does this solve the stated gap? |
| Dataset/Construction | Build trust | Why should I believe the artifact is high quality? |
| Experiments | Prove and diagnose | What does the artifact reveal that old evaluation missed? |
| Discussion/Limitations | Scope the claim | What does this imply and where does it stop? |
| Conclusion | Reclaim the spine | What should the field remember? |

## Paragraph function tags

Before revising, tag every paragraph with exactly one function:

- `Background`: establishes field context.
- `Problem`: states a failure, contradiction, or bottleneck.
- `Gap`: explains what prior work misses.
- `Bridge`: transitions from problem to solution.
- `Design`: introduces a component or principle.
- `Rationale`: explains why a design is necessary.
- `Example`: makes an abstract design concrete.
- `Evidence`: reports data, experiment, or quality signal.
- `Interpretation`: explains what evidence means.
- `Insight`: turns interpretation into a broader finding.
- `Limitation`: scopes the claim.
- `Impact`: connects the result to future work.

A paragraph with three tags is usually overloaded and should be split.

## Road-sign first sentence

Each paragraph's first sentence should function as a road sign. It should define the paragraph's claim, question, or transition.

Good road signs:

- `Previous benchmarks predominantly evaluate isolated questions, which obscures whether models reason consistently across related evidence.`
- `To address this limitation, we organize video understanding into a progressive three-level capability hierarchy.`
- `This degradation suggests a cascading bottleneck rather than an isolated high-level reasoning failure.`

Weak road signs:

- `Recently, many works have studied this topic.`
- `Table 2 shows the results.`
- `We also conduct more experiments.`

## Claim-like subsection titles

For experiments and analysis, prefer takeaway titles over neutral labels.

Weak:

- `Experiment 1`
- `Results on Models`
- `Analysis`

Strong:

- `Group-based scoring exposes inconsistent reasoning`
- `Errors in visual aggregation propagate to temporal reasoning`
- `Thinking prompts help with subtitles but regress in pure-visual settings`

A reader should understand the paper's story by scanning section titles and first sentences.

## Design-to-experiment closure

Every major design must reappear in experiments or analysis.

| If the paper designs... | Experiments should show... |
| --- | --- |
| capability hierarchy | scores and failures by level |
| group-based scoring | comparison against per-question accuracy |
| strict annotation pipeline | ambiguity/leakage/QA evidence |
| adversarial distractors | shortcut or text-only baseline analysis |
| long-context input | controlled frame/context comparison |
| reasoning mode | condition where it helps and where it hurts |

If a design is not evaluated, label it as a construction principle, not a proven contribution.

## Number-to-meaning rule

Never leave a number alone. Use:

```text
number → comparison → interpretation → implication
```

Example:

```markdown
The best model achieves 49.4, compared with 90.7 for human experts. This gap indicates that the benchmark is far from saturated. The largest drop occurs at the temporal-reasoning level, suggesting that high-level failures often originate in lower-level grounding errors.
```

## Concrete example after abstract concept

When introducing a new concept, add one concrete example immediately after it.

Pattern:

```markdown
We define coherence-based question groups to evaluate whether a model can preserve a reasoning chain across related queries. For example, in a scene where a character feigns death, the group first asks the model to localize the visual clue, then verify the anomaly, then infer the motive, and finally answer the narrative-level question.
```

## Revision checklist

- Can every paragraph be labeled with one function tag?
- Does each paragraph's first sentence tell the reader why the paragraph exists?
- Does each section answer a distinct reader question?
- Does every design choice correspond to a previous limitation?
- Does every major design choice come back in experiments or analysis?
- Do experiment subsections have takeaway titles?
- Does every number have interpretation and implication?
- Does the conclusion recover the same spine introduced in the abstract/introduction?
