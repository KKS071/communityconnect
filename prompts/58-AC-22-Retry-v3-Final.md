# Prompt 58 — AC-22 Retry v3 Final Corrections

The three independent reviewers have completed their review of `AGENT-03-AC22-retry-v2.patch`.

Their findings SF-1 through SF-7 have been reviewed. Prepare a complete replacement patch:

`agent-patches/AGENT-03-AC22-retry-v3.patch`

Do not modify or apply v1 or v2.

## Approved decisions

**SF-1 — Conflicting processor result**

Accept this as a documented residual risk under the D32 single-runner assumption.

Do not add a conflict-state table, additional payment status, reconciliation workflow, or other schema changes beyond the approved `failed_on` migration.

Add a concise explanation to D35 that a conflicting completion raises an exception but does not persist a conflict marker. If D32 is violated, a later retry could create a duplicate external charge. Record this as an unresolved risk for the human ledger entry.

**SF-2 — Documentation patch context**

Rewrite the §5 Payment table hunk with sufficient surrounding context so `git apply` can reliably locate it.

**SF-3 — Locking explanation**

Update the Step 1 clarification in `docs/design/S-6.md`:

- Scheduled attempt 1 and retry attempts use the same unit-row lock as manual payments.
- READ COMMITTED is explicitly configured before the first query.
- Preserve the D32 single-runner limitation.

**SF-4 — Test assumptions**

Add `_require_retries()` to the five tests identified by test-analyst.

Ensure test assumptions are explicit and do not introduce hard-coded business-policy values.

**SF-5 — Conflicting completion tests**

Parametrize the existing conflicting-completion test to cover:

1. Stored Failed, processor succeeded.
2. Stored Paid, processor declined.

Both must raise and preserve the stored row.

**SF-6 — Failure-date assertions**

Directly verify that `failed_on` records the date of the run that produced Failed.

Verify that Paid payments retain `failed_on = NULL`.

**SF-7 — Migration repeatability**

Add a regression test that calls `db.init_db()` again after creating an existing Failed payment.

Verify that the existing payment remains intact and subsequent processing behaves correctly.

## Constraints

- Preserve every existing AC-18 through AC-22 acceptance-test assertion.
- Keep AC-22 unskipped.
- Preserve F-01 through F-05 and F-11 protections.
- Preserve D16 counting, D17 retry timing, D25–D27 behavior and D34 ACH exclusion.
- Do not resolve OQ2, OQ3 or OQ5.
- Do not add unrelated features.

Approved files only:

- `app/settings.py`
- `app/db.py`
- `app/payments.py`
- `tests/test_s6_payments.py`
- `docs/design/S-6.md`

## Workflow restrictions

Generate only the new unified v3 patch.

Do not directly modify application files, apply any patch, run tests, commit, push, or edit LEDGER.md or prompts/.

Do not claim tests have passed.

Report:
- Exact changed files.
- Corrections for SF-1 through SF-7.
- Number of new test functions and collected cases.
- Remaining risks.
- Commands for human verification.

Stop for human approval.