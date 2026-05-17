# Codex Agent Recipes for oh_my_paper

These recipes describe how to use repo-local Codex subagent roles for oh my paper panels. They are artifact contracts, not a dependency on an external orchestration runtime.

## Research panel

Roles: `paper-research-question`, `paper-bibliography`, `paper-source-verifier`, `paper-synthesis`, `paper-devils-advocate`.

Inputs: topic, `paper/CLAIMS.md`, `paper/EVIDENCE_MAP.md`, source notes.
Outputs: `paper/RESEARCH_BRIEF.md`, source matrix, synthesis notes, scoped claim updates.
Gate: no claim becomes supported without traceable evidence.

## Writing panel

Roles: `paper-structure-architect`, `paper-argument-builder`, `paper-draft-writer`, `paper-citation-auditor`, `paper-visualization-planner`.

Inputs: paper brief, claims, evidence map, experiment notes.
Outputs: outline, section drafts, figure/table plan, citation audit notes.
Gate: unsupported claims remain marked or are removed.

## Reviewer panel

Roles: `paper-field-analyst`, `paper-review-eic`, `paper-methodology-reviewer`, `paper-domain-reviewer`, `paper-perspective-reviewer`, `paper-devils-advocate-reviewer`, `paper-editorial-synthesizer`.

Inputs: current draft bundle, evidence map, target venue constraints when known.
Outputs: review reports, editorial decision, prioritized fix plan.
Gate: fatal concerns block submission-ready claims.

## Integrity panel

Roles: `paper-integrity-verifier`, `paper-claim-reference-auditor`, `paper-citation-auditor`, `paper-compliance-verifier`, `paper-state-tracker`.

Inputs: claim ledger, evidence map, citation anchors, Material Passport JSON.
Outputs: integrity report, citation anchor audit, process summary.
Gate: unresolved unsupported claims or malformed integrity reports block finalization.
