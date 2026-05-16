# Rebuttal guide

A rebuttal is a limited correction opportunity, not a replacement for submission quality. Write for both reviewers and the area chair. Make the decision-relevant evidence easy to see without rereading the entire paper.

## Workflow

1. Parse reviews into atomic concerns.
2. Group duplicates and identify consensus blockers.
3. For each concern, map evidence, concession, or promised revision.
4. Draft full answers before compressing.
5. Put decision-relevant concerns before minor wording fixes.
6. Audit tone and overpromises.
7. Produce AC-facing summary if allowed/appropriate.

## Concern table

| Reviewer | Concern | Severity | Evidence | Response strategy | Promised revision | Space priority |
| --- | --- | --- | --- | --- | --- | --- |

## Response pattern

Concern → direct answer → evidence/context → concrete revision if needed → polite close.

## Tone rules

- Be direct, respectful, and self-contained.
- Do not blame reviewers or say they “failed to understand.”
- Acknowledge valid concerns quickly.
- Push back only with evidence.
- Do not promise experiments that are not done or approved.

## AC-facing priorities

- Which concerns affect the decision?
- Which concerns are resolved by existing evidence?
- Which concerns require paper clarification only?
- Which limitations remain after rebuttal?

## Common failures

- Uses space on minor comments before fatal concerns.
- Promises future fixes instead of giving current evidence.
- Answers each reviewer separately but misses cross-reviewer consensus.
- Tone becomes defensive.
- Compresses away the actual answer.

## Material-derived case cards

### Case 1: Rebuttal language style

Source excerpt (rights-cleared rebuttal material):

> 问啥答啥。不要扯其他的东西，这样会分散Reviewer的注意力。把Reviewer问的东西放在段落最前面。尽量按Reviewer问题的顺序回答Reviewer。尽量在每个Reviewer Section下列出Reviewer的所有问题，然后一一回复。

Imitation recipe:

```markdown
**R2.Q1: <reviewer's concern in compact form>.**
Answer: <direct answer first>. Evidence: <paper/table/experiment/supplement>. Revision: <specific edit if any>. Caveat: <remaining limitation if needed>.
```

Bad response:

> Thank you. Our method is novel and we have many advantages. Please see the paper.

Good response:

> **R2.Q1: Does the improvement come from the constraint graph or from extra parameters?** The ablation in Table 3 isolates this: removing the graph while keeping parameter count comparable reduces <provided metric>. We will add this comparison to Sec. 4.3 and clarify that the claim is about compositional layouts, not all prompts.

### Case 2: Rebuttal process

Source excerpt:

> 首先整理review的内容；然后回答justification和weaknesses里提出的问题；写完rebuttal的初稿后，标记每个reviewer的重点问题...反复确认是否正确回答了reviewer的问题，是否能convince reviewer。也找同学看看。

Use this workflow:

1. Build reviewer concern table.
2. Mark decision-relevant concerns from justification/weaknesses.
3. Draft complete answers.
4. Run convincingness audit.
5. Ask peer/agent reviewer to judge whether each answer actually addresses the concern.
6. Compress only after content is complete.

### Case 3: AC-aware response from public article summary

Adapted pattern from external rebuttal article: write for reviewers and the area chair. The AC needs to quickly see whether concerns are addressed.

AC summary template:

```markdown
The main concerns are <A>, <B>, and <C>. We address <A> with existing evidence in Table/Fig <x>; <B> is a presentation issue and we propose a concrete clarification; <C> is a valid limitation and we scope the claim accordingly. No new unsupported result is promised.
```
