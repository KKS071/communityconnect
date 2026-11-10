"""Create communities, units, users and memberships (S-1 D13, D17). No endpoints use this.

Each function enforces the section 5 rules and raises ValueError on a violation."""

from app import db

ROLES = ("resident", "board_member", "manager", "admin")


def _insert(sql: str, params: tuple) -> int:
    db.init_db()
    conn = db.connect()
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    except Exception as exc:  # sqlite3.IntegrityError and friends
        raise ValueError(str(exc)) from exc
    finally:
        conn.close()


def create_community(name: str) -> int:
    if not isinstance(name, str) or not 1 <= len(name) <= 100:
        raise ValueError("name must be 1 to 100 characters")
    return _insert("INSERT INTO communities (name) VALUES (?)", (name,))


def create_unit(community_id: int, label: str) -> int:
    if not isinstance(label, str) or not 1 <= len(label) <= 20:
        raise ValueError("label must be 1 to 20 characters")
    return _insert("INSERT INTO units (community_id, label) VALUES (?, ?)", (community_id, label))


def create_user() -> int:
    return _insert("INSERT INTO users DEFAULT VALUES", ())


def add_membership(user_id: int, community_id: int, role: str, unit_id: int | None = None) -> None:
    if role not in ROLES:
        raise ValueError(f"role must be one of {ROLES}")
    if role == "resident":
        if unit_id is None:
            raise ValueError("a resident needs a unit")
        conn = db.connect()
        try:
            row = conn.execute("SELECT community_id FROM units WHERE id = ?", (unit_id,)).fetchone()
        finally:
            conn.close()
        if row is None or row["community_id"] != community_id:
            raise ValueError("the unit must be in the same community")
    _insert(
        "INSERT INTO memberships (user_id, community_id, role, unit_id) VALUES (?, ?, ?, ?)",
        (user_id, community_id, role, unit_id),
    )
