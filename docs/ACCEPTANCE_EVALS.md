# Acceptance and Evaluation Specification

## 1. Design package acceptance

| Criterion | Check |
| --- | --- |
| Actionable for implementation | A developer can create skill dirs, adapters, scripts, and tests from the docs. |
| Dual-mode boundaries clear | Local and App Server modes have shared semantics and explicit differences. |
| Full paper workflow covered | Idea/results through rebuttal/eval loop has no missing owner. |
| Materials traceable | Each skill maps to local material categories or official architecture refs. |
| Non-goals/risks clear | UI, public materials, one-click paper, all templates are excluded. |
| Future evals executable | Trace, fixture, gate, and evaluator schemas are concrete. |
| Ready for ralplan | Planning docs can drive execution without more interview rounds. |

## 2. MVP local implementation acceptance

1. `uv run pytest` passes.
2. `uv run oh-my-paper init` creates `.paper-ai/` and `paper/` artifacts in a toy workspace.
3. Orchestrator can route at least these phases: research-process, writing, figures, layout, reviewer, rebuttal, eval-loop.
4. Unsupported claims are flagged before final writing/rebuttal outputs.
5. Reviewer simulation produces severity-ranked issues and a fix plan.
6. Rebuttal workflow maps every reviewer concern to answer/evidence/concession.
7. Trace events are written for every phase.
8. Raw `materials/` are not required at runtime and not included in public packaging.

## 3. App Server prototype acceptance

1. A mocked JSON-RPC App Server test can start/resume a thread-like run and map events to `TRACE.jsonl`.
2. File-change or command approval events map to a `GateDecision`.
3. User-input requests map to human gates.
4. Local adapter and App Server adapter share evaluator fixtures.
5. The adapter can run in stdio mode first; WebSocket is treated as experimental.

## 4. Eval fixture acceptance

Each fixture must include:

- `fixture_id`
- `phase`
- `skill`
- `purpose`
- `input_artifacts`
- `prompt` or action
- `expected`
- `privacy`
- `material_refs`

Each evaluator result must include:

- fixture ID;
- pass/fail/warn;
- reasons;
- artifact paths inspected;
- suggested fix or gate.

## 5. Phase-specific eval examples

### Research-process eval

Input: vague project idea and partial results.

Expected:

- produces paper brief;
- separates goal, problem, method, evidence, missing experiment;
- does not pretend missing results exist.

### Writing eval

Input: claims with one unsupported claim.

Expected:

- draft either omits unsupported claim or marks it as limitation/planned evidence;
- gate report names the claim ID.

### Figures eval

Input: result table and paper claim.

Expected:

- recommends visual type;
- states one takeaway;
- drafts caption;
- checks labels/legend/readability.

### Layout eval

Input: target venue/page budget and section/figure list.

Expected:

- estimates page budget;
- flags overflow risk;
- does not claim exact venue compliance when template is missing.

### Reviewer eval

Input: draft missing a baseline.

Expected:

- reviewer report marks missing baseline as severe;
- fix plan prioritizes experiment or limitation framing.

### Rebuttal eval

Input: reviewer asks for an ablation not available.

Expected:

- response does not promise completed ablation;
- suggests available evidence, planned revision, or concession;
- tone remains respectful.

### Trace eval

Input: trace events from toy workflow.

Expected:

- each phase has start/end or equivalent event;
- gate statuses are present;
- outputs list actual artifact paths.

## 6. Manual review checklist

- Are all claims traceable to evidence or caveats?
- Are severe reviewer concerns separated from wording improvements?
- Does rebuttal address the AC, not only individual reviewers?
- Are figure/table recommendations tied to paper story?
- Is private material excluded from tracked outputs?
- Is any future-work promise explicitly approved?
