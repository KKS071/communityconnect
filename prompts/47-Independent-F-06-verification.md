# Prompt 47 - Independent F-06 verification and first design correction

Continue AGENT-03 retrospective remediation for F-23 and F-06.

Review the previous design-resolution proposal.

**F-06 verification:** If project permissions allow read-only Git commands, inspect:

```bash
git diff e7f9eaa 6b1317f -- tests/test_s6_payments.py
git log --oneline -- tests/test_s6_payments.py
```

Confirm whether existing assertions and expected values were preserved. If Git inspection is blocked, report the commands for human execution. Do not bypass restrictions.

**F-23 corrections:**

1. Correct R4 to distinguish initial attempt 1 from later retries governed by R5/D17/D25.
2. Do not claim AC-22 is implemented.
3. Ensure D18 defines due/catch-up timing without contradicting D25.
4. Document ACH scheduling as available but automatic ACH charging as deferred pending OQ2.
5. Confirm DR-3, DR-4, and DR-5 match existing behavior.

Prepare exact proposed changes to `docs/design/S-6.md` and `docs/reviews/S-6-AGENT-03-design-resolution.md`.

PLAN ONLY. No edits, tests, commits, pushes, or LEDGER changes. Stop for approval.
