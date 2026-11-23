"""S-6 Hypothesis property tests (Milestone 2, AGENT-16). Not acceptance tests.

Property 1 comes from R1 (at most one Paid Payment per unit and month) and R2/D4 (a run
never charges twice for the same month): any sequence of runs in one billing month leaves
each due debit schedule with exactly one Paid attempt-1 Payment and one processor charge.

Property 2 comes from R5/D17/D35 (AC-22): a declined attempt is not retried before
RETRY_DELAY_DAYS have passed since its failed_on date, and once they have, the run makes
exactly one retry in the same billing month (D25), however often it runs that day.

Hypothesis cannot use the function-scoped db_schema/world/s6 fixtures once per example, so
each example builds its own schema and sample data with app/seed.py, the same way
tests/conftest.py does, and drops it afterwards. Clock, processor and settings are
restored after every example. Charges use FakeProcessor only (D29); no network calls.
"""

import uuid
from contextlib import contextmanager
from datetime import date, datetime, timezone

import hypothesis
import pytest
from fastapi.testclient import TestClient
from hypothesis import given, strategies as st

from tests.acceptance.s6_support import (
    DECLINED_TOKEN, DUES_CENTS, GOOD_TOKEN, MONTH, history, schedule,
)
from tests.conftest import TEST_DATABASE_URL, World

YEAR, MON = (int(part) for part in MONTH.split("-"))  # billing month 2026-12 (31 days)
DAYS_IN_MONTH = 31
CLOCK_NOW = datetime(2026, 11, 20, 12, 0, tzinfo=timezone.utc)  # as in the s6 fixture

PROPERTY_SETTINGS = hypothesis.settings(
    max_examples=10,
    deadline=None,       # each example creates a PostgreSQL schema
    derandomize=True,    # the same examples on every run
    database=None,       # no .hypothesis/ example database written to the repository
)


@contextmanager
def fresh_s6_world():
    """A new schema with Mountain Ridge (units 12 and 20, R1, R3, manager M1), dues set,
    a fixed clock and a FakeProcessor. Everything is restored or dropped on exit."""
    import psycopg

    from app import clock, processor, seed, settings
    from app.main import create_app

    try:
        admin = psycopg.connect(TEST_DATABASE_URL, autocommit=True, connect_timeout=5)
    except psycopg.OperationalError as exc:
        pytest.fail(f"PostgreSQL test database not reachable at {TEST_DATABASE_URL}: {exc}",
                    pytrace=False)
    schema = f"test_{uuid.uuid4().hex}"
    saved_settings = {name: getattr(settings, name)
                      for name in ("DATABASE_URL", "DATABASE_SCHEMA", "RETRY_DELAY_DAYS")}
    saved_now = clock.now
    saved_processor = processor.get_processor()
    try:
        settings.DATABASE_URL = TEST_DATABASE_URL
        settings.DATABASE_SCHEMA = schema
        clock.now = lambda: CLOCK_NOW
        fake = processor.FakeProcessor(declined_tokens=frozenset({DECLINED_TOKEN}))
        processor.set_processor(fake)

        w = World(client=TestClient(create_app()))
        mr = seed.create_community("Mountain Ridge")
        w.communities = {"MR": mr}
        w.units = {"MR-12": seed.create_unit(mr, "12"), "MR-20": seed.create_unit(mr, "20")}
        for name in ["R1", "R3", "M1"]:
            w.users[name] = seed.create_user()
        seed.add_membership(w.users["R1"], mr, "resident", w.units["MR-12"])
        seed.add_membership(w.users["R3"], mr, "resident", w.units["MR-20"])
        seed.add_membership(w.users["M1"], mr, "manager")
        seed.set_dues(mr, DUES_CENTS)
        w.fake = fake
        yield w
    finally:
        for name, value in saved_settings.items():
            setattr(settings, name, value)
        clock.now = saved_now
        processor.set_processor(saved_processor)
        admin.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')
        admin.close()


def run_on(day):
    from app.payments import run_due_payments

    return run_due_payments(date(YEAR, MON, day))


@PROPERTY_SETTINGS
@given(
    due_day=st.integers(min_value=1, max_value=28),             # D21: day 1 to 28
    residents=st.sampled_from([("R1",), ("R3",), ("R1", "R3")]),
    run_days=st.lists(st.integers(min_value=1, max_value=DAYS_IN_MONTH),
                      min_size=2, max_size=5),
)
def test_property_r1_repeated_runs_charge_each_unit_once(due_day, residents, run_days):
    # R1, R2, D4, D25 (AC-19, AC-20): runs in date order, repeats allowed, in one month.
    with fresh_s6_world() as w:
        for user in residents:
            assert schedule(w, day=due_day, token=GOOD_TOKEN, user=user).status_code == 201
        unit_ids = {w.units["MR-12" if user == "R1" else "MR-20"] for user in residents}

        charged = sum(run_on(day).charged for day in sorted(run_days))

        due = any(day >= due_day for day in run_days)
        rows = history(w, user="M1")  # the manager sees every unit's Payments (D8, D23)
        if not due:
            assert rows == []
            assert w.fake.calls == []
            assert charged == 0
            return
        assert sorted(r["unit_id"] for r in rows) == sorted(unit_ids)  # one row per unit
        assert all(r["status"] == "Paid" and r["attempt"] == 1 for r in rows)
        assert all(r["amount_cents"] == DUES_CENTS for r in rows)
        assert len(w.fake.calls) == len(unit_ids)  # one processor charge per unit
        assert len({key for _, _, key in w.fake.calls}) == len(unit_ids)
        assert charged == len(unit_ids)  # RunResult counts each charge once (D16)


@st.composite
def retry_cases(draw):
    """A delay, a due day and an early day, all inside one 31-day billing month (D25)."""
    delay = draw(st.integers(min_value=1, max_value=10))
    due_day = draw(st.integers(min_value=1, max_value=min(28, DAYS_IN_MONTH - delay)))
    early = draw(st.integers(min_value=0, max_value=delay - 1))  # 0: the failure day itself
    return delay, due_day, early


@PROPERTY_SETTINGS
@given(case=retry_cases())
def test_property_r5_declined_charge_retried_once_after_delay(case):
    # R5, D17, D35 (AC-22): no retry before RETRY_DELAY_DAYS; exactly one once they pass.
    from app import settings

    delay, due_day, early = case
    with fresh_s6_world() as w:
        settings.RETRY_DELAY_DAYS = delay  # restored by fresh_s6_world (S-6 D15)
        assert settings.MAX_PAYMENT_ATTEMPTS >= 2, "R5 needs at least one retry"
        assert schedule(w, day=due_day, token=DECLINED_TOKEN).status_code == 201

        run_on(due_day)
        assert [(r["attempt"], r["status"]) for r in history(w)] == [(1, "Failed")]

        run_on(due_day + early)  # before the delay has passed: no new attempt
        assert [(r["attempt"], r["status"]) for r in history(w)] == [(1, "Failed")]

        retry_day = due_day + delay
        run_on(retry_day)
        run_on(retry_day)  # a second run the same day makes no further attempt
        rows = history(w)
        assert [(r["attempt"], r["status"]) for r in rows] == [(1, "Failed"), (2, "Failed")]
        assert len(w.fake.calls) == 2  # one charge per attempt
        assert len({key for _, _, key in w.fake.calls}) == 2  # each attempt has its own key
