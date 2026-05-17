# References

Representative citation set for the demo paper:

1. Sutton and Barto (2018) define the reinforcement-learning problem and remain the standard background reference for value functions, policy optimization, and exploration.
2. Schulman et al. (2015) introduce trust-region policy optimization, motivating constrained policy updates before PPO.
3. Schulman et al. (2017) introduce proximal policy optimization, the PPO seed material for this demo.
4. Mnih et al. (2015) establish deep Q-learning on Atari and show how benchmark scores can drive rapid RL progress.
5. Bellemare et al. (2013) describe the Arcade Learning Environment, a canonical benchmark platform for RL evaluation.
6. Machado et al. (2018) revisit ALE evaluation protocols and motivate more careful benchmark methodology.
7. Brockman et al. (2016) introduce OpenAI Gym, making standardized environment APIs central to RL reporting.
8. Lillicrap et al. (2016) propose DDPG, a deterministic actor-critic baseline often compared with policy-gradient methods.
9. Fujimoto et al. (2018) propose TD3, showing how implementation and evaluation details affect continuous-control comparisons.
10. Haarnoja et al. (2018) introduce soft actor-critic, a strong off-policy baseline for stability-oriented discussions.
11. Henderson et al. (2018) show that deep RL results can be fragile across seeds, codebases, and hyperparameters.
12. Agarwal et al. (2021) argue that aggregate point estimates can be statistically misleading in deep RL benchmarks.
13. Cobbe et al. (2019) introduce Procgen to study generalization rather than memorized environment behavior.
14. Dulac-Arnold et al. (2021) summarize challenges for real-world RL, including robustness, safety, and deployment constraints.
15. Amodei et al. (2016) frame concrete AI safety problems that motivate robust and honest evaluation beyond reward maximization.
16. Christiano et al. (2017) connect reinforcement learning with human preferences, highlighting evaluation issues around learned objectives.
17. Ouyang et al. (2022) show instruction-following alignment with human feedback, a modern policy-optimization application context.
18. Bai et al. (2022) discuss constitutional AI and preference-based alignment, reinforcing why policy quality cannot be reduced to one scalar reward.

## Citation note

These references are included to demonstrate expected citation coverage for a PPO/RL evaluation demo. A live paper run should verify metadata with the configured citation checker and replace representative placeholders with the exact works used by the author. The companion `demo/references.bib` file provides BibTeX scaffolding for these entries.
