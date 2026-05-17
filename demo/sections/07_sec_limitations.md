# 6. Limitations

## Section contract

- Reader question: State what this demo does not prove and what a live API-backed run would add.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

This repository demo is deterministic and offline. It does not call a live Gemini endpoint during committed generation, does not run RL environments, and does not create final raster figures. Instead, it records the prompts and protocols that a live run should execute. This boundary is deliberate: committed demo outputs should be reproducible without secrets or network availability.

A live run would add three elements. First, it would use the configured reviewer model to select among candidate paper ideas. Second, it would iterate section drafts until the reviewer score reaches the configured threshold or a maximum round limit is hit. Third, it would call Codex imagegen to produce bitmap figures and save them with an audit trail.

The demo also does not guarantee that an 85 score means publishability. It means the configured reviewer agent judged the draft acceptable according to the local rubric. Human supervision remains necessary for real claims, real citations, and real submission decisions.
