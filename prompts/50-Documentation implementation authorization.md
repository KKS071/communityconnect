# Prompt 50: Documentation implementation authorization

I approve the AGENT-03 F-23/F-06 documentation decisions DR-1, DR-2, DR-2a, DR-ACH, DR-3, DR-4, DR-5, and DR-6, including the documented temporary ACH limitation.

Human Git verification of F-06 has already been completed:

```bash
git diff e7f9eaa 6b1317f -- tests/test_s6_payments.py
git log --oneline -- tests/test_s6_payments.py
```

The diff showed only the new `s6_schedule` fixture, removal of the AC-18 skip marker, test parameter change, and `s6 = s6_schedule` alias. Existing assertions, expected values, and constants were unchanged.

You are authorized to prepare and apply documentation changes ONLY to:

1. `docs/design/S-6.md`
2. `docs/reviews/S-6-AGENT-03-design-resolution.md`

Use the latest corrected proposal.

Record F-06 verification as PASSED and document the historical scope exception. Record the approved design decisions.

Keep the ACH operational limitation explicit. Ensure R4 covers only eligible initial attempt-1 creation and D25 includes the Pending-after-replay branch. Preserve all requirements outside the approved amendments.

Before editing, inspect the current branch and working tree using permitted commands. If Git access is denied, ask me to verify them. Do not edit on `main`.

Do not modify `app/`, `tests/`, `LEDGER.md`, `AGENTS.md`, or any other files.

Do not implement AC-22 or address F-25.

After editing, show the complete diff for human review and stop.

Do not commit or push until separately authorized. If editing is denied by project permissions, provide a patch for human application. Do not bypass restrictions.