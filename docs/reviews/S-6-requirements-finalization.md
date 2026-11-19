# S-6 requirements finalization — Step 1

**Target:** `KKS071/communityconnect` (`main`). **Status:** proposed documentation patch, pending independent human review; not merged or implemented.

## Sources reviewed

| File | Git blob SHA |
| --- | --- |
| `docs/requirements/backlog.md` | `9ab36704b442092a628663f6db8badca6707e23d` |
| `docs/design/S-6.md` | `46b19bc4dff1f7d24269003e1cbc836a66e1b1cb` |
| `docs/requirements/traceability.md` | `22643856a926b4c4ec2e4a4d230f909b1130f167` |
| `docs/design/S-6-gapcheck.md` (read-only) | `1649b44f16117fd7f93e7866972e822cb6201129` |

Also read `tests/test_s6_payments.py`, `AGENTS.md`, and `prompts/17-gapcheck-S-6.md`; no changes proposed to them. The gap check retains its 48 questions, 10 answered and 38 classified real gaps, plus historical provenance.

## Finalized interpretation of the existing acceptance criteria

| AC | Requirement and existing test | Current status |
| --- | --- | --- |
| AC-18 | ACH day-5 schedule shown via `GET .../payment-schedules/mine`, without token in `ScheduleOut`; `test_ac18_schedule_shown_on_payments_page`. No ACH settlement inference (D10, D34). | Skipped |
| AC-19 | Debit fake-processor due run: one `Paid` row for the month at community `DUES_AMOUNT_CENTS`, no duplicate on rerun; `test_ac19_due_day_charges_exactly_once` (R1–R3). | Skipped |
| AC-20 | Persist `Pending` and idempotency key before charging, reuse same key after simulated post-charge exception, end with one `Paid` row; `test_ac20_restart_mid_run_keeps_one_payment` (D4, D29, D31). | Skipped |
| AC-21 | Pre-recorded manual `Paid` suppresses scheduled charge; `test_ac21_manual_payment_prevents_scheduled_charge` (R3, D13, D27). | Skipped |
| AC-22 | Retry after `RETRY_DELAY_DAYS`, subject to `MAX_PAYMENT_ATTEMPTS`, preserving failed attempt; `test_ac22_declined_charge_retried_after_delay` (R5, D15, D17). | Skipped |

**Contract preserved:** Schedule methods `ach`, `debit`, `credit`; token secrecy; day 1–28; existing 401/404/409/422 semantics and role boundaries; UTC dates; integer-cent amounts; PostgreSQL unique idempotency key and at-most-one-`Paid` partial index; one runner at a time; Stripe test mode planned and fake processor used by tests. D1–D34 are unchanged.

**AC-20 evidence limitation:** The existing test simulates a crash but retains the same fake processor object. It does not prove a real process restart or independent processor durability. Improving the test is a separately approved step, not part of this patch.

## Open policy gates

- **OQ1:** Card processing fees — Do not build anything that depends on this. Stop and ask.
- **OQ2:** ACH settlement/return window and `Paid` semantics — Do not build anything that depends on this. Stop and ask.
- **OQ3:** Prior-month arrears — Do not build anything that depends on this. Stop and ask.
- **OQ4:** Board-member payment visibility — Do not build anything that depends on this. Stop and ask.
- **OQ5:** Manual receipt during a `Pending` scheduled charge — Do not build anything that depends on this. Stop and ask.

## Review and implementation gates

Only the three existing documentation files and this new review record are included. No tests, implementation, migrations, gap-check, prompts, ledger, or repository instructions change. The design is lengthy; any course page-limit compliance must be checked separately without dropping rules. S-6 remains unbuilt and its tests remain skipped. A collaborator must inspect the patch, verify the source revisions still match, and record their own approval. No teammate approval or passing payment tests are claimed.
