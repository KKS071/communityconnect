# Deliverable 1: Proposal follow-up

Approval decision: **Approved. You may start building.** The approval listed no required
changes. It gave two pieces of advice, and we answer each one below.

| # | Item from the approval feedback | Our response | Where |
|---|---|---|---|
| 1 | "Payments carry the most risk in your plan. Keep the cut line in view." | We ranked the payment stories (S-8 scheduled dues, S-9 overdue reminders) 8th and 9th, just above the cut line, and we restated the proposal's trigger next to the ranking: if S-1's access tests are not all passing by Milestone 2, S-8 and S-9 drop below the line. Payment values the interviews have not settled (retry delay, overdue grace period) are named settings and open questions, not numbers. | `docs/requirements/backlog.md` §4e; evidence log Q-4 |
| 2 | "Run the cross-community access tests from the first week." | We chose community isolation (S-1) as the first story to build. Its test suite calls every Milestone 1 read endpoint as a resident, board member and manager from outside the community and checks that each call is blocked, plus a signed-out case. Those tests run under the one test command, `python -m pytest`, so every later change runs them. | `docs/design/S-1.md`; `tests/test_s1_community_isolation.py`; README |
