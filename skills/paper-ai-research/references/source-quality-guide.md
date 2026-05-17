# Source quality and search strategy guide

Use this reference when deciding whether a source can support a paper claim. The goal is source discipline: a citation should not merely exist; it should be appropriate for the strength and type of claim.

## Source-quality matrix

| Source | Claim supported | Evidence type | Quality | Caveat | Use |
| --- | --- | --- | --- | --- | --- |
| `<citation/source>` | `C1` | benchmark / experiment / review / official doc / grey literature | A/B/C/D/F | `<scope or risk>` | primary / support / caveat / do not use |

## General quality grades

- **A — primary support:** peer-reviewed, methodologically strong, current for the topic, and directly aligned with the claim.
- **B — supporting evidence:** credible and relevant, with minor limitations or indirectness.
- **C — caveated evidence:** useful for context or weak support, but needs explicit scope caveats.
- **D — background only:** cite only for motivation, history, or contrast; do not use for central empirical claims.
- **F — unusable:** unverifiable, predatory, methodologically broken, or too misaligned with the claim.

## Evidence hierarchy by field

Do not force every field into a biomedical pyramid. Adjust standards:

| Field / task | Strong evidence usually means | Watch for |
| --- | --- | --- |
| ML systems / benchmarks | reproducible experiments, strong baselines, ablations, public protocols | cherry-picked settings, weak baselines, leakage |
| AI evaluation papers | benchmark design rationale, annotation/QA evidence, metric ablation, model-human gap | leaderboard-only claims |
| Medicine / health | systematic reviews, RCTs, registered protocols, effect sizes | outdated reviews, underpowered studies |
| Education / social science | quasi-experimental, longitudinal, mixed-method, validated instruments | overcausal claims from observational data |
| Policy / practice | triangulated reports, transparent methods, stakeholder analysis | advocacy reports used as neutral evidence |
| Humanities / theory | primary texts, conceptual precision, argumentative coherence | treating authority as empirical proof |

## Search planning checklist

Before collecting sources, define:

1. Research question and claim type.
2. Required source types: empirical, theoretical, benchmark, survey, official documentation, or policy evidence.
3. Databases or venues expected by reviewers.
4. Keyword families and synonyms.
5. Inclusion and exclusion criteria.
6. Date range and freshness requirement.
7. Contradictory or negative-evidence search terms.

## Shortcut and contamination risks

Flag sources when:

- the venue or publisher looks predatory;
- the source is a blog or marketing page supporting a strong scientific claim;
- the paper is too old for a fast-moving technical claim;
- the claim in your draft is stronger than the source's actual conclusion;
- multiple citations trace back to the same weak original evidence;
- a benchmark/source may overlap with training, test, or evaluation data.

## Citation-to-claim rule

For every important citation, write one sentence:

```markdown
This source supports claim <ID> only under <scope>, because <specific evidence>; it does not support <overclaim>.
```

If you cannot write that sentence, the citation is not ready to support the claim.
