# AGENTS.md: standing instructions for AI coding tools

Read this file before every task in this repository. Claude Code loads it through `CLAUDE.md`.

## Language and framework

- Python 3.11+. API: FastAPI. Storage: PostgreSQL 14+ through `psycopg` 3 (no ORM).
- SQL lives only in `app/db.py`, `app/access.py`, `app/auth.py`, `app/seed.py` and `app/main.py`;
  use `%s` placeholders, never string formatting.
- Tests: pytest with FastAPI's `TestClient`; coverage with `pytest-cov`.
- Do not add a dependency without asking. The allowed list is `requirements.txt`.

## Commands

Details are in README.md. A human must re-check each command on a fresh clone.

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt  # install
docker compose up -d db        # database; README.md gives the createdb alternative
uvicorn app.main:app --reload  # run the API
python -m pytest               # run all tests
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80  # coverage
```

The tests need a running PostgreSQL server. Each test gets its own schema.

## Repository layout

- `app/`: API service. S-6 logic: `payments.py`, `processor.py`, `clock.py`, `db.py`, `settings.py`;
  routes in `main.py`; membership and roles in `access.py`.
- `docs/design/<story ID>.md`: design docs, the source of truth. `docs/plans/<story ID>-plan.md`: plans.
- `docs/requirements/`: evidence log, backlog with the acceptance criteria, traceability.
- `tests/acceptance/`: acceptance tests, one per AC with the AC ID in the test name, locked at the
  tag `m2-tests-locked`. Other tests live elsewhere under `tests/`.
- `prompts/`: every prompt referenced from `LEDGER.md`. `evidence/`: tool output only.

## Workflow rules

1. **Show a plan and wait.** Before editing any file, list the files you will change and what
   you will change in each. Wait for a team member to approve. Do not start editing on your own.
2. Work on one task, tied to one acceptance criterion (AC), at a time.
3. Change only the files the task prompt names. If another file needs to change, stop and ask.
4. Stop as soon as the check named in the task prompt passes. Do not continue to the next task.
5. The design doc is the source of truth. If it does not answer something, do not guess: stop
   and ask.
6. Values the interviews did not settle are named settings in `app/settings.py`. Never
   hard-code those numbers anywhere else.

## Testing rules

- Tests come from the acceptance criteria and the design doc, not from the code. Expected values
  come from the criteria, never from running or reading the implementation.
- Never edit, delete, skip or weaken a test in `tests/acceptance/`, or change any test's expected
  value, to make code pass. If you think a test is wrong, stop and say why; only a human changes
  it (design doc first, then the criterion, then the test).
- Run `python -m pytest` before reporting a task as done, and report the real result.

## Git and ledger rules

- One task per commit. The message names the task and its AC ID, for example
  `task 3: retry after delay (AC-22)`.
- One `LEDGER.md` entry per task, with the fields artifact, tool, prompts, review, checks,
  evidence and risk. Name the subagent in `tool` when one did the work. Save every referenced
  prompt in `prompts/`.
- Never commit `.env` or any key. Never push; a human pushes.

## Files and folders you must not change

- `tests/acceptance/`, and the expected values of any test.
- `docs/` (design docs, requirements, plans): read only. Humans change these.
- `LEDGER.md`, `prompts/` and `evidence/`: humans write these; evidence files are tool output only.
- `AGENTS.md`, `CLAUDE.md`, `.claude/`, `README.md`, `requirements.txt`, `pytest.ini`.

## Access rule (applies to every endpoint)

The caller is read from the `X-User-Id` header by one function in `app/auth.py` (S-1 D1, D14).
Membership and role are decided only in `app/access.py`; endpoints never query `memberships`
themselves. A record the caller may not see returns 404 with exactly the same body as a record
that does not exist: `{"detail": "Not found"}` (S-1 R2, D3).

## Stories

- S-1 (maintenance requests): built in Milestone 1. `docs/design/S-1.md`, `tests/test_s1_requests.py`.
- S-6 (scheduled dues payment): the Milestone 2 story. AC-18 to AC-22 are implemented and merged
  (LEDGER.md Entry 54). Design `docs/design/S-6.md`, plan `docs/plans/S-6-plan.md`; its tests are
  in `tests/test_s6_payments.py` until they move to `tests/acceptance/`.
- S-6 open questions OQ1–OQ5 are settled by human decisions in `docs/design/S-6.md` §8: residents
  pay no card fee; ACH is not charged or settled automatically; a run charges only the current
  month; board members still get 404 on the payments list; a manual payment is refused while a
  scheduled charge is `Pending`. Build nothing beyond these decisions without asking.
