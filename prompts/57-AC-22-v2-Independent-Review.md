# Prompt 57 — AC-22 v2 Final Independent Review

Review `agent-patches/AGENT-03-AC22-retry-v2.patch` against the current committed CommunityConnect baseline.

This is a read-only review. Do not modify files, rewrite the patch, apply it, run tests, commit, or push.

Use three independent reviewers:

1. **security-reviewer:** Verify transaction isolation, payment-state integrity, conflicting processor results, Paid/Pending protection, idempotency, and retry concurrency assumptions.

2. **test-analyst:** Verify AC-22 assertions remain unchanged, the skip marker is removed, the new tests cover the eight approved corrections, and the predicted test counts are consistent.

3. **code-reviewer:** Verify the complete patch applies conceptually against the baseline, touches only the five approved files, preserves existing functionality, and correctly documents the new database field and migration.

Pay special attention to:

- Whether `connect_read_committed()` establishes isolation before the first database query.
- Whether `finish_payment()` and `payment_status()` correctly distinguish agreeing and conflicting completions.
- Whether retry eligibility is rechecked under the unit-row lock.
- Whether a failed Pending replay starts its retry delay on the actual failure date.
- Whether the migration is safe for existing records and repeatable.
- Whether the §5 documentation hunk has sufficient context to apply reliably.
- Whether all tests are isolated from processor state and settings overrides.
- Whether the patch introduces any new requirement beyond the approved AC-22 scope.

Classify findings as BLOCKER, SHOULD FIX, or ACCEPTABLE.

Report the exact affected code and recommended corrections for every finding.

Do not assume the tests pass merely because the patch appears correct.

Stop and return the combined report for human approval.