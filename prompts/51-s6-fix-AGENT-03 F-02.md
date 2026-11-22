**Prompt 1 — F-02 Investigation (Plan Only)**

Investigate AGENT-03 finding F-02 in `run_due_payments()`. Determine whether an earlier Paid payment can be overlooked when `latest_payment()` returns a later Failed or Pending record. Examine the existing payment functions, identify the smallest safe correction, and propose regression tests. Explain the relationship to F-01 concurrency, AC-22 retries, and OQ5. Do not modify files, run tests, or commit. Report findings for human approval.

**Prompt 2 — Approved F-02 Implementation and Regression Tests**

Implement the approved F-02 correction by checking `db.has_paid_payment()` before `db.latest_payment()` in the due-schedule loop. If a Paid payment exists for the unit and billing month, increment `skipped` and do not create another Payment or call the processor.

Preserve existing Pending and Failed behavior. Do not implement AC-22.

Add six regression tests covering:
1. Earlier Paid followed by later Failed.
2. Paid with Pending, preserving the Pending row.
3. Manual Paid after a declined attempt.
4. Repeated processing of an already Paid month.
5. Paid in another billing month.
6. Paid for another unit.

Modify only `app/payments.py` and `tests/test_s6_payments.py`. Preserve existing acceptance-test assertions and constants. Follow the restricted patch-generation workflow. Do not apply changes, run tests, commit, or push. Stop for human review.