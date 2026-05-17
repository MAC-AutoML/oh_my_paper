# Reviewer loop protocol: revise until score >= 85

A live run should use multiple role agents or model calls:

| Role | Responsibility |
| --- | --- |
| Orchestrator | Maintains paper state and decides which section to revise. |
| Idea selector | Extracts candidate directions from user material. |
| Section writer | Writes one section from a contract and evidence map. |
| Citation auditor | Checks whether representative citations support the paper context. |
| Critic | Finds unsupported claims and weak logic. |
| Reviewer | Scores the paper/section and returns required revisions. |
| Figure planner | Converts final claims into imagegen prompts. |
| LaTeX packager | Copies the built-in template and compiles when TeX tools exist. |

## Loop

1. Write or revise a section.
2. Reviewer returns JSON: `score`, `verdict`, `blocking_issues`, `required_revisions`, `citation_gaps`.
3. If `score < 85`, create a revision brief and return to the responsible section writer.
4. If any revision creates a new unsupported claim, send it back to critic before reviewer scoring.
5. Stop when score is at least 85 or max rounds is reached; if max rounds is reached, mark the artifact as not accepted.

## Example trajectory

```json
[
  {"round": 1, "score": 72, "verdict": "major_revision", "reason": "method loop unclear and citations missing"},
  {"round": 2, "score": 81, "verdict": "minor_revision", "reason": "figure workflow under-specified"},
  {"round": 3, "score": 87, "verdict": "accept_demo", "reason": "claims, citations, caveats, and workflow are aligned"}
]
```
