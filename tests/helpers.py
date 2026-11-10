"""Test-only helpers (S-1 D13, D18). They connect with DATABASE_URL and DATABASE_SCHEMA directly
because the API does not expose these operations. Column names are the ones in
docs/design/S-1.md section 5."""

import psycopg

from app import settings


def _connect():
    return psycopg.connect(settings.DATABASE_URL,
                           options=f"-c search_path={settings.DATABASE_SCHEMA}")


def set_status(request_id: int, status: str) -> None:
    with _connect() as conn:
        cur = conn.execute("UPDATE requests SET status = %s WHERE id = %s", (status, request_id))
        assert cur.rowcount == 1, f"no request with id {request_id}"


def count_requests() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
