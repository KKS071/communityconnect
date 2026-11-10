"""Test-only helpers (S-1 D13, D18). They open DATABASE_PATH directly because the API does
not expose these operations. Column names are the ones in docs/design/S-1.md section 5."""

import sqlite3

from app import settings


def _connect():
    return sqlite3.connect(settings.DATABASE_PATH)


def set_status(request_id: int, status: str) -> None:
    conn = _connect()
    try:
        cur = conn.execute("UPDATE requests SET status = ? WHERE id = ?", (status, request_id))
        assert cur.rowcount == 1, f"no request with id {request_id}"
        conn.commit()
    finally:
        conn.close()


def count_requests() -> int:
    conn = _connect()
    try:
        return conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    finally:
        conn.close()
