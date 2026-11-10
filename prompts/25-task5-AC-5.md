# Prompt 25: S-1 task 5 (AC-5)

Implement AC-5 from docs/design/S-1.md. Change only app/main.py. Do not change tests/, docs/, AGENTS.md, README.md, requirements.txt, pytest.ini, LEDGER.md, prompts/. The request list holds only the caller's own requests (D2), newest first (D11), and is [] when there are none (D20). Show me a plan and wait. Stop when `python -m pytest tests/test_s1_requests.py -k "ac5_ or d11_ or d20_ or r4_"` passes.

The task is task 5 of docs/plans/S-1-plan.md (approved by Kundan Singh, 2026-11-09).
