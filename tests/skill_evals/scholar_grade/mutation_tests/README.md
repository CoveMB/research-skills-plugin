# Scholar-Grade Mutation Tests

This directory tests evaluator sensitivity, not skill output quality by itself.

`run_mutation_tests.py` starts from selected passing reference outputs in `tests/skill_evals/scholar_grade/outputs/`, copies one output at a time into a temporary mutation directory, applies a deterministic scholarly-error mutation, and runs the existing scholar-grade output harness for the affected fixture.

The mutation cases cover fabricated DOI verification, fabricated page or quote locators, unsupported causal strengthening, unsupported consensus claims, unpermitted external-search verification, missing reliance-limit uncertainty, hidden answer-key leakage, compact output hiding a blocker, and prose repair that changes claim strength without flagging ambiguity.

Passing mutation tests prove only that these known corrupted outputs are rejected by the evaluator for the expected reason or hard-fail class. They do not prove source truth, citation existence, field consensus, real-world retrieval quality, or publication readiness.

Run:

```bash
python3 tests/skill_evals/scholar_grade/mutation_tests/run_mutation_tests.py
python3 scripts/run_package_checks.py --scope scholar-mutation
```
