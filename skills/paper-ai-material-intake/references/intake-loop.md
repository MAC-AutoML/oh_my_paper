# Material intake loop

1. Stage material under `/temp`.
2. Ingest into `/materials/paper-ai/external/<id>`.
3. Classify by category.
4. Produce public-safe synthesis.
5. Convert synthesis into skill instructions, gates, or synthetic eval fixtures.
6. Verify `git ls-files materials temp` is empty before commit.
