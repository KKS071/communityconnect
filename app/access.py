"""Membership and role checks. The only module that reads `memberships` (AGENTS.md)."""

import psycopg


class NotFound(Exception):
    """Every hidden or missing record (S-1 R2, D3). Turned into 404 {"detail": "Not found"}."""


def require_member(conn: psycopg.Connection, user_id: int, community_id: int) -> dict:
    row = conn.execute(
        "SELECT * FROM memberships WHERE user_id = %s AND community_id = %s", (user_id, community_id)
    ).fetchone()
    if row is None:
        raise NotFound()
    return row


def require_resident(conn: psycopg.Connection, user_id: int, community_id: int) -> dict:
    """Return the caller's resident membership (with its unit_id), or raise NotFound (R3, D10)."""
    row = require_member(conn, user_id, community_id)
    if row["role"] != "resident":
        raise NotFound()
    return row


def require_payment_viewer(conn: psycopg.Connection, user_id: int,
                           community_id: int) -> int | None:
    """Decide who may list a community's payments (S-6 D8, D23; AGENT-03 F-05).

    Return the caller's unit_id for a resident (their own unit only), or None for a manager
    (every unit in the community; the caller's query must still filter by community_id).
    Raise NotFound for everyone else: admins, non-members and, until OQ4 is answered, board
    members. This keeps main.py's pre-F-05 resident/manager rule and does not decide OQ4,
    with one change: a resident membership with no unit (seed.py rejects it, the schema
    allows it) now gets NotFound instead of an empty list, so None never reaches a resident.
    """
    row = require_member(conn, user_id, community_id)
    if row["role"] == "resident" and row["unit_id"] is not None:
        return row["unit_id"]
    if row["role"] == "manager":
        return None
    raise NotFound()
