"""Bearer-token check (docs/design/S-1.md R2, D7, D8, D9)."""

import sqlite3

from fastapi import HTTPException, Request

PREFIX = "Bearer "


def _unauthenticated() -> HTTPException:
    return HTTPException(status_code=401, detail="Not authenticated")


def lookup_user(conn: sqlite3.Connection, header: str | None) -> sqlite3.Row:
    if header is None or not header.startswith(PREFIX):
        raise _unauthenticated()
    token = header[len(PREFIX):]
    if token == "" or token != token.strip() or " " in token:
        raise _unauthenticated()
    row = conn.execute("SELECT id, is_admin FROM users WHERE token = ?", (token,)).fetchone()
    if row is None:
        raise _unauthenticated()
    return row


def make_current_user(get_conn):
    def current_user(request: Request) -> sqlite3.Row:
        conn = get_conn()
        try:
            return lookup_user(conn, request.headers.get("authorization"))
        finally:
            conn.close()

    return current_user
