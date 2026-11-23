# Prompt 75 — Milestone 2 Acceptance-Test Audit

Project: CommunityConnect — CS690 Milestone 2

Task: Audit the existing S-1 and S-6 acceptance tests before moving them to `tests/acceptance/` and locking them.

**Authorization: READ-ONLY AUDIT ONLY.**

Do not modify tracked files, create patches, move tests, execute tests, change permissions, commit, push, or create Git tags.

## Context

- The S-1 implementation was completed during Milestone 1.
- The S-6 implementation (AC-18 through AC-22) is already merged.
- OQ1–OQ5 have been resolved through human-approved design decisions.
- AC-18 was amended to verify the payment-schedule JSON response for ACH scheduling and display, not automatic ACH charging.
- The human's latest pytest run passed 197 tests.
- The human's latest coverage run passed with 93.55% total coverage.
- AGENT-09 configuration changes have been committed.
- Acceptance tests have not yet been moved or locked.

## Sources to inspect

1. `handout/CS690_Milestone2_Handout.pdf`
2. `AGENTS.md`
3. `CLAUDE.md`
4. `docs/design/S-1.md`
5. `docs/design/S-6.md`
6. `docs/requirements/backlog.md`
7. `docs/requirements/traceability.md`
8. `tests/test_s1_requests.py`
9. `tests/test_s6_payments.py`
10. `pytest.ini`
11. `LEDGER.md`

Read the relevant handout requirements directly. If the handout is unavailable, state that limitation.

Delegate the acceptance-test review to the `test-writer` and `reviewer` subagents in read-only mode, if available. The main agent must reconcile their findings.

## Task 1 — Identify acceptance tests

Identify the existing acceptance tests corresponding to:

- S-1: AC-1 through AC-6
- S-6: AC-18 through AC-22

For each AC, report:

- Story ID
- AC ID
- Test function name
- Current file path
- Design or backlog reference
- Whether the test is collected normally
- Whether it contains skip or xfail markers
- Whether its assertions match the approved AC

Do not assume that all 197 tests are acceptance tests.

## Task 2 — Review test quality

For each acceptance test, determine whether:

1. Expected results are derived from the acceptance criteria rather than implementation behavior.
2. The test verifies observable behavior.
3. Assertions are meaningful and sufficiently specific.
4. Positive, negative, authorization, and boundary conditions are covered where required.
5. Fixtures and setup are appropriate.
6. No test silently weakens or contradicts the AC.
7. The test is independent and repeatable.

For S-6, pay particular attention to:

- AC-18: ACH scheduling and JSON display.
- AC-19: Due-day charging and exactly-once behavior.
- AC-20: Restart and idempotency.
- AC-21: Manual payment preventing duplicate scheduled charges.
- AC-22: Decline, retry delay, and retry limits.

Respect the documented OQ1–OQ5 decisions. Do not invent additional payment policy.

## Task 3 — Identify the safest test organization

Determine which existing tests should move to:

`tests/acceptance/`

Recommend a minimal file layout.

Identify shared fixtures, imports, pytest configuration, and any collection issues that could arise.

Preserve existing test behavior and expected values.

Do not move all 197 tests automatically.

If separating acceptance tests from other tests requires splitting files, explain the smallest safe approach.

## Task 4 — Evaluate red-run evidence

Milestone 2 requires genuine red-run evidence before acceptance-test locking.

Because S-6 implementation is already merged, assess whether a legitimate red run can be reproduced against a pre-implementation commit without altering current `main`.

Identify:

- A suitable historical commit, if verifiable.
- Which acceptance tests should fail against it.
- Whether the tests can run against that historical version.
- Any compatibility or setup issues.
- How the human could capture `evidence/red.txt` honestly.

Do not fabricate a red run.

Do not modify the current implementation or intentionally break tests to manufacture a failure.

If the required historical red/green sequence cannot be reproduced faithfully, identify the limitation for the ledger and Milestone 2 reflection.

## Task 5 — Plan the acceptance-test lock

Propose the sequence for:

1. Human approval of the acceptance-test audit.
2. Preparing a minimal test-organization patch.
3. Human application and review.
4. Running pytest and recording results.
5. Capturing genuine red evidence where feasible.
6. Adding the acceptance-test edit-denial rule to `.claude/settings.json`.
7. Verifying an actual permission denial.
8. Creating `evidence/permission-denied.md`.
9. Creating and pushing the `m2-tests-locked` tag.

Do not perform any of these actions in this prompt.

## Required output

Provide:

**A. Acceptance-Test Inventory**

A table covering all 11 ACs.

**B. Findings**

For each finding, include:
- File and line
- AC ID
- Severity: blocking or minor
- Problem
- Recommended correction

**C. Test Organization Plan**

Exact proposed paths and whether files must be split.

**D. Red-Evidence Feasibility**

Historical commit candidates, compatibility risks, and a truthful evidence-capture plan.

**E. Test-Lock Checklist**

Actions needed before creating `m2-tests-locked`.

**F. Minimal Patch Plan**

List exact files that would change in Prompt 76.

**G. Human Approval Required**

List unresolved decisions.

Do not create or apply any patch.

Do not run commands or tests.

Stop after reporting and wait for human approval.