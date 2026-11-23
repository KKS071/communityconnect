**AGENT-20 — Mutation Survivor Analysis (Read-Only)**

Analyze the five surviving mutants from the controlled Milestone 2 mutation-testing experiment.

Evidence:
- `evidence/mutation-baseline.txt`: 25 killed, 5 survived out of 30
- `evidence/mutation-properties.txt`: 25 killed, 5 survived out of the same 30
- Commit: `9474ad4`
- Mutmut: 3.8.1

Survivors:
1. `app.payments.x__count_outcome__mutmut_5`
2. `app.payments.x__count_outcome__mutmut_20`
3. `app.payments.x_run_due_payments__mutmut_89`
4. `app.payments.x_run_due_payments__mutmut_109`
5. `app.payments.x__charge_pending__mutmut_38`

Instructions:

1. Inspect the exact mutant diffs using `mutmut show` and relevant production code.
2. Review the existing regression, acceptance, and Hypothesis tests.
3. Classify each survivor as:
   - Genuine test coverage gap
   - Likely equivalent mutation
   - Redundant/unobservable behavior
   - Uncertain — requires further investigation
4. For each genuine gap, propose a minimal test scenario and expected assertions grounded in existing requirements.
5. Explain why the two Hypothesis properties did not kill these survivors.
6. Identify whether the existing tests already cover the intended business behavior through another code path.
7. Recommend whether to add tests or document the survivor as a limitation.

Constraints:
- READ-ONLY analysis.
- Do not modify production code, tests, configuration, or evidence files.
- Do not execute mutation tests or the full test suite.
- Do not commit or push.
- Do not modify locked acceptance tests.
- Do not assume that every survivor represents a defect.
- Provide exact file and line references for all conclusions.

Return a concise five-row survivor analysis table and prioritized recommendations. Stop after reporting.