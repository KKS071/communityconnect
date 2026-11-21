# Prompt 48:Incorporate human Git verification

Continue AGENT-03 retrospective remediation for F-23 and F-06 only.

The human executed:

```bash
git diff e7f9eaa 6b1317f -- tests/test_s6_payments.py
git log --oneline -- tests/test_s6_payments.py
```

Verified result: The AC-18 diff adds only the `s6_schedule` fixture, removes the skip marker, changes the test parameter, and adds `s6 = s6_schedule`. No existing assertions, expected values, or constants changed.

Update the proposed documentation plan:

1. Record F-06 as Git-verified and recommend ratification as a historical scope exception.
2. Correct R4 for eligible initial attempt-1 creation only.
3. Document the D25 Pending-after-replay branch, provided it matches the current code.
4. Keep automatic ACH charging deferred pending OQ2 and ACH excluded from RunResult.
5. Preserve DR-3, DR-4, and DR-5.
6. Keep F-25 outside scope.

Prepare the exact final proposed diff for:

- `docs/design/S-6.md`
- `docs/reviews/S-6-AGENT-03-design-resolution.md`

PLAN ONLY. Do not edit files, run tests, commit, push, modify LEDGER.md, or implement AC-22.

Stop for human approval.