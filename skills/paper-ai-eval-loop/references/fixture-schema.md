# Eval fixture schema

Canonical executable fixtures live in `tests/fixtures/evals/*.jsonl`.

Each line should include:

- `fixture_id`
- `phase`
- `skill`
- `purpose`
- `input_artifacts`
- `prompt` or action
- `expected`
- `privacy`
- `material_refs`
