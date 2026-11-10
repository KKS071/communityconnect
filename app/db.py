"""SQLite storage (docs/design/S-1.md section 5, D12, D16)."""

import sqlite3

from app import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS communities (
    id   INTEGER PRIMARY KEY AUTOINCREMENT CHECK (id >= 1),
    name TEXT NOT NULL UNIQUE CHECK (length(name) BETWEEN 1 AND 100)
);
CREATE TABLE IF NOT EXISTS units (
    id           INTEGER PRIMARY KEY AUTOINCREMENT CHECK (id >= 1),
    community_id INTEGER NOT NULL REFERENCES communities(id),
    label        TEXT NOT NULL CHECK (length(label) BETWEEN 1 AND 20),
    UNIQUE (community_id, label)
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT CHECK (id >= 1)
);
CREATE TABLE IF NOT EXISTS memberships (
    user_id      INTEGER NOT NULL REFERENCES users(id),
    community_id INTEGER NOT NULL REFERENCES communities(id),
    role         TEXT NOT NULL CHECK (role IN ('resident', 'board_member', 'manager', 'admin')),
    unit_id      INTEGER REFERENCES units(id),
    PRIMARY KEY (user_id, community_id)
);
CREATE TABLE IF NOT EXISTS requests (
    id           INTEGER PRIMARY KEY AUTOINCREMENT CHECK (id >= 1),
    community_id INTEGER NOT NULL REFERENCES communities(id),
    unit_id      INTEGER NOT NULL REFERENCES units(id),
    submitted_by INTEGER NOT NULL REFERENCES users(id),
    category     TEXT NOT NULL,
    description  TEXT NOT NULL CHECK (length(description) >= 1),
    status       TEXT NOT NULL CHECK (status IN ('Open', 'In progress', 'Resolved')),
    created_at   TEXT NOT NULL
);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = connect()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
