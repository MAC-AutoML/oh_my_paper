# Benchmark / dataset / evaluation paper pattern

Use this pattern when writing benchmark, dataset, diagnostic evaluation, leaderboard, or model-evaluation papers. The goal is not to say “we made a dataset”; the goal is to prove a field-level evaluation gap and show that the new benchmark reveals failures that old evaluation hides.

## Core narrative

```text
Existing evaluation is failing
→ a stronger benchmark/evaluation protocol is necessary
→ our design is systematic, strict, and credible
→ experiments reveal a gap or bottleneck hidden by prior benchmarks
→ the benchmark becomes a diagnostic testbed for future work
```

The abstract and introduction should tell this story as a short scientific argument, not as a catalog of dataset statistics.

## Abstract structure

| Function | What to write | Why it works |
| --- | --- | --- |
| Field context | Recent progress in <field> has raised <evaluation need>. | Places the work in an active area. |
| Crisis/gap | Existing benchmarks are saturated, shortcut-prone, or misaligned with real-world capability. | Creates research necessity. |
| Motivation | Leaderboard scores diverge from robust, faithful, or deployable capability. | Turns “new benchmark” into a field problem. |
| Solution | We introduce <benchmark>, a <definition> designed to evaluate <capability>. | Names the artifact and its scientific target. |
| Systematic design | A hierarchy, taxonomy, protocol, or construction principle decomposes capability. | Shows the benchmark is not random data collection. |
| Evaluation innovation | New scoring/diagnostic protocol addresses a flaw in conventional accuracy. | Adds method contribution beyond data. |
| Quality signal | Annotation/review rounds, human-hours, agreement, leakage control, audits. | Builds trust. |
| Key result | Best model vs. human / old benchmark vs. new benchmark / hidden failure. | Proves the benchmark matters. |
| Diagnostic insight | Error propagation, bottleneck, condition-specific failure. | Makes it more than a leaderboard. |
| Impact | A demanding diagnostic testbed for next-generation systems. | Ends with field-level relevance. |

## Contrastive framing

Weak:

> We introduce a new benchmark with many videos and questions.

Strong:

> Existing video benchmarks increasingly fail to distinguish genuine multimodal reasoning from shortcut-based correctness. We introduce <X>, a diagnostic benchmark that evaluates whether models remain consistent across related queries requiring visual evidence aggregation, temporal dynamics modeling, and multimodal reasoning.

Always contrast old vs. new:

| Old evaluation | New evaluation |
| --- | --- |
| Isolated per-question accuracy | Group-level or consistency-aware scoring |
| Larger data only | Capability hierarchy / diagnostic taxonomy |
| Leaderboard ranking | Failure-mode diagnosis |
| “Carefully annotated” | Concrete QA pipeline, reviewers, rounds, agreement |

## Capability hierarchy pattern

Do not list question types as a flat taxonomy if the paper can support a hierarchy. A hierarchy creates a theory of difficulty and enables deeper analysis.

Example structure:

```text
Level 1: Evidence aggregation — find and combine relevant observations.
Level 2: Temporal / relational modeling — understand how evidence changes or interacts.
Level 3: Complex reasoning — answer questions whose correctness depends on lower-level evidence and temporal structure.
```

Then make experiments mirror the design:

- main score by level;
- error propagation across levels;
- model/human gap by level;
- examples where low-level failure limits high-level reasoning.

## Evaluation protocol pattern

A benchmark paper becomes stronger when it questions the metric, not only the data.

Good metric contribution sentence:

> Unlike conventional per-question accuracy, our group-based protocol assigns credit only when a model remains consistent across related queries that jointly test the same underlying reasoning process.

Avoid unverifiable wording:

- Too strong: “assigns credit only to valid reasoning.”
- Safer: “assigns credit only when answers remain consistent across related queries designed to require the same underlying evidence.”

## Data-quality credibility signals

Use concrete signals, not adjectives alone.

Better than “carefully annotated”:

```text
The benchmark was constructed by <N> annotators, reviewed by <M> independent reviewers, revised through up to <R> quality-control rounds, and audited for <leakage/ambiguity/answerability>.
```

If these details are not available, do not fabricate them. Write TODOs or mark the claim as planned.

## Results should produce insight

A strong benchmark paper reports three layers:

1. **Performance:** who scores how high?
2. **Diagnosis:** where and why do models fail?
3. **Field insight:** what should next-generation systems improve?

Bad:

> Our benchmark is challenging for current models.

Good:

> The best model remains far below human performance, and the gap widens from evidence aggregation to temporal modeling to multimodal reasoning, suggesting that high-level reasoning failures often originate in earlier grounding errors.

## Mature limitation style

High-quality evaluation papers should avoid marketing. Replace self-praise with verifiable scope.

Avoid:

> This is one of the most authoritative benchmarks.

Prefer:

> This benchmark provides a rigorously curated and diagnostically informative testbed for measuring robust video understanding.

## Abstract template

```markdown
Despite recent progress in <field>, existing <benchmarks/evaluations> increasingly struggle with <failure>, creating a gap between <leaderboard/proxy metric> and <real capability>. To address this gap, we introduce <Benchmark>, a <one-sentence definition> designed to evaluate <target capability>. <Benchmark> is organized around <capability hierarchy/design principle>, enabling systematic assessment of <levels>. In addition, we propose <evaluation protocol> that <contrast with conventional metric> and penalizes <shortcut/failure>. Constructed with <quality pipeline>, the benchmark provides <coverage/credibility>. Experiments with <models> show <key quantitative result>. Further analysis reveals <diagnostic insight>, suggesting <field implication>. These results establish <Benchmark> as a challenging diagnostic testbed for <future systems>.
```

## Review checklist for benchmark abstracts

- Does it start from a real evaluation crisis, not from “we introduce X”?
- Is the scientific target clear: robustness, faithfulness, temporal grounding, consistency, calibration, etc.?
- Is the benchmark design systematic rather than just “diverse”?
- Is there a metric/protocol contribution or a strong justification for standard metrics?
- Are data-quality claims backed by concrete process details?
- Does the abstract include at least one key result number or planned evidence slot?
- Does it report an insight, not only a score?
- Are impact claims restrained and verifiable?
