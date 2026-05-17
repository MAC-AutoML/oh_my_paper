# Experiment writing and design guide

Experiment sections answer reviewer questions: what was tested, why this setup is fair, what happened, and what the result means for each claim.

## Evidence coverage table

| Claim | Dataset/task | Baseline | Metric | Result artifact | Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- |

## Section structure

1. Experimental questions.
2. Datasets/tasks and why they match the claims.
3. Baselines and comparison fairness.
4. Metrics and statistical/significance treatment when relevant.
5. Main results.
6. Ablations and diagnostics.
7. Failure cases/limitations.

## Result paragraph pattern

Question → setup → key observed result → interpretation → claim link → caveat.

Never invent numeric values. If a number is missing, write a TODO or ask for the artifact.

## Rigor checklist

- Standard datasets or justified custom data.
- Strong and current baselines.
- Metric matches claim.
- Ablation for each major component.
- Sensitivity/diagnostic analysis for key assumptions.
- Reproducibility details sufficient for reviewer confidence.

## Common failures

- Claims “better” without naming baseline/metric.
- Uses cherry-picked examples as main evidence.
- Ablations do not correspond to method components.
- Appendix carries crucial evidence that should be in main paper.
- Result interpretation overstates what the experiment proves.

## Material-derived case cards

### Case 1: Experiment design stack

Source excerpt (rights-cleared tutorial):

> 公认的标准数据和 state-of-the-art 系统；实验先辅后主；辅助实验（开发集）：参数的影响；主实验（测试集）：证明显著超过 baseline；必须有显著性检验；不辞辛劳，做到极致。

Imitation recipe:

```markdown
Main claim → standard dataset/task → strong baseline → metric → main test result → significance/uncertainty
Mechanism claim → dev/auxiliary experiment → parameter/ablation analysis
Robustness claim → stress/failure analysis → caveat
```

### Case 2: Experiment record habit

Source excerpt (rights-cleared experiment-record material):

> 实验的目的：描述为什么做这个实验，想通过实验获得什么。实验的 setting：什么样的数据上做的实验，算法上有什么改动。记录实验结果：记录效果好和效果不好的实验结果，包括可视化结果和量化结果。分析实验结果：观察实验结果是否符合预期。如果不符合预期，需要分析实验不work的原因。Next step：你是project的leader，不断地思考如何进行下一步，列出接下来要做的实验，而不是等待instructions。

Use this table:

| Date | Purpose | Setting/change | Quant result | Visual result | Expected? | Analysis | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Case 3: Result paragraph imitation

Bad:

> Our method performs better than baselines, proving effectiveness.

Good:

> To test whether the constraint graph improves object binding (C2), we compare against <baseline> on <dataset> using <metric>. The result shows <provided number or qualitative artifact>. This supports C2 because <interpretation>. The evidence is limited to <scope/caveat>.

## Benchmark/evaluation experiment pattern

Benchmark experiments must prove that the benchmark is useful, not only report leaderboard numbers.

Required experiment layers:

1. **Main performance:** state-of-the-art model scores, human performance, and legacy benchmark comparison if available.
2. **Capability breakdown:** results by hierarchy level, task type, domain, duration, modality, or reasoning requirement.
3. **Metric/protocol ablation:** compare conventional accuracy with the proposed scoring protocol.
4. **Quality/reliability evidence:** annotation agreement, reviewer audit, leakage checks, ambiguity resolution, or QA rounds.
5. **Error analysis:** identify recurring failure modes and whether lower-level errors propagate upward.
6. **Condition-specific insight:** when reasoning prompts, subtitles, longer context, or tools help and when they hurt.

Result interpretation pattern:

```markdown
Performance: <model> achieves <score>, compared with <human/baseline>.
Diagnosis: The gap is largest in <capability level>, indicating <bottleneck>.
Metric insight: Under <old metric>, the model appears stronger because <shortcut>; under <new metric>, inconsistent groups are penalized.
Field implication: Future models need <specific capability>, not only higher average accuracy.
```

Ablation examples:

| Question | Possible ablation |
| --- | --- |
| Does group scoring matter? | per-question accuracy vs. group-consistency score |
| Does hierarchy diagnose failure? | score by evidence aggregation / temporal modeling / reasoning |
| Is quality control necessary? | before-vs-after QA ambiguity/noise rate |
| Do reasoning prompts help? | with subtitles vs. pure visual settings |

Never invent annotation counts, human-hours, model scores, or reviewer numbers. If missing, use `TODO: provide artifact`.

## Experiment sections as interpretation, not table dumping

Begin result subsections with the takeaway, not with “Table X shows.”

Weak:

> Table 1 shows the benchmark results.

Strong:

> Current video MLLMs remain far below human reliability on the proposed benchmark.

Use this paragraph rhythm:

```text
takeaway title/first sentence → key number → comparison → interpretation → broader implication
```

Common diagnostic moves:

- Convert a score drop across levels into an error-propagation explanation.
- Compare old and new metrics to show what old evaluation hides.
- Compare with/without text, audio, frames, or reasoning mode to reveal dependence on cues.
- Use mean/variance or ratio analysis to separate average ability from stability.
- End analysis with what future models need, not only who ranked first.
