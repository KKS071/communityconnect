"""CommunityConnect API service: S-1 maintenance requests (docs/design/S-1.md) and the
S-6 payment schedule and payment history endpoints (docs/design/S-6.md)."""

import json
import re
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

from app import clock, db, settings
from app.access import NotFound, require_payment_viewer, require_resident
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


def _schedule_out(row) -> dict:
    """Never include the stored payment token in API output (S-6 section 5)."""
    return {
        "id": row["id"],
        "unit_id": row["unit_id"],
        "method": row["method"],
        "day_of_month": row["day_of_month"],
        "active": row["active"],
    }


def create_app() -> FastAPI:
    db.init_db()
    app = FastAPI(title="CommunityConnect", redirect_slashes=False)

    @app.exception_handler(NotFound)
    async def _not_found(request: Request, exc: NotFound):
        return JSONResponse(status_code=404, content={"detail": "Not found"})

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException):
        # D21: unknown paths use the same 404 body as hidden records; other framework
        # errors (405, the 401 from app.auth) keep their {"detail": ...} message.
        detail = "Not found" if exc.status_code == 404 else exc.detail
        return JSONResponse(status_code=exc.status_code, content={"detail": detail},
                            headers=getattr(exc, "headers", None))

    @app.exception_handler(Invalid)
    async def _invalid(request: Request, exc: Invalid):
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.post("/communities/{community_id}/requests", status_code=201)
    async def submit_request(community_id: str, request: Request, user: int = Depends(current_user)):
        cid = _parse_id(community_id)
        with db.connect() as conn:
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
            row = conn.execute(
                "INSERT INTO requests (community_id, unit_id, submitted_by, category, description,"
                " status, created_at) VALUES (%s, %s, %s, %s, %s, 'Open', %s) RETURNING *",
                (cid, membership["unit_id"], user, category, description, _now()),
            ).fetchone()
            return _out(row)

    @app.get("/communities/{community_id}/requests")
    def list_requests(community_id: str, user: int = Depends(current_user)):
        cid = _parse_id(community_id)
        with db.connect() as conn:
            require_resident(conn, user, cid)  # D10, D19
            rows = conn.execute(
                "SELECT * FROM requests WHERE community_id = %s AND submitted_by = %s"
                " ORDER BY created_at DESC, id DESC",  # D2, D11
                (cid, user),
            ).fetchall()
            return [_out(r) for r in rows]

    @app.get("/requests/{request_id}")
    def get_request(request_id: str, user: int = Depends(current_user)):
        rid = _parse_id(request_id)
        with db.connect() as conn:
            row = conn.execute("SELECT * FROM requests WHERE id = %s", (rid,)).fetchone()
            if row is None:
                raise NotFound()
            require_resident(conn, user, row["community_id"])
            if row["submitted_by"] != user:  # R1: hidden answers like missing (R2)
                raise NotFound()
            return _out(row)

    @app.post("/communities/{community_id}/payment-schedules", status_code=201)
    async def create_payment_schedule(
        community_id: str, request: Request, user: int = Depends(current_user)
    ):
        cid = _parse_id(community_id)
        with db.connect() as conn:
            membership = require_resident(conn, user, cid)  # S-6 D7, D22
            body = await _json_object(request)
            method = body.get("method")
            day = body.get("day_of_month")
            token = body.get("token")
            # D12/D21: validate shape/types first, then values in field order.
            if (not isinstance(method, str) or type(day) is not int
                    or not isinstance(token, str)):
                raise Invalid("Invalid request body")
            if method not in ("ach", "debit", "credit"):
                raise Invalid("Unknown method")
            if not 1 <= day <= 28:
                raise Invalid("Day must be 1 to 28")
            if not token.strip():
                raise Invalid("Token is required")
            # D22: duplicate check follows validation, even if the unit already has a schedule.
            existing = conn.execute(
                "SELECT id FROM schedules WHERE unit_id = %s", (membership["unit_id"],)
            ).fetchone()
            if existing is not None:
                return JSONResponse(status_code=409,
                                    content={"detail": "Schedule already exists"})
            row = conn.execute(
                "INSERT INTO schedules (unit_id, method, day_of_month, token, active, created_at)"
                " VALUES (%s, %s, %s, %s, TRUE, %s) RETURNING *",
                (membership["unit_id"], method, day, token,
                 clock.now().strftime("%Y-%m-%dT%H:%M:%SZ")),
            ).fetchone()
            return _schedule_out(row)

    @app.get("/communities/{community_id}/payment-schedules/mine")
    def get_my_payment_schedule(community_id: str, user: int = Depends(current_user)):
        cid = _parse_id(community_id)
        with db.connect() as conn:
            membership = require_resident(conn, user, cid)
            row = conn.execute(
                "SELECT * FROM schedules WHERE unit_id = %s", (membership["unit_id"],)
            ).fetchone()
            if row is None:
                raise NotFound()
            return _schedule_out(row)

    @app.get("/communities/{community_id}/payments")
    def list_payments(community_id: str, month: str | None = None,
                      user: int = Depends(current_user)):
        cid = _parse_id(community_id)
        with db.connect() as conn:
            unit_id = require_payment_viewer(conn, user, cid)  # S-6 D8/D23 decided in access.py
            if month is None or re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", month) is None:
                raise Invalid("Invalid month")
            query = (
                "SELECT p.id, p.unit_id, p.billing_month, p.amount_cents, p.method, "
                "p.status, p.attempt, p.created_at FROM payments p "
                "JOIN units u ON u.id = p.unit_id "
                "WHERE u.community_id = %s AND p.billing_month = %s"
            )
            params: tuple = (cid, month)
            if unit_id is not None:  # a resident: only their own unit (D8)
                query += " AND p.unit_id = %s"
                params += (unit_id,)
            query += " ORDER BY p.unit_id, p.attempt, p.id"
            return conn.execute(query, params).fetchall()

    return app



_app = None


def __getattr__(name: str):
    """`app.main:app` for uvicorn (D16), built on first use so that importing this module
    does not need a running database."""
    global _app
    if name == "app":
        if _app is None:
            _app = create_app()
        return _app
    raise AttributeError(name)
