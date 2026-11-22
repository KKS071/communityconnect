# Prompt 55 — AC-22 Approved Implementation and Regression Tests

The AC-22 investigation in Prompt 54 has been reviewed. Proceed with a restricted, patch-only implementation using the decisions below.

Follow AGENTS.md, CLAUDE.md and docs/design/S-6.md. Preserve all existing S-6 behavior outside the approved retry scope.

## Approved decisions

1. **Failure timestamp:** Add a nullable `payments.failed_on` field. Set it to the `today` argument of the run in which an attempt actually becomes Failed. Do not use the original creation date to calculate the retry delay.

2. **Cross-month behavior:** Do not implement retries for earlier billing months. Preserve D25 and leave OQ3 unresolved. Document the limitation.

3. **Legacy Failed rows:** A Failed payment with `failed_on = NULL` must not be automatically retried.

4. **RunResult:** Preserve D16 counting. Successful retries increment `charged`, declined retries increment `failed`, and waiting or exhausted attempts do not increment `skipped`.

5. **Settings:** Add `RETRY_DELAY_DAYS = 3` and `MAX_PAYMENT_ATTEMPTS = 2` to `app/settings.py` as provisional D15 defaults. Read settings dynamically. Do not introduce undocumented validation rules.

6. **Retry amount:** A newly created retry uses the community dues amount at the time of its creation, as D30 specifies. Replaying an existing Pending retry must use its persisted amount.

7. **Approved files:** `app/settings.py`, `app/db.py`, `app/payments.py`, `tests/test_s6_payments.py`, and `docs/design/S-6.md`.

## Implementation requirements

- Preserve attempt-1 behavior.
- Add retry attempts numbered 2 through MAX_PAYMENT_ATTEMPTS.
- Use distinct idempotency keys in the format `{unit_id}:{billing_month}:{attempt}`.
- Persist each retry as Pending before calling the processor.
- Preserve the original key, amount and attempt number when replaying Pending payments.
- Use the existing unit-row lock to serialize scheduled retries and manual payments.
- Recheck Paid, Pending, latest attempt, retry delay and maximum-attempt eligibility inside the locked transaction.
- Ensure that no retry can be created before the configured delay.
- Never create another attempt after a Paid payment or after the maximum is reached.
- Keep ACH automatic charging excluded pending OQ2.
- Preserve the D32 single-runner assumption.
- Add the F-11 state-transition guard so `finish_payment()` cannot overwrite an already completed payment. Verify compatibility with existing tests.

## Database migration

Add the nullable `failed_on` column and an additive, repeatable migration in `init_db()`.

Preserve existing payment records and avoid destructive schema changes.

Document the schema addition and migration in `docs/design/S-6.md`.

## Tests

Remove only the AC-22 skip marker. Do not modify the acceptance-test assertions.

Add focused regression tests covering:

- No retry before RETRY_DELAY_DAYS.
- Exactly one retry on the eligible date.
- No attempts beyond MAX_PAYMENT_ATTEMPTS.
- Unique idempotency keys.
- Retry success followed by no further charging.
- Failure date measured from the actual decline run.
- Crash recovery during a retry.
- Processor unavailability during a retry.
- Manual payment before a retry.
- Manual payment racing with retry creation.
- Manual payment while a retry is Pending.
- Dues changes between attempts.
- New-month attempt numbering.
- Cross-month retry limitation.
- Legacy Failed rows without failed_on.
- Completed-payment state-transition protection.

Use existing test fixtures and application functions. Do not introduce SQL into the tests.

## Independent review

After preparing the patch, request read-only reviews from security-reviewer, test-analyst and code-reviewer.

Classify findings as BLOCKER, SHOULD FIX or ACCEPTABLE.

## Restrictions

Generate a new unified patch under:

`agent-patches/AGENT-03-AC22-retry.patch`

Do not directly edit approved application files, apply the patch, run tests, commit, push, or modify LEDGER.md or prompts/.

Documentation changes must remain in the patch for human application.

Report the exact changed files, proposed tests, migration effects, remaining risks and human verification commands.

Stop for human approval.