"""S-6 Scheduled monthly dues payment (docs/design/S-6.md).

Written before any S-6 code exists (handout 6b). S-6 is not built in Milestone 1, so every test
is skipped with a reason that names its AC ID. Do not delete or weaken them; remove the skip
marker when S-6 is built. Imports of S-6 modules are inside the tests so that collection works
before those modules exist.

Interfaces used: app.payments (run_due_payments, record_manual_payment), app.processor
(FakeProcessor, set_processor), app.clock.now, app.seed.set_dues (S-6 D24, D28 to D30).
Values come from app.settings (RETRY_DELAY_DAYS, MAX_PAYMENT_ATTEMPTS; D15). Per D34 the
charge tests use debit schedules, so they settle nothing about ACH (OQ2).
"""

from datetime import date, datetime, timedelta, timezone

import pytest

from app import settings

NOT_BUILT = "S-6 (scheduled dues payment) not built in Milestone 1"
MONTH = "2026-12"
DUE_DAY = 5
DUES_CENTS = 18500  # sample data for set_dues, not a business rule (D30)
GOOD_TOKEN = "pm_card_visa"
DECLINED_TOKEN = "pm_card_chargeDeclined"


class SimulatedCrash(Exception):
    """Raised after the processor has charged, before the Payment is saved (S-6 D31)."""


@pytest.fixture
def s6(world, monkeypatch):
    """R1 (unit 12, Mountain Ridge) with dues set and a FakeProcessor installed.
    The clock reads 2026-11-20, so a day-5 schedule is first due on 2026-12-05 (D25)."""
    from app import clock, processor, seed

    seed.set_dues(world.communities["MR"], DUES_CENTS)
    monkeypatch.setattr(clock, "now", lambda: datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc))
    fake = processor.FakeProcessor(declined_tokens=frozenset({DECLINED_TOKEN}))
    processor.set_processor(fake)
    world.fake = fake
    return world


def schedule(w, method="debit", day=DUE_DAY, token=GOOD_TOKEN, user="R1"):
    return w.post(f"/communities/{w.communities['MR']}/payment-schedules", user,
                  json={"method": method, "day_of_month": day, "token": token})


def history(w, user="R1", month=MONTH):
    resp = w.get(f"/communities/{w.communities['MR']}/payments?month={month}", user)
    assert resp.status_code == 200
    return resp.json()


@pytest.mark.skip(reason=f"AC-18: {NOT_BUILT}")
def test_ac18_schedule_shown_on_payments_page(s6):
    # AC-18: R1 schedules payment on day 5 by ACH; the Payments page (D10: GET .../mine)
    # shows "Scheduled: day 5 of each month, ACH".
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


@pytest.mark.skip(reason=f"AC-19: {NOT_BUILT}")
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


@pytest.mark.skip(reason=f"AC-20: {NOT_BUILT}")
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


@pytest.mark.skip(reason=f"AC-21: {NOT_BUILT}")
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


@pytest.mark.skip(reason=f"AC-22: {NOT_BUILT}")
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
