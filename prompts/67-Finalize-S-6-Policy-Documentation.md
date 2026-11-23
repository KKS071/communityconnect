# Prompt 67 — Finalize S-6 Policy Documentation

The human reviewer has approved OQ1–OQ5, and the AGENT-04 patch has been applied.

The following additional settings have been approved by the human reviewer:
- RETRY_DELAY_DAYS = 3 calendar days.
- MAX_PAYMENT_ATTEMPTS = 2 total attempts.
- DUES_AMOUNT_CENTS = 18500 for Mountain Ridge demonstration data only, not an interview-confirmed amount.

Prepare one minimal unified patch that:
1. Records these approved settings and their human-decision source in docs/design/S-6.md.
2. Reconciles stale references to OQ1–OQ5 in D8, D26, D27, D34, D35 and section 2, without changing behavior.
3. Corrects the statement implying Prompt 65 itself was the approval. The human approved the decisions before Prompt 65; Claude verified them afterward.
4. Leaves section 9 test paths unchanged until tests are actually moved.
5. Does not change acceptance criteria, application code, or tests.

Save the proposed patch to agent-patches/AGENT-05-S6-policy-finalization.patch.

Do not apply the patch, modify tracked files, run commands, commit, or push. Stop for human approval.