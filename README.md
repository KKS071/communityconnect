# CommunityConnect

A community management portal for property-management companies that look after
several homeowner associations (HOAs). One login per person. Residents, board members,
community managers and a management-company admin each see only what their role and
their communities allow.

CS 690 AI-Assisted Software Engineering, Fall 2026. Team: Gustavo Abreu (project lead),
Kundan Singh (requirements lead; also quality and test lead since Matthew Belanger left the
team), Sandeep Garg (architecture lead).

## Status (Milestone 1)

| Story | What it is | State |
|---|---|---|
| S-1 | A resident submits a maintenance request and sees its status | Built; every S-1 test passes |
| S-6 | Scheduled monthly dues payment, charged at most once per unit per month | Design doc and tests written; tests skipped until built |

Interviews: `docs/interviews/`. Evidence log, backlog and traceability: `docs/requirements/`.
Design docs and gap checks: `docs/design/`. Build plan: `docs/plans/`. AI provenance: `LEDGER.md`
and `prompts/`.

## Install

Requires Python 3.11 or newer and PostgreSQL 14 or newer.

```bash
git clone <repo-url> communityconnect
cd communityconnect
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Start PostgreSQL

Either with Docker (creates the `communityconnect` and `communityconnect_test` databases,
user `postgres`, password `postgres`, on port 5432):

```bash
docker compose up -d db
```

Or with a PostgreSQL server you already run, create the two databases yourself:

```bash
createdb communityconnect
createdb communityconnect_test
```

The defaults are `postgresql://postgres:postgres@localhost:5432/communityconnect` for the app and
`postgresql://postgres:postgres@localhost:5432/communityconnect_test` for the tests. Change them
with the environment variables `COMMUNITYCONNECT_DATABASE_URL` and
`COMMUNITYCONNECT_TEST_DATABASE_URL` (S-1 design doc, D16 and D18).

## Run all the tests

With PostgreSQL running:

```bash
python -m pytest
```

Each test creates its own schema in the test database and drops it afterwards, so the tests never
touch the app's data. Expected at Milestone 1: every S-1 test passes, and the five S-6 tests are
reported as skipped, each with its AC ID (AC-18 to AC-22) in the skip reason. If PostgreSQL is not
reachable, every test fails with a message naming the database URL it tried.

## Run the API locally (optional)

```bash
uvicorn app.main:app --reload
```

The tables are created on start-up (S-1 D16). Users, communities and memberships are created only
with the functions in `app/seed.py` (S-1 D13, D17); there are no sign-up endpoints. Callers
identify themselves with the `X-User-Id` header (S-1 D1). The tests are the main way to exercise
the API.

## Layout

```
app/            API service (FastAPI + PostgreSQL)
tests/          pytest suites, one file per story; AC IDs in test names
docs/design/    design docs (docs/design/<story ID>.md) and AI gap-check replies
docs/plans/     build plans (docs/plans/<story ID>-plan.md)
docs/interviews/    interview questions, participation table, raw notes
docs/requirements/  proposal follow-up, evidence log, backlog, traceability
prompts/        every prompt referenced from LEDGER.md
LEDGER.md       provenance ledger
AGENTS.md       standing instructions for AI coding tools
docker-compose.yml  local PostgreSQL for development and tests
db/init/        SQL run once when the Docker database is first created
```
