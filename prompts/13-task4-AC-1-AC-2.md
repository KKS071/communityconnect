# Prompt 13: bounded task 4

Implement the AC-1/AC-2 hardening from docs/design/S-1.md: D10 (integer IDs outside 1..2^63-1 raise
NotFound before reaching SQLite) and D17 (trailing slash gives 404). Change only app/main.py. Do not
change tests/, docs/, other app/ files, AGENTS.md, README.md, LEDGER.md, prompts/. Show me a plan and
wait. Stop when `python -m pytest tests/test_s1_community_isolation.py -k "ac1 or ac2 or d10 or d17"`
passes, and then `python -m pytest` shows every S-1 test passing and the 7 S-2 tests skipped.

Exact error from the run before this task (test_d10_out_of_range_ids_are_404[9223372036854775808]):
E       OverflowError: Python int too large to convert to SQLite INTEGER
