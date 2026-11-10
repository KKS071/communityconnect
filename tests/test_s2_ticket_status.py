"""S-2 Ticket status lifecycle: tests written from AC-6..AC-12 in docs/design/S-2.md.
S-2 is not built in Milestone 1, so every test is skipped with its AC ID in the reason.
Do not delete or weaken these; unskip them when S-2 is built."""

import sqlite3
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from conftest import FakeClock, World, _seed

NOT_FOUND = {"detail": "Not found"}


def skip_until_built(ac_id):
    return pytest.mark.skip(reason=f"{ac_id}: S-2 (ticket status lifecycle) not built in Milestone 1")


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def s2(tmp_path, clock):
    db_path = str(tmp_path / "s2.db")
    app = create_app(db_path, clock=clock)
    w = World(db_path=db_path, client=TestClient(app))
    conn = sqlite3.connect(db_path)
    _seed(conn, w)
    conn.commit()
    conn.close()
    return w


@pytest.fixture
def window_days():
    from app import settings
    return settings.REOPEN_WINDOW_DAYS


def set_status(w, user, ticket_key, status):
    return w.client.post(
        f"/tickets/{w.items[ticket_key]}/status", json={"status": status}, headers=w.headers(user)
    )


def reopen(w, user, ticket_key):
    return w.client.post(f"/tickets/{w.items[ticket_key]}/reopen", headers=w.headers(user))


def view(w, user, ticket_key):
    return w.get(f"/tickets/{w.items[ticket_key]}", user)


def history_pairs(resp):
    return [(h["from_status"], h["to_status"]) for h in resp.json()["history"]]


@skip_until_built("AC-6")
def test_ac6_manager_starts_ticket_resident_sees_in_progress(s2, clock):
    assert set_status(s2, "mgr_ac", "ticket_a_res", "in_progress").status_code == 200
    seen = view(s2, "res_a", "ticket_a_res")
    assert seen.json()["status"] == "in_progress"
    assert history_pairs(seen) == [("open", "in_progress")]
    assert seen.json()["history"][0]["changed_at"] == clock.now.strftime("%Y-%m-%dT%H:%M:%SZ")


@skip_until_built("AC-7")
def test_ac7_manager_resolves_ticket_resident_sees_resolved(s2):
    set_status(s2, "mgr_ac", "ticket_a_res", "in_progress")
    assert set_status(s2, "mgr_ac", "ticket_a_res", "resolved").status_code == 200
    seen = view(s2, "res_a", "ticket_a_res")
    assert seen.json()["status"] == "resolved"
    assert history_pairs(seen)[-1] == ("in_progress", "resolved")


@skip_until_built("AC-8")
def test_ac8_skipping_in_progress_is_refused(s2):
    resp = set_status(s2, "mgr_ac", "ticket_a_res", "resolved")
    assert resp.status_code == 409
    assert view(s2, "res_a", "ticket_a_res").json()["status"] == "open"


@skip_until_built("AC-9")
def test_ac9_resident_cannot_advance_ticket(s2):
    resp = set_status(s2, "res_a", "ticket_a_res", "in_progress")
    assert resp.status_code == 403
    assert view(s2, "res_a", "ticket_a_res").json()["status"] == "open"


@skip_until_built("AC-10")
def test_ac10_reopen_within_window(s2, clock, window_days):
    set_status(s2, "mgr_ac", "ticket_a_res", "in_progress")
    set_status(s2, "mgr_ac", "ticket_a_res", "resolved")
    clock.now += timedelta(days=window_days) - timedelta(seconds=1)
    assert reopen(s2, "res_a", "ticket_a_res").status_code == 200
    seen = view(s2, "res_a", "ticket_a_res").json()
    assert seen["status"] == "open"
    last = seen["history"][-1]
    assert (last["from_status"], last["to_status"], last["kind"]) == ("resolved", "open", "reopen")
    assert last["changed_by"] == s2.ids["res_a"]


@skip_until_built("AC-11")
def test_ac11_reopen_after_window_refused(s2, clock, window_days):
    set_status(s2, "mgr_ac", "ticket_a_res", "in_progress")
    set_status(s2, "mgr_ac", "ticket_a_res", "resolved")
    clock.now += timedelta(days=window_days)
    resp = reopen(s2, "res_a", "ticket_a_res")
    assert resp.status_code == 409
    assert resp.json() == {"detail": "Reopen window has passed"}
    assert view(s2, "res_a", "ticket_a_res").json()["status"] == "resolved"


@skip_until_built("AC-12")
def test_ac12_manager_of_other_community_gets_404(s2):
    resp = set_status(s2, "mgr_c", "ticket_a_res", "in_progress")
    assert resp.status_code == 404 and resp.json() == NOT_FOUND
    assert view(s2, "mgr_ac", "ticket_a_res").json()["status"] == "open"
