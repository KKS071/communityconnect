# CommunityConnect

A community management portal for property-management companies that look after
several homeowner associations (HOAs). One login per person. Residents, board members,
community managers and a management-company admin each see only what their role and
their communities allow.

CS 690 AI-Assisted Software Engineering, Fall 2026. Team: Gustavo Abreu (project lead),
Kundan Singh (requirements & quality and test lead), Sandeep Garg (architecture lead).

## Status (Milestone 1)

| Story | What it is | State |
|---|---|---|
| S-1 | A resident submits a maintenance request and sees its status | Built; every S-1 test passes |
| S-6 | Scheduled monthly dues payment, charged at most once per unit per month | Design doc and tests written; tests skipped until built |

Interviews: `docs/interviews/`. Evidence log, backlog and traceability: `docs/requirements/`.
Design docs and gap checks: `docs/design/`. Build plan: `docs/plans/`. AI provenance: `LEDGER.md`
and `prompts/`.

## Install

Requires Python 3.11 or newer.

```bash
git clone <repo-url> communityconnect
cd communityconnect
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run all the tests

```bash
python -m pytest
```

Expected at Milestone 1: every S-1 test passes, and the five S-6 tests are reported as skipped,
each with its AC ID (AC-18 to AC-22) in the skip reason.

## Run the API locally (optional)

```bash
COMMUNITYCONNECT_DB=dev.db uvicorn app.main:app --reload
```

Users, communities and memberships are created only with the functions in `app/seed.py`
(S-1 D13, D17); there are no sign-up endpoints. Callers identify themselves with the
`X-User-Id` header (S-1 D1). The tests are the main way to exercise the API.

## Layout

```
app/            API service (FastAPI + SQLite)
tests/          pytest suites, one file per story; AC IDs in test names
docs/design/    design docs (docs/design/<story ID>.md) and AI gap-check replies
docs/plans/     build plans (docs/plans/<story ID>-plan.md)
docs/interviews/    interview questions, participation table, raw notes
docs/requirements/  proposal follow-up, evidence log, backlog, traceability
prompts/        every prompt referenced from LEDGER.md
LEDGER.md       provenance ledger
AGENTS.md       standing instructions for AI coding tools
```
