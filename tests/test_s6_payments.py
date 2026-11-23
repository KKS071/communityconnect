"""S-6 Scheduled monthly dues payment: regression tests (docs/design/S-6.md).

The AC-18 to AC-22 acceptance tests moved to tests/acceptance/test_s6_acceptance.py, and the
constants, fixtures and helpers they share with this file moved unchanged to
tests/acceptance/s6_support.py. Do not delete or weaken any test. Imports of S-6 modules stay
inside the tests. The AGENT-03 and AC-22 regression tests in this file add checks and change no
AC expectation.

Interfaces used: app.payments (run_due_payments, record_manual_payment), app.processor
(FakeProcessor, set_processor), app.clock.now, app.seed.set_dues (S-6 D24, D28 to D30).
Values come from app.settings (RETRY_DELAY_DAYS, MAX_PAYMENT_ATTEMPTS; D15). Per D34 the
charge tests use debit schedules, so they settle nothing about ACH (OQ2).
"""

from datetime import date, datetime, timedelta, timezone

import pytest

from app import settings
from tests.acceptance.s6_support import (  # noqa: F401  (s6 and s6_schedule are fixtures)
    DECLINED_TOKEN, DUE_DAY, DUES_CENTS, GOOD_TOKEN, MONTH, NOT_BUILT, SimulatedCrash, history,
    s6, s6_schedule, schedule,
)


# AGENT-03 F-02 regression tests (approved scope). The run must skip a month that has any
# Paid payment (D25 first branch; R1, R3), not only when the latest attempt is Paid. States
# the API cannot create are built with app.db functions, so the tests add no SQL.


def _record_attempt(w, status):
    """Store one scheduled attempt-1 row for R1's unit this month, then set its status."""
    from app import db

    unit = w.units["MR-12"]
    payment_id = db.create_pending_payment(
        unit, MONTH, DUES_CENTS, "debit", f"{unit}:{MONTH}:1", "2026-11-20T12:00:00Z")
    if status != "Pending":
        db.finish_payment(payment_id, status, f"test_{payment_id}")
    return payment_id


def test_f02_earlier_paid_then_later_failed_is_not_charged(s6):
    # T1: an earlier Paid payment and a later Failed attempt in the same month. The Failed
    # row sorts as the latest, so only a check for any Paid row skips the month.
    from app.payments import RunResult, record_manual_payment, run_due_payments

    assert schedule(s6).status_code == 201
    record_manual_payment(s6.units["MR-12"], MONTH)
    _record_attempt(s6, "Failed")
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert s6.fake.calls == []
    assert [r["status"] for r in history(s6)] == ["Paid", "Failed"]
    assert result == RunResult(charged=0, failed=0, skipped=1)


def test_f02_paid_with_pending_is_not_charged_and_pending_unchanged(s6):
    # T2: Paid and Pending in the same month (the OQ5 race state, built here by setup only).
    # Verifies existing D26 behaviour and the D25 skip count; it does not resolve OQ5.
    from app.payments import RunResult, record_manual_payment, run_due_payments

    assert schedule(s6).status_code == 201
    record_manual_payment(s6.units["MR-12"], MONTH)
    _record_attempt(s6, "Pending")
    before = history(s6)
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert s6.fake.calls == []
    assert history(s6) == before
    assert [r["status"] for r in before] == ["Paid", "Pending"]
    assert result == RunResult(charged=0, failed=0, skipped=1)


def test_f02_manual_payment_after_decline_is_not_charged(s6):
    # T3: attempt 1 is declined, then the manager records a manual payment (D27).
    from app.payments import RunResult, record_manual_payment, run_due_payments

    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(date(2026, 12, DUE_DAY))
    assert [r["status"] for r in history(s6)] == ["Failed"]
    record_manual_payment(s6.units["MR-12"], MONTH)
    calls_before = len(s6.fake.calls)
    result = run_due_payments(date(2026, 12, DUE_DAY + 1))
    assert len(s6.fake.calls) == calls_before
    assert result == RunResult(charged=0, failed=0, skipped=1)


def test_f02_second_run_same_day_counts_paid_month_as_skipped(s6):
    # T4: the AC-19 rerun, with the RunResult counts pinned (D16).
    from app.payments import RunResult, run_due_payments

    assert schedule(s6).status_code == 201
    assert run_due_payments(date(2026, 12, DUE_DAY)) == RunResult(charged=1, failed=0, skipped=0)
    assert run_due_payments(date(2026, 12, DUE_DAY)) == RunResult(charged=0, failed=0, skipped=1)
    assert len(s6.fake.calls) == 1


def test_f02_paid_in_another_month_does_not_block_this_month(s6):
    # T5: the Paid check is per billing month.
    from app.payments import RunResult, record_manual_payment, run_due_payments

    assert schedule(s6).status_code == 201
    record_manual_payment(s6.units["MR-12"], "2026-11")
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert result == RunResult(charged=1, failed=0, skipped=0)
    assert [r["status"] for r in history(s6)] == ["Paid"]
    assert [r["method"] for r in history(s6, month="2026-11")] == ["manual"]


def test_f02_paid_for_another_unit_does_not_block_this_unit(s6):
    # T6: the Paid check is per unit (R3's unit 20 is paid; R1's unit 12 is not).
    from app.payments import RunResult, record_manual_payment, run_due_payments

    assert schedule(s6).status_code == 201
    record_manual_payment(s6.units["MR-20"], MONTH)
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert result == RunResult(charged=1, failed=0, skipped=0)
    assert [r["status"] for r in history(s6)] == ["Paid"]


# AGENT-03 F-01 and F-03 regression tests (approved scope). F-01: a manual payment and a
# scheduled attempt for the same unit and month cannot both succeed. F-03: crash recovery
# keeps the Pending row, the key and the stored amount (D4, D26, D30, D31).


def _crash_after_charge_processor():
    """Install a FakeProcessor that notes the Pending rows it sees and crashes after charging."""
    from app import db, processor

    class CrashAfterCharge(processor.FakeProcessor):
        crash = True

        def __init__(self):
            super().__init__()
            self.pending_seen = []

        def charge(self, token, amount_cents, idempotency_key):
            self.pending_seen.append(
                [(p["idempotency_key"], p["amount_cents"]) for p in db.pending_payments()])
            result = super().charge(token, amount_cents, idempotency_key)
            if self.crash:
                raise SimulatedCrash()
            return result

    crashing = CrashAfterCharge()
    processor.set_processor(crashing)
    return crashing


def test_f03_crash_recovery_reuses_pending_key_and_amount(s6):
    # F-03: Pending is saved before the charge; the restart replays it with the same key and
    # the stored amount, adds no attempt or row, and ends with exactly one Paid payment.
    from app import seed
    from app.payments import run_due_payments

    crashing = _crash_after_charge_processor()
    assert schedule(s6).status_code == 201
    key = f"{s6.units['MR-12']}:{MONTH}:1"
    with pytest.raises(SimulatedCrash):
        run_due_payments(date(2026, 12, DUE_DAY))
    # 1. The Pending row existed when the processor was called (D4).
    assert crashing.pending_seen == [[(key, DUES_CENTS)]]
    assert [(r["attempt"], r["status"]) for r in history(s6)] == [(1, "Pending")]

    seed.set_dues(s6.communities["MR"], DUES_CENTS + 100)  # dues change before the restart
    crashing.crash = False
    result = run_due_payments(date(2026, 12, DUE_DAY))
    # 2 and 3. Same key and the stored amount on replay (D4, D26, D30).
    assert crashing.calls == [(GOOD_TOKEN, DUES_CENTS, key), (GOOD_TOKEN, DUES_CENTS, key)]
    # 4 and 5. No new attempt or row, and exactly one Paid payment.
    assert [(r["attempt"], r["status"], r["amount_cents"]) for r in history(s6)] == [
        (1, "Paid", DUES_CENTS)]
    assert result.charged == 1
    run_due_payments(date(2026, 12, DUE_DAY + 1))
    assert len(crashing.calls) == 2
    assert len(history(s6)) == 1


def test_f01_manual_payment_committed_during_run_prevents_charge(s6, monkeypatch):
    # F-01: the manager's payment commits after the run's pre-checks but before its Pending
    # insert. The locked re-check sees it, so the processor is never called (R1, R3, D27).
    from app import db
    from app.payments import RunResult, record_manual_payment, run_due_payments

    assert schedule(s6).status_code == 201
    real_latest_payment = db.latest_payment

    def manual_payment_in_window(unit_id, billing_month):
        prior = real_latest_payment(unit_id, billing_month)
        record_manual_payment(s6.units["MR-12"], MONTH)
        return prior

    monkeypatch.setattr(db, "latest_payment", manual_payment_in_window)
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert s6.fake.calls == []
    assert [(r["method"], r["status"]) for r in history(s6)] == [("manual", "Paid")]
    assert result == RunResult(charged=0, failed=0, skipped=1)


def test_f01_manual_payment_during_charge_is_refused_as_pending(s6):
    # F-01: once the scheduled Pending row is committed, a manual payment raises
    # PaymentPending (D27). It would block if the run held the unit lock during the charge.
    from app import processor
    from app.payments import PaymentPending, RunResult, record_manual_payment, run_due_payments

    outcomes = []

    class ManualPaymentDuringCharge(processor.FakeProcessor):
        def charge(self, token, amount_cents, idempotency_key):
            try:
                record_manual_payment(s6.units["MR-12"], MONTH)
                outcomes.append("recorded")
            except PaymentPending:
                outcomes.append("PaymentPending")
            return super().charge(token, amount_cents, idempotency_key)

    processor.set_processor(ManualPaymentDuringCharge())
    assert schedule(s6).status_code == 201
    result = run_due_payments(date(2026, 12, DUE_DAY))
    assert outcomes == ["PaymentPending"]
    assert [(r["method"], r["status"]) for r in history(s6)] == [("debit", "Paid")]
    assert result == RunResult(charged=1, failed=0, skipped=0)


# AGENT-03 F-04 negative and authorization tests and F-05 access-layer tests (approved scope).
# They pin the existing S-6 contract (section 4; D6 to D9, D11 to D13, D16, D18, D21 to D23,
# D25, D27, D30, D31, D34) and add no policy. Board-member access to the payments list is OQ4
# and is deliberately untested. Wrong-typed unit_id or billing_month inputs are not tested
# because D27 does not specify them.

NOT_FOUND = {"detail": "Not found"}
UNKNOWN_USER = {"detail": "Unknown user"}


def _payments_url(w, community="MR", month=MONTH):
    return f"/communities/{w.communities[community]}/payments?month={month}"


def _mine_url(w, community="MR"):
    return f"/communities/{w.communities[community]}/payment-schedules/mine"


def _two_manual_payments(w):
    """Manual Paid payments this month for R1's unit 12 and R3's unit 20 (Mountain Ridge)."""
    from app.payments import record_manual_payment

    record_manual_payment(w.units["MR-12"], MONTH)
    record_manual_payment(w.units["MR-20"], MONTH)


def _viewer_scope(w, user, community):
    """Call the F-05 access-layer decision directly for a seeded caller."""
    from app import db
    from app.access import require_payment_viewer

    with db.connect() as conn:
        return require_payment_viewer(conn, w.users[user], w.communities[community])


def test_f04_resident_sees_only_own_unit_payments(s6):
    # D8: a resident sees their own unit's payments, never a neighbour's.
    _two_manual_payments(s6)
    assert [r["unit_id"] for r in history(s6, user="R1")] == [s6.units["MR-12"]]
    assert [r["unit_id"] for r in history(s6, user="R3")] == [s6.units["MR-20"]]


def test_f04_manager_sees_every_unit_of_managed_community(s6):
    # D8, D23: M1 sees both Mountain Ridge units, ordered by unit_id.
    _two_manual_payments(s6)
    assert [r["unit_id"] for r in history(s6, user="M1")] == sorted(
        [s6.units["MR-12"], s6.units["MR-20"]])


def test_f04_payments_isolated_between_communities(s6):
    # D8, D23 (S-1 R2): with real payments in Mountain Ridge and Elm Court, each list shows
    # only its own community, and callers from the other community get 404.
    from app import seed
    from app.payments import record_manual_payment

    seed.set_dues(s6.communities["EC"], DUES_CENTS)
    _two_manual_payments(s6)
    record_manual_payment(s6.units["EC-5"], MONTH)
    assert [r["unit_id"] for r in history(s6, user="M1")] == sorted(
        [s6.units["MR-12"], s6.units["MR-20"]])
    assert [r["unit_id"] for r in history(s6, user="R1")] == [s6.units["MR-12"]]
    for user in ("M2", "R4"):
        resp = s6.get(_payments_url(s6, community="EC"), user)
        assert resp.status_code == 200
        assert [r["unit_id"] for r in resp.json()] == [s6.units["EC-5"]]
    for user in ("M1", "R1"):
        resp = s6.get(_payments_url(s6, community="EC"), user)
        assert resp.status_code == 404
        assert resp.json() == NOT_FOUND
    resp = s6.get(_payments_url(s6, community="PH"), "M1")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.parametrize("user", ["ADMIN", "NOBODY", "M2", "R2"])
def test_f04_payments_hidden_from_other_callers(s6, user):
    # D8: admins, non-members and members of other communities get 404 with the same body
    # as a missing record (S-1 R2, D3). B1 (board member) is OQ4 and is not tested.
    _two_manual_payments(s6)
    resp = s6.get(_payments_url(s6), user)
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND


@pytest.mark.parametrize("community_id", ["999999999", "abc"])
def test_f04_payments_unknown_community_is_not_found(s6, community_id):
    # D6 (S-1 D14): a missing or malformed community id is 404 "Not found".
    resp = s6.get(f"/communities/{community_id}/payments?month={MONTH}", "M1")
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND


def test_f04_payments_unknown_user_is_401(s6):
    # D6 (S-1 D1): a missing, malformed or unknown X-User-Id is 401 "Unknown user".
    unknown = str(max(s6.users.values()) + 1000)
    for headers in ({}, {"X-User-Id": "abc"}, {"X-User-Id": unknown}):
        resp = s6.client.get(_payments_url(s6), headers=headers)
        assert resp.status_code == 401
        assert resp.json() == UNKNOWN_USER


@pytest.mark.parametrize("month", ["", "2026-13", "2026-00", "2026-1", "2026-12-01"])
def test_f04_payments_invalid_month_is_422(s6, month):
    # D9: month must be YYYY-MM with month 01 to 12.
    resp = s6.get(_payments_url(s6, month=month), "R1")
    assert resp.status_code == 422
    assert resp.json() == {"detail": "Invalid month"}


def test_f04_payments_missing_month_is_422(s6):
    # D9: month is required.
    resp = s6.get(f"/communities/{s6.communities['MR']}/payments", "M1")
    assert resp.status_code == 422
    assert resp.json() == {"detail": "Invalid month"}


@pytest.mark.parametrize("user", ["NOBODY", "ADMIN"])
def test_f04_payments_membership_checked_before_month(s6, user):
    # D6 (S-1 D6): the 404 membership check runs before the 422 month check.
    resp = s6.get(_payments_url(s6, month="2026-13"), user)
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND


def test_f04_payments_future_month_empty_and_rows_have_paymentout_fields(s6):
    # D9: a future month is an empty list. Section 4, D23: rows carry only PaymentOut fields.
    _two_manual_payments(s6)
    assert history(s6, user="M1", month="2027-06") == []
    rows = history(s6, user="M1")
    assert len(rows) == 2
    for row in rows:
        assert set(row) == {"id", "unit_id", "billing_month", "amount_cents", "method",
                            "status", "attempt", "created_at"}


def test_f05_payment_viewer_scope_for_residents_and_managers(s6):
    # D8, D23: a manager gets None (every unit; main.py still filters by community_id), and
    # a resident gets their own concrete unit id, never None.
    assert _viewer_scope(s6, "M1", "MR") is None
    assert _viewer_scope(s6, "M1", "PH") is None
    assert _viewer_scope(s6, "M2", "EC") is None
    assert _viewer_scope(s6, "R1", "MR") == s6.units["MR-12"]
    assert _viewer_scope(s6, "R3", "MR") == s6.units["MR-20"]
    assert _viewer_scope(s6, "R2", "PH") == s6.units["PH-3"]


@pytest.mark.parametrize("user, community", [("ADMIN", "MR"), ("NOBODY", "MR"), ("M2", "MR"),
                                             ("R1", "PH")])
def test_f05_payment_viewer_refuses_other_callers(s6, user, community):
    # D8: admins, non-members, and a manager or resident of another community get NotFound,
    # never manager-wide None. Board members are OQ4 and are not tested.
    from app.access import NotFound

    with pytest.raises(NotFound):
        _viewer_scope(s6, user, community)


def test_f05_resident_without_unit_never_gets_manager_scope(monkeypatch):
    # F-05: seed.py cannot create a resident membership without a unit, so the membership row
    # is stubbed (no SQL in tests). Such a resident gets NotFound, never None.
    from app import access

    monkeypatch.setattr(access, "require_member",
                        lambda conn, user_id, community_id: {"role": "resident",
                                                             "unit_id": None})
    with pytest.raises(access.NotFound):
        access.require_payment_viewer(None, 1, 1)


@pytest.mark.parametrize("user", ["M1", "ADMIN", "B1", "NOBODY", "R2"])
def test_f04_schedules_need_resident_of_community(s6, user):
    # D7, D22: only a resident of the community may create or read a schedule; any other
    # caller gets 404 "Not found", and no schedule is stored for any resident's unit.
    resp = schedule(s6, user=user)
    assert resp.status_code == 404
    assert resp.json() == NOT_FOUND
    mine = s6.get(_mine_url(s6), user)
    assert mine.status_code == 404
    assert mine.json() == NOT_FOUND
    for resident, community in (("R1", "MR"), ("R3", "MR"), ("R2", "PH")):
        assert s6.get(_mine_url(s6, community), resident).status_code == 404


def test_f04_schedules_unknown_user_is_401(s6):
    # D6, D22 (S-1 D1): 401 "Unknown user" before any other check.
    path = f"/communities/{s6.communities['MR']}/payment-schedules"
    body = {"method": "debit", "day_of_month": DUE_DAY, "token": GOOD_TOKEN}
    for headers in ({}, {"X-User-Id": str(max(s6.users.values()) + 1000)}):
        post = s6.client.post(path, headers=headers, json=body)
        assert (post.status_code, post.json()) == (401, UNKNOWN_USER)
        mine = s6.client.get(_mine_url(s6), headers=headers)
        assert (mine.status_code, mine.json()) == (401, UNKNOWN_USER)
    assert s6.get(_mine_url(s6), "R1").status_code == 404


# D12 lists the field order and D21 the messages. Cases that mix a wrong type in one field
# with a bad value in an earlier field (for example method "bogus" with day_of_month "5")
# are deliberately excluded until the human D12 ruling on F-10.
@pytest.mark.parametrize("body, detail", [
    ({"day_of_month": DUE_DAY, "token": GOOD_TOKEN}, "Invalid request body"),
    ({"method": "debit", "token": GOOD_TOKEN}, "Invalid request body"),
    ({"method": "debit", "day_of_month": DUE_DAY}, "Invalid request body"),
    ({"method": "debit", "day_of_month": True, "token": GOOD_TOKEN}, "Invalid request body"),
    ({"method": "debit", "day_of_month": 5.0, "token": GOOD_TOKEN}, "Invalid request body"),
    ({"method": "debit", "day_of_month": "5", "token": GOOD_TOKEN}, "Invalid request body"),
    ({"method": "debit", "day_of_month": DUE_DAY, "token": None}, "Invalid request body"),
    ({"method": "manual", "day_of_month": DUE_DAY, "token": GOOD_TOKEN}, "Unknown method"),
    ({"method": "Debit", "day_of_month": DUE_DAY, "token": GOOD_TOKEN}, "Unknown method"),
    ({"method": "debit", "day_of_month": 0, "token": GOOD_TOKEN}, "Day must be 1 to 28"),
    ({"method": "debit", "day_of_month": 29, "token": GOOD_TOKEN}, "Day must be 1 to 28"),
    ({"method": "debit", "day_of_month": DUE_DAY, "token": ""}, "Token is required"),
    ({"method": "debit", "day_of_month": DUE_DAY, "token": "   "}, "Token is required"),
    ({"method": "bogus", "day_of_month": 29, "token": ""}, "Unknown method"),
    ({"method": "debit", "day_of_month": 29, "token": ""}, "Day must be 1 to 28"),
])
def test_f04_schedule_validation_is_422_and_stores_nothing(s6, body, detail):
    # D12, D21: fixed 422 messages, checked in the order method, day_of_month, token.
    resp = s6.post(f"/communities/{s6.communities['MR']}/payment-schedules", "R1", json=body)
    assert resp.status_code == 422
    assert resp.json() == {"detail": detail}
    assert s6.get(_mine_url(s6), "R1").status_code == 404


@pytest.mark.parametrize("kwargs", [{"json": [1, 2]}, {"content": b"{not json"}])
def test_f04_schedule_body_must_be_json_object(s6, kwargs):
    # Section 4: a body that is not a JSON object is 422 "Invalid request body".
    resp = s6.post(f"/communities/{s6.communities['MR']}/payment-schedules", "R1", **kwargs)
    assert resp.status_code == 422
    assert resp.json() == {"detail": "Invalid request body"}
    assert s6.get(_mine_url(s6), "R1").status_code == 404


def test_f04_second_schedule_is_409_only_after_validation(s6):
    # D11, D22: any existing schedule gives 409, but the body checks come first.
    assert schedule(s6).status_code == 201
    dup = schedule(s6, method="credit", day=10)
    assert dup.status_code == 409
    assert dup.json() == {"detail": "Schedule already exists"}
    bad = schedule(s6, method="manual")
    assert bad.status_code == 422
    assert bad.json() == {"detail": "Unknown method"}
    mine = s6.get(_mine_url(s6), "R1").json()
    assert (mine["method"], mine["day_of_month"]) == ("debit", DUE_DAY)


def test_f04_schedule_post_response_omits_token_and_mine_is_per_unit(s6):
    # Section 5: the token is never returned. D7, D22: R3 does not see R1's unit schedule.
    resp = schedule(s6)
    assert resp.status_code == 201
    assert set(resp.json()) == {"id", "unit_id", "method", "day_of_month", "active"}
    other = s6.get(_mine_url(s6), "R3")
    assert other.status_code == 404
    assert other.json() == NOT_FOUND


def test_f04_manual_payment_twice_raises_already_paid(s6):
    # D13: a second manual payment for a Paid month raises AlreadyPaid and records nothing.
    from app.payments import AlreadyPaid, record_manual_payment

    record_manual_payment(s6.units["MR-12"], MONTH)
    with pytest.raises(AlreadyPaid):
        record_manual_payment(s6.units["MR-12"], MONTH)
    assert [(r["method"], r["status"]) for r in history(s6)] == [("manual", "Paid")]


def test_f04_manual_payment_while_pending_raises_payment_pending(s6):
    # D16, D27: an unavailable processor leaves attempt 1 Pending; a manual payment for the
    # month then raises PaymentPending and records nothing.
    from app.payments import PaymentPending, RunResult, record_manual_payment, run_due_payments

    s6.fake.unavailable = True
    assert schedule(s6).status_code == 201
    assert run_due_payments(date(2026, 12, DUE_DAY)) == RunResult(charged=0, failed=0, skipped=1)
    with pytest.raises(PaymentPending):
        record_manual_payment(s6.units["MR-12"], MONTH)
    assert [(r["method"], r["status"]) for r in history(s6)] == [("debit", "Pending")]


@pytest.mark.parametrize("billing_month", ["2026-13", "2026-1", ""])
def test_f04_manual_payment_invalid_month_raises_value_error(s6, billing_month):
    # D27: an invalid billing_month raises ValueError and records nothing.
    from app.payments import record_manual_payment

    with pytest.raises(ValueError):
        record_manual_payment(s6.units["MR-12"], billing_month)
    assert history(s6) == []


@pytest.mark.parametrize("unit_id", [999999999, 0])
def test_f04_manual_payment_unknown_unit_raises_value_error(s6, unit_id):
    # D27: an unknown unit raises ValueError.
    from app.payments import record_manual_payment

    with pytest.raises(ValueError):
        record_manual_payment(unit_id, MONTH)


def test_f04_manual_payment_without_dues_raises_value_error(s6):
    # D27, D30 (DR-4): Pine Hollow has no dues set, so nothing is recorded for R2's unit.
    from app.payments import record_manual_payment

    with pytest.raises(ValueError):
        record_manual_payment(s6.units["PH-3"], MONTH)
    resp = s6.get(_payments_url(s6, community="PH"), "R2")
    assert resp.status_code == 200
    assert resp.json() == []


def test_f04_unavailable_processor_leaves_pending_and_next_run_reuses_key(s6):
    # D16, D26: ProcessorUnavailable leaves attempt 1 Pending; the next run charges the same
    # key and the month ends Paid. skipped on the second run is not pinned (F-08).
    from app.payments import RunResult, run_due_payments

    s6.fake.unavailable = True
    assert schedule(s6).status_code == 201
    assert run_due_payments(date(2026, 12, DUE_DAY)) == RunResult(charged=0, failed=0, skipped=1)
    assert [(r["attempt"], r["status"]) for r in history(s6)] == [(1, "Pending")]
    s6.fake.unavailable = False
    assert run_due_payments(date(2026, 12, DUE_DAY + 1)).charged == 1
    assert [(r["attempt"], r["status"]) for r in history(s6)] == [(1, "Paid")]
    key = f"{s6.units['MR-12']}:{MONTH}:1"
    assert [call[2] for call in s6.fake.calls] == [key, key]


@pytest.mark.parametrize("unreachable", ["R1", "R3"])
def test_f04_run_continues_after_processor_unavailable_for_one_unit(s6, unreachable):
    # D31: ProcessorUnavailable for one unit does not stop the run. Both orders are tested, so
    # the result does not depend on which unit the run reaches first.
    from app import processor
    from app.payments import RunResult, run_due_payments

    class UnreachableForOneToken(processor.FakeProcessor):
        def charge(self, token, amount_cents, idempotency_key):
            if token == "pm_unreachable":
                raise processor.ProcessorUnavailable("unreachable for this test")
            return super().charge(token, amount_cents, idempotency_key)

    units = {"R1": s6.units["MR-12"], "R3": s6.units["MR-20"]}
    previous = processor.get_processor()
    processor.set_processor(UnreachableForOneToken())
    try:
        for user in units:
            token = "pm_unreachable" if user == unreachable else GOOD_TOKEN
            assert schedule(s6, token=token, user=user).status_code == 201
        result = run_due_payments(date(2026, 12, DUE_DAY))
    finally:
        processor.set_processor(previous)  # restore the s6 fixture's processor (F-16)
    assert result == RunResult(charged=1, failed=0, skipped=1)
    expected = sorted((unit, "Pending" if user == unreachable else "Paid")
                      for user, unit in units.items())
    assert [(r["unit_id"], r["status"]) for r in history(s6, user="M1")] == expected


def test_f04_declined_attempt_is_failed_and_counted(s6):
    # D16: a declined attempt 1 is Failed and counted once in failed (retries are AC-22).
    from app.payments import RunResult, run_due_payments

    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    assert run_due_payments(date(2026, 12, DUE_DAY)) == RunResult(charged=0, failed=1, skipped=0)
    assert [(r["attempt"], r["status"]) for r in history(s6)] == [(1, "Failed")]


def test_f04_not_due_before_day_and_caught_up_later_in_month(s6):
    # D18, D25: nothing before day_of_month; a missed run is caught up later in the month.
    from app.payments import RunResult, run_due_payments

    assert schedule(s6).status_code == 201
    assert run_due_payments(date(2026, 12, DUE_DAY - 1)) == RunResult()
    assert s6.fake.calls == []
    assert history(s6) == []
    assert run_due_payments(date(2026, 12, 28)) == RunResult(charged=1, failed=0, skipped=0)
    assert [r["status"] for r in history(s6)] == ["Paid"]


def test_f04_first_due_month_follows_created_at(s6):
    # D18, D25: the clock reads 2026-11-20. A day-20 schedule is not due in November (its
    # date must be strictly after created_at) and is first due on 2026-12-20.
    from app.payments import RunResult, run_due_payments

    assert schedule(s6, day=20).status_code == 201
    assert run_due_payments(date(2026, 11, 20)) == RunResult()
    assert run_due_payments(date(2026, 11, 30)) == RunResult()
    assert history(s6, month="2026-11") == []
    assert run_due_payments(date(2026, 12, 19)) == RunResult()
    assert run_due_payments(date(2026, 12, 20)).charged == 1


def test_f04_day_after_creation_is_due_in_the_same_month(s6):
    # D18, D25: the clock reads 2026-11-20, so a day-28 schedule is first due on 2026-11-28.
    from app.payments import RunResult, run_due_payments

    assert schedule(s6, day=28).status_code == 201
    assert run_due_payments(date(2026, 11, 27)) == RunResult()
    assert run_due_payments(date(2026, 11, 28)) == RunResult(charged=1, failed=0, skipped=0)
    assert [r["status"] for r in history(s6, month="2026-11")] == ["Paid"]


def test_f04_community_without_dues_and_ach_schedules_are_not_charged(s6):
    # D30, D22: Pine Hollow has no dues, so R2's schedule (accepted under D22) is never due
    # and its history stays empty. D34 (DR-ACH): an ach schedule is not charged or counted
    # until OQ2 is answered.
    from app.payments import RunResult, run_due_payments

    ph = s6.post(f"/communities/{s6.communities['PH']}/payment-schedules", "R2",
                 json={"method": "debit", "day_of_month": DUE_DAY, "token": GOOD_TOKEN})
    assert ph.status_code == 201
    assert schedule(s6, method="ach").status_code == 201
    assert run_due_payments(date(2026, 12, DUE_DAY)) == RunResult()
    assert s6.fake.calls == []
    assert history(s6) == []
    pine = s6.get(_payments_url(s6, community="PH"), "R2")
    assert pine.status_code == 200
    assert pine.json() == []


# AC-22 retry regression tests (approved scope, Prompts 55 to 58). They follow R5, D15 to
# D17, D25, D26, D27, D30 and D35: failed_on is the `today` of the run in which an attempt
# became Failed, a Failed row without failed_on is never retried, and an earlier billing
# month is never retried (OQ3 stays open). Settings are read, or overridden with
# monkeypatch, never copied as numbers. The F-11 tests check the finish_payment state guard
# and conflicting completions; the F-01 test checks READ COMMITTED on the lock transactions.

FIRST = date(2026, 12, DUE_DAY)


@pytest.fixture
def install_processor(s6, monkeypatch):
    """Use the given processor for one test. monkeypatch restores get_processor afterwards
    (AGENT-03 F-16) without changing the s6 fixture."""
    from app import processor

    def install(p):
        monkeypatch.setattr(processor, "get_processor", lambda: p)
        return p

    return install


def _require_retries():
    """Settings assumptions for tests that need a retry inside December (D15)."""
    assert settings.MAX_PAYMENT_ATTEMPTS >= 2, "these tests need at least one retry"
    last_day = FIRST.day + settings.MAX_PAYMENT_ATTEMPTS * (settings.RETRY_DELAY_DAYS + 2)
    assert last_day <= 31, "these tests need every retry date inside December"


def _attempts(w, user="R1", month=MONTH):
    return [(r["attempt"], r["status"]) for r in history(w, user=user, month=month)]


def _failed_on(w, month=MONTH):
    """failed_on of R1's latest attempt in the month, read with app.db (no SQL in tests)."""
    from app import db

    return db.latest_payment(w.units["MR-12"], month)["failed_on"]


def _key(w, attempt, unit="MR-12", month=MONTH):
    return f"{w.units[unit]}:{month}:{attempt}"


def _declining_keys(keys):
    """A FakeProcessor that declines exactly the given idempotency keys (D29 otherwise)."""
    from app import processor

    class DeclineKeys(processor.FakeProcessor):
        def charge(self, token, amount_cents, idempotency_key):
            self.declined_tokens = (frozenset({token}) if idempotency_key in keys
                                    else frozenset())
            return super().charge(token, amount_cents, idempotency_key)

    return DeclineKeys()


def _completing_processor(stored_status):
    """A FakeProcessor that, like a second runner, completes the Pending row itself with
    stored_status before returning its own result (D32 broken on purpose; F-11)."""
    from app import db, processor

    class CompletesFirst(processor.FakeProcessor):
        def charge(self, token, amount_cents, idempotency_key):
            for p in db.pending_payments():
                if p["idempotency_key"] == idempotency_key:
                    db.finish_payment(p["id"], stored_status, "other_runner",
                                      FIRST.isoformat())
            return super().charge(token, amount_cents, idempotency_key)

    return CompletesFirst(declined_tokens=frozenset({DECLINED_TOKEN}))


def _failed_attempt_1(w, failed_on):
    """Attempt 1 for R1's unit this month, Failed on failed_on, built with app.db (no SQL)."""
    from app import db

    payment_id = db.create_pending_payment(
        w.units["MR-12"], MONTH, DUES_CENTS, "debit", _key(w, 1), "2026-11-20T12:00:00Z")
    assert db.finish_payment(payment_id, "Failed", "test_declined", failed_on.isoformat())


def _claim(w, attempt, **retry):
    """Call the locked claim directly for R1's unit this month (D35); no SQL in tests."""
    from app import db

    return db.claim_pending_payment(w.units["MR-12"], MONTH, DUES_CENTS, "debit",
                                    _key(w, attempt), "2026-11-20T12:00:00Z",
                                    attempt=attempt, **retry)


def test_ac22_no_retry_before_retry_delay_days(s6):
    # R5, D17: no run before RETRY_DELAY_DAYS have passed makes a new attempt.
    from app.payments import RunResult, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    assert run_due_payments(FIRST) == RunResult(charged=0, failed=1, skipped=0)
    for days in range(settings.RETRY_DELAY_DAYS):
        assert run_due_payments(FIRST + timedelta(days=days)) == RunResult()
    assert _attempts(s6) == [(1, "Failed")]
    assert len(s6.fake.calls) == 1


def test_ac22_exactly_one_retry_on_the_first_eligible_run(s6):
    # R5, D16, D17: the first run RETRY_DELAY_DAYS after the decline makes one attempt 2 with
    # its own key, counted in failed; a second run that day makes no attempt.
    from app.payments import RunResult, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    assert run_due_payments(retry_day) == RunResult(charged=0, failed=1, skipped=0)
    assert run_due_payments(retry_day) == RunResult()
    assert _attempts(s6) == [(1, "Failed"), (2, "Failed")]
    assert [call[2] for call in s6.fake.calls] == [_key(s6, 1), _key(s6, 2)]


def test_ac22_retry_follows_a_nondefault_retry_delay(s6, monkeypatch):
    # D15, R5: the delay is read from settings at run time, so one more day than the default
    # means no retry on the default's day and one retry a day later.
    from app.payments import run_due_payments

    monkeypatch.setattr(settings, "RETRY_DELAY_DAYS", settings.RETRY_DELAY_DAYS + 1)
    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    run_due_payments(FIRST + timedelta(days=settings.RETRY_DELAY_DAYS - 1))
    assert _attempts(s6) == [(1, "Failed")]
    run_due_payments(FIRST + timedelta(days=settings.RETRY_DELAY_DAYS))
    assert _attempts(s6) == [(1, "Failed"), (2, "Failed")]


def test_ac22_late_run_still_makes_exactly_one_retry(s6):
    # R5: the retry happens on the first run at least RETRY_DELAY_DAYS after the decline,
    # even when that run comes days later than the eligible date.
    from app.payments import RunResult, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    late_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS + 2)
    assert run_due_payments(late_day) == RunResult(charged=0, failed=1, skipped=0)
    assert run_due_payments(late_day) == RunResult()
    assert _attempts(s6) == [(1, "Failed"), (2, "Failed")]


def test_ac22_attempts_stop_at_max_with_unique_keys(s6, monkeypatch):
    # R2, R5, D17: with one more attempt allowed than the default, attempts stop at the
    # maximum, each with its own key, later runs this month do nothing, and the schedule
    # stays active.
    from app.payments import run_due_payments

    monkeypatch.setattr(settings, "MAX_PAYMENT_ATTEMPTS", settings.MAX_PAYMENT_ATTEMPTS + 1)
    _require_retries()
    maximum, delay = settings.MAX_PAYMENT_ATTEMPTS, settings.RETRY_DELAY_DAYS
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    for n in range(maximum):
        assert run_due_payments(FIRST + timedelta(days=n * delay)).failed == 1
    for day in range(FIRST.day, 32):
        run_due_payments(date(2026, 12, day))
    assert _attempts(s6) == [(n, "Failed") for n in range(1, maximum + 1)]
    keys = [call[2] for call in s6.fake.calls]
    assert keys == [_key(s6, n) for n in range(1, maximum + 1)]
    assert len(set(keys)) == len(keys)
    assert s6.get(_mine_url(s6), "R1").json()["active"] is True


def test_ac22_successful_retry_is_paid_and_nothing_is_charged_after(s6, install_processor):
    # R1, R3, D16: a retry that succeeds is Paid and counted in charged; no later run in the
    # month calls the processor, and the Paid attempt keeps failed_on null (D35).
    from app.payments import RunResult, run_due_payments

    _require_retries()
    fake = install_processor(_declining_keys({_key(s6, 1)}))
    assert schedule(s6).status_code == 201
    assert run_due_payments(FIRST) == RunResult(charged=0, failed=1, skipped=0)
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    assert run_due_payments(retry_day) == RunResult(charged=1, failed=0, skipped=0)
    for day in range(retry_day.day, 32):
        run_due_payments(date(2026, 12, day))
    assert _attempts(s6) == [(1, "Failed"), (2, "Paid")]
    assert _failed_on(s6) is None
    assert [call[2] for call in fake.calls] == [_key(s6, 1), _key(s6, 2)]


def test_ac22_delay_counts_from_the_run_that_declined(s6):
    # D16, D17, D35: attempt 1 stays Pending while the processor is unavailable on day 5 and
    # is declined by the D26 replay on day 6, so failed_on is day 6 and the retry waits for it.
    from app.payments import RunResult, run_due_payments

    _require_retries()
    s6.fake.unavailable = True
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    assert run_due_payments(FIRST) == RunResult(charged=0, failed=0, skipped=1)
    s6.fake.unavailable = False
    declined_day = FIRST + timedelta(days=1)
    assert run_due_payments(declined_day).failed == 1
    assert _failed_on(s6) == declined_day.isoformat()  # not FIRST, when attempt 1 was created
    run_due_payments(declined_day + timedelta(days=settings.RETRY_DELAY_DAYS - 1))
    assert _attempts(s6) == [(1, "Failed")]
    retry_day = declined_day + timedelta(days=settings.RETRY_DELAY_DAYS)
    run_due_payments(retry_day)
    assert _attempts(s6) == [(1, "Failed"), (2, "Failed")]
    assert _failed_on(s6) == retry_day.isoformat()


def test_ac22_crash_during_retry_replays_its_key_and_stored_amount(s6, install_processor):
    # D4, D26, D30, D31: attempt 2 is Pending before its charge; after a crash the restart
    # replays key :2 with its stored amount, adds no attempt, and leaves one Paid payment.
    from app import db, processor, seed
    from app.payments import run_due_payments

    _require_retries()
    first_key, retry_key = _key(s6, 1), _key(s6, 2)

    class CrashOnRetry(processor.FakeProcessor):
        crash = True

        def __init__(self):
            super().__init__()
            self.pending_seen = []

        def charge(self, token, amount_cents, idempotency_key):
            self.declined_tokens = (frozenset({token}) if idempotency_key == first_key
                                    else frozenset())
            self.pending_seen.append(
                [(p["idempotency_key"], p["amount_cents"]) for p in db.pending_payments()])
            result = super().charge(token, amount_cents, idempotency_key)
            if self.crash and idempotency_key == retry_key:
                raise SimulatedCrash()
            return result

    crashing = install_processor(CrashOnRetry())
    assert schedule(s6).status_code == 201
    run_due_payments(FIRST)
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    with pytest.raises(SimulatedCrash):
        run_due_payments(retry_day)
    assert crashing.pending_seen[-1] == [(retry_key, DUES_CENTS)]
    assert _attempts(s6) == [(1, "Failed"), (2, "Pending")]

    seed.set_dues(s6.communities["MR"], DUES_CENTS + 100)
    crashing.crash = False
    assert run_due_payments(retry_day).charged == 1
    assert crashing.calls == [(GOOD_TOKEN, DUES_CENTS, first_key),
                              (GOOD_TOKEN, DUES_CENTS, retry_key),
                              (GOOD_TOKEN, DUES_CENTS, retry_key)]
    assert [(r["attempt"], r["status"], r["amount_cents"]) for r in history(s6)] == [
        (1, "Failed", DUES_CENTS), (2, "Paid", DUES_CENTS)]


def test_ac22_unavailable_processor_during_retry_keeps_it_pending(s6):
    # D16, D26: an unavailable retry stays Pending without using an attempt; the next run
    # replays key :2 and makes no further attempt.
    from app.payments import RunResult, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    s6.fake.unavailable = True
    assert run_due_payments(retry_day) == RunResult(charged=0, failed=0, skipped=1)
    assert _attempts(s6) == [(1, "Failed"), (2, "Pending")]
    s6.fake.unavailable = False
    assert run_due_payments(retry_day + timedelta(days=1)).failed == 1
    assert _attempts(s6) == [(1, "Failed"), (2, "Failed")]
    assert [call[2] for call in s6.fake.calls] == [_key(s6, 1), _key(s6, 2), _key(s6, 2)]


def test_ac22_manual_payment_before_retry_prevents_it(s6):
    # R3, D25, D27: a manual payment recorded after the decline stops the retry.
    from app.payments import RunResult, record_manual_payment, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    record_manual_payment(s6.units["MR-12"], MONTH)
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    assert run_due_payments(retry_day) == RunResult(charged=0, failed=0, skipped=1)
    assert len(s6.fake.calls) == 1
    assert [(r["attempt"], r["method"], r["status"]) for r in history(s6)] == [
        (1, "debit", "Failed"), (1, "manual", "Paid")]


def test_ac22_manual_payment_racing_retry_creation_prevents_charge(s6, monkeypatch):
    # F-01, D27: the manual payment commits after the run's pre-checks but before the retry
    # is claimed. The locked re-check sees it, so attempt 2 is never created or charged.
    from app import db
    from app.payments import RunResult, record_manual_payment, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    real_latest_payment = db.latest_payment

    def manual_payment_in_window(unit_id, billing_month):
        prior = real_latest_payment(unit_id, billing_month)
        record_manual_payment(s6.units["MR-12"], MONTH)
        return prior

    monkeypatch.setattr(db, "latest_payment", manual_payment_in_window)
    result = run_due_payments(FIRST + timedelta(days=settings.RETRY_DELAY_DAYS))
    assert result == RunResult(charged=0, failed=0, skipped=1)
    assert len(s6.fake.calls) == 1
    assert [(r["attempt"], r["method"], r["status"]) for r in history(s6)] == [
        (1, "debit", "Failed"), (1, "manual", "Paid")]


def test_ac22_manual_payment_while_retry_pending_raises_payment_pending(s6):
    # D27: while attempt 2 is Pending, a manual payment raises PaymentPending and records
    # nothing.
    from app.payments import PaymentPending, record_manual_payment, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    s6.fake.unavailable = True
    run_due_payments(FIRST + timedelta(days=settings.RETRY_DELAY_DAYS))
    with pytest.raises(PaymentPending):
        record_manual_payment(s6.units["MR-12"], MONTH)
    assert _attempts(s6) == [(1, "Failed"), (2, "Pending")]


def test_ac22_retry_uses_current_dues_and_replay_uses_stored_amount(s6):
    # D30, D35: a new retry takes the dues at its creation; replaying that Pending retry
    # later uses its stored amount even after the dues change again.
    from app import seed
    from app.payments import run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    seed.set_dues(s6.communities["MR"], DUES_CENTS + 100)
    s6.fake.unavailable = True
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    run_due_payments(retry_day)
    seed.set_dues(s6.communities["MR"], DUES_CENTS + 200)
    s6.fake.unavailable = False
    run_due_payments(retry_day + timedelta(days=1))
    assert [(r["attempt"], r["amount_cents"]) for r in history(s6)] == [
        (1, DUES_CENTS), (2, DUES_CENTS + 100)]
    assert [call[1] for call in s6.fake.calls] == [
        DUES_CENTS, DUES_CENTS + 100, DUES_CENTS + 100]


def test_ac22_new_month_starts_again_at_attempt_1(s6):
    # D17, D25: after the last allowed attempt fails in December, January starts at
    # attempt 1 with its own key, and December keeps its attempts.
    from app.payments import run_due_payments

    _require_retries()
    maximum, delay = settings.MAX_PAYMENT_ATTEMPTS, settings.RETRY_DELAY_DAYS
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    for n in range(maximum):
        run_due_payments(FIRST + timedelta(days=n * delay))
    assert len(history(s6)) == maximum
    assert run_due_payments(date(2027, 1, DUE_DAY)).failed == 1
    assert _attempts(s6, month="2027-01") == [(1, "Failed")]
    assert s6.fake.calls[-1][2] == _key(s6, 1, month="2027-01")
    assert len(history(s6)) == maximum


def test_ac22_decline_is_not_retried_in_a_later_month(s6, monkeypatch):
    # D17, D25, D35 (OQ3 stays open): a decline on 2026-11-28 whose retry date falls in
    # December is never retried for November; December gets its own attempt 1.
    from app.payments import run_due_payments

    declined_day = date(2026, 11, 28)
    monkeypatch.setattr(settings, "RETRY_DELAY_DAYS", (date(2026, 12, 1) - declined_day).days)
    _require_retries()
    assert schedule(s6, day=28, token=DECLINED_TOKEN).status_code == 201
    assert run_due_payments(declined_day).failed == 1
    for today in (date(2026, 11, 29), date(2026, 11, 30), date(2026, 12, 1),
                  date(2026, 12, 28)):
        run_due_payments(today)
    assert _attempts(s6, month="2026-11") == [(1, "Failed")]
    assert _attempts(s6, month="2026-12") == [(1, "Failed")]


def test_ac22_failed_row_without_failed_on_is_never_retried(s6):
    # D35 (Prompt 55 decision 3): a Failed attempt stored without failed_on, as before the
    # migration, is never retried. It is built with app.db functions, so no SQL is added.
    from app.payments import RunResult, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    _record_attempt(s6, "Failed")
    for day in range(FIRST.day, 32):
        assert run_due_payments(date(2026, 12, day)) == RunResult()
    assert s6.fake.calls == []
    assert _attempts(s6) == [(1, "Failed")]


def test_ac22_init_db_again_keeps_payments_and_retry_still_works(s6):
    # D35 (Prompt 58 SF-7): the failed_on migration is repeatable. Running init_db() again
    # keeps an existing Failed payment and its failed_on, and the next eligible run retries it.
    from app import db
    from app.payments import RunResult, run_due_payments

    _require_retries()
    assert schedule(s6, token=DECLINED_TOKEN).status_code == 201
    run_due_payments(FIRST)
    before = history(s6)
    db.init_db()
    db.init_db()
    assert history(s6) == before
    assert _failed_on(s6) == FIRST.isoformat()
    retry_day = FIRST + timedelta(days=settings.RETRY_DELAY_DAYS)
    assert run_due_payments(retry_day) == RunResult(charged=0, failed=1, skipped=0)
    assert _attempts(s6) == [(1, "Failed"), (2, "Failed")]


def test_ac22_claim_refuses_an_attempt_beyond_max_attempts(s6):
    # D17, D35: under the lock, attempt 2 is refused when max_attempts allows only one
    # attempt, and inserted when it allows two, on the same eligible day.
    attempt = 2
    _failed_attempt_1(s6, FIRST)
    retry = {"today": FIRST + timedelta(days=settings.RETRY_DELAY_DAYS),
             "retry_delay_days": settings.RETRY_DELAY_DAYS}
    assert _claim(s6, attempt, max_attempts=attempt - 1, **retry) == (None, "Exists")
    assert _attempts(s6) == [(1, "Failed")]
    payment_id, conflict = _claim(s6, attempt, max_attempts=attempt, **retry)
    assert conflict is None and payment_id is not None
    assert _attempts(s6) == [(1, "Failed"), (2, "Pending")]


def test_ac22_claim_refuses_a_skipped_attempt_number(s6):
    # D17, D35: a retry must be the latest attempt + 1, so attempt 3 after a Failed attempt 1
    # is refused even when enough attempts are allowed; attempt 2 is then inserted.
    skipped = 3
    _failed_attempt_1(s6, FIRST)
    retry = {"today": FIRST + timedelta(days=settings.RETRY_DELAY_DAYS),
             "retry_delay_days": settings.RETRY_DELAY_DAYS, "max_attempts": skipped}
    assert _claim(s6, skipped, **retry) == (None, "Exists")
    assert _attempts(s6) == [(1, "Failed")]
    payment_id, conflict = _claim(s6, skipped - 1, **retry)
    assert conflict is None and payment_id is not None
    assert _attempts(s6) == [(1, "Failed"), (2, "Pending")]


@pytest.mark.parametrize("missing", ["today", "retry_delay_days", "max_attempts"])
def test_ac22_claim_retry_needs_every_retry_argument(s6, missing):
    # D35: a retry claim without today, retry_delay_days or max_attempts raises ValueError
    # before any database work, and nothing is stored.
    attempt = 2
    _failed_attempt_1(s6, FIRST)
    retry = {"today": FIRST + timedelta(days=settings.RETRY_DELAY_DAYS),
             "retry_delay_days": settings.RETRY_DELAY_DAYS, "max_attempts": attempt}
    retry[missing] = None
    with pytest.raises(ValueError):
        _claim(s6, attempt, **retry)
    assert _attempts(s6) == [(1, "Failed")]


def test_f11_finish_payment_never_overwrites_a_completed_payment(s6):
    # D4 (AGENT-03 F-11): only a Pending payment can be completed. Finishing a Paid or a
    # Failed payment again changes nothing and returns False.
    from app import db

    paid = _record_attempt(s6, "Paid")
    assert db.finish_payment(paid, "Failed", "late_result", "2026-12-09") is False
    assert _attempts(s6) == [(1, "Paid")]
    unit = s6.units["MR-20"]
    failed = db.create_pending_payment(
        unit, MONTH, DUES_CENTS, "debit", f"{unit}:{MONTH}:1", "2026-11-20T12:00:00Z")
    assert db.finish_payment(failed, "Failed", "first_result", "2026-12-05") is True
    assert db.finish_payment(failed, "Paid", "late_result") is False
    assert _attempts(s6, user="R3") == [(1, "Failed")]


def test_f11_agreeing_completion_is_left_unchanged_and_not_counted(s6, install_processor):
    # Prompt 56 decision 2 (F-11, D16): the row was already completed with the processor's
    # own result, so the run leaves it as it is and counts no second completion.
    from app.payments import RunResult, run_due_payments

    install_processor(_completing_processor("Paid"))
    assert schedule(s6).status_code == 201
    assert run_due_payments(FIRST) == RunResult()
    assert _attempts(s6) == [(1, "Paid")]
    assert _failed_on(s6) is None  # a date passed with Paid is not stored (D35)


@pytest.mark.parametrize("stored, token", [("Failed", GOOD_TOKEN), ("Paid", DECLINED_TOKEN)])
def test_f11_conflicting_completion_stops_the_run_without_overwriting(s6, install_processor,
                                                                      stored, token):
    # Prompt 56 decision 2 (F-11, D31; Prompt 58 SF-5): the row is already stored with the
    # opposite of the processor's result (Failed vs success, or Paid vs decline), so the run
    # stops with an error and the stored row, including its failed_on, is kept.
    from app.payments import run_due_payments

    install_processor(_completing_processor(stored))
    assert schedule(s6, token=token).status_code == 201
    with pytest.raises(RuntimeError, match="processor reported"):
        run_due_payments(FIRST)
    assert _attempts(s6) == [(1, stored)]
    assert _failed_on(s6) == (FIRST.isoformat() if stored == "Failed" else None)


def test_f01_locking_transactions_use_read_committed(s6, monkeypatch):
    # Prompt 56 decision 1: the scheduled claim and record_manual_payment open their
    # unit-lock transaction on a connection set to READ COMMITTED before its first query.
    import psycopg
    from app import db
    from app.payments import record_manual_payment, run_due_payments

    seen = []
    real_connect = db.connect_read_committed

    def spy():
        conn = real_connect()
        seen.append((conn.isolation_level, conn.info.transaction_status))
        return conn

    monkeypatch.setattr(db, "connect_read_committed", spy)
    record_manual_payment(s6.units["MR-20"], MONTH)
    assert schedule(s6).status_code == 201
    run_due_payments(FIRST)
    expected = (psycopg.IsolationLevel.READ_COMMITTED, psycopg.pq.TransactionStatus.IDLE)
    assert seen == [expected, expected]
    assert _attempts(s6) == [(1, "Paid")]
