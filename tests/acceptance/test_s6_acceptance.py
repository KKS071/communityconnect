"""S-6 acceptance tests, AC-18 to AC-22 (docs/requirements/backlog.md; docs/design/S-6.md).

Moved unchanged from tests/test_s6_payments.py; only the AC-18 comment now cites the amended
criterion. These tests are to be locked at the tag m2-tests-locked: never edit, delete, skip
or weaken them (AGENTS.md). Imports of S-6 modules stay inside the tests. Values come from
app.settings (RETRY_DELAY_DAYS, MAX_PAYMENT_ATTEMPTS; D15). Per D34 the charge tests use
debit schedules, so they settle nothing about ACH (OQ2).
"""

from datetime import date, timedelta

import pytest

from app import settings
from tests.acceptance.s6_support import (  # noqa: F401  (s6 and s6_schedule are fixtures)
    DECLINED_TOKEN, DUE_DAY, DUES_CENTS, MONTH, SimulatedCrash, history, s6, s6_schedule,
    schedule,
)


def test_ac18_schedule_shown_on_payments_page(s6_schedule):
    # AC-18 (amended by human decision, 2026-11-23): R1 schedules payment on day 5 by ACH;
    # the JSON from GET .../mine (D10) shows method "ach", day_of_month 5 and active true.
    s6 = s6_schedule
    resp = schedule(s6, method="ach", day=5)
    assert resp.status_code == 201
    mine = s6.get(f"/communities/{s6.communities['MR']}/payment-schedules/mine", "R1")
    assert mine.status_code == 200
    body = mine.json()
    assert body["method"] == "ach"
    assert body["day_of_month"] == 5
    assert body["active"] is True
    assert body["unit_id"] == s6.units["MR-12"]
    assert "token" not in body  # §5: never returned by the API


def test_ac19_due_day_charges_exactly_once(s6):
    # AC-19: on day 5, with no payment for the month, the run leaves exactly one payment
    # for the month, marked Paid, for Mountain Ridge's DUES_AMOUNT_CENTS.
    from app.payments import run_due_payments

    assert schedule(s6).status_code == 201
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert result.charged == 1
    rows = history(s6)
    assert len(rows) == 1
    assert rows[0]["status"] == "Paid"
    assert rows[0]["billing_month"] == MONTH
    assert rows[0]["amount_cents"] == DUES_CENTS
    run_due_payments(date(2026, 12, DUE_DAY))  # a second run the same day changes nothing
    assert len(history(s6)) == 1


def test_ac20_restart_mid_run_keeps_one_payment(s6):
    # AC-20: the run is interrupted after R1 was charged and restarted; R1's history still
    # shows exactly one payment for the month.
    from app import processor
    from app.payments import run_due_payments

    class CrashAfterCharge(processor.FakeProcessor):
        crash = True

        def charge(self, token, amount_cents, idempotency_key):
            result = super().charge(token, amount_cents, idempotency_key)
            if self.crash:
                raise SimulatedCrash()
            return result

    crashing = CrashAfterCharge()
    processor.set_processor(crashing)
    assert schedule(s6).status_code == 201
    with pytest.raises(SimulatedCrash):
        run_due_payments(date(2026, 12, DUE_DAY))

    crashing.crash = False  # the restarted run, same processor state
    run_due_payments(date(2026, 12, DUE_DAY))
    rows = history(s6)
    assert [r["status"] for r in rows] == ["Paid"]
    keys = {call[2] for call in crashing.calls}
    assert len(keys) == 1  # every call used the same idempotency key (R2, D4)


def test_ac21_manual_payment_prevents_scheduled_charge(s6):
    # AC-21: the manager recorded a check payment for unit 12 this month; on day 5 no
    # scheduled charge is made and the history shows one payment for the month.
    from app.payments import record_manual_payment, run_due_payments

    assert schedule(s6).status_code == 201
    record_manual_payment(s6.units["MR-12"], MONTH)
    run_due_payments(date(2026, 12, DUE_DAY))
    assert s6.fake.calls == []
    rows = history(s6)
    assert len(rows) == 1
    assert rows[0]["method"] == "manual"
    assert rows[0]["status"] == "Paid"


def test_ac22_declined_charge_retried_after_delay(s6):
    # AC-22: the processor declines on day 5; once RETRY_DELAY_DAYS have passed the history
    # shows the first attempt as Failed and one retry attempt.
    from app.payments import run_due_payments

    assert settings.MAX_PAYMENT_ATTEMPTS >= 2, "AC-22 needs at least one retry"
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    first = date(2026, 12, DUE_DAY)
    run_due_payments(first)
    assert [(r["attempt"], r["status"]) for r in history(s6)] == [(1, "Failed")]

    if settings.RETRY_DELAY_DAYS > 1:  # R5: no retry before the delay
        run_due_payments(first + timedelta(days=settings.RETRY_DELAY_DAYS - 1))
        assert len(history(s6)) == 1

    run_due_payments(first + timedelta(days=settings.RETRY_DELAY_DAYS))
    rows = history(s6)
    assert [r["attempt"] for r in rows] == [1, 2]
    assert rows[0]["status"] == "Failed"
