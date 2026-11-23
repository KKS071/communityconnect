"""Shared S-6 test support, moved unchanged from tests/test_s6_payments.py.

Constants, fixtures and helpers used by the AC-18 to AC-22 acceptance tests in
tests/acceptance/test_s6_acceptance.py and by the S-6 regression tests in
tests/test_s6_payments.py. This file is locked together with the acceptance tests. The only
change from the original is that the s6 fixture restores the processor it replaced
(AGENT-03 F-16); payment behavior is unchanged. Per D34 the charge tests use debit
schedules, so they settle nothing about ACH (OQ2).
"""

from datetime import datetime, timezone

import pytest

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
    The clock reads 2026-11-20, so a day-5 schedule is first due on 2026-12-05 (D25).
    The processor in place before the test is restored afterwards (AGENT-03 F-16)."""
    from app import clock, processor, seed

    seed.set_dues(world.communities["MR"], DUES_CENTS)
    monkeypatch.setattr(clock, "now", lambda: datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc))
    previous = processor.get_processor()
    fake = processor.FakeProcessor(declined_tokens=frozenset({DECLINED_TOKEN}))
    processor.set_processor(fake)
    world.fake = fake
    yield world
    processor.set_processor(previous)


@pytest.fixture
def s6_schedule(world, monkeypatch):
    """AC-18 only: a fixed UTC clock, without AC-19 payment setup."""
    from app import clock

    monkeypatch.setattr(clock, "now", lambda: datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc))
    return world


def schedule(w, method="debit", day=DUE_DAY, token=GOOD_TOKEN, user="R1"):
    return w.post(f"/communities/{w.communities['MR']}/payment-schedules", user,
                  json={"method": method, "day_of_month": day, "token": token})


def history(w, user="R1", month=MONTH):
    resp = w.get(f"/communities/{w.communities['MR']}/payments?month={month}", user)
    assert resp.status_code == 200
    return resp.json()
