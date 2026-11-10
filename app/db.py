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
