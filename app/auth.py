"""Who is calling (S-1 D1, D14)."""

import re

from fastapi import HTTPException, Request

from app import db

_USER_ID = re.compile(r"[1-9][0-9]*")
_MAX_ID = 9223372036854775807


def current_user(request: Request) -> int:
    """Return the caller's user id, or raise 401 "Unknown user"."""
    values = request.headers.getlist("x-user-id")
    if len(values) == 1 and _USER_ID.fullmatch(values[0]) and int(values[0]) <= _MAX_ID:
        user_id = int(values[0])
        conn = db.connect()
        try:
            found = conn.execute("SELECT 1 FROM users WHERE id = ?", (user_id,)).fetchone()
        finally:
            conn.close()
        if found:
            return user_id
    raise HTTPException(status_code=401, detail="Unknown user")
