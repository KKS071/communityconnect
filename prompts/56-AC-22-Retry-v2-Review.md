# Prompt 56 — AC-22 Retry v2: Approved Review Corrections

The AC-22 patch and independent reviewer findings have been reviewed.

Prepare `agent-patches/AGENT-03-AC22-retry-v2.patch`.

The original patch must remain unchanged.

## Approved decisions

1. Explicitly use READ COMMITTED isolation in the unit-row-locking transactions for scheduled claims and manual payments. Preserve the existing transaction and lock behavior.

2. When a processor returns a result but `finish_payment()` cannot update the Pending row, read the stored payment status. If it disagrees with the processor result, raise an exception and stop the run without overwriting the stored row. If it agrees, leave the row unchanged and do not count another completion. Add regression tests.

3. Reword S-6 documentation so it describes the proposed implementation and unskipped tests without claiming tests have already passed.

4. Add `failed_on` to the §5 Payment data table. Keep `create_manual_payment()` using `RETURNING *` for this change.

5. Keep `finish_payment(..., failed_on=None)` compatible with legacy tests. Ensure production code always supplies the actual run date when recording Failed.

## Required reviewer corrections

- Add a regression test using a nondefault RETRY_DELAY_DAYS.
- Add a late catch-up retry test.
- Add direct `db.claim_pending_payment()` tests for maximum-attempt rejection, skipped attempt numbers, and missing retry arguments.
- Add a conflicting processor-result test.
- Add appropriate settings assumptions to tests that depend on retry availability.
- Correct the F-11/D16 comment and document the conflicting-completion behavior.
- Preserve all existing acceptance-test assertions and remove only the AC-22 skip marker.

## Additional safeguards

Verify that READ COMMITTED is established before the relevant transaction's first query.

Preserve the existing unit-row lock, Paid/Pending checks, idempotency keys, retry timing, migration, manual-payment protection and ACH exclusion.

Do not change unrelated application behavior or resolve OQ2, OQ3 or OQ5.

## Approved file scope

- `app/settings.py`
- `app/db.py`
- `app/payments.py`
- `tests/test_s6_payments.py`
- `docs/design/S-6.md`

## Restrictions

Patch-only workflow. Do not directly modify application files, apply the patch, run tests, commit, push, or edit LEDGER.md or prompts/.

Review the complete v2 patch for consistency and report its exact test count, changed files, remaining risks, and human verification commands.

Stop for human approval.