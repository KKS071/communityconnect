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
| S-1 | Community isolation: nobody reads another community's tickets, documents or announcements | Built, tests pass |
| S-2 | Ticket status lifecycle (Open → In progress → Resolved, reopen) | Design doc + tests written; tests skipped until built |

Requirements, backlog and evidence: `docs/requirements/`. Design docs: `docs/design/`.
Build plan: `docs/plans/`. AI provenance: `LEDGER.md` and `prompts/`.

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

Expected at Milestone 1: every S-1 test passes; every S-2 test is reported as skipped,
with its AC ID in the skip reason.

## Run the API locally (optional)

```bash
COMMUNITYCONNECT_DB=dev.db uvicorn app.main:app --reload
```

Milestone 1 has no demo-data script (S-1 design doc, D13), so a fresh database has no users.
The tests are the way to exercise the API.

## Layout

```
app/            API service (FastAPI + SQLite)
tests/          pytest suites, one file per story; AC IDs in test names
docs/design/    design docs (docs/design/<story ID>.md) and AI gap-check replies
docs/plans/     build plans (docs/plans/<story ID>-plan.md)
docs/requirements/  interview kit, notes, evidence log, backlog, traceability
prompts/        every prompt referenced from LEDGER.md
LEDGER.md       provenance ledger
AGENTS.md       standing instructions for AI coding tools
```
