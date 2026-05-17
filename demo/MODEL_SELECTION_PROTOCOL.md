# Model selection protocol

A live run should not hard-code the paper idea. It should perform this selection step before drafting.

## Candidate generation

The idea agent proposes 3-5 paper directions from the user's material, for example:

1. reliability benchmark for policy optimization;
2. reproduction protocol for PPO-style experiments;
3. survey/tutorial on RL evaluation failure modes;
4. robustness checklist for RLHF-style policy updates.

## Reviewer-model selection

Use the configured reviewer model. If the user config points to Gemini or a Gemini-compatible relay, this is the Gemini-backed selection step.

```text
System: You are a strict academic program chair. Select the best paper direction from user material.
User: Score each candidate 0-100 for novelty, feasibility, evidence fit, citation availability, risk, and expected paper clarity. Return JSON with selected_candidate, score, risk, required caveats, and citation gaps.
```

## Offline demo status

This committed demo records the protocol and uses a deterministic selected direction: reliability benchmark/workflow for policy optimization. It does not call live APIs during repository generation.
