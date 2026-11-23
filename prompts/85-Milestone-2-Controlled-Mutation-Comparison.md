# Prompt 85 — Milestone 2 Controlled Mutation Comparison

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-19

Mode: READ-ONLY ANALYSIS AND PLAN

## Verified results

Mutmut 3.8.1 successfully generated 603 mutants across app/payments.py and app/db.py.

Nine selected mutants were tested and all nine were killed by the regression and acceptance tests.

The existing source and locked acceptance files remain unchanged.

## Objective

Prepare a controlled mutation-testing comparison using 30 selected mutants.

Compare:
- Baseline A: tests/test_s6_payments.py and tests/acceptance
- Baseline B: the same tests plus tests/test_s6_properties.py

## Requirements

1. Inspect the existing mutant inventory without running mutation tests.
2. Select 30 distinct mutant identifiers from:
   - app.payments._count_outcome
   - app.payments.run_due_payments
   - app.payments._charge_pending
   - app.db._retry_allowed
3. Include the nine previously tested mutants.
4. Include mutations that exercise payment idempotency, outcome counting, retry timing, and attempt limits.
5. Avoid selecting only the earliest mutants in each function.
6. Inspect selected mutants with mutmut show and identify the actual behavioral changes.
7. Explain how the same 30 mutants will be executed under both test configurations.
8. Propose commands to capture raw output, exact mutant statuses, and comparison results.
9. Ensure clean mutation workspaces between baselines.
10. Include database-safety checks before and after each run.

## Evidence

Plan:
- evidence/mutation-baseline.txt
- evidence/mutation-properties.txt

Preserve separate handout-oriented before/after evidence for subsequent test improvements.

## Restrictions

Do not:
- Run mutation tests.
- Modify application or test code.
- Modify locked acceptance files.
- Modify pyproject.toml or requirements.txt.
- Delete mutants/.
- Modify LEDGER.md.
- Commit or push.

## Required output

1. The exact 30 mutant identifiers.
2. Mutation descriptions and why they matter.
3. Baseline A commands.
4. Baseline B commands.
5. Cache-isolation strategy.
6. Expected runtime and database risks.
7. Proposed comparison table.
8. Human approval request.

Stop after preparing the plan.