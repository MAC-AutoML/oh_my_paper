# 5. Discussion

## Section contract

- Reader question: Explain what the workflow teaches about reliable academic generation.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

The most important observation is that long academic writing needs governance. Without an explicit loop, the model can produce a polished but unsupported section. With a loop, each section must declare what question it answers, what evidence it has, and what remains uncertain. This is especially important for benchmark papers because benchmark claims often sound authoritative even when the dataset or protocol is only proposed.

The reviewer threshold also changes the behavior of the system. If the acceptance target is 85, the first draft is expected to fail unless it already has clear claims, evidence boundaries, figures, and limitations. Failure is not treated as a dead end; it becomes a revision brief. This mirrors software testing: a failing review identifies the next patch.

Finally, image generation is separated from scientific evidence. The figure prompt can make the story easier to understand, but it cannot create evidence. The caption and audit must still point back to claims, tables, or protocols.
