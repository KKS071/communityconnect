"""CommunityConnect API service (docs/design/S-1.md)."""

import os
from collections.abc import Callable, Iterator
from datetime import datetime

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app import db
from app.access import NotFound
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
        raise NotFound()

    @app.get("/tickets/{ticket_id}")
    def get_ticket(ticket_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        raise NotFound()

    @app.get("/communities/{community_id}/documents")
    def list_documents(community_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        raise NotFound()

    @app.get("/documents/{document_id}")
    def get_document(document_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        raise NotFound()

    @app.get("/communities/{community_id}/announcements")
    def list_announcements(community_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        raise NotFound()

    @app.get("/announcements/{announcement_id}")
    def get_announcement(announcement_id: int, user=Depends(current_user), conn=Depends(conn_dep)):
        raise NotFound()

    return app


app = create_app(os.environ.get("COMMUNITYCONNECT_DB", "communityconnect.db"))
