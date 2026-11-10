# Prompt 21: S-1 task 1 (AC-1)

Implement AC-1 from docs/design/S-1.md. Change only app/__init__.py, app/settings.py, app/db.py, app/seed.py, app/auth.py, app/access.py, app/main.py (all new). Do not change tests/, docs/, AGENTS.md, README.md, requirements.txt, pytest.ini, LEDGER.md, prompts/. In this task the POST body gets only the "Invalid request body" check, the list returns every request in the community, and `GET /requests/{id}` always answers 404 "Not found" (fail closed). Show me a plan and wait. Stop when `python -m pytest tests/test_s1_requests.py -k "ac1 or d1 or d14 or d17"` passes.

The task is task 1 of docs/plans/S-1-plan.md (approved by Kundan Singh, 2026-11-09).
