# AGENTS.md: standing instructions for AI coding tools

Read this file before every task in this repository.

## Language and framework

- Python 3.11+.
- API: FastAPI. Storage: SQLite through the standard-library `sqlite3` module (no ORM).
- Tests: pytest with FastAPI's `TestClient`.
- Do not add a dependency without asking. The allowed list is `requirements.txt`.

## Test command

```bash
python -m pytest
```

A task is not done until this command passes for the story being built. Tests for stories
that are not being built stay skipped; do not unskip them.

## Workflow rules

1. **Show a plan and wait.** Before editing any file, list the files you will change and
   what you will change in each. Wait for a team member to approve. Do not start editing
   on your own.
2. Work on one acceptance criterion (AC) at a time, as named in the task prompt.
3. Change only the files the task prompt names. If another file needs to change, stop and ask.
4. Stop as soon as the check named in the task prompt passes. Do not continue to the next AC.
5. The design doc (`docs/design/<story ID>.md`) is the source of truth. If it does not answer
   something, do not guess: stop and ask. Never build anything that depends on an item listed
   under "Open questions".
6. Values the interviews did not settle are named settings in `app/settings.py`
   (for example `REOPEN_WINDOW_DAYS`). Never hard-code those numbers anywhere else.

## Files and folders you must not change

- `tests/`: never change an expected value, delete a test, or weaken an assertion to make
  code pass. If you think a test is wrong, stop and say why.
- `docs/` (design docs, requirements, plans): read only. Humans change these.
- `LEDGER.md` and `prompts/`: humans write these.
- `AGENTS.md`, `README.md`, `requirements.txt`, `pytest.ini`.

## Access rule (applies to every endpoint)

Every endpoint that returns community data calls `app.access.require_member` (or a helper
built on it) before reading anything. A resource outside the caller's communities returns
404 with exactly the same body as a resource that does not exist. There is no other place
where community access is decided.
