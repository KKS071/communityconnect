"""Create communities, units, users and memberships (S-1 D13, D17). No endpoints use this.

Each function enforces the section 5 rules and raises ValueError on a violation."""

import psycopg

from app import db

ROLES = ("resident", "board_member", "manager", "admin")


def _insert(sql: str, params: tuple) -> int | None:
    db.init_db()
    try:
        with db.connect() as conn:
            cur = conn.execute(sql, params)
            row = cur.fetchone() if cur.description else None  # memberships return nothing
            return row["id"] if row else None
    except psycopg.Error as exc:  # unique, foreign-key and check violations
        raise ValueError(str(exc)) from exc


def create_community(name: str) -> int:
    if not isinstance(name, str) or not 1 <= len(name) <= 100:
        raise ValueError("name must be 1 to 100 characters")
    return _insert("INSERT INTO communities (name) VALUES (%s) RETURNING id", (name,))


def create_unit(community_id: int, label: str) -> int:
    if not isinstance(label, str) or not 1 <= len(label) <= 20:
        raise ValueError("label must be 1 to 20 characters")
    return _insert(
        "INSERT INTO units (community_id, label) VALUES (%s, %s) RETURNING id", (community_id, label)
    )


def create_user() -> int:
    return _insert("INSERT INTO users DEFAULT VALUES RETURNING id", ())


def add_membership(user_id: int, community_id: int, role: str, unit_id: int | None = None) -> None:
    if role not in ROLES:
        raise ValueError(f"role must be one of {ROLES}")
    if role == "resident":
        if unit_id is None:
            raise ValueError("a resident needs a unit")
        db.init_db()
        with db.connect() as conn:
            row = conn.execute("SELECT community_id FROM units WHERE id = %s", (unit_id,)).fetchone()
        if row is None or row["community_id"] != community_id:
            raise ValueError("the unit must be in the same community")
    _insert(
        "INSERT INTO memberships (user_id, community_id, role, unit_id) VALUES (%s, %s, %s, %s)",
        (user_id, community_id, role, unit_id),
    )


def set_dues(community_id: int, dues_amount_cents: int) -> None:
    """Set positive monthly dues in integer cents (S-6 D14, D30)."""
    if type(dues_amount_cents) is not int or dues_amount_cents <= 0:
        raise ValueError("dues_amount_cents must be a positive integer")
    db.init_db()
    with db.connect() as conn:
        row = conn.execute(
            "UPDATE communities SET dues_amount_cents = %s WHERE id = %s RETURNING id",
            (dues_amount_cents, community_id),
        ).fetchone()
        if row is None:
            raise ValueError("unknown community")
