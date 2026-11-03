# Prompt 12: bounded task 3b (follow-up from review of task 3; approved by Kundan Singh in session)

Review of task 3 found that GET /me/communities in app/main.py queries the memberships table directly,
which breaks D4 in docs/design/S-1.md. Move that query into a new function
`communities_of(conn: sqlite3.Connection, user_id: int) -> list[sqlite3.Row]` in app/access.py and call
it from app/main.py. Change only app/access.py and app/main.py. Do not change tests/, docs/, other app/
files, AGENTS.md, README.md, LEDGER.md, prompts/. Show me a plan and wait. Stop when
`grep -n memberships app/main.py` prints nothing and
`python -m pytest tests/test_s1_community_isolation.py -k "ac4 or edge3"` still passes.
