# Prompt 83 — Milestone 2 Mutation Testing Preparation

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-17

Mode: READ-ONLY AUDIT AND PLAN

## Objective

Prepare a controlled mutation-testing plan using mutmut for the S-6 payment implementation.

Baseline:
- Current commit: 1573ae3
- GREEN tag: m2-green
- Acceptance-test lock: m2-tests-locked
- Full suite: 199 passing tests
- Branch-aware coverage: 94.34%
- Hypothesis properties: 2 tests, 20 generated examples

Do not execute mutation testing during this task.

## Step 1 — Inspect

Read:
- AGENTS.md
- CLAUDE.md
- requirements.txt
- pytest.ini
- app/payments.py
- tests/test_s6_payments.py
- tests/test_s6_properties.py
- tests/acceptance/test_s6_acceptance.py (read-only)
- LEDGER.md
- Existing milestone audit and mutation-testing instructions, if present

Determine whether mutmut is installed and compatible with the project's Python 3.12 environment.

Use only read-only commands for inspection.

## Step 2 — Identify mutation targets

Evaluate narrowly scoped mutation candidates in app/payments.py, particularly:
- Payment outcome counting
- Idempotency safeguards
- Retry-delay comparisons
- Maximum-attempt checks

Identify which mutations are likely to be caught by:
1. Existing S-6 regression tests
2. Locked acceptance tests
3. The two new Hypothesis properties

Distinguish test coverage from actual mutation detection.

## Step 3 — Plan the comparison

Propose a reproducible method for comparing:

Baseline A:
Existing regression and acceptance tests, excluding the new Hypothesis property tests.

Baseline B:
The same tests plus the two Hypothesis property tests.

Use the same mutation target and mutant set for both baselines.

Explain how to measure:
- Killed mutants
- Surviving mutants
- Timeout or error mutants
- Mutation score
- Mutants additionally killed by property tests

Do not claim that Hypothesis improves mutation scores until results demonstrate it.

## Step 4 — Control runtime and safety

Mutation testing must:
- Avoid production databases.
- Use the isolated test database.
- Preserve the locked acceptance tests.
- Avoid modifying production source permanently.
- Avoid committing generated mutation artifacts.
- Avoid running the entire test suite for every mutant if a focused selection is sufficient.
- Use a small, reproducible mutant set.
- Avoid concurrent mutation workers if they could interfere with database isolation.

Review mutmut version compatibility and configuration syntax before proposing commands.

## Step 5 — Evidence plan

Prepare commands for capturing raw mutation-testing output in:

- evidence/mutation-baseline.txt
- evidence/mutation-properties.txt

Also propose a concise comparison report identifying which mutants were additionally killed by the Hypothesis tests.

Do not create or modify these evidence files yet.

## Step 6 — Restrictions

Do not:
- Modify production code.
- Modify tests.
- Modify locked acceptance tests.
- Modify requirements.txt.
- Create or edit configuration files.
- Install packages.
- Execute mutation tests.
- Commit, push or create tags.

This is an inspection and planning task only.

## Required output

1. Environment and mutmut Compatibility
2. Recommended Mutation Scope
3. Baseline A — Without Properties
4. Baseline B — With Properties
5. Reproducible Comparison Method
6. Runtime and Database Safety
7. Evidence Files and Reporting
8. Risks and Open Questions
9. Exact Proposed Human Commands
10. Final Recommendation

If mutmut is not installed or compatibility is uncertain, explain what needs approval before proceeding.

Stop after producing the plan. Wait for explicit human approval before executing mutation testing.