"""SQLite connection and schema (docs/design/S-1.md sections 5, D11, D12)."""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id           INTEGER PRIMARY KEY CHECK (id >= 1),
    display_name TEXT    NOT NULL CHECK (length(display_name) BETWEEN 1 AND 100),
    token        TEXT    NOT NULL UNIQUE CHECK (length(token) >= 32),
    is_admin     INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0, 1))
);
CREATE TABLE IF NOT EXISTS communities (
    id   INTEGER PRIMARY KEY CHECK (id >= 1),
    name TEXT    NOT NULL UNIQUE CHECK (length(name) BETWEEN 1 AND 100)
);
CREATE TABLE IF NOT EXISTS memberships (
    user_id      INTEGER NOT NULL REFERENCES users(id),
    community_id INTEGER NOT NULL REFERENCES communities(id),
    role         TEXT    NOT NULL CHECK (role IN ('resident', 'board', 'manager')),
    PRIMARY KEY (user_id, community_id)
);
CREATE TABLE IF NOT EXISTS tickets (
    id           INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    created_by   INTEGER NOT NULL REFERENCES users(id),
    title        TEXT    NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
    category     TEXT    NOT NULL CHECK (length(category) BETWEEN 1 AND 50),
    status       TEXT    NOT NULL CHECK (status IN ('open', 'in_progress', 'resolved')),
    created_at   TEXT    NOT NULL
);
CREATE TABLE IF NOT EXISTS documents (
    id           INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    folder       TEXT    NOT NULL CHECK (folder IN ('community', 'board_only')),
    title        TEXT    NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
    uploaded_by  INTEGER NOT NULL REFERENCES users(id),
    uploaded_at  TEXT    NOT NULL
);
CREATE TABLE IF NOT EXISTS announcements (
    id           INTEGER PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES communities(id),
    title        TEXT    NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
    body         TEXT    NOT NULL CHECK (length(body) BETWEEN 1 AND 5000),
    posted_by    INTEGER NOT NULL REFERENCES users(id),
    posted_at    TEXT    NOT NULL
);
"""


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(db_path: str) -> None:
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()
