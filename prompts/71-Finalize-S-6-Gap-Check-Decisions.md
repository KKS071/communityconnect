# Prompt 71 — Finalize S-6 Gap Check Decisions

The human has reviewed the Gap Check 2 triage and approves the following proposed decisions:

1. AC-18: Amend the acceptance criterion to verify the JSON API response rather than literal UI display text. The response must show method = "ach", day_of_month = 5, and active = true. Record this as a human-approved acceptance-criterion change, not as a pass against the original wording.

2. ACH token: For the FakeProcessor-based demonstration, an opaque test token is acceptable. The existing pm_card_visa test token does not represent a real bank account. Do not claim real ACH settlement is implemented.

3. ACH scope: Creating and viewing ACH schedules is in scope. Automatic ACH charging and settlement are deferred.

4. Future-month payments: Clarify D9 so a month without Payment records returns an empty list. Do not change existing code behavior.

5. Replay counting: Document the existing behavior and any limitation. Do not claim a defect is fixed without a test.

6. Remaining documentation ambiguities: Propose minimal clarifications based on existing verified behavior. Do not introduce new features.

7. Deferred Stripe, concurrency, token-security, and manual-payment authorization concerns must remain explicit limitations or risks.

Read:
- docs/design/S-6.md
- docs/requirements/backlog.md
- docs/design/S-6-gap-check-2.md
- Existing relevant code and tests as needed

Prepare:
- A proposed patch for documentation only.
- A concise Gap Check 2 triage summary suitable for MILESTONE2.md.
- A list of remaining unresolved issues.

Write the patch only to:
agent-patches/AGENT-07-S6-final-decisions.patch

Do not modify tracked files.
Do not apply patches.
Do not change code or tests.
Do not run commands.
Do not commit, tag, or push.

Return the proposed changes and stop for human review.

The human explicitly approved all recommended Gap Check 2 decisions on November 23, 2026.

AGENT-06 has already been applied and verified, if confirmed by the human's checks. Do not recreate its changes.

Record AC-18's change from literal display text to API JSON fields as a human-approved acceptance-criterion amendment.

Keep the existing test-token demonstration separate from real ACH bank-account support.

Ensure the proposed AGENT-07 patch applies against the current working tree, including AGENT-06 changes.

Do not modify tracked files, apply patches, run tests, commit, tag, or push.

Return the proposed patch and any remaining unresolved issues for human review.