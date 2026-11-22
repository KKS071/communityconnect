# Prompt 54 — AC-22 Retry Implementation: Investigation and Plan

Investigate implementation of AC-22 for CommunityConnect S-6 scheduled payments.

Read AGENTS.md, CLAUDE.md, docs/design/S-6.md, the current committed application code, and tests/test_s6_payments.py.

Current baseline: F-01 through F-05 and F-25 are implemented. The human-run full suite reported 169 passed and 1 skipped. AC-22 is the remaining skipped acceptance test.

## Required behavior

Implement only the documented retry policy:

- A declined scheduled charge becomes Failed.
- No new attempt is created before RETRY_DELAY_DAYS.
- On the first eligible run, create exactly one next attempt.
- Never exceed MAX_PAYMENT_ATTEMPTS.
- Use a distinct idempotency key for each attempt.
- Persist each attempt as Pending before calling the processor.
- Recover interrupted Pending attempts with their original key and amount.
- A Paid payment prevents further charges.
- Preserve manual-payment protection and the F-01/F-02/F-03 remediations.
- ACH automatic charging remains excluded pending OQ2.
- Preserve the D32 single-runner limitation.

## Investigation requirements

1. Verify how RETRY_DELAY_DAYS and MAX_PAYMENT_ATTEMPTS should be defined in app/settings.py.
2. Examine how the system can reliably record the date on which an attempt becomes Failed.
3. Determine whether the existing database schema supports D17 or whether an additional field is required.
4. Explain how to perform an atomic check-and-insert for retry attempts without reintroducing F-01 concurrency risks.
5. Explain how retry eligibility interacts with Pending replay, manual Paid payments, and the maximum-attempt limit.
6. Identify any ambiguity requiring a design decision before implementation.
7. Propose focused regression tests for early retries, eligible retries, exhausted attempts, crash recovery, and manual-payment interference.

Do not weaken or modify existing acceptance-test assertions.

The AC-22 skip marker may be removed only after implementation is approved and the acceptance test passes.

## Output

Provide:
- Current implementation gaps.
- Recommended minimal design.
- Exact files requiring changes.
- Database migration implications, if any.
- Proposed test cases.
- Remaining risks and open questions.

Do not modify files, generate a patch, run tests, commit, or push.

Stop for human approval before implementation.