"""The one place where community access is decided (docs/design/S-1.md D4)."""

import sqlite3


class NotFound(Exception):
    """Raised for every 404: missing item, item in another community, or hidden item."""


def require_member(conn: sqlite3.Connection, user_id: int, community_id: int) -> str:
    """Return the caller's role in the community, or raise NotFound (R3)."""
    row = conn.execute(
        "SELECT role FROM memberships WHERE user_id = ? AND community_id = ?",
        (user_id, community_id),
    ).fetchone()
    if row is None:
        raise NotFound()
    return row["role"]


def communities_of(conn: sqlite3.Connection, user_id: int) -> list[sqlite3.Row]:
    """Communities the user is a member of, ordered by id (S-1 AC-4, D21)."""
    return conn.execute(
        "SELECT c.id, c.name FROM communities c"
        " JOIN memberships m ON m.community_id = c.id"
        " WHERE m.user_id = ? ORDER BY c.id",
        (user_id,),
    ).fetchall()
