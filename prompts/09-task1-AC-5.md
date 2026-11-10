# Prompt 09: bounded task 1

Implement AC-5 from docs/design/S-1.md. Change only app/__init__.py, app/settings.py, app/db.py,
app/auth.py, app/access.py, app/main.py (all new). Do not change tests/, docs/, AGENTS.md, README.md,
requirements.txt, pytest.ini, LEDGER.md, prompts/. Every authenticated route raises NotFound in this
task (fail closed). Show me a plan and wait. Stop when
`python -m pytest tests/test_s1_community_isolation.py -k "ac5 or d9"` passes.

Plan shown before editing: task 1 of docs/plans/S-1-plan.md (approved).
