"""CommunityConnect API service (docs/design/S-1.md)."""

import os
from collections.abc import Callable, Iterator
from datetime import datetime

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app import db
from app.access import NotFound, require_member
from app.auth import make_current_user


def create_app(db_path: str, clock: Callable[[], datetime] | None = None) -> FastAPI:
    # `clock` is unused by S-1; kept so the skipped S-2 tests import cleanly (plan, approved).
    db.init_schema(db_path)

    def get_conn():
        return db.connect(db_path)

    current_user = make_current_user(get_conn)

    def conn_dep() -> Iterator:
        conn = get_conn()
        try:
            yield conn
        finally:
            conn.close()

    app = FastAPI(title="CommunityConnect", redirect_slashes=False)
    app.state.clock = clock

    @app.exception_handler(NotFound)
    async def not_found_handler(request: Request, exc: NotFound):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    @app.get("/me/communities")
    def my_communities(user=Depends(current_user), conn=Depends(conn_dep)):
        raise NotFound()

    @app.get("/communities/{community_id}/tickets")
    def list_tickets(community_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        role = require_member(conn, user["id"], community_id)
        return _tickets_visible(conn, user["id"], role, community_id)

    @app.get("/tickets/{ticket_id}")
    def get_ticket(ticket_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        row = _load(conn, "SELECT * FROM tickets WHERE id = ?", ticket_id)
        role = require_member(conn, user["id"], row["community_id"])
        if role != "manager" and row["created_by"] != user["id"]:  # R5
            raise NotFound()
        return _ticket(row)

    @app.get("/communities/{community_id}/documents")
    def list_documents(community_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        require_member(conn, user["id"], community_id)
        rows = conn.execute(
            "SELECT * FROM documents WHERE community_id = ? AND folder = 'community' ORDER BY id",
            (community_id,),
        ).fetchall()
        return [_document(r) for r in rows]

    @app.get("/documents/{document_id}")
    def get_document(document_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        row = _load(conn, "SELECT * FROM documents WHERE id = ? AND folder = 'community'", document_id)
        require_member(conn, user["id"], row["community_id"])
        return _document(row)

    @app.get("/communities/{community_id}/announcements")
    def list_announcements(community_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        require_member(conn, user["id"], community_id)
        rows = conn.execute(
            "SELECT * FROM announcements WHERE community_id = ? ORDER BY posted_at DESC, id ASC",
            (community_id,),
        ).fetchall()
        return [_announcement(r) for r in rows]

    @app.get("/announcements/{announcement_id}")
    def get_announcement(announcement_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        row = _load(conn, "SELECT * FROM announcements WHERE id = ?", announcement_id)
        require_member(conn, user["id"], row["community_id"])
        return _announcement(row)

    return app


def _load(conn, sql: str, item_id: int):
    """Load one item by ID or raise NotFound (D14: item first, then require_member)."""
    row = conn.execute(sql, (item_id,)).fetchone()
    if row is None:
        raise NotFound()
    return row


def _tickets_visible(conn, user_id: int, role: str, community_id: int) -> list[dict]:
    # R5 / D5: managers see every ticket; residents and board members only their own.
    if role == "manager":
        rows = conn.execute(
            "SELECT * FROM tickets WHERE community_id = ? ORDER BY id", (community_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tickets WHERE community_id = ? AND created_by = ? ORDER BY id",
            (community_id, user_id),
        ).fetchall()
    return [_ticket(r) for r in rows]


def _ticket(r) -> dict:
    return {k: r[k] for k in ("id", "community_id", "created_by", "title", "category", "status", "created_at")}


def _document(r) -> dict:
    return {k: r[k] for k in ("id", "community_id", "folder", "title", "uploaded_by", "uploaded_at")}


def _announcement(r) -> dict:
    return {k: r[k] for k in ("id", "community_id", "title", "body", "posted_by", "posted_at")}


app = create_app(os.environ.get("COMMUNITYCONNECT_DB", "communityconnect.db"))
