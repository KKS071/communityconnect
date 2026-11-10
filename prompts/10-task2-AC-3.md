# Prompt 10: bounded task 2 

Implement AC-3 from docs/design/S-1.md (with rules R1, R4, R5 and decisions D4, D14, D15). Change only
app/access.py and app/main.py. Do not change tests/, docs/, app/db.py, app/auth.py, app/settings.py,
AGENTS.md, README.md, LEDGER.md, prompts/. Leave GET /me/communities failing closed (that is task 3).
Show me a plan and wait. Stop when
`python -m pytest tests/test_s1_community_isolation.py -k "ac3 or r4 or r5"` passes and
`-k "ac1 or ac2 or ac5"` still passes.

Plan shown before editing: task 2 of docs/plans/S-1-plan.md (approved).
