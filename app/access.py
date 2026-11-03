"""The one place where community access is decided (docs/design/S-1.md D4)."""

import sqlite3


class NotFound(Exception):
    """Raised for every 404: missing item, item in another community, or hidden item."""


def require_member(conn: sqlite3.Connection, user_id: int, community_id: int) -> str:
    # Task 1: fail closed. Real check arrives in task 2.
    raise NotFound()
