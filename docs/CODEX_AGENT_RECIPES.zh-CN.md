# oh_my_paper 的 Codex Agent Recipes

这些 recipes 说明如何用项目内 Codex subagent roles 组织 ARS 风格的 panel。它们是 artifact contracts，不依赖外部编排运行时。

## Research panel

角色：`paper-research-question`、`paper-bibliography`、`paper-source-verifier`、`paper-synthesis`、`paper-devils-advocate`。

输入：topic、`paper/CLAIMS.md`、`paper/EVIDENCE_MAP.md`、source notes。
输出：`paper/RESEARCH_BRIEF.md`、source matrix、synthesis notes、scoped claim updates。
Gate：没有可追踪证据的 claim 不能变成 supported。

## Writing panel

角色：`paper-structure-architect`、`paper-argument-builder`、`paper-draft-writer`、`paper-citation-auditor`、`paper-visualization-planner`。

输入：paper brief、claims、evidence map、experiment notes。
输出：outline、section drafts、figure/table plan、citation audit notes。
Gate：unsupported claims 必须保留标记或删除，不能被润色成确定结论。

## Reviewer panel

角色：`paper-field-analyst`、`paper-review-eic`、`paper-methodology-reviewer`、`paper-domain-reviewer`、`paper-perspective-reviewer`、`paper-devils-advocate-reviewer`、`paper-editorial-synthesizer`。

输入：当前 draft bundle、evidence map、已知 venue constraints。
输出：review reports、editorial decision、prioritized fix plan。
Gate：fatal concerns 未解决时不能声称 submission-ready。

## Integrity panel

角色：`paper-integrity-verifier`、`paper-claim-reference-auditor`、`paper-citation-auditor`、`paper-compliance-verifier`、`paper-state-tracker`。

输入：claim ledger、evidence map、citation anchors、Material Passport JSON。
输出：integrity report、citation anchor audit、process summary。
Gate：未解决的 unsupported claims 或格式错误的 integrity reports 会阻塞 finalization。
