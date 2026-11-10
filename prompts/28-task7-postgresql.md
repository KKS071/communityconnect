# Prompt 28: S-1 task 7 (PostgreSQL storage)

Implement the revised D12, D16 and D18 from docs/design/S-1.md: move storage from SQLite to
PostgreSQL with psycopg 3. Change only app/settings.py, app/db.py, app/seed.py, app/auth.py,
app/access.py, app/main.py. Do not change tests/, docs/, AGENTS.md, README.md, requirements.txt,
pytest.ini, docker-compose.yml, LEDGER.md, prompts/. Keep every endpoint's behaviour, message and
check order exactly as it is. Show me a plan and wait. Stop when `python -m pytest` passes
(every S-1 test passes, the five S-6 tests skipped).

The task is task 7 of docs/plans/S-1-plan.md (requested by Kundan Singh, 2026-11-09, prompt 27).
