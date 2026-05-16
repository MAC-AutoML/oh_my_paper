# Harness and Evaluation Loop

## 1. Objective

`oh my paper` should improve from real usage without relying on memory or vague anecdotes. Each workflow run should leave traces, gate decisions, and failure cases that can become regression fixtures.

## 2. Loop

```text
Run workflow → Capture trace → Detect weak output/gate failure → Create fixture → Run evaluator → Patch skill/reference/script → Re-run fixture → Record changelog
```

## 3. Trace schema

Each line in `.paper-ai/TRACE.jsonl` is one event.

```json
{
  "schema_version": "0.1",
  "event_id": "evt_...",
  "timestamp": "2026-05-17T00:00:00+08:00",
  "project_id": "paper_project_slug",
  "runtime": "local-skill|app-server",
  "phase": "writing|figures|layout|reviewer|rebuttal|eval-loop",
  "skill": "paper-ai-writing",
  "action": "draft_section|run_gate|request_approval|write_artifact|run_eval",
  "inputs": ["paper/CLAIMS.md"],
  "outputs": ["paper/draft/introduction.md"],
  "gate": {"name": "evidence", "status": "pass|fail|warn|not_run"},
  "human_decision": {"required": false, "decision": null},
  "summary": "short event summary"
}
```

## 4. Fixture schema

Fixtures should be small, redacted when needed, and phase-specific.

```json
{
  "schema_version": "0.1",
  "fixture_id": "writing_claim_support_001",
  "phase": "writing",
  "skill": "paper-ai-writing",
  "purpose": "unsupported claim should be flagged",
  "input_artifacts": {
    "paper/CLAIMS.md": "...",
    "paper/EVIDENCE_MAP.md": "..."
  },
  "prompt": "Draft the experiment paragraph.",
  "expected": {
    "must_flag_claim_ids": ["C3"],
    "must_not_invent_results": true,
    "required_outputs": ["draft", "gate_report"]
  },
  "material_refs": ["materials/paper-ai/categories/writing.md"],
  "privacy": "synthetic|redacted|private"
}
```

## 5. Evaluator classes

| Evaluator | Purpose | Example pass condition |
| --- | --- | --- |
| `ArtifactCompletenessEval` | Required outputs exist and use schema. | `CLAIMS.md` has claim IDs/statuses. |
| `EvidenceGroundingEval` | Claims cite evidence or caveats. | Unsupported claims are flagged, not embellished. |
| `WritingStructureEval` | Draft follows section goal and paragraph logic. | Abstract includes problem/method/result/impact. |
| `FigureReadabilityEval` | Figure/table plan has takeaway/readability checks. | Every visual has claim link and caption. |
| `ReviewerStrictnessEval` | Reviewer simulation catches major weaknesses. | Missing baseline is marked high severity. |
| `RebuttalSafetyEval` | Responses are grounded and non-combative. | No promised experiment without evidence/approval. |
| `LayoutConstraintEval` | Formatting/page budget constraints are checked. | Page limit and template assumptions stated. |
| `TraceIntegrityEval` | Workflow emitted useful events. | Trace includes phase, skill, inputs, outputs, gate status. |

## 6. Human gates

Human gates are required for:

- keeping an unsupported or partial claim;
- promising new experiments, code, datasets, or major revisions;
- using private/copyrighted material in a public output;
- declaring submission-ready status after severe reviewer findings;
- exporting traces or fixtures that may contain private paper text.

Gate decision schema:

```json
{
  "gate_id": "gate_...",
  "name": "rebuttal_promise",
  "severity": "low|medium|high|blocking",
  "reason": "Response promises a new ablation not present in evidence map.",
  "options": ["approve", "revise", "remove", "mark_as_future_work"],
  "decision": "revise",
  "decider": "human|policy|test",
  "timestamp": "2026-05-17T00:00:00+08:00"
}
```

## 7. Regression workflow

1. Save weak output and minimal inputs as a fixture.
2. Add expected failure/pass criteria.
3. Run current evaluator; confirm failure if this is a bug fixture.
4. Change skill instructions/reference/script.
5. Re-run fixture; require pass before claiming fix.
6. Add changelog note with fixture ID.

## 8. Metrics

- Gate failure rate per phase.
- Unsupported claim count before/after writing pass.
- Reviewer severe issue count before/after fix pass.
- Rebuttal concern coverage percentage.
- Eval pass rate per skill version.
- Number of fixtures created from real user corrections.

## 9. Privacy modes

| Mode | Meaning | Public commit allowed? |
| --- | --- | --- |
| `synthetic` | No real paper data. | Yes. |
| `redacted` | Real structure but anonymized content. | Maybe, after review. |
| `private` | Contains unpublished paper/review text. | No. |

## 10. First eval set

MVP should include at least one synthetic fixture for each:

- unsupported claim detection;
- weak abstract structure;
- unreadable figure/caption plan;
- missing baseline reviewer critique;
- overpromising rebuttal response;
- incomplete trace event.
