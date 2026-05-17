# Research workflow guide

This reference adapts the previous Claude Code academic research workflow into the current Codex paper-skill structure. Keep the workflow paper-facing: the goal is not an encyclopedic report, but a defensible evidence base that can feed claims, related work, method choices, experiments, figures, and rebuttal.

## Research modes

| User situation | Recommended mode | Output |
| --- | --- | --- |
| Vague topic, unclear question | Socratic scoping | research-question brief and decision options |
| Clear question, needs sources | Literature plan | search strings, source matrix, inclusion/exclusion criteria |
| Has sources, needs trust judgment | Source verification | source-quality matrix and citation risk notes |
| Has evidence, needs paper story | Evidence synthesis | claim/evidence map and gap analysis |
| Needs systematic review logic | Systematic-review lite | protocol skeleton, screening plan, PRISMA-style count placeholders |

Prefer scoping before full synthesis when the user's question is broad, value-laden, or method-first.

## Paper-facing research pipeline

```text
question scoping
→ methodology and evidence blueprint
→ search strategy and source collection
→ source verification and quality grading
→ cross-source synthesis
→ claim/evidence handoff
→ writing, related work, method, experiments, or limitations
```

Each stage should answer one reader-facing question:

1. **Scoping:** What exactly are we trying to learn or prove?
2. **Methodology blueprint:** What kind of evidence could answer this question?
3. **Search strategy:** Where would a skeptical reviewer expect us to look?
4. **Source verification:** Which sources are trustworthy enough to support claims?
5. **Synthesis:** What is agreed, disputed, missing, or newly implied?
6. **Handoff:** Which paper claims are supported, partial, planned, or unsupported?

## Research brief template

```markdown
# Research Brief

## Working question
- Main RQ:
- Sub-questions:
- In scope:
- Out of scope:

## Evidence blueprint
- Best evidence type:
- Acceptable evidence type:
- Evidence that would be too weak:
- Minimum publishable evidence:

## Search plan
- Databases / sources:
- Keywords / Boolean strings:
- Inclusion criteria:
- Exclusion criteria:
- Freshness constraints:

## Synthesis
- Established findings:
- Disputed findings:
- Gaps:
- Implications for this paper:

## Handoff
- Supported claims:
- Partial claims:
- Unsupported or risky claims:
- Next skill:
```

## Handoff rules

- To `paper-ai-idea`: when the question, audience, or contribution is still unstable.
- To `paper-ai-related-work`: when the literature clusters and closest-work risks are visible.
- To `paper-ai-method`: when the research question implies a specific method or evaluation design.
- To `paper-ai-experiments`: when evidence gaps require new experiments, baselines, or ablations.
- To `paper-ai-writing`: when the evidence base is stable enough for cross-section story work.
- To `paper-ai-limitations`: when the evidence base supports only a narrower claim.

## Adapted lessons from the previous Claude Code project

- Keep a clear separation between research, writing, review, and integrity checks.
- Use checkpoints at evidence boundaries, not after every trivial action.
- Treat source quality as a first-class artifact, not an afterthought in references.
- A research pipeline should produce a handoff, not force every user through a monolithic full workflow.

## ARS-compatible modes in Codex

This skill owns the Codex-native entry point for deep-research `full`, `quick`, `lit-review`, `fact-check`, and `systematic-review` intents. Treat old slash-style phrases as equivalent intents, not literal commands unless a dispatcher is explicitly running.

- `full`: produce a research brief, methodology blueprint, source matrix, and scoped claims.
- `quick`: produce a compact research brief with source-quality notes.
- `lit-review`: produce a literature matrix and synthesis map; hand related-work prose to `paper-ai-related-work`.
- `fact-check`: validate claim support and mark unsupported claims instead of rewriting them.
- `systematic-review`: advisory first pass using protocol/checklist artifacts until full PRISMA validators exist.

Machine-readable mode ownership lives in `oh_my_paper.ars_compat` registries.
