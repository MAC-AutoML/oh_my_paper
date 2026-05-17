# Academic Pipeline guide

This guide connects research, writing, review, revision, and integrity closure.

1. Treat the pipeline as stage orchestration, not as a generic chat prompt.
2. Stage 1 produces research scope, material passport, and citation candidates.
3. Stage 2 produces literature corpus, claims, evidence map, and research brief.
4. Stage 2.5 is an integrity gate before polished writing.
5. Stage 3 produces the full paper draft and section artifacts.
6. Stage 4 runs strict reviewer simulation and revision planning.
7. Stage 4.5 checks whether suspected issues were cleared or explicitly overridden.
8. Stage 5 finalizes summary, repro lock, and publish-ready handoff notes.
9. The writing lane should not see hidden rubrics or gold scoring data.
10. The reviewer lane should receive enough evidence to critique, but not be softened by author intent.
11. Every stage should record inputs, outputs, status, and blockers.
12. Semantic Scholar mode should be recorded as api_key, no_key, disabled, or auto-resolved.
13. Rate limits should be visible and should not become verified citations.
14. Missing credentials should degrade to no-key or disabled mode according to config.
15. A repro lock documents configuration and limitations; it is not a byte-level replay guarantee.
16. Config snapshots must redact secrets and show only presence flags.
17. Private raw materials and temporary runs stay outside packaged skill content.
18. The pipeline may resume from existing artifacts when their required hashes or timestamps are coherent.
19. If a required artifact is missing, report the next stage rather than pretending completion.
20. If review fails, route back to writing with required fixes.
21. If integrity fails, block finalization unless an explicit manual override exists.
22. Manual overrides require reason, actor, timestamp, and affected issue id.
23. The summary should distinguish completed, skipped, blocked, and not-run work.
24. Exact cost guarantees are out of scope; rough call counts may be logged.
25. The pipeline's purpose is to make AI assistance auditable and less likely to corrupt scholarship.
