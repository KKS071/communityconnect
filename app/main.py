"""CommunityConnect API service: S-1 submit and track a maintenance request (docs/design/S-1.md)."""

import json
import re
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app import db, settings
from app.access import NotFound, require_resident
from app.auth import current_user

_ID = re.compile(r"[1-9][0-9]*")
_MAX_ID = 9223372036854775807


class Invalid(Exception):
    """A 422 with a fixed message (S-1 section 4)."""

    def __init__(self, message: str):
        self.message = message


def _parse_id(raw: str) -> int:
    """Path ids (D14): anything else is 404 "Not found"."""
    if _ID.fullmatch(raw) and int(raw) <= _MAX_ID:
        return int(raw)
    raise NotFound()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # D5


def _out(row) -> dict:
    return {
        "id": row["id"],
        "community_id": row["community_id"],
        "unit_id": row["unit_id"],
        "category": row["category"],
        "description": row["description"],
        "status": row["status"],
        "created_at": row["created_at"],
    }


async def _json_object(request: Request) -> dict:
    try:
        body = json.loads(await request.body())
    except ValueError:
        raise Invalid("Invalid request body")
    if not isinstance(body, dict):
        raise Invalid("Invalid request body")
    return body


def create_app() -> FastAPI:
    db.init_db()
    app = FastAPI(title="CommunityConnect", redirect_slashes=False)

    @app.exception_handler(NotFound)
    async def _not_found(request: Request, exc: NotFound):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    @app.exception_handler(Invalid)
    async def _invalid(request: Request, exc: Invalid):
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.post("/communities/{community_id}/requests", status_code=201)
    async def submit_request(community_id: str, request: Request, user: int = Depends(current_user)):
        cid = _parse_id(community_id)
        conn = db.connect()
        try:
            membership = require_resident(conn, user, cid)  # R3
            body = await _json_object(request)
            category, description = body.get("category"), body.get("description")
            if not isinstance(category, str) or not isinstance(description, str):
                raise Invalid("Invalid request body")
            description = description.strip()  # D9
            if len(description) == 0:
                raise Invalid("Description is required")
            if len(description) > settings.MAX_DESCRIPTION_CHARS:
                raise Invalid("Description is too long")
            if category not in settings.REQUEST_CATEGORIES:  # D4: exact, case-sensitive
                raise Invalid("Unknown category")
            cur = conn.execute(
                "INSERT INTO requests (community_id, unit_id, submitted_by, category, description,"
                " status, created_at) VALUES (?, ?, ?, ?, ?, 'Open', ?)",
                (cid, membership["unit_id"], user, category, description, _now()),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM requests WHERE id = ?", (cur.lastrowid,)).fetchone()
            return _out(row)
        finally:
            conn.close()

    @app.get("/communities/{community_id}/requests")
    def list_requests(community_id: str, user: int = Depends(current_user)):
        cid = _parse_id(community_id)
        conn = db.connect()
        try:
            require_resident(conn, user, cid)  # D10, D19
            rows = conn.execute(
                "SELECT * FROM requests WHERE community_id = ? ORDER BY created_at DESC, id DESC",
                (cid,),
            ).fetchall()
            return [_out(r) for r in rows]
        finally:
            conn.close()

    @app.get("/requests/{request_id}")
    def get_request(request_id: str, user: int = Depends(current_user)):
        _parse_id(request_id)
        raise NotFound()  # fail closed until task 4

    return app


app = create_app()
