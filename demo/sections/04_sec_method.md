# 3. Method

## Section contract

- Reader question: Describe the actual workflow: candidate extraction, reviewer selection, multi-agent section writing, and score-gated revision.
- Evidence status: demo/synthetic unless explicitly grounded in the input material.
- Revision rule: a reviewer score below 85 must create another revision brief.

## Final revised section

The workflow begins with structured intake. The user material is converted into a compact input card containing topic, candidate claims, evidence status, forbidden overclaims, target venue style, and desired outputs. From this card, an idea agent proposes several paper directions. For the PPO-oriented demo, plausible directions include a reliability benchmark, a tutorial survey, a reproduction protocol, and a robustness checklist. A reviewer model then scores these directions for novelty, feasibility, evidence fit, and risk. The selected direction becomes the paper contract.

After selection, the writing loop operates section by section. A planner produces a section contract with a reader question, section job, claim IDs, paragraph messages, required evidence, and caveats. A drafting agent writes the section from that contract. A critic agent audits unsupported claims, paragraph drift, weak transitions, and missing caveats. A revision agent rewrites the section. The loop can repeat until the reviewer score reaches the configured acceptance target, which is 85 in this demo protocol.

The reviewer is not merely a grammar checker. It returns a structured score with dimensions for problem framing, evidence discipline, method clarity, experiment credibility, figure usefulness, limitations, and overall readiness. If the score is below threshold, the orchestrator creates a revision brief and sends it back to the relevant owner skill. This makes the flow closer to a small research team than to a one-shot prompt.

Figures follow a separate path. The figure agent reads the latest section claims and writes figure intent cards. Each card becomes a prompt for Codex imagegen. Deterministic SVG previews may exist for reproducibility, but generated paper figures should be produced through imagegen and then audited for text accuracy, unsupported values, and caption alignment.
