# S-6 AGENT-03 design resolution: F-23 and F-06

**Human approval status: APPROVED** on 2026-11-20 by the human reviewer (name to be recorded in LEDGER.md by a human).
**Source:** AGENT-03 retrospective audit of AC-18 to AC-21 (findings F-23, F-06).
**Scope:** documentation only (`docs/design/S-6.md` and this record). No application code, test, LEDGER, or behavior change.
AC-22 (retries) is **not implemented** and is not authorized by this record.
F-25 (stale "not built"/"skipped" wording) is out of scope.

## Decisions (all approved)

| ID | Finding | Decision | Rationale | Matches merged code |
|----|---------|----------|-----------|---------------------|
| DR-1 | F-23a: D18 vs D25 | D18 defines due/catch-up timing only; D25 decides the action for a due schedule. | D18's "while the unit has no Payment" contradicted D17, D25 and R5. | Yes: `app/payments.py:66-78` |
| DR-2 | F-23b: R4 scope | R4 covers only creating attempt 1 for a due `debit`/`credit` schedule whose unit had no Payment for the month when the run reached it. An existing `Paid`, `Pending` or `Failed` Payment never triggers another attempt 1; `Pending` is handled by D26/D25, and `Failed` by R5/D17 (AC-22, not implemented). | Separates the implemented initial charge from replay and from unimplemented retry policy. | Yes: `app/payments.py:73-85` |
| DR-2a | F-23b: D25 Pending case | If the latest attempt is still `Pending` after the D26 replay, the run makes no new attempt. | Documents existing behavior; prevents a second attempt while a charge's result is unknown (D4). | Yes: `app/payments.py:37-38`, `:63-64`, `:77-78` |
| DR-ACH | F-23b: R4 vs ACH | `ach` schedules are excluded from automatic charging, D26 replay and RunResult until OQ2 is answered. They can still be created and shown (AC-18). | OQ2 forbids ACH `Paid` semantics; AC-18 requires ACH scheduling. | Yes: `app/payments.py:55-56`, `:71-72` |
| DR-3 | F-23c: §4 vs D27 | §4 lists `AlreadyPaid`, `PaymentPending`, `ValueError` for `record_manual_payment`. | Editorial alignment with D27. | Yes: `app/payments.py:100-109`, `app/db.py:171-172` |
| DR-4 | F-23d: no dues | Keep `ValueError` when the community has no dues_amount_cents. | D2 forbids an entered amount; `amount_cents` must be > 0. | Yes: `app/db.py:173-174` |
| DR-5 | F-23e/f: §5 vs D30/D32 | `Community.dues_amount_cents` is null until set by `set_dues`. `Payment.amount_cents` is fixed when the Payment is created (D30). | Matches D30, D32's nullable `ALTER TABLE`, and replay of the stored amount. | Yes: `app/db.py:91-92`, `app/seed.py:58-61`, `app/payments.py:57`, `:80-81` |
| DR-6 | F-06: AC-18 fixture | Retroactively approved: the `s6_schedule` fixture added in `6b1317f` stands, with no test change. See "Historical scope exception". | The original `s6` fixture needed `app.processor` and `seed.set_dues`, which did not exist until AC-19. Git verification passed. | n/a |

## F-06 verification evidence

- **Result: PASSED.** Human Git verification completed on 2026-11-20.
- **Commands:** `git diff e7f9eaa 6b1317f -- tests/test_s6_payments.py` and `git log --oneline -- tests/test_s6_payments.py`.
- **Changes found:** the new `s6_schedule` fixture; removal of the AC-18 skip marker; the test parameter change; the `s6 = s6_schedule` alias.
- **Confirmed unchanged:** existing assertions, expected values, and constants.
- **The agent did not run Git.** Shell access is denied by `.claude/settings.json`; the human reviewer performed and reported the verification.
- **Supporting evidence:** `tests/test_s6_payments.py:46-52`, `:66-79`; LEDGER entry 38.

## Historical scope exception (retroactively approved)

The AC-18 commit `6b1317f` changed `tests/test_s6_payments.py`, which was outside the plan §2.1 file list (`app/db.py`, `app/main.py`, `app/clock.py`). The change also went beyond the plan's skip-marker-only test authorization. A human requested the change (LEDGER entry 38) because the shared `s6` fixture needed `app.processor` and `seed.set_dues`, which did not exist until AC-19. Git verification shows that no assertion, expected value or constant changed, so the AGENTS.md rule against weakening tests was not broken. DR-6 retroactively approves this as a one-time scope exception. It is not a precedent: future test-file changes still need separate approval.

## Accepted limitations

1. **ACH:** a unit with an `ach` schedule is never charged by `run_due_payments` until OQ2 is answered. The run creates no Payment, replays none, does not count the schedule in RunResult, and gives no signal. Dues for these units can be recorded only with `record_manual_payment`, and no UI exists (D10). The association must collect ACH dues by other means in the meantime.
2. **Retries:** retries (R5, D17) are specified but not implemented. A `Failed` attempt 1 currently gets no further attempt that month. Retries depend on AC-22, which needs separate approval.
3. **Pending results:** a `Pending` Payment whose processor result is still unavailable blocks new attempts and manual entry (D27) for that month until a later replay settles it.
4. **Manual payments without dues:** a manual payment cannot be recorded for a community without dues set.

## Not changed by this record

F-02 (the Paid check uses only the latest payment), F-08 (RunResult counting) and F-25 (stale wording) are outside this record. The amended D25 text describes the intended order and does not change the code.

## Unresolved questions

1. **ACH reporting:** should excluded `ach` schedules be reported in some form instead of being uncounted? This is deferred and not decided here.

## Approval

- Approved by: human reviewer (name to be recorded in LEDGER.md)
- Date: 2026-11-20
- Decisions approved: DR-1, DR-2, DR-2a, DR-ACH, DR-3, DR-4, DR-5, DR-6
- F-06 Git verification: PASSED (human-performed)
- Historical scope exception: retroactively approved (DR-6)
