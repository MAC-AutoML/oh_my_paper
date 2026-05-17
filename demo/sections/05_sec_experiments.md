# 4. Demonstration and Synthetic Results

## Section contract

- Reader question: Show the reporting style while making clear that no real RL environment was run.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Citation status: representative references are included for field positioning; synthetic values remain non-empirical.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

This demo uses synthetic values only to show how a reliability paper would present results. The example compares a mean-return view with a diagnostic view. Under the mean-return view, PPO-like and off-policy baselines appear close. Under the diagnostic view, policies lose credit when performance varies across seeds, collapses under perturbation, or lacks support from task-relevant state features. This reporting style is motivated by reproducibility and statistical-evaluation concerns in deep RL [11,12], but the values below are not copied from those works.

| Method | Mean-return view | Stability check | Robustness check | Decision-support check | Diagnostic score |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO-style baseline | 82.0 | 74.0 | 58.0 | 46.0 | 52.4 |
| Off-policy baseline | 84.0 | 78.0 | 64.0 | 51.0 | 58.2 |
| Deterministic actor baseline | 79.0 | 70.0 | 55.0 | 43.0 | 49.7 |
| Reference policy | 95.0 | 93.0 | 88.0 | 86.0 | 88.9 |

The intended lesson is structural rather than empirical. A real paper would need environment definitions, public seeds, perturbation settings, training curves, statistical intervals, and reproducible code. It would also need to compare against canonical baselines from both value-based and actor-critic traditions [4,8,9,10]. The demo table simply illustrates the kind of discrepancy that motivates diagnostic evaluation. The reviewer loop should penalize any draft that presents this table as a real PPO result.
