# Related work guide

Related work should position the paper, not merely list papers. Organize by contrast axes that matter to the current contribution.

## Build a contrast map

| Cluster | What it solves | Main assumption | Limitation/gap | Our difference |
| --- | --- | --- | --- | --- |

Useful axes:

- task setting or supervision;
- data requirements;
- model family or objective;
- inference/training cost;
- evaluation protocol;
- guarantees or failure modes;
- deployment constraints.

## Writing pattern

1. Define the cluster and why it matters.
2. Summarize representative work fairly.
3. State the limitation or open gap.
4. Explain how the current paper differs without strawman wording.

## Closest-work paragraph

A strong paper names its closest competitors directly. Use:

- “Most similar to our work is ...”
- “Unlike ..., our setting assumes ...”
- “This distinction matters because ...”
- “We compare empirically in ...”

## Failure modes

- Chronological laundry list.
- Hides closest work until reviewers bring it up.
- Claims novelty by weakening prior work unfairly.
- Missing citations for obvious baselines.
- Related work does not prepare the reader for the method or experiments.

## Material-derived case card

The idea materials emphasize literature trees: novelty tree and challenge-insight tree. Use them to avoid a flat related-work list.

Imitation structure:

```markdown
Cluster A solves <problem> with <paradigm>, but assumes <assumption>.
Cluster B removes <assumption>, but introduces <new limitation>.
Our work targets <gap> by <idea>; compare empirically against <closest work>.
```

Bad:

> Many works study this task. A does X. B does Y. C does Z.

Good:

> Prior work splits into retrieval-based and generation-based approaches. Retrieval methods preserve factuality but fail when evidence is implicit; generation methods improve coverage but hallucinate under sparse evidence. Our method targets this trade-off by ...
