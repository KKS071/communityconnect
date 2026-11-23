# CommunityConnect

A community management portal for property-management companies that look after
several homeowner associations (HOAs). One login per person. Residents, board members,
community managers and a management-company admin each see only what their role and
their communities allow.

CS 690 AI-Assisted Software Engineering, Fall 2026. Team: Gustavo Abreu (project lead),
Kundan Singh (requirements lead; also quality and test lead since Matthew Belanger left the
team), Sandeep Garg (architecture lead).

## Project status — Milestones 1 and 2

| Story | Milestone 1 | Milestone 2 |
|---|---|---|
| S-1: Maintenance requests | Implemented; S-1 tests passing | Retained and covered by regression tests |
| S-6: Scheduled monthly dues payment | Designed; five acceptance tests initially skipped | Implemented; AC-18 through AC-22 exercised by acceptance tests |

Milestone 1 delivered the resident maintenance-request workflow and prepared the S-6 design and acceptance tests. 
Milestone 2 implemented S-6 scheduling and payment processing, expanded regression tests, and evaluated test effectiveness with mutation testing. See MILESTONE2.md for the 
Milestone 2 summary.

Interviews: `docs/interviews/`. Evidence log, backlog and traceability: `docs/requirements/`.
Design docs and gap checks: `docs/design/`. Build plan: `docs/plans/`. AI provenance: `LEDGER.md`
and `prompts/`.

## Install

Requires Python 3.11 or newer and PostgreSQL 14 or newer.

```bash
git clone git@github.com:KKS071/communityconnect.git communityconnect
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
touch the app's data. At Milestone 1, every S-1 test passed while the five S-6 acceptance tests
(AC-18 through AC-22) were skipped pending implementation. At Milestone 2, S-6 is implemented
and those acceptance tests are no longer skipped. If PostgreSQL is not reachable, tests fail
with a message naming the database URL they tried.

Run the Milestone 2, S-6 acceptance tests specifically:

```bash
python -m pytest tests/acceptance/test_s6_acceptance.py
```

Run branch-aware coverage:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

The recorded Milestone 2 regression run reported **202 passed** and **94.34% branch-aware
coverage**, exceeding the 80% threshold. These are recorded results, not a fresh test run
performed for this README. See `evidence/mutation-regression-tests.txt`.

## Run the API locally (optional)

```bash
uvicorn app.main:app --reload
```

The tables are created on start-up (S-1 D16). Users, communities and memberships are created only
with the functions in `app/seed.py` (S-1 D13, D17); there are no sign-up endpoints. Callers
identify themselves with the `X-User-Id` header (S-1 D1). The tests are the main way to exercise
the API.

The local FastAPI API documentation is available at `http://127.0.0.1:8000/docs` when the
server is running. A seeded database and an authorized user's ID are needed to exercise
endpoints interactively.

## Milestone 2 — Scheduled monthly dues payments (S-6)

Milestone 2 implements AC-18 through AC-22. Residents can create a monthly payment
schedule, retrieve their schedule, and view payment history for a selected month.
Scheduled **debit and credit** payments are processed through the Python payment-run
function in the tested workflow. A prior manual payment prevents a duplicate scheduled
charge; retries and interrupted-run recovery follow the S-6 design rules.

### Payment schedule and history API

Create a schedule (resident authorization required):

```http
POST /communities/{community_id}/payment-schedules
X-User-Id: {resident_user_id}
Content-Type: application/json
```

Example JSON body using an illustrative test token:

```json
{"method": "ach", "day_of_month": 5, "token": "test_token"}
```

A successful request returns HTTP 201. The scheduling day must be 1–28, and the
payment token is not returned in the API response. ACH scheduling is supported,
**but automatic ACH charging/settlement is not implemented**.

Retrieve the resident's schedule:

```http
GET /communities/{community_id}/payment-schedules/mine
X-User-Id: {resident_user_id}
```

Retrieve payment history for an authorized viewer:

```http
GET /communities/{community_id}/payments?month=2026-12
X-User-Id: {authorized_user_id}
```

### Scheduled processing and reproducible demonstration

The payment runner is a Python function rather than a standalone daily-run CLI:

```python
from datetime import date
from app.payments import run_due_payments

result = run_due_payments(date(2026, 12, 5))
print(result)
```

This example requires a running initialized database, suitable seeded schedules and
dues, and a configured payment processor; it is not a turnkey live-payment demo.
The most reproducible demonstration is the acceptance-test suite:

```bash
python -m pytest -v tests/acceptance/test_s6_acceptance.py
```

The acceptance tests exercise schedule creation/display (AC-18), a due-day charge
(AC-19), crash/restart idempotency (AC-20), manual-payment protection (AC-21),
and declined-payment retries (AC-22). The charging tests use `FakeProcessor`.

### Mutation-testing evidence

The Milestone 2 mutation experiment generated 603 mutants in the configured source
files and **executed 30 selected mutants**. The baseline killed 25/30 (83.33%);
after three additional deterministic regression tests, 28/30 (93.33%) were killed.
Adding Hypothesis properties to the baseline selection did not increase the number
killed. These scores apply only to the selected 30 mutants, not the entire source.

Two selected mutants remained: one raises an unresolved concurrency-policy question,
and one is equivalent through the reviewed public API. See
[docs/audits/mutation-summary.md](docs/audits/mutation-summary.md) and the raw
`evidence/mutation-*.txt` files for details and reproducibility caveats.

### Known limitations

- ACH schedules can be created and viewed, but automatic ACH settlement is excluded.
- `StripeTestProcessor` is a placeholder that raises `ProcessorUnavailable`; live
  Stripe payments are not verified.
- The standalone `python -m app.run_payments` daily-run CLI is not implemented.
- The application is an API service; a browser-based payment UI is not delivered.
- Editing, pausing, or cancelling schedules is outside the current S-6 scope.
- The mutation after-run reused a cached mutmut workspace; the evidence documents
  the associated configuration and reproducibility limitations.

## Layout

```
app/                API service (FastAPI + PostgreSQL), including S-6 payments
tests/              pytest suites, regression tests and property-based tests
tests/acceptance/   locked acceptance tests with AC IDs in test names
docs/design/        design docs (docs/design/<story ID>.md) and AI gap-check replies
docs/plans/         build plans (docs/plans/<story ID>-plan.md)
docs/interviews/    interview questions, participation table, raw notes
docs/requirements/  proposal follow-up, evidence log, backlog, traceability
docs/audits/        mutation-testing audit and supporting analysis
prompts/            every prompt referenced from LEDGER.md
evidence/           preserved tool output
agent-patches/      retained agent patch proposals
LEDGER.md           provenance ledger
MILESTONE2.md       Milestone 2 submission summary
AGENTS.md           standing instructions for AI coding tools
docker-compose.yml  local PostgreSQL for development and tests
db/init/            SQL run once when the Docker database is first created
```
