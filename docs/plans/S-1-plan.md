# S-1 Community isolation: build plan

- Written by: Claude Opus 5.5 (AI coding tool), 2026-11-03, before any file in `app/` existed.
- Source of truth: `docs/design/S-1.md` (after gap check, commit `7a94c87`).
- Tests that must pass: `tests/test_s1_community_isolation.py` (written first, commit `7a94c87`).
- Approval: see the "Approval" section at the end. No task starts before it is filled in.

## How

**Files that change** (all new; nothing outside `app/` is touched):

| File | What it holds |
|---|---|
| `app/__init__.py` | empty package marker |
| `app/settings.py` | named settings; S-1 needs none yet, but S-2's `REOPEN_WINDOW_DAYS` placeholder lives here (D5 of S-2) so the skipped S-2 tests can import it |
| `app/db.py` | `connect(db_path) -> sqlite3.Connection` (foreign keys on, `sqlite3.Row` rows) and `init_schema(conn)` with the six tables from §5, using `CREATE TABLE IF NOT EXISTS`, `NOT NULL` and `CHECK` constraints (D11, D12) |
| `app/auth.py` | `current_user` FastAPI dependency: parses `Authorization: Bearer <token>` exactly (D8), looks the token up in `users`, and raises 401 `{"detail": "Not authenticated"}` otherwise |
| `app/access.py` | `NotFound` exception; `require_member(conn, user_id, community_id) -> str` returning the role or raising `NotFound` (D4) |
| `app/main.py` | `create_app(db_path, clock=None)`: builds the FastAPI app with `redirect_slashes=False` (D17), registers the `NotFound` → 404 handler, adds `current_user` as a router-level dependency so auth runs before path parsing (D9), and defines the seven routes. Module-level `app` reads `COMMUNITYCONNECT_DB` (D6). |

**How data is stored.** One SQLite file whose path is passed to `create_app`. Each request opens its
own connection and closes it afterwards (D11). Tables and columns are exactly §5 of the design doc.
Timestamps are text in `YYYY-MM-DDTHH:MM:SSZ` (D16). Every route that touches community data calls
`require_member` first; list queries filter by `community_id` (and by `folder = 'community'`, and by
`created_by` for residents and board members) in SQL (D15, R4, R5).

`clock` is accepted by `create_app` and stored, but S-1 does not use it. It exists only so that the
S-2 test module can be imported and skipped cleanly. *(This is a step we did not strictly ask for; see
Approval.)*

## Tasks

Each task is one bounded agent run, with a commit before and after.

1. **AC-5: unauthenticated requests are blocked.** Create `app/__init__.py`, `app/settings.py`,
   `app/db.py`, `app/auth.py`, `app/access.py` and `app/main.py`, with the schema, the auth dependency
   and all seven routes registered. In this task every authenticated route raises `NotFound` (fail
   closed). Check: `python -m pytest tests/test_s1_community_isolation.py -k "ac5 or d9"` passes.
2. **AC-3: members read their own community.** Implement `require_member` and the bodies of the six
   community routes, with SQL filtering for R4 and R5. Change only `app/access.py` and `app/main.py`.
   Check: `-k "ac3 or r4 or r5"` passes, and `-k "ac1 or ac2 or ac5"` still passes.
3. **AC-4: a manager switches communities with one token.** Implement `GET /me/communities`
   (ordered by `id`). Change only `app/main.py`. Check: `-k "ac4 or edge3"` passes.
4. **AC-1 and AC-2 hardening: blocked equals missing.** Make out-of-range IDs (0, negative, ≥ 2^63)
   raise `NotFound` instead of reaching SQLite (D10), and confirm trailing slashes give 404 (D17).
   Change only `app/main.py`. Check: `-k "ac1 or ac2 or d10 or d17"` passes, then the full
   `python -m pytest` run shows every S-1 test passing and the 7 S-2 tests skipped.

## Approval

- Approved by: Kundan Singh (kks59), in the Claude session, on 2026-11-03, before any `app/` file existed. The answer was "Approve as written".
- Steps crossed out: none. The unused `clock` argument was flagged to the approver as a step not strictly asked for, and was kept on purpose.
