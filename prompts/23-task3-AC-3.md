# Prompt 23: S-1 task 3 (AC-3)

Implement AC-3 from docs/design/S-1.md. Change only app/main.py, app/access.py. Do not change tests/, docs/, AGENTS.md, README.md, requirements.txt, pytest.ini, LEDGER.md, prompts/. The request list answers only callers with the resident role in that community; everyone else gets 404 (D10, D19). Show me a plan and wait. Stop when `python -m pytest tests/test_s1_requests.py -k "ac3_ or d10_ or r3_ or r1_"` passes.

The task is task 3 of docs/plans/S-1-plan.md (approved by Kundan Singh, 2026-11-09).
