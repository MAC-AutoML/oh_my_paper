# Long-form iterative writing protocol

Use this reference whenever a paper section, full paper, or long demo output must be generated. The core rule is simple: long academic writing is a controlled iteration process, not a single completion.

## Mandatory section loop

For each major section, record or mentally execute six passes:

| Pass | Output | Purpose |
| --- | --- | --- |
| 1. Section contract | reader question, section job, claim IDs, evidence status | prevents generic prose |
| 2. Paragraph plan | paragraph messages and transitions | enforces one-message-per-paragraph |
| 3. Draft | full prose | turns the plan into text |
| 4. Critique | unsupported claims, missing evidence, flow gaps | catches AI overconfidence |
| 5. Revision | improved prose | resolves critique rather than adding polish only |
| 6. Rationale note | Chinese explanation of why written this way | makes the system explainable |

The section is not complete until pass 5 resolves pass 4 or explicitly marks unresolved issues as caveats/future work.

## Section contract template

```markdown
## <Section name> contract
Reader question:
Section job:
Main claim:
Claim IDs:
Evidence available:
Evidence missing:
Paragraph plan:
- P1 message:
- P2 message:
- P3 message:
Figure/table dependency:
Caveats:
Stop condition:
```

## Critique checklist

Ask these questions before finalizing each section:

1. Does the first paragraph answer why this section exists?
2. Does each paragraph have exactly one message?
3. Are numerical claims source-supported, synthetic, or proposed?
4. Are benchmark/design claims later evaluated or caveated?
5. Does the section prepare the next section?
6. Does it avoid author-process narration unless process is the contribution?
7. Does the Chinese rationale explain why the structure is necessary?

## Long-paper control

For a full paper, use a global loop plus section loops:

1. Candidate direction extraction from the user's material.
2. Reviewer-model selection of the strongest direction; use the configured Gemini-compatible reviewer if available.
3. Global thesis and contribution check for the selected direction.
4. Section contracts for all major sections.
5. Section drafts using contracts.
6. Reviewer score pass.
7. Cross-section critique: repeated claims, missing loops, unsupported evidence, inconsistent terminology.
8. Full-paper revision.
9. Repeat score/critique/revision until score is at least 85 or the maximum round limit is reached.
10. Figure/table prompt generation from final claims.
11. Final rationale and integrity note.

## Reviewer threshold loop

Use this loop for live API-backed writing:

```text
draft -> reviewer score -> if score < 85: revision brief -> revise -> reviewer score
```

The reviewer should return structured output with `score`, `verdict`, `blocking_issues`, and `required_revisions`. A low score is not a failure of the workflow; it is the next revision input.

## Figure integration

Do not create a figure because a section “needs a figure.” Create it only when it reduces reviewer effort. The writing loop should produce figure intents first:

```markdown
Figure intent:
Claim supported:
Reader takeaway:
Required labels/data:
Caption claim:
Image-generation prompt needed: yes/no
Audit risk:
```

Then hand the figure intent to `paper-ai-figures` or Codex `imagegen` for raster generation.
