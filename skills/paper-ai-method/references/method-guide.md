# Method section guide

Method writing should make the idea understandable before formal details. The reader needs assumptions, intuition, notation, and component rationale in the right order.

## Method structure

1. Problem setup and assumptions.
2. Short overview of the method.
3. Running example or motivating case.
4. Notation table and definitions.
5. Components in dependency order.
6. Algorithm/objective/training/inference details.
7. Complexity or implementation notes if decision-relevant.
8. Link from components to claims/ablations.

## Running example pattern

Use a small example before equations when the method is complex:

- Show the input/output.
- Name what the baseline would do.
- Show what the new method changes.
- Map example objects to notation.
- Then introduce formal equations or algorithm steps.

## Component rationale

For each component:

```markdown
- Component:
- Purpose:
- Assumption:
- Claim supported:
- Ablation/evidence:
- Failure mode if removed:
```

## Common failures

- Starts with equations before the reader knows the problem.
- Uses notation that is not defined or changes meaning.
- Describes implementation but not why components exist.
- Hides assumptions that later reviewers will attack.
- No connection between method components and experiment ablations.

## Material-derived case cards

### Case 1: Running example before formalism

Source excerpt (rights-cleared tutorial):

> 正确的顺序：首先给出 running example；然后利用 running example，用通俗语言描述你的想法；最后才是形式化描述。每个公式都有语言学意义，都来自你的直觉和想法，直接告诉审稿人，不要让他/她去揣摩。

Imitation recipe:

```markdown
1. Running example: show a tiny input/output and baseline failure.
2. Plain-language idea: explain what the method changes.
3. Formalization: introduce notation matching the example.
4. Formula meaning: after every equation, write what it means and why it exists.
```

Bad method opening:

> Let X be a tensor and define L = ...

Good method opening:

> Consider a prompt with two objects whose spatial relation is ambiguous. A standard model often binds attributes to the wrong object. Our method first constructs an object-relation graph, then uses the graph to constrain cross-attention. We formalize this as follows...

### Case 2: Component rationale table

Use this before writing prose:

| Component | Reader intuition | Formal object | Claim supported | Ablation |
| --- | --- | --- | --- | --- |
| Constraint graph | makes relations explicit | G=(V,E) | C1 | remove graph |
| Attention mask | prevents wrong binding | M | C2 | replace with dense attention |

### Case 3: Formula explanation pattern

After each equation add:

- What quantity it computes.
- Which intuition it encodes.
- Which component uses it.
- What would fail without it.

## Method as design necessity

A method section is fluent when every component is a response to a previously stated limitation.

Use this local pattern for each component:

```markdown
Previous approaches usually <old design>, which fails to capture <missing property>. To address this limitation, we design <component>. Specifically, <component> consists of <subpart A>, <subpart B>, and <subpart C>. This design enables <benefit> by <mechanism>.
```

For hierarchical designs, write with dependency language:

- `Building on Level 1...`
- `Extending this foundation...`
- `At the highest level...`

Then close the loop:

```markdown
This hierarchy is evaluated directly in Section <experiments>, where we report performance and error propagation across levels.
```

Do not introduce a component that never returns in ablations, diagnostics, or limitations unless it is explicitly scoped as implementation detail.
