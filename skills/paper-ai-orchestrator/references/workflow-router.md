# Full paper workflow router

Use this router only to choose the next natural paper step, not to create a bureaucracy. The workflow is a loop over paper artifacts:

1. **Idea**: clarify problem, audience, contribution hypothesis, and evidence needed.
2. **Writing scaffold**: decide paper story and section order.
3. **Title/abstract**: create the first reviewer impression.
4. **Introduction**: build problem → gap → idea → contributions.
5. **Related work**: position against closest work and comparison axes.
6. **Method**: explain assumptions, running example, notation, and algorithm.
7. **Experiments**: connect results to claims with baselines/metrics/ablations.
8. **Figures/tables**: make evidence and method visually legible.
9. **Limitations**: state scope honestly without self-sabotage.
10. **Layout/polish**: page budget, language, PDF/template checks.
11. **Reviewer simulation**: strict first-impression and technical review.
12. **Rebuttal**: parse concerns, map evidence, write AC-aware answers.

## Routing rules

- If no clear contribution exists, route to `paper-ai-idea`.
- If the user asks for a specific section, route directly to that section skill.
- If claims are unsupported, route through the relevant section but keep claim/evidence gates visible.
- If review comments exist, route to `paper-ai-rebuttal`; use `paper-ai-reviewer` only to audit the draft or rebuttal.
- If new material arrives, use the CLI intake workflow from docs, then internalize lessons into the relevant skill reference.

## Minimal state note

Do not create excessive management files. If state is useful, write only:

```markdown
# Paper AI State
- Current step:
- Available artifacts:
- Blocking evidence gaps:
- Next skill:
- Human decision needed:
```

## Material-derived case card: natural writing order

Source excerpt (rights-cleared writing template):

> 画 pipeline figure 草图 → 梳理论文 story / Introduction 思路 / comparison experiments / ablation studies → 写 Method 同时做实验 → 改 Introduction 和 Method → 实验稳定后写 Experiment → 美化 pipeline figure 和 teaser → 写 Related work → Review 论文 → 写 Abstract → 取标题 → 反复 review 和修改。

Use this order as default when the user asks “下一步做什么”:

1. If no story/pipeline exists: `paper-ai-idea` + `paper-ai-figures` sketch.
2. If story exists but method unclear: `paper-ai-method`.
3. If experiments unstable: `paper-ai-experiments` for evidence plan/record.
4. If draft exists: introduction/method/experiments review loop.
5. Near submission: abstract/title, layout, reviewer simulation.

## oh my paper pipeline contract

The Codex-native pipeline equivalent routes through durable artifacts rather than an external orchestration runtime:

1. Research brief and methodology blueprint.
2. Outline and claim/evidence map.
3. Draft sections and figure/table plans.
4. Integrity check before reviewer simulation.
5. Reviewer panel and fix plan.
6. Revision and traceability matrix.
7. Final integrity report.
8. Layout/disclosure/process summary.

Use `paper/MATERIAL_PASSPORT.json` for reset/resume metadata. If the passport is malformed or the resume hash is invalid, do not claim the run can resume safely.
