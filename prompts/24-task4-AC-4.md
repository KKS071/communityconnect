# Prompt 24: S-1 task 4 (AC-4)

Implement AC-4 from docs/design/S-1.md. Change only app/main.py, app/access.py. Do not change tests/, docs/, AGENTS.md, README.md, requirements.txt, pytest.ini, LEDGER.md, prompts/. Build GET /requests/{request_id}: a request the caller may not see answers exactly like a missing id (R1, R2, D3). Also give unknown paths 404 {"detail": "Not found"} and wrong methods 405 {"detail": "Method Not Allowed"} (D21). Show me a plan and wait. Stop when `python -m pytest tests/test_s1_requests.py -k "ac4_ or r2_ or d21_ or d5_ or d12_"` passes.

The task is task 4 of docs/plans/S-1-plan.md (approved by Kundan Singh, 2026-11-09).
