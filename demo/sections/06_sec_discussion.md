# 5. Discussion

## Section contract

- Reader question: Explain what the workflow teaches about reliable academic generation.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Citation status: representative references are included for field positioning; synthetic values remain non-empirical.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

The most important observation is that long academic writing needs governance. Without an explicit loop, the model can produce a polished but unsupported section. With a loop, each section must declare what question it answers, what evidence it has, what citations are representative, and what remains uncertain. This is especially important for benchmark papers because benchmark claims often sound authoritative even when the dataset or protocol is only proposed.

The reviewer threshold also changes the behavior of the system. If the acceptance target is 85, the first draft is expected to fail unless it already has clear claims, evidence boundaries, citations, figures, and limitations. Failure is not treated as a dead end; it becomes a revision brief. This mirrors software testing: a failing review identifies the next patch.

Finally, image generation and LaTeX compilation are separated from scientific evidence. A figure prompt can make the story easier to understand, and a template can make the paper look submission-ready, but neither creates evidence. Captions, citations, and audit notes must still point back to claims, tables, protocols, or source material.
