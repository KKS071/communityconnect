"""PostgreSQL storage (docs/design/S-1.md section 5, D12, D16)."""

import re

import psycopg
from psycopg.rows import dict_row

from app import settings

_SCHEMA_NAME = re.compile(r"[a-z_][a-z0-9_]*")

TABLES = """
CREATE TABLE IF NOT EXISTS communities (
    id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (char_length(name) BETWEEN 1 AND 100)
);
CREATE TABLE IF NOT EXISTS units (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    community_id BIGINT NOT NULL REFERENCES communities(id),
    label        TEXT NOT NULL CHECK (char_length(label) BETWEEN 1 AND 20),
    UNIQUE (community_id, label)
);
CREATE TABLE IF NOT EXISTS users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS memberships (
    user_id      BIGINT NOT NULL REFERENCES users(id),
    community_id BIGINT NOT NULL REFERENCES communities(id),
    role         TEXT NOT NULL CHECK (role IN ('resident', 'board_member', 'manager', 'admin')),
    unit_id      BIGINT REFERENCES units(id),
    PRIMARY KEY (user_id, community_id)
);
CREATE TABLE IF NOT EXISTS requests (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    community_id BIGINT NOT NULL REFERENCES communities(id),
    unit_id      BIGINT NOT NULL REFERENCES units(id),
    submitted_by BIGINT NOT NULL REFERENCES users(id),
    category     TEXT NOT NULL,
    description  TEXT NOT NULL CHECK (char_length(description) >= 1),
    status       TEXT NOT NULL CHECK (status IN ('Open', 'In progress', 'Resolved')),
    created_at   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS schedules (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    unit_id      BIGINT NOT NULL UNIQUE REFERENCES units(id),
    method       TEXT NOT NULL CHECK (method IN ('ach', 'debit', 'credit')),
    day_of_month INTEGER NOT NULL CHECK (day_of_month BETWEEN 1 AND 28),
    token        TEXT NOT NULL CHECK (char_length(btrim(token)) > 0),
    active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS payments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    unit_id         BIGINT NOT NULL REFERENCES units(id),
    billing_month   TEXT NOT NULL CHECK (billing_month ~ '^[0-9]{4}-(0[1-9]|1[0-2])$'),
    amount_cents    BIGINT NOT NULL CHECK (amount_cents > 0),
    method          TEXT NOT NULL CHECK (method IN ('ach', 'debit', 'credit', 'manual')),
    status          TEXT NOT NULL CHECK (status IN ('Pending', 'Paid', 'Failed')),
    attempt         INTEGER NOT NULL CHECK (attempt >= 1),
    idempotency_key TEXT NOT NULL UNIQUE,
    processor_id    TEXT,
    created_at      TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS payments_one_paid_per_unit_month
    ON payments (unit_id, billing_month) WHERE status = 'Paid';
"""


def _schema() -> str:
    name = settings.DATABASE_SCHEMA
    if not _SCHEMA_NAME.fullmatch(name):
        raise ValueError(f"invalid DATABASE_SCHEMA: {name!r}")
    return name


def connect() -> psycopg.Connection:
    """A new connection whose rows are dicts. Use it in a `with` block: it commits on success,
    rolls back on an exception, and closes (D16)."""
    return psycopg.connect(
        settings.DATABASE_URL,
        options=f"-c search_path={_schema()}",
        row_factory=dict_row,
    )


def init_db() -> None:
    """Create DATABASE_SCHEMA and the section 5 tables if they are missing (D16)."""
    with connect() as conn:
        conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{_schema()}"')
        conn.execute(TABLES)
        conn.execute("ALTER TABLE communities ADD COLUMN IF NOT EXISTS dues_amount_cents "
                     "BIGINT CHECK (dues_amount_cents > 0)")


def due_schedules() -> list[dict]:
    """Active schedules with configured dues, in deterministic order."""
    with connect() as conn:
        return conn.execute(
            "SELECT s.unit_id, s.method, s.day_of_month, s.token, s.created_at, "
            "c.dues_amount_cents FROM schedules s "
            "JOIN units u ON u.id = s.unit_id "
            "JOIN communities c ON c.id = u.community_id "
            "WHERE s.active = TRUE AND c.dues_amount_cents IS NOT NULL "
            "ORDER BY s.unit_id"
        ).fetchall()


def latest_payment(unit_id: int, billing_month: str) -> dict | None:
    with connect() as conn:
        return conn.execute(
            "SELECT status FROM payments WHERE unit_id = %s AND billing_month = %s "
            "ORDER BY attempt DESC, id DESC LIMIT 1", (unit_id, billing_month)
        ).fetchone()


def create_pending_payment(unit_id: int, billing_month: str, amount_cents: int,
                           method: str, key: str, created_at: str) -> int:
    with connect() as conn:
        row = conn.execute(
            "INSERT INTO payments (unit_id, billing_month, amount_cents, method, "
            "status, attempt, idempotency_key, processor_id, created_at) "
            "VALUES (%s, %s, %s, %s, 'Pending', 1, %s, NULL, %s) RETURNING id",
            (unit_id, billing_month, amount_cents, method, key, created_at),
        ).fetchone()
        return row["id"]


def finish_payment(payment_id: int, status: str, processor_id: str) -> None:
    with connect() as conn:
        conn.execute(
            "UPDATE payments SET status = %s, processor_id = %s WHERE id = %s",
            (status, processor_id, payment_id),
        )
