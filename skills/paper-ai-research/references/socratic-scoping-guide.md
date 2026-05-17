# Socratic scoping guide for research questions

Use this guide when the user has a vague topic, a method-first idea, or uncertainty about what can become a paper. Ask just enough to sharpen the research path; do not turn scoping into an interview loop unless the user explicitly wants guided exploration.

## Six question families

### 1. Clarify concepts

- What do you mean by the key term in this topic?
- Can you give one concrete example and one non-example?
- What is included, and what is outside the scope?

### 2. Probe assumptions

- What are you assuming about the task, model, data, or users?
- Which assumption would most damage the paper if false?
- Who in the field would disagree with this framing?

### 3. Probe evidence

- What evidence do you already have?
- What evidence would convince a skeptical reviewer?
- What evidence would falsify the idea quickly?

### 4. Explore perspectives

- How would a method reviewer frame this differently from an application reviewer?
- What would the closest-work authors say is missing or unfair?
- Does another discipline use a better vocabulary for this problem?

### 5. Trace implications

- If the claim is true, what should future systems, benchmarks, or methods change?
- What practical or scientific decision depends on this result?
- What limitation would still remain after the paper succeeds?

### 6. Question the question

- Is this really the question, or is it a symptom of a deeper evaluation/design problem?
- Is the current question answerable with available evidence?
- Is the contribution filling a gap, changing understanding, or only repackaging a trend?

## Scoping funnel

```text
broad interest
→ concrete phenomenon
→ failure mode or contradiction
→ answerable research question
→ falsifiable hypothesis
→ evidence plan
→ paper contribution
```

## Output pattern

```markdown
## Scoping result
- Current topic:
- Sharpened research question:
- Hypothesis or thesis:
- Why it matters:
- Closest-work pressure:
- Evidence needed:
- Fast falsification test:
- Recommended next skill:
```

## Method-first rewrite

When the user starts with a technique, convert it:

```markdown
Method-first: We use <technique> for <task>.
Problem-first: In <task>, current systems fail when <condition>. This matters because <impact>. We test whether <technique or insight> addresses <failure mode> using <evidence>.
```

## Stop condition

Scoping is complete when the question is specific, answerable, valuable to a target audience, and connected to a plausible evidence path. If one of those is missing, route back to `paper-ai-idea` rather than drafting.
