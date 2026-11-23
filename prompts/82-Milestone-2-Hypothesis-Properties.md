# Prompt 82 — Milestone 2 Hypothesis Property-Based Testing

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-16

Mode: PATCH PREPARATION ONLY

## Objective

Prepare exactly two new Hypothesis property-based tests for existing S-6 payment behavior.

Baseline:
- Refactor commit: `35df1d9`
- GREEN tag: `m2-green`
- Acceptance-test lock: `m2-tests-locked`
- Current full suite: 197 passing tests
- Branch-aware coverage: 94.34%

## Step 1 — Inspect

Read:
- `AGENTS.md`
- `CLAUDE.md`
- `app/payments.py`
- `app/db.py`
- `app/settings.py`
- `tests/test_s6_payments.py`
- `tests/conftest.py` (read-only)
- `tests/acceptance/test_s6_acceptance.py` (read-only)
- `LEDGER.md`

Identify existing test fixtures, payment APIs and deterministic test setup.

Do not assume that a fixture or function exists without checking.

## Step 2 — Design two properties

Property 1 — Payment idempotency

For valid generated payment schedules and dates, running the payment processor repeatedly for the same billing period must not create duplicate successful payments or duplicate processor charges.

Property 2 — Retry timing

For generated valid retry-delay values and dates, a failed payment must not be retried before the configured delay, and must be eligible for exactly one retry when the delay has elapsed, subject to the existing maximum-attempts policy.

Use the actual existing implementation and documented business rules. If either property is too broad or conflicts with the current contract, narrow it and explain why.

## Step 3 — Testing constraints

- Use Hypothesis `@given` and suitable strategies.
- Generate only valid domain inputs.
- Keep test execution deterministic where practical.
- Use bounded examples, such as `@settings(max_examples=10, deadline=None)`, to control runtime.
- Assert externally observable behavior, not implementation details.
- Avoid arbitrary sleeps or real network calls.
- Reuse existing fixtures and public APIs.
- Do not change production code.
- Do not change existing tests.
- Do not modify the five locked acceptance tests.
- Do not alter pytest configuration.
- Do not introduce additional dependencies unless already installed.

## Step 4 — Patch preparation

Create a patch that adds one new test file:

`tests/test_s6_properties.py`

Save the patch as:

`agent-patches/AGENT-16-M2-hypothesis-properties.patch`

The patch must contain exactly two property-based test functions.

Do not apply the patch.

Do not run tests.

Do not modify the ledger or evidence files.

Do not commit, push or tag.

## Step 5 — Review

Explain:
1. The invariant tested by each property.
2. The generated input ranges.
3. How test isolation is maintained between Hypothesis examples.
4. Why the assertions are meaningful.
5. Whether the properties overlap with existing tests.
6. Estimated execution cost.
7. Potential flaky behavior.
8. Exact commands for human review, patch application and testing.

## Step 6 — Verification plan

Recommend:
- `git apply --check`
- `git diff --check`
- Focused Hypothesis test execution
- Full suite with branch-aware coverage
- Protected-file integrity comparison against `m2-tests-locked`

Human execution must capture raw output in:

`evidence/properties.txt`

## Required output

Use these headings:

1. Property 1 — Idempotency
2. Property 2 — Retry Timing
3. Generated Inputs
4. Test Isolation
5. Patch Details
6. Risks and Runtime
7. Human Verification Commands
8. Final Recommendation

Stop after preparing the patch and wait for human approval.