# S-1 build plan: submit and track a maintenance request

Written by the AI tool before any `app/` file existed, from `docs/design/S-1.md` (commit `2a2f114`)
and `tests/test_s1_requests.py` (commit `e7f9eaa`). Prompt: `prompts/20-plan-S-1.md`.

## How

**Files that change** (all new): `app/__init__.py`, `app/settings.py`, `app/db.py`, `app/seed.py`,
`app/auth.py`, `app/access.py`, `app/main.py`. Nothing in `tests/`, `docs/`, `AGENTS.md`, `README.md`,
`requirements.txt` or `pytest.ini` changes.

- `app/settings.py`: `REQUEST_CATEGORIES`, `MAX_DESCRIPTION_CHARS` (D8) and `DATABASE_PATH` from
  `COMMUNITYCONNECT_DB` (D16). Every other module reads these as `settings.X` when it uses them.
- `app/db.py`: `connect()` opens `settings.DATABASE_PATH` with foreign keys on and `sqlite3.Row`
  rows; `init_db()` runs `CREATE TABLE IF NOT EXISTS` for the §5 tables.
- `app/seed.py`: the four D17 functions, each validating the §5 rules and raising `ValueError`.
- `app/auth.py`: `current_user` dependency: exactly one `X-User-Id` header matching `^[1-9][0-9]*$`
  for an existing user, otherwise `401 "Unknown user"` (D1, D14).
- `app/access.py`: `NotFound` exception and `require_resident(conn, user_id, community_id) -> Row`
  (returns the membership, so its `unit_id` is used by D20). This is the only module that reads
  `memberships`.
- `app/main.py`: `create_app() -> FastAPI` (calls `init_db()`), module-level `app`, the three §4
  endpoints, and exception handlers that give every error the `{"detail": ...}` body (D7, D21).
  Path ids are taken as strings and checked by one `_parse_id` (D14), so FastAPI never answers 422
  for a path. The POST body is read as raw JSON and checked in the D6 order.

**How the data is stored:** SQLite at `DATABASE_PATH` (D12), one connection per API or seed call
(D16). Tables `communities`, `units`, `users`, `memberships` (primary key `(user_id, community_id)`)
and `requests` (`id INTEGER PRIMARY KEY AUTOINCREMENT`, `status` CHECK in the three §5 values,
`created_at` as `YYYY-MM-DDTHH:MM:SSZ` text, D5). Descriptions are stored trimmed (D9).

## Tasks

Each task is one bounded prompt in `prompts/`, with a commit before it as an undo point.

1. **AC-1.** Create all seven files: settings, schema, seed, caller check, `require_resident`,
   `POST /communities/{id}/requests` (resident only, R3) and `GET /communities/{id}/requests`
   returning the community's requests. `GET /requests/{id}` exists but always answers 404 (fail
   closed). Only the "Invalid request body" check on the body in this task.
   Check: `python -m pytest tests/test_s1_requests.py -k "ac1_ or d1_ or d14_ or d17_"`.
2. **AC-2.** Description, category and body-shape checks in the D6 order (D4, D7, D9, D15, R5).
   Check: `-k "ac2_ or r5_ or d15_ or d4_ or d9_ or d6_"`.
3. **AC-3.** The list answers only callers with the `resident` role in that community; everyone
   else gets 404 (D10, D19). Check: `-k "ac3_ or d10_ or r3_ or r1_"`.
4. **AC-4.** `GET /requests/{id}`, with hidden and missing ids answering identically (R2, D3),
   plus the D21 unknown-path and wrong-method bodies. Check: `-k "ac4_ or r2_ or d21_ or d5_ or d12_"`.
5. **AC-5.** The list holds only the caller's own requests (D2), newest first (D11), and `[]` when
   empty (D20). Check: `-k "ac5_ or d11_ or d20_ or r4_"`.
6. **AC-6.** The detail shows the stored status. Check: `-k ac6_`, then the full `python -m pytest`
   (every S-1 test passes, the five S-6 tests skipped).

## Steps not asked for

None proposed. (The AI considered adding a `/me/communities` endpoint for S-3, but that is not
part of S-1, so it is not in the plan.)

## Change during the build

After task 1, the checks were changed to end each name with `_` (for example `ac1_` instead of `ac1`),
because `pytest -k` matches substrings and `d1` also selected `d10`, `d12` and `d15`. No task or step
changed. Recorded in LEDGER.md.

## Change after the build: PostgreSQL (task 7)

The team chose PostgreSQL instead of SQLite (S-1 D12, D16 and D18 rewritten first). Task 7 changes
`app/settings.py` (`DATABASE_URL`, `DATABASE_SCHEMA` replace `DATABASE_PATH`), `app/db.py` (`psycopg`
connection with `search_path`, schema creation, `BIGINT GENERATED ALWAYS AS IDENTITY` ids),
`app/seed.py`, `app/auth.py`, `app/access.py` and `app/main.py` (`%s` placeholders, `RETURNING id`
instead of `lastrowid`). Tests change only in `tests/conftest.py` and `tests/helpers.py` (per-test
schema); no expected value changes. Check: `python -m pytest` (every S-1 test passes, S-6 skipped).
Prompt: `prompts/28-task7-postgresql.md`.
