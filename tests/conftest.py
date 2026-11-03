"""Shared fixtures. Data is inserted with plain SQL using the column names in
docs/design/S-1.md section 5, so the tests depend on the design doc, not on app code."""

import secrets
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

TS = "2026-10-01T12:00:00Z"  # format from S-1 D16


@dataclass
class World:
    db_path: str
    client: TestClient
    tokens: dict = field(default_factory=dict)   # user key -> token
    ids: dict = field(default_factory=dict)      # user key -> user id
    items: dict = field(default_factory=dict)    # item key -> id

    def headers(self, user_key):
        return {"Authorization": f"Bearer {self.tokens[user_key]}"}

    def get(self, path, user_key=None, headers=None):
        if headers is None:
            headers = self.headers(user_key) if user_key else {}
        return self.client.get(path, headers=headers)


# Communities: A=1, B=2, C=3
COMMUNITIES = {"A": 1, "B": 2, "C": 3}

# user key -> (is_admin, [(community, role), ...])
USERS = {
    "res_a": (0, [("A", "resident")]),
    "res_a2": (0, [("A", "resident")]),
    "board_a": (0, [("A", "board")]),
    "mgr_ac": (0, [("A", "manager"), ("C", "manager")]),
    "res_b": (0, [("B", "resident")]),
    "board_b": (0, [("B", "board")]),
    "mgr_b": (0, [("B", "manager")]),
    "res_c": (0, [("C", "resident")]),
    "mgr_c": (0, [("C", "manager")]),
    "admin": (1, []),
}

# Every text that belongs to community B contains this marker, so a test can
# check that no B data leaked by searching the raw response body.
B_MARK = "B-SECRET"


def _seed(conn, world):
    for name, cid in COMMUNITIES.items():
        conn.execute("INSERT INTO communities (id, name) VALUES (?, ?)", (cid, f"Community {name}"))
    for uid, (key, (is_admin, memberships)) in enumerate(USERS.items(), start=1):
        token = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO users (id, display_name, token, is_admin) VALUES (?, ?, ?, ?)",
            (uid, f"user {key}", token, is_admin),
        )
        for community, role in memberships:
            conn.execute(
                "INSERT INTO memberships (user_id, community_id, role) VALUES (?, ?, ?)",
                (uid, COMMUNITIES[community], role),
            )
        world.tokens[key] = token
        world.ids[key] = uid

    def ticket(key, community, creator, title):
        cur = conn.execute(
            "INSERT INTO tickets (community_id, created_by, title, category, status, created_at)"
            " VALUES (?, ?, ?, ?, 'open', ?)",
            (COMMUNITIES[community], world.ids[creator], title, "plumbing", TS),
        )
        world.items[key] = cur.lastrowid

    def document(key, community, folder, uploader, title):
        cur = conn.execute(
            "INSERT INTO documents (community_id, folder, title, uploaded_by, uploaded_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (COMMUNITIES[community], folder, title, world.ids[uploader], TS),
        )
        world.items[key] = cur.lastrowid

    def announcement(key, community, poster, title, posted_at=TS):
        cur = conn.execute(
            "INSERT INTO announcements (community_id, title, body, posted_by, posted_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (COMMUNITIES[community], title, f"Body of {title}", world.ids[poster], posted_at),
        )
        world.items[key] = cur.lastrowid

    ticket("ticket_a_res", "A", "res_a", "A leaky faucet")
    ticket("ticket_a_res2", "A", "res_a2", "A broken gate")
    ticket("ticket_b", "B", "res_b", f"{B_MARK} ticket roof leak")
    ticket("ticket_c", "C", "res_c", "C pool pump")
    document("doc_a", "A", "community", "board_a", "A bylaws")
    document("doc_a_board", "A", "board_only", "board_a", "A board minutes")
    document("doc_b", "B", "community", "board_b", f"{B_MARK} doc budget")
    announcement("ann_a", "A", "mgr_ac", "A pool opening")
    announcement("ann_b", "B", "mgr_b", f"{B_MARK} announcement")
    announcement("ann_c", "C", "mgr_ac", "C parking notice")


@pytest.fixture
def world(tmp_path):
    db_path = str(tmp_path / "test.db")
    app = create_app(db_path)
    w = World(db_path=db_path, client=TestClient(app))
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    _seed(conn, w)
    conn.commit()
    conn.close()
    return w


class FakeClock:
    """Settable UTC clock for S-2 (design doc S-2 section 4, D10)."""

    def __init__(self, now=None):
        self.now = now or datetime(2026, 10, 1, 12, 0, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.now
