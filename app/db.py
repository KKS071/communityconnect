"""PostgreSQL storage (docs/design/S-1.md section 5, D12, D16)."""

from datetime import date, timedelta
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


def connect_read_committed() -> psycopg.Connection:
    """connect() with READ COMMITTED set before the first query (AGENT-03 F-01, AC-22).

    The unit-row-locking transactions re-read payments after FOR UPDATE; at READ COMMITTED
    that read sees rows another transaction committed while this one waited for the lock.
    """
    conn = connect()
    conn.isolation_level = psycopg.IsolationLevel.READ_COMMITTED
    return conn


def init_db() -> None:
    """Create DATABASE_SCHEMA and the section 5 tables if they are missing (D16)."""
    with connect() as conn:
        conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{_schema()}"')
        conn.execute(TABLES)
        conn.execute("ALTER TABLE communities ADD COLUMN IF NOT EXISTS dues_amount_cents "
                     "BIGINT CHECK (dues_amount_cents > 0)")
        # AC-22 (S-6 D35): additive, repeatable migration. failed_on is the `today` of the run
        # in which an attempt became Failed; it is NULL for every other row, including old ones.
        conn.execute("ALTER TABLE payments ADD COLUMN IF NOT EXISTS failed_on TEXT "
                     "CHECK (failed_on ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$')")


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
            "SELECT status, attempt, failed_on FROM payments WHERE unit_id = %s "
            "AND billing_month = %s ORDER BY attempt DESC, id DESC LIMIT 1", (unit_id, billing_month)
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


def claim_pending_payment(unit_id: int, billing_month: str, amount_cents: int,
                          method: str, key: str, created_at: str, attempt: int = 1,
                          today: date | None = None, retry_delay_days: int | None = None,
                          max_attempts: int | None = None) -> tuple[int | None, str | None]:
    """Insert a scheduled attempt as Pending only while the month allows it (D4, D17, D25).

    Locks the unit row, as create_manual_payment does, so a scheduled attempt and a manual
    payment for the same unit are serialized and each sees the other's committed row
    (AGENT-03 F-01; READ COMMITTED is set before the first query). Under the lock: any Paid
    payment gives (None, 'Paid') and any Pending payment gives (None, 'Exists'). Attempt 1
    needs no payment for the month. A retry, attempt N > 1, needs _retry_allowed (D17, D35).
    Otherwise (None, 'Exists'). The transaction commits before returning; the processor is
    called afterwards, outside it. Return (payment_id, None) when the attempt was inserted.
    """
    if attempt > 1 and None in (today, retry_delay_days, max_attempts):
        raise ValueError("A retry claim needs today, retry_delay_days and max_attempts")
    with connect_read_committed() as conn:
        unit = conn.execute(
            "SELECT id FROM units WHERE id = %s FOR UPDATE", (unit_id,)
        ).fetchone()
        if unit is None:
            raise ValueError("Unknown unit")
        states = conn.execute(
            "SELECT status, attempt, failed_on FROM payments "
            "WHERE unit_id = %s AND billing_month = %s ORDER BY attempt DESC, id DESC",
            (unit_id, billing_month),
        ).fetchall()
        if any(p["status"] == "Paid" for p in states):
            return None, "Paid"
        if any(p["status"] == "Pending" for p in states):
            return None, "Exists"
        if attempt == 1:
            if states:
                return None, "Exists"
        elif not _retry_allowed(states, attempt, today, retry_delay_days, max_attempts):
            return None, "Exists"
        row = conn.execute(
            "INSERT INTO payments (unit_id, billing_month, amount_cents, method, "
            "status, attempt, idempotency_key, processor_id, created_at) "
            "VALUES (%s, %s, %s, %s, 'Pending', %s, %s, NULL, %s) RETURNING id",
            (unit_id, billing_month, amount_cents, method, attempt, key, created_at),
        ).fetchone()
        return row["id"], None


def _retry_allowed(states: list[dict], attempt: int, today: date, retry_delay_days: int,
                   max_attempts: int) -> bool:
    """D17 eligibility for retry attempt `attempt`, checked under the unit lock (D35).

    `states` are the month's payments, latest attempt first. The latest must be attempt - 1
    and Failed with a failed_on date at least retry_delay_days before today, and attempt
    must not exceed max_attempts. A Failed row without failed_on is never retried.
    """
    if not states or attempt > max_attempts:
        return False
    latest = states[0]
    if latest["status"] != "Failed" or latest["attempt"] != attempt - 1:
        return False
    if latest["failed_on"] is None:
        return False
    return date.fromisoformat(latest["failed_on"]) + timedelta(days=retry_delay_days) <= today


def finish_payment(payment_id: int, status: str, processor_id: str,
                   failed_on: str | None = None) -> bool:
    """Complete a Pending payment as Paid or Failed (D4, D17; AGENT-03 F-11).

    Only a Pending row changes, so a completed payment is never overwritten. failed_on is
    the `today` (YYYY-MM-DD) of the run in which the attempt became Failed; it is stored
    only for Failed. The run always passes it; it defaults to None only for older callers
    such as test helpers. Return True if the row changed.
    """
    with connect() as conn:
        cur = conn.execute(
            "UPDATE payments SET status = %s, processor_id = %s, failed_on = %s "
            "WHERE id = %s AND status = 'Pending'",
            (status, processor_id, failed_on if status == "Failed" else None, payment_id),
        )
        return cur.rowcount == 1


def payment_status(payment_id: int) -> str | None:
    """The stored status of one payment, or None if it does not exist (AGENT-03 F-11)."""
    with connect() as conn:
        row = conn.execute(
            "SELECT status FROM payments WHERE id = %s", (payment_id,)
        ).fetchone()
        return None if row is None else row["status"]



def pending_payments() -> list[dict]:
    """All Pending payments, including original amount, key and schedule token."""
    with connect() as conn:
        return conn.execute(
            "SELECT p.id, p.unit_id, p.billing_month, p.amount_cents, p.method, "
            "p.idempotency_key, s.token "
            "FROM payments p JOIN schedules s ON s.unit_id = p.unit_id "
            "WHERE p.status = 'Pending' ORDER BY p.id"
        ).fetchall()


def has_paid_payment(unit_id: int, billing_month: str) -> bool:
    """Protect a Paid month when an older Pending row exists (D26/OQ5)."""
    with connect() as conn:
        return conn.execute(
            "SELECT 1 FROM payments WHERE unit_id = %s AND billing_month = %s "
            "AND status = 'Paid' LIMIT 1",
            (unit_id, billing_month),
        ).fetchone() is not None


def create_manual_payment(unit_id: int, billing_month: str, created_at: str) -> tuple[dict | None, str | None]:
    """Atomically check payment state and insert manual Paid payment (D13/D27).

    Return (payment, None), or (None, 'Paid'/'Pending') for conflicts.
    Lock the unit row to serialize manual entries for the same unit. A single
    payment runner remains the design's operational assumption (D32).
    """
    with connect_read_committed() as conn:  # READ COMMITTED before the first query (F-01)
        unit = conn.execute(
            "SELECT c.dues_amount_cents FROM units u "
            "JOIN communities c ON c.id = u.community_id "
            "WHERE u.id = %s FOR UPDATE OF u", (unit_id,),
        ).fetchone()
        if unit is None:
            raise ValueError("Unknown unit")
        if unit["dues_amount_cents"] is None:
            raise ValueError("Dues amount is not configured")

        states = conn.execute(
            "SELECT status FROM payments WHERE unit_id = %s AND billing_month = %s",
            (unit_id, billing_month),
        ).fetchall()
        if any(p["status"] == "Paid" for p in states):
            return None, "Paid"
        if any(p["status"] == "Pending" for p in states):
            return None, "Pending"

        key = f"{unit_id}:{billing_month}:manual"
        row = conn.execute(
            "INSERT INTO payments (unit_id, billing_month, amount_cents, method, "
            "status, attempt, idempotency_key, processor_id, created_at) "
            "VALUES (%s, %s, %s, 'manual', 'Paid', 1, %s, NULL, %s) "
            "RETURNING *",
            (unit_id, billing_month, unit["dues_amount_cents"], key, created_at),
        ).fetchone()
        return row, None
