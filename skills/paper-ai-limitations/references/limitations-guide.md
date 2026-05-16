# Limitations guide

Limitations increase trust when they honestly scope claims. They should not become a self-rejection letter, but they must reveal constraints that affect interpretation.

## Limitation categories

- Scope: task/domain/data setting where claims apply.
- Assumptions: method depends on a condition that may fail.
- Evidence: missing baselines, small datasets, or incomplete ablations.
- Compute: training/inference cost or resource constraints.
- Reproducibility: unavailable code/data or fragile setup.
- Robustness/safety/fairness: known deployment risks.
- Generality: result may not transfer to other domains.

## Wording pattern

1. State the limitation concretely.
2. Explain which claim or setting it affects.
3. Say what evidence partially mitigates it, if any.
4. Avoid promising unsupported future experiments.

## Claim caveat examples

- Replace “works for all settings” with “we evaluate in X and expect Y to require additional validation.”
- Replace “solves robustness” with “improves robustness under the tested perturbations.”
- Replace “general framework” with “framework for settings satisfying assumption A.”

## Common failures

- Limitation section is generic and disconnected from claims.
- Hides the main weakness until rebuttal.
- Over-apologizes for minor issues while ignoring major evidence gaps.
- Promises future work that sounds necessary for the current claim.

## Material-derived case card

Materials repeatedly warn that claims, especially in Abstract and Introduction, must be experimentally supported. Use limitations to make unsupported scope explicit instead of hiding it.

Bad limitation:

> Our method may have some limitations, which we leave to future work.

Good limitation:

> Our evidence supports compositional prompts with up to three objects. We have not validated dense scenes or video prompts, so claims about general spatial reasoning should be treated as future work rather than a conclusion of this paper.

Imitation rule:

For every broad claim, ask: “What setting would make this false?” If that setting is not tested, add a scope caveat.
