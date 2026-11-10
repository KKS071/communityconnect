# Prompt 27: switch to PostgreSQL; record the team change (Kundan Singh, 2026-11-09)

> Matthew has left the team and we want to use the PostgreSQL as the DB, please change the
> documents, code, Ledger, report etc. everywhere accordingly and give me the completed project and
> documentation to check-in in GitHub

How the AI applied it (handout 6d: change the design doc first, then the tests, then the code):
1. Rewrite S-1 D12, D16 and D18 and S-6 D32 for PostgreSQL; note the change at the top of both gap
   checks; update AGENTS.md, README.md, requirements.txt, the S-1 plan; add docker-compose.yml.
   Record the team change in the proposal follow-up and the README.
2. Change only the test fixtures (tests/conftest.py, tests/helpers.py) so each test uses its own
   PostgreSQL schema. Do not change any expected value.
3. Change the code in one bounded task (prompt 28).
