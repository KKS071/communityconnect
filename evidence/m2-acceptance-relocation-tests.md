# Milestone 2 — S-6 Acceptance-Test Relocation: Successful Test Evidence

**Project:** CommunityConnect  
**Story:** S-6 — Scheduled Monthly Dues Payments  
**Acceptance Criteria:** AC-18 through AC-22  
**Patches:** AGENT-10 and AGENT-11  
**Execution:** Human-run commands in the local WSL environment  
**Status:** PASS — acceptance tests, full regression suite and coverage

## 1. Environment

- Repository: `KKS071/communityconnect`
- Working directory: `/home/garsande/CommunityConnect`
- Operating system: Linux under WSL
- Python: 3.12.3
- pytest: 9.2.0
- pytest-cov: 7.1.0
- Hypothesis: 6.170.15
- Database: PostgreSQL test environment

## 2. Acceptance-Test Collection

Command:

`python -m pytest --collect-only -q tests/acceptance`

**Result: 5 tests collected in 0.45 seconds.**

Collected tests:

1. `test_ac18_schedule_shown_on_payments_page`
2. `test_ac19_due_day_charges_exactly_once`
3. `test_ac20_restart_mid_run_keeps_one_payment`
4. `test_ac21_manual_payment_prevents_scheduled_charge`
5. `test_ac22_declined_charge_retried_after_delay`

All five tests were collected from `tests/acceptance/test_s6_acceptance.py`.

## 3. Acceptance-Test Execution

Command:

`python -m pytest tests/acceptance -v`

| Acceptance criterion | Result |
|---|---|
| AC-18 — Schedule shown on payments page | PASSED |
| AC-19 — Due-day charge exactly once | PASSED |
| AC-20 — Restart maintains one payment | PASSED |
| AC-21 — Manual payment prevents scheduled charge | PASSED |
| AC-22 — Declined payment retried after delay | PASSED |

**Observed pytest summary:**

`5 passed, 1 warning in 13.02s`

No failures, errors, skips or xfails.

## 4. Full Regression Suite

Command:

`python -m pytest`

**Observed pytest summary:**

`197 passed, 1 warning in 415.98s (0:06:55)`

The complete suite included the relocated S-6 acceptance tests, S-1 tests and remaining S-6 regression tests.

The test count remained 197 following the relocation.

## 5. Branch-Aware Coverage

Command:

`python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80`

| Metric | Observed result |
|---|---:|
| Statements | 428 |
| Missed statements | 20 |
| Branches | 146 |
| Partial branches | 13 |
| Displayed coverage | 94% |
| Exact total coverage | 93.55% |
| Required coverage | 80% |
| Full-suite tests passed | 197 |

**Observed coverage result:**

`Required test coverage of 80% reached. Total coverage: 93.55%`

**Observed pytest summary:**

`197 passed, 1 warning in 458.07s (0:07:38)`

The required coverage threshold was exceeded by 13.55 percentage points.

## 6. Warning

All three test executions reported one `StarletteDeprecationWarning` originating from `fastapi/testclient.py`, concerning deprecated `httpx` usage with `starlette.testclient`.

This warning did not cause any test failures or prevent the coverage threshold from being met.

## 7. Change Verification

The acceptance-test relocation was prepared in:

`agent-patches/AGENT-10-S6-acceptance-organization.patch`

The documentation synchronization was prepared in:

`agent-patches/AGENT-11-S6-acceptance-docs.patch`

The acceptance tests were moved into `tests/acceptance/` while preserving their expected values. The remaining regression tests were retained in `tests/test_s6_payments.py`.

A documentation search for old S-6 acceptance-test paths returned no matches.

## 8. Outstanding Milestone 2 Requirements

- Historical red-run evidence has not yet been captured.
- Acceptance-test edit-denial rules have not yet been verified.
- The `m2-tests-locked` tag has not yet been created.
- Reviewer-subagent configuration conflict remains to be resolved.
- Final commit SHA is pending.

## 9. Evidence Integrity Statement

The test results in this document are transcribed from terminal output supplied by the human reviewer.

Claude Code prepared the changes but did not execute the reported tests.

The acceptance tests and full regression suite passed after the AGENT-10 relocation. These results demonstrate successful testing of the relocated suite; they do not establish that the Milestone 2 acceptance-test locking requirements have been completed.

**Final result: PASS — 5/5 acceptance tests, 197/197 total tests, 93.55% branch-aware coverage.**