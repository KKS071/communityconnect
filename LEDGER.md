# Provenance ledger

Format from the course assignments. One entry per reviewable change. Full prompts are in `prompts/`.

**Read this before submitting.** Entries 1–15 were drafted by the AI tool that did the work, on
2026-11-03. The **review** field records two things: what the AI checked, and the human review.
The human review line says "PENDING" until a named team member has read the change and replaced it
with what they read, changed or rejected. Do not submit a PENDING line as if it were done: the
handout treats unreviewed AI work and invented ledger entries as integrity violations.

Tool abbreviation used below: **Opus** = Claude Opus 5.5 (`claude-opus-5-5`), claude.ai agent session
(Claude Code harness), used 2026-11-03.

## Entry 1

artifact: repository scaffold: `README.md`, `AGENTS.md`, `requirements.txt`, `pytest.ini`, `.gitignore`. Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: user request to complete Milestone 1 (`prompts/00-session-request.md`); scaffold instructions (`prompts/01-scaffold-and-agents.md`)

review: AI: checked AGENTS.md against handout §6a (language/framework, test command, files not to change, plan-and-wait rule): all four present. Later, after D13, removed the README instructions for a seed script that does not exist. Human: PENDING (Gustavo Abreu).

checks: `python -m pytest` run on the scaffold: collection error "No module named 'app.main'", as expected before any code existed.

evidence: Milestone 1 handout §6a

risk: The README install steps have only been run in a Linux container with Python 3.13. Windows and Python 3.11 are unverified.

## Entry 2

artifact: `docs/requirements/proposal-followup.md`, `interview-kit.md`, `interviews.md`, `compliments-and-predictions.md`, `interview-notes/TEMPLATE.md`. Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: requirements drafting (`prompts/02-requirements.md`)

review: AI: checked that each role's question list has ≥ 5 past-event (★) questions, opens with the person's situation and closes with "who else"; kept proposal Appendix C questions 1–5 as manager Q2, Q5, Q7, Q8, Q9. Deliberately wrote **no** interview content; participation table and notes are empty templates. Human: PENDING (Kundan Singh).

checks: Manual count of ★ (past-event) questions: manager 10, resident 5, board 4. The kit claimed every list had ≥ 5, so a fifth board question (dues review) was added in the entry 15 commit.

evidence: Milestone 1 handout §2a; proposal Appendix C

risk: No interview has happened yet. Deliverables 2b–2e and the "most useful thing we learned" paragraph are empty, and the four-interview minimum is not met.

## Entry 3

artifact: `docs/requirements/evidence-log.md` (A-1…A-12, Q-1…Q-8) and `docs/requirements/backlog.md` (S-1…S-11, AC-1…AC-28, ranking, cut line). Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: requirements drafting (`prompts/02-requirements.md`)

review: AI: every story is traced to an A entry and a clarifying question (handout 4b allows this when no E entry exists). Checked that no AC uses a number the interviews did not settle: the reopen window, categories, photo size, retry delay and grace period are all named settings. Human: PENDING (Kundan Singh).

checks: Manual: 11 stories (≥ 8); 12 A entries (≥ 3); 8 Q entries (≥ 3); 0 E entries (≥ 12 required, still to come from interviews).

evidence: proposal §§1–3 and Appendix B; professor's approval feedback

risk: Every story rests on team assumptions. If interviews contradict A-5 or A-12, the ranking of S-1 itself is unverified.

## Entry 4

artifact: `docs/design/S-1.md`: draft in commit `8b3e8f0`; decisions D7–D21, R2 rewording and Q-3 rewording after the gap check in commit `7a94c87`.

tool: Opus, 2026-11-03

prompts: `prompts/03-design-S-1.md`

review: AI: checked the nine sections are present, with ≥ 3 rules, ≥ 3 edge cases, ≥ 3 decisions and ≥ 2 open questions each followed by the stop line. After the gap check, rewrote R2 because "before any community data is read" could not be checked from outside. Human: PENDING (Sandeep Garg).

checks: Gap check (entry 6): 41 questions, 14 answered, 27 real gaps, all resolved in §8.

evidence: S-1; A-5, A-12; Q-3, Q-5, Q-7

risk: After the gap-check additions the doc runs to about two pages, the handout's upper limit. The page length has not been measured in the PDF.

## Entry 5

artifact: `docs/design/S-2.md`: draft `8b3e8f0`; D4 expanded and D5–D14 added in `7a94c87`.

tool: Opus, 2026-11-03

prompts: `prompts/04-design-S-2.md`

review: AI: the reopen window appears only as `REOPEN_WINDOW_DAYS`. D5 marks the value in `app/settings.py` as a placeholder pending Q-1. Q-6 (backward moves) is left open and listed as a non-goal. Human: PENDING (Matthew Belanger).

checks: Gap check (entry 7): 43 questions, 25 answered, 18 real gaps (one of them, #1, is part answered and part gap), all resolved in §8.

evidence: S-2; A-6, A-7; Q-1, Q-6

risk: The placeholder `REOPEN_WINDOW_DAYS = 7` came from the team's proposal, not a user. It must be replaced once Q-1 is answered.

## Entry 6

artifact: `docs/design/S-1-gapcheck.md` (full reply and triage). Commit `7a94c87`.

tool: Claude Sonnet subagent launched from the Opus session, 2026-11-03. The exact Sonnet version was not reported to the session.

prompts: lecture gap-finding prompt, plus an instruction to read only the doc (`prompts/05-gapcheck-S-1.md`)

review: AI (Opus): marked each of the 41 questions as real gap or already answered, naming the section. Rejected none as irrelevant. Human: PENDING (Sandeep Garg) — check the triage verdicts.

checks: Each "Real gap" row names a D-number that exists in `docs/design/S-1.md` §8 (checked by reading §8).

evidence: S-1

risk: The checking model is from the same vendor as the drafting model, so they may share blind spots. No second-vendor gap check was run.

## Entry 7

artifact: `docs/design/S-2-gapcheck.md`. Commit `7a94c87`.

tool: Claude Sonnet subagent from the Opus session, 2026-11-03.

prompts: `prompts/06-gapcheck-S-2.md`

review: AI (Opus): triaged all 43 questions. Several were answered only by S-1.md, so the triage names that file. Human: PENDING (Matthew Belanger).

checks: Each "Real gap" row maps to a D-number in `docs/design/S-2.md` §8.

evidence: S-2

risk: Concurrency decision D4 has not been tested, and S-2 has no concurrency test yet.

## Entry 8

artifact: tests written before code: `tests/conftest.py`, `tests/test_s1_community_isolation.py`, `tests/test_s2_ticket_status.py`. Commit `7a94c87`.

tool: Opus, 2026-11-03

prompts: `prompts/07-tests-first.md`

review: AI: expected values come from the ACs and the doc's exact error bodies. Fixtures insert rows with raw SQL using §5 column names, so the tests do not depend on app code. Every S-2 test is skipped with a reason that starts with its AC ID. Added non-AC tests for R4, R5, edge 3, D9, D10 and D17. Human: PENDING (Matthew Belanger).

checks: `python -m pytest` before any app code: `ImportError … No module named 'app.main'` (expected).

evidence: AC-1 … AC-12

risk: AC-1/AC-2 cover only the seven Milestone 1 read endpoints. "Every API endpoint", from proposal success measure 1, will need the matrix extended as write endpoints arrive. Nothing yet enforces that.

## Entry 9

artifact: `docs/plans/S-1-plan.md`. Commit `612a3dd`.

tool: Opus, 2026-11-03

prompts: `prompts/08-plan-S-1.md`

review: AI flagged one step not asked for (an unused `clock` argument on `create_app`). Human: **Kundan Singh approved the plan as written in the session on 2026-11-03, before any `app/` file existed. No steps were crossed out.**

checks: None run. The plan is a document.

evidence: S-1, AC-1 … AC-5

risk: The approval was given in the chat session. Other team members have not reviewed the plan yet.

## Entry 10

artifact: S-1 task 1 (AC-5): `app/__init__.py`, `app/settings.py`, `app/db.py`, `app/auth.py`, `app/access.py`, `app/main.py`. Undo point `612a3dd`, result commit **`c87a0f5`**.

tool: Opus, 2026-11-03

prompts: `prompts/09-task1-AC-5.md`

review: AI: read the diff. Every authenticated route raises `NotFound` (fail closed). Header parsing follows D8 exactly. Human: PENDING (Sandeep Garg).

checks: `python -m pytest tests/test_s1_community_isolation.py -k "ac5 or d9"` → 36 passed. Full run → 62 passed, 8 failed (AC-3 ×5, AC-4, R4, edge 3: all expected before tasks 2–3), 7 skipped.

evidence: S-1 AC-5; D7, D8, D9, D11, D12

risk: After this task, the AC-1/AC-2 tests pass only because every route is closed, not because the membership check works. Task 2 is what makes them meaningful.

## Entry 11

artifact: S-1 task 2 (AC-3): `app/access.py`, `app/main.py`. Undo point `c87a0f5`, result commit **`9b62475`**.

tool: Opus, 2026-11-03

prompts: `prompts/10-task2-AC-3.md`

review: AI: read the diff. Item endpoints load the item, then call `require_member` (D14). Board-only documents are filtered in SQL for both list and item (R4). Residents and board members are filtered by `created_by` (R5). Human: PENDING (Gustavo Abreu).

checks: `-k "ac3 or r4 or r5"` → 7 passed; `-k "ac1 or ac2 or ac5"` → 56 passed. Full run → 67 passed, 3 failed, including a new one, `test_d10_out_of_range_ids_are_404[9223372036854775808]`, with `OverflowError: Python int too large to convert to SQLite INTEGER`. That was expected now that routes reach SQLite; it went to task 4 verbatim.

evidence: S-1 AC-3; R1, R4, R5

risk: R1 (every returned item belongs to a caller's community) is checked only on the seeded fixture. No property-based or randomised test covers it.

## Entry 12

artifact: S-1 task 3 (AC-4): `app/main.py`. Undo point `9b62475`, result commit **`914fc6a`**.

tool: Opus, 2026-11-03

prompts: `prompts/11-task3-AC-4.md`

review: AI review of the diff found that the new endpoint queried `memberships` inside `app/main.py`, breaking D4. Fixing it needed a file outside the task's bounds, so it was **not** fixed in place. Kundan Singh chose a follow-up task (entry 13). Human: PENDING (Sandeep Garg).

checks: `-k "ac4 or edge3"` → 2 passed.

evidence: S-1 AC-4; D21

risk: AC-4 is checked for one manager with two communities. No test checks a user removed from a community mid-session: their token stays valid, and D4 should then give 404, but this is unverified.

## Entry 13

artifact: S-1 task 3b (D4 fix): `app/access.py` (`communities_of`), `app/main.py`. Prompt commit `7d3a9cb`, result commit **`1eb85e4`**.

tool: Opus, 2026-11-03

prompts: `prompts/12-task3b-D4-fix.md`

review: AI: read the diff. The query moved unchanged. Human: Kundan Singh approved this follow-up task in the session. Code review PENDING (Sandeep Garg).

checks: `grep -n memberships app/main.py` → no output; `-k "ac4 or edge3"` → 2 passed.

evidence: S-1 D4

risk: D4 is enforced only by review and a grep. No automated check stops a later change from querying `memberships` outside `app/access.py`.

## Entry 14

artifact: S-1 task 4 (AC-1/AC-2 hardening, D10): `app/main.py`. Prompt commit `ce16574`, result commit **`f11ae96`**.

tool: Opus, 2026-11-03

prompts: `prompts/13-task4-AC-1-AC-2.md` (includes the exact `OverflowError` from entry 11)

review: AI: read the diff. `_check_id` runs before every SQLite lookup on an ID. Manually tried design-doc edge cases with no test: edge 2 (board in A and resident in B: role per community, and B's list shows only own tickets → `[]`), D17 wrong method → 405, edge 4 trailing space in token → 401, edge 5 `/tickets/abc` with a valid token → 422. All matched the doc. Human: PENDING (Matthew Belanger).

checks: `-k "ac1 or ac2 or d10 or d17"` → 25 passed; `python -m pytest` → **70 passed, 7 skipped** (the skips are AC-6 … AC-12).

evidence: S-1 AC-1, AC-2; D10, D17

risk: Importing `app.main` creates `communityconnect.db` in the current folder, because the module-level `app` for uvicorn is built at import. The file is git-ignored but appears on every test run.

## Entry 15

artifact: `docs/requirements/traceability.md`, this `LEDGER.md`, the board-question fix in `interview-kit.md` (from entry 2), and the Milestone 1 report document. Commit: the one that adds this file (SHA given in the report's table of contents).

tool: Opus, 2026-11-03

prompts: user request (`prompts/00-session-request.md`); no separate prompt. The AI drafted these as part of completing the request.

review: AI: checked every AC-1 … AC-28 has one row, and every S-1/S-2 test name in the matrix exists (`python -m pytest --collect-only -q`). Human: PENDING (Gustavo Abreu).

checks: `python -m pytest --collect-only -q` lists every test name used in the matrix. Fresh clone + new venv + `pip install -r requirements.txt` + `python -m pytest` → 70 passed, 7 skipped, plus 1 StarletteDeprecationWarning ("Using `httpx` with `starlette.testclient` is deprecated; install `httpx2`"), left alone because AGENTS.md forbids new dependencies without asking. Gap-check counts in entries 4–5 corrected after recounting the triage tables.

evidence: all ACs

risk: The ledger's human-review lines are not filled in. Until each named member replaces "PENDING", the ledger does not yet show human review for those entries.
