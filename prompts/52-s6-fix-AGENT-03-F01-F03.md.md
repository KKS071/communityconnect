Task: AGENT-03 F-02 — Implement Approved Paid-Payment Guard

The F-02 investigation is complete. I approve the minimal fix and regression-test preparation.

Read AGENTS.md, CLAUDE.md, app/payments.py, app/db.py, tests/test_s6_payments.py, and the current S-6 design.

Implement the following in the proposed patch:

1. In the due-schedule loop of `run_due_payments()`, call `db.has_paid_payment(unit_id, billing_month)` before `db.latest_payment()`.

2. If any Paid payment exists, increment `skipped` and continue without creating a Payment or calling FakeProcessor.

3. Preserve the existing handling of Pending and Failed payments. Do not implement AC-22 retries.

4. Add focused regression tests:
   - T1: Earlier Paid(1), later Failed(2) → no processor call, no new payment, skipped = 1.
   - T2: Paid + Pending → no new processor call, Pending remains unchanged, skipped = 1 under the current D26/OQ5 behavior.
   - T3: Failed attempt followed by manual Paid → no charge, skipped = 1.
   - T4: Previously Paid month processed again → skipped = 1.
   - T5: Paid in November does not block December's eligible charge.
   - T6: Paid for one unit does not block another unit's eligible charge.

Use existing test fixtures and approved test database conventions. If direct SQL test setup violates AGENTS.md, stop and explain the alternative.

Only these source files are approved:
- app/payments.py
- tests/test_s6_payments.py

Do not modify existing acceptance-test assertions, expected values, or constants.

Do not change app/db.py, app/main.py, documentation, AGENTS.md, CLAUDE.md, settings, or LEDGER.md.

Do not implement F-01, AC-22, or other findings.

Follow the current restricted patch-generation workflow. Create a new unified patch at:

`agent-patches/AGENT-03-F02-paid-guard.patch`

The patch must apply to the current repository HEAD.

Do not apply the patch, run tests, commit, or push.

Report the exact files changed, tests added, expected behavior, and remaining risks.

Stop for human review.