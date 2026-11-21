# Prompt 49: Final R4/Pending clarification

Continue AGENT-03 F-23/F-06 documentation planning only.

Correct R4 so it covers only eligible initial attempt-1 creation, without implying that existing Pending or Failed attempts trigger another attempt-1 Payment.

Document D25's existing behavior: if a Pending payment remains unresolved after D26 replay, the run makes no new attempt. Confirm this against `app/payments.py`.

Keep ACH schedules excluded from automatic charging, replay, and RunResult pending OQ2. Explicitly document the operational limitation.

Retain `ValueError` for missing dues and preserve the DR-3 and DR-5 corrections.

Keep F-25 outside scope.

Keep DR-6 conditional until human Git verification is supplied.

Provide the corrected exact documentation diff and decision record.

No edits, tests, commits, or pushes. Stop for human approval.
