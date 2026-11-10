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
