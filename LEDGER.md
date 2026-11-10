# Provenance ledger

Format from the course assignments. One entry per reviewable change. Full prompts are in `prompts/`.

Tool abbreviations used below:
- **Opus** = Claude Opus 5.5 (`claude-opus-5-5`), claude.ai agent session (Claude Code harness).
- **Sonnet** = a Claude Sonnet model run as a separate agent from the Opus session for gap checks;
  the session did not report the exact Sonnet version.

**Entries 1 to 15 (2026-11-03) cover the pre-interview version of the repository:** S-1 community
isolation, S-2 ticket lifecycle, bearer tokens. That work was replaced on 2026-11-09 (entries 17 to
29) to match the team's Milestone 1 report, which is based on the interviews. The files it describes
are still in the git history at the SHAs given. Entry 16 records the commit between the two versions. Entries 30 to 33 record the team change
(Matthew Belanger left) and the move from SQLite to PostgreSQL.

## Entry 1

artifact: repository scaffold: `README.md`, `AGENTS.md`, `requirements.txt`, `pytest.ini`, `.gitignore`. Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: user request to complete Milestone 1 (`prompts/00-session-request.md`); scaffold instructions (`prompts/01-scaffold-and-agents.md`)

review: Gustavo Abreu: checked AGENTS.md against handout §6a (language/framework, test command, files not to change, plan-and-wait rule): all four present. Later, after D13, removed the README instructions for a seed script that does not exist.

checks: `python -m pytest` run on the scaffold: collection error "No module named 'app.main'", as expected before any code existed.

evidence: Milestone 1 handout §6a

risk: The README install steps have only been run in a Linux container with Python 3.13. Windows and Python 3.11 are unverified.

## Entry 2

artifact: `docs/requirements/proposal-followup.md`, `interview-kit.md`, `interviews.md`, `compliments-and-predictions.md`, `interview-notes/TEMPLATE.md`. Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: requirements drafting (`prompts/02-requirements.md`)

review: Kundan Singh: checked that each role's question list has ≥ 5 past-event (★) questions, opens with the person's situation and closes with "who else"; kept proposal Appendix C questions 1–5 as manager Q2, Q5, Q7, Q8, Q9. Deliberately wrote **no** interview content; participation table and notes are empty templates.

checks: Manual count of ★ (past-event) questions: manager 10, resident 5, board 4. The kit claimed every list had ≥ 5, so a fifth board question (dues review) was added in the entry 15 commit.

evidence: Milestone 1 handout §2a; proposal Appendix C

risk: No interview has happened yet. Deliverables 2b–2e and the "most useful thing we learned" paragraph are empty, and the four-interview minimum is not met.

## Entry 3

artifact: `docs/requirements/evidence-log.md` (A-1…A-12, Q-1…Q-8) and `docs/requirements/backlog.md` (S-1…S-11, AC-1…AC-28, ranking, cut line). Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: requirements drafting (`prompts/02-requirements.md`)

review: Kundan Singh: every story is traced to an A entry and a clarifying question (handout 4b allows this when no E entry exists). Checked that no AC uses a number the interviews did not settle: the reopen window, categories, photo size, retry delay and grace period are all named settings.

checks: Manual: 11 stories (≥ 8); 12 A entries (≥ 3); 8 Q entries (≥ 3); 0 E entries (≥ 12 required, still to come from interviews).

evidence: proposal §§1–3 and Appendix B; professor's approval feedback

risk: Every story rests on team assumptions. If interviews contradict A-5 or A-12, the ranking of S-1 itself is unverified.

## Entry 4

artifact: `docs/design/S-1.md`: draft in commit `8b3e8f0`; decisions D7–D21, R2 rewording and Q-3 rewording after the gap check in commit `7a94c87`.

tool: Opus, 2026-11-03

prompts: `prompts/03-design-S-1.md`

review: Sandeep Garg: checked the nine sections are present, with ≥ 3 rules, ≥ 3 edge cases, ≥ 3 decisions and ≥ 2 open questions each followed by the stop line. After the gap check, rewrote R2 because "before any community data is read" could not be checked from outside.

checks: Gap check (entry 6): 41 questions, 14 answered, 27 real gaps, all resolved in §8.

evidence: S-1; A-5, A-12; Q-3, Q-5, Q-7

risk: After the gap-check additions the doc runs to about two pages, the handout's upper limit. The page length has not been measured in the PDF.

## Entry 5

artifact: `docs/design/S-2.md`: draft `8b3e8f0`; D4 expanded and D5–D14 added in `7a94c87`.

tool: Opus, 2026-11-03

prompts: `prompts/04-design-S-2.md`

review: Sandeep Garg: the reopen window appears only as `REOPEN_WINDOW_DAYS`. D5 marks the value in `app/settings.py` as a placeholder pending Q-1. Q-6 (backward moves) is left open and listed as a non-goal.

checks: Gap check (entry 7): 43 questions, 25 answered, 18 real gaps (one of them, #1, is part answered and part gap), all resolved in §8.

evidence: S-2; A-6, A-7; Q-1, Q-6

risk: The placeholder `REOPEN_WINDOW_DAYS = 7` came from the team's proposal, not a user. It must be replaced once Q-1 is answered.

## Entry 6

artifact: `docs/design/S-1-gapcheck.md` (full reply and triage). Commit `7a94c87`.

tool: Claude Sonnet subagent launched from the Opus session, 2026-11-03. The exact Sonnet version was not reported to the session.

prompts: lecture gap-finding prompt, plus an instruction to read only the doc (`prompts/05-gapcheck-S-1.md`)

review: Sandeep Garg: marked each of the 41 questions as real gap or already answered, naming the section. Rejected none as irrelevant.

checks: Each "Real gap" row names a D-number that exists in `docs/design/S-1.md` §8 (checked by reading §8).

evidence: S-1

risk: The checking model is from the same vendor as the drafting model, so they may share blind spots. No second-vendor gap check was run.

## Entry 7

artifact: `docs/design/S-2-gapcheck.md`. Commit `7a94c87`.

tool: Claude Sonnet subagent from the Opus session, 2026-11-03.

prompts: `prompts/06-gapcheck-S-2.md`

review: Kundan Singh: triaged all 43 questions. Several were answered only by S-1.md, so the triage names that file.

checks: Each "Real gap" row maps to a D-number in `docs/design/S-2.md` §8.

evidence: S-2

risk: Concurrency decision D4 has not been tested, and S-2 has no concurrency test yet.

## Entry 8

artifact: tests written before code: `tests/conftest.py`, `tests/test_s1_community_isolation.py`, `tests/test_s2_ticket_status.py`. Commit `7a94c87`.

tool: Opus, 2026-11-03

prompts: `prompts/07-tests-first.md`

review: Gustavo Abreu: expected values come from the ACs and the doc's exact error bodies. Fixtures insert rows with raw SQL using §5 column names, so the tests do not depend on app code. Every S-2 test is skipped with a reason that starts with its AC ID. Added non-AC tests for R4, R5, edge 3, D9, D10 and D17.

checks: `python -m pytest` before any app code: `ImportError … No module named 'app.main'` (expected).

evidence: AC-1 … AC-12

risk: AC-1/AC-2 cover only the seven Milestone 1 read endpoints. "Every API endpoint", from proposal success measure 1, will need the matrix extended as write endpoints arrive. Nothing yet enforces that.

## Entry 9

artifact: `docs/plans/S-1-plan.md`. Commit `612a3dd`.

tool: Opus, 2026-11-03

prompts: `prompts/08-plan-S-1.md`

review: AI flagged one step not asked for (an unused `clock` argument on `create_app`). **Kundan Singh approved the plan as written in the session on 2026-11-03, before any `app/` file existed. No steps were crossed out.**

checks: None run. The plan is a document.

evidence: S-1, AC-1 … AC-5

risk: The approval was given in the chat session. Other team members have not reviewed the plan yet.

## Entry 10

artifact: S-1 task 1 (AC-5): `app/__init__.py`, `app/settings.py`, `app/db.py`, `app/auth.py`, `app/access.py`, `app/main.py`. Undo point `612a3dd`, result commit **`c87a0f5`**.

tool: Opus, 2026-11-03

prompts: `prompts/09-task1-AC-5.md`

review: Sandeep Garg: read the diff. Every authenticated route raises `NotFound` (fail closed). Header parsing follows D8 exactly.

checks: `python -m pytest tests/test_s1_community_isolation.py -k "ac5 or d9"` → 36 passed. Full run → 62 passed, 8 failed (AC-3 ×5, AC-4, R4, edge 3: all expected before tasks 2–3), 7 skipped.

evidence: S-1 AC-5; D7, D8, D9, D11, D12

risk: After this task, the AC-1/AC-2 tests pass only because every route is closed, not because the membership check works. Task 2 is what makes them meaningful.

## Entry 11

artifact: S-1 task 2 (AC-3): `app/access.py`, `app/main.py`. Undo point `c87a0f5`, result commit **`9b62475`**.

tool: Opus, 2026-11-03

prompts: `prompts/10-task2-AC-3.md`

review: Gustavo Abreu: read the diff. Item endpoints load the item, then call `require_member` (D14). Board-only documents are filtered in SQL for both list and item (R4). Residents and board members are filtered by `created_by` (R5).

checks: `-k "ac3 or r4 or r5"` → 7 passed; `-k "ac1 or ac2 or ac5"` → 56 passed. Full run → 67 passed, 3 failed, including a new one, `test_d10_out_of_range_ids_are_404[9223372036854775808]`, with `OverflowError: Python int too large to convert to SQLite INTEGER`. That was expected now that routes reach SQLite; it went to task 4 verbatim.

evidence: S-1 AC-3; R1, R4, R5

risk: R1 (every returned item belongs to a caller's community) is checked only on the seeded fixture. No property-based or randomised test covers it.

## Entry 12

artifact: S-1 task 3 (AC-4): `app/main.py`. Undo point `9b62475`, result commit **`914fc6a`**.

tool: Opus, 2026-11-03

prompts: `prompts/11-task3-AC-4.md`

review: AI review of the diff found that the new endpoint queried `memberships` inside `app/main.py`, breaking D4. Fixing it needed a file outside the task's bounds, so it was **not** fixed in place. Kundan Singh chose a follow-up task (entry 13). Completed by Sandeep Garg.

checks: `-k "ac4 or edge3"` → 2 passed.

evidence: S-1 AC-4; D21

risk: AC-4 is checked for one manager with two communities. No test checks a user removed from a community mid-session: their token stays valid, and D4 should then give 404, but this is unverified.

## Entry 13

artifact: S-1 task 3b (D4 fix): `app/access.py` (`communities_of`), `app/main.py`. Prompt commit `7d3a9cb`, result commit **`1eb85e4`**.

tool: Opus, 2026-11-03

prompts: `prompts/12-task3b-D4-fix.md`

review: AI: read the diff. The query moved unchanged. Human: Kundan Singh approved this follow-up task in the session. Code review done by Sandeep Garg.

checks: `grep -n memberships app/main.py` → no output; `-k "ac4 or edge3"` → 2 passed.

evidence: S-1 D4

risk: D4 is enforced only by review and a grep. No automated check stops a later change from querying `memberships` outside `app/access.py`.

## Entry 14

artifact: S-1 task 4 (AC-1/AC-2 hardening, D10): `app/main.py`. Prompt commit `ce16574`, result commit **`f11ae96`**.

tool: Opus, 2026-11-03

prompts: `prompts/13-task4-AC-1-AC-2.md` (includes the exact `OverflowError` from entry 11)

review: Gustavo Abreu: read the diff. `_check_id` runs before every SQLite lookup on an ID. Manually tried design-doc edge cases with no test: edge 2 (board in A and resident in B: role per community, and B's list shows only own tickets → `[]`), D17 wrong method → 405, edge 4 trailing space in token → 401, edge 5 `/tickets/abc` with a valid token → 422. All matched the doc.

checks: `-k "ac1 or ac2 or d10 or d17"` → 25 passed; `python -m pytest` → **70 passed, 7 skipped** (the skips are AC-6 … AC-12).

evidence: S-1 AC-1, AC-2; D10, D17

risk: Importing `app.main` creates `communityconnect.db` in the current folder, because the module-level `app` for uvicorn is built at import. The file is git-ignored but appears on every test run.

## Entry 15

artifact: `docs/requirements/traceability.md`, this `LEDGER.md`, the board-question fix in `interview-kit.md` (from entry 2), and the Milestone 1 report document. Commit: the one that adds this file (SHA given in the report's table of contents).

tool: Opus, 2026-11-03

prompts: user request (`prompts/00-session-request.md`); no separate prompt. The AI drafted these as part of completing the request.

review: Gustavo Abreu: checked every AC-1 … AC-28 has one row, and every S-1/S-2 test name in the matrix exists (`python -m pytest --collect-only -q`).

checks: `python -m pytest --collect-only -q` lists every test name used in the matrix. Fresh clone + new venv + `pip install -r requirements.txt` + `python -m pytest` → 70 passed, 7 skipped, plus 1 StarletteDeprecationWarning ("Using `httpx` with `starlette.testclient` is deprecated; install `httpx2`"), left alone because AGENTS.md forbids new dependencies without asking. Gap-check counts in entries 4–5 corrected after recounting the triage tables.

evidence: all ACs

## Entry 16

artifact: the two commits not named above: `f5fe0c4` and `4b0a2bc` (entry 15's traceability matrix, ledger and recount, 2026-11-03), and commit `42ef893` (2026-11-09, Kundan Singh): `.gitignore` gains `venv/`, `env/`, `.env`; file modes changed to executable; a README line and three lines of `docs/requirements/interviews.md` removed; in this ledger, the 3 Nov "AI: … Human: PENDING (name)" review lines of entries 1 to 9 were rewritten to name a team member as the reviewer, and the note saying unreviewed lines must stay PENDING was removed.

tool: none (manual edit by Kundan Singh, 2026-11-09)

prompts: none

review: Opus read the diff on 2026-11-09 while checking the repository against the handout and reported it to Kundan Singh. Nothing in this commit was reverted.

checks: `git show --stat 42ef893`; `python -m pytest` on that commit → 70 passed, 7 skipped.

evidence: none (housekeeping)

risk: The repository cannot show whether each member named in the review fields of entries 1 to 9 actually did the review recorded under their name; the 3 Nov text had marked those reviews as still pending. The team should confirm each one or restore "PENDING".

## Entry 17

artifact: Deliverables 1 to 4 copied from the team's Milestone 1 report into the repository: `docs/requirements/proposal-followup.md`, `docs/interviews/interviews.md` (questions, participation table, raw notes INT-01 to INT-04, compliments and predictions, AI summaries "None", what we learned), `docs/requirements/evidence-log.md` (E-1 to E-21, A-1 to A-5, Q-1 to Q-6) and `docs/requirements/backlog.md` (S-1 to S-11, AC-1 to AC-29, INVEST, ranking, cut line). The pre-interview kit, empty note templates and old drafts were deleted. Commit `e9ff9d7`.

tool: Opus, 2026-11-09

prompts: session request (`prompts/14-session-request-2026-11-09.md`); copy instruction (`prompts/15-docs-from-report.md`)

review: Kundan Singh decided in the session that the report is the final version and the repository must match it. The AI copied the text without changing any interview note, quote, evidence entry or criterion; it did not write interview content. AI check of the copied content against the handout: 8 past-event questions (2 to 9; ≥ 5 required); 4 interviews; every note paragraph has an INT:P ID; 21 E entries (≥ 12), 5 A (≥ 3), 6 Q (≥ 3), each Q written as a question; 11 stories (≥ 8), each with an E trace or, for S-11, "Assumption, rests on A-5" plus a clarifying question; every INVEST fail names a problem; every value not settled by an interview is a named setting.

checks: A script compared every line of the four files (after the heading the AI added) with the report's text converted by `pandoc`: 0 lines differ. One reference was changed afterwards: `interviews.md` now points to "LEDGER.md Entry 17" (this entry) instead of "Entry 1", because entry 1 is the 3 Nov scaffold. Counts above made with `grep -c`.

evidence: INT-01 to INT-04; E-1 to E-21

risk: The report says the interviews were held 2026-10-31 and 2026-11-01, but this ledger's entry 2 (2026-11-03) says no interview had been held yet. Which is right is not shown by the repository; the team must reconcile the dates or say how the notes were produced (handout 2b allows AI-model interviews if they are reviewed).

## Entry 18

artifact: design docs `docs/design/S-1.md` (submit and track a maintenance request) and `docs/design/S-6.md` (scheduled monthly dues payment), copied from section 5 of the report; `docs/design/S-2.md` and its gap check deleted. Commit `36926c7`.

tool: Opus, 2026-11-09

prompts: `prompts/15-docs-from-report.md`

review: AI check against handout §5: both stories are above the cut line (ranks 1 and 7); S-6 holds an invariant (R1: at most one Paid payment per unit per month); each doc has the nine sections, ≥ 2 non-goals, ≥ 3 rules written as checkable statements, ≥ 3 edge cases, ≥ 3 decisions and ≥ 2 open questions, each followed by "Do not build anything that depends on this. Stop and ask."

checks: Manual read of each section against the handout list.

evidence: S-1 (E-1, E-2, E-12); S-6 (E-9, E-21)

risk: The report's S-1 and S-6 section 8 claimed gap checks had already been done, but no gap-check file existed for these docs in the repository; entries 19 and 20 are the first gap checks on record for them.

## Entry 19

artifact: gap check of S-1: `docs/design/S-1-gapcheck.md` (full reply and triage) and decisions D14 to D21 plus a §9 pointer added to `docs/design/S-1.md`. Commit `2a2f114`.

tool: Sonnet (gap check) and Opus (triage), 2026-11-09

prompts: lecture gap-finding prompt, given only `S-1.md` (`prompts/16-gapcheck-S-1.md`); triage instruction (`prompts/18-gap-triage.md`)

review: AI (Opus) marked each of the 42 questions as answered (17, naming the section) or real gap (25), and decided every real gap in §8 without answering OQ1 or OQ2. D19 sets the default while OQ2 is open: a board member who is not a resident gets 404, the narrowest rule. Human review of the triage verdicts: PENDING (assign a team member before submitting).

checks: Every "Real gap" row names a D-number or §9, and each one exists in `S-1.md` (checked with `grep -n "D1[4-9]\|D2[01]" docs/design/S-1.md`).

evidence: S-1

risk: The checking model is from the same vendor as the drafting model, so they may share blind spots; no other vendor's model was used. With D14 to D21, S-1.md is about 1,340 words; it has not been measured on the PDF page, and the handout limit is two pages.

## Entry 20

artifact: gap check of S-6: `docs/design/S-6-gapcheck.md` (full reply and triage) and decisions D21 to D34 plus a §9 pointer added to `docs/design/S-6.md`. Commit `2a2f114`.

tool: Sonnet (gap check) and Opus (triage), 2026-11-09

prompts: lecture gap-finding prompt, given `S-6.md` and, only for its cross-references, `S-1.md` (`prompts/17-gapcheck-S-6.md`); triage instruction (`prompts/18-gap-triage.md`)

review: AI (Opus) marked 48 questions: 10 answered, 38 real gaps, all decided in §8. Question 48 showed that AC-19 expects a Paid payment for R1, whose schedule in AC-18 is ACH, which quietly settles OQ2 (handout 4d). D34 keeps OQ2 open: the tests for AC-19 to AC-22 use debit schedules. D27 makes `record_manual_payment` refuse while a charge is Pending instead of choosing an answer to OQ5. Human review of the triage verdicts: PENDING (assign a team member before submitting).

checks: Every "Real gap" row names a D-number or §9 that exists in `S-6.md`.

evidence: S-6; AC-18 to AC-22; OQ2, OQ5

risk: S-6.md is now about 1,940 words, very likely over the handout's two-page limit; it has not been shortened. No S-6 code exists, so none of D21 to D34 has been tried in code, and `StripeTestProcessor` (D33) has never called Stripe.

## Entry 21

artifact: tests written before the code: `tests/conftest.py`, `tests/helpers.py`, `tests/__init__.py`, `tests/test_s1_requests.py` (AC-1 to AC-6 plus tests for R1 to R5 and decisions D1, D4 to D6, D9 to D12, D14, D15, D17, D19 to D21), `tests/test_s6_payments.py` (AC-18 to AC-22, each skipped with a reason starting with its AC ID). The pre-interview `app/` and tests were deleted. `AGENTS.md` and `README.md` were updated for the new design. Commit `e7f9eaa`.

tool: Opus, 2026-11-09

prompts: `prompts/19-tests-first.md`

review: AI: every expected value comes from the criterion text in `backlog.md` or an exact message in the design doc; values the interviews did not settle are read from `app.settings` (REQUEST_CATEGORIES, MAX_DESCRIPTION_CHARS, RETRY_DELAY_DAYS, MAX_PAYMENT_ATTEMPTS). Sample data follows the backlog (R1 unit 12 and R3 unit 20 in Mountain Ridge, R2 Pine Hollow, M1, M2). Before writing the D1 header tests, the AI checked with a throwaway FastAPI app that `TestClient` passes header whitespace and repeated headers through unchanged, so those tests can fail for the right reason. Human review: PENDING (assign a team member before submitting).

checks: `python -m pytest` before any app code: 2 collection errors, `ModuleNotFoundError: No module named 'app'` (expected).

evidence: AC-1 to AC-6, AC-18 to AC-22

risk: The S-6 tests have never run, because they are skipped and no S-6 module exists; a mistake in them (for example the `FakeProcessor` subclass in AC-20) will show only when S-6 is built.

## Entry 22

artifact: `docs/plans/S-1-plan.md` (How section, six tasks each tied to one AC) and the task 1 prompt. Commit `19e9ef6`.

tool: Opus, 2026-11-09

prompts: `prompts/20-plan-S-1.md`

review: **Kundan Singh approved the plan as written in the session on 2026-11-09, before any `app/` file existed. No steps were crossed out; the AI proposed none that were not asked for.** Before task 1 started, and before the commit was pushed, the AI noticed that its task 1 check named two tests (`d12`, `d5`) that need `GET /requests/{id}` from task 4. It moved them to task 4's check and made task 1 create that route fail-closed. No step was added or removed.

checks: None run. The plan is a document.

evidence: S-1, AC-1 to AC-6

risk: The approval was given in the chat session by one member; the other members have not reviewed the plan.

## Entry 23

artifact: S-1 task 1 (AC-1): new `app/__init__.py`, `app/settings.py`, `app/db.py`, `app/seed.py`, `app/auth.py`, `app/access.py`, `app/main.py`; check selectors in `docs/plans/S-1-plan.md`. Undo point `19e9ef6`, result commit **`fa7b712`**.

tool: Opus, 2026-11-09

prompts: `prompts/21-task1-AC-1.md`

review: AI read the diff: only the seven named files plus the plan's selectors changed; `GET /requests/{id}` always answers 404 (fail closed); `memberships` is read only in `app/access.py`. The first check run reported `5 failed, 47 passed` because `pytest -k "d1"` also selects `d10`, `d12` and `d15` (substring match): the failures were later tasks' tests, not task 1 code. The plan's selectors were changed to end in `_`, and the check was rerun. Human review of the diff: PENDING (assign a team member before submitting).

checks: `python -m pytest tests/test_s1_requests.py -k "ac1_ or d1_ or d14_ or d17_"` → 38 passed. Full run → 16 failed (later tasks), 74 passed, 5 skipped.

evidence: S-1 AC-1; D1, D5, D8, D12 to D17

risk: Importing `app.main` builds the module-level `app`, which creates `communityconnect.db` in the current folder on every test run (git-ignored).

## Entry 24

artifact: S-1 task 2 (AC-2): `app/main.py`. Undo point `d003bad`, result commit **`7c5bf42`**.

tool: Opus, 2026-11-09

prompts: `prompts/22-task2-AC-2.md`

review: AI read the diff: the checks run in the D6 order (body shape, then description required and too long, then category), and the description is stored trimmed (D9). Human review of the diff: PENDING (assign a team member before submitting).

checks: `-k "ac2_ or r5_ or d15_ or d4_ or d9_ or d6_"` → 27 passed.

evidence: S-1 AC-2; R5; D4, D6, D7, D9, D15

risk: Descriptions are checked with Python's `str.strip()` and `len()` (D9); no test uses non-ASCII whitespace or combining characters.

## Entry 25

artifact: S-1 task 3 (AC-3): `app/main.py` (the list now calls `require_resident`). Undo point `20dc028`, result commit **`5fdd3a0`**.

tool: Opus, 2026-11-09

prompts: `prompts/23-task3-AC-3.md`

review: AI read the diff: one line changed, plus the import. The AC-3 test already passed after task 1, because the list query filters by `community_id`; this task made managers, board members and admins get 404 on the list (D10, D19). Human review of the diff: PENDING (assign a team member before submitting).

checks: `-k "ac3_ or d10_ or r3_ or r1_"` → 13 passed.

evidence: S-1 AC-3; R1, R3; D10, D19

risk: The board-member result (404) is only the default chosen while OQ2 is open; it will change if the team answers OQ2.

## Entry 26

artifact: S-1 task 4 (AC-4): `app/main.py` (`GET /requests/{id}` built; handler for framework HTTP errors). Undo point `f67f6e8`, result commit **`0bbd3fc`**.

tool: Opus, 2026-11-09

prompts: `prompts/24-task4-AC-4.md`

review: AI read the diff: a missing id, another community's id and a neighbour's id all raise the same `NotFound` (R2, D3); unknown paths get `{"detail": "Not found"}` and wrong methods keep Starlette's `{"detail": "Method Not Allowed"}` (D21). The full run after this task showed exactly one failure, AC-5, which is task 5. Human review of the diff: PENDING (assign a team member before submitting).

checks: `-k "ac4_ or r2_ or d21_ or d5_ or d12_"` → 12 passed. Full run → 1 failed (`test_ac5_neighbor_in_same_community_does_not_see_request`), 89 passed, 5 skipped.

evidence: S-1 AC-4; R1, R2; D3, D5, D12, D21

risk: R2 is checked on status and body only; response headers and timing for hidden and missing records are not compared.

## Entry 27

artifact: S-1 task 5 (AC-5): `app/main.py` (the list filters by `submitted_by`). Undo point `cf58209`, result commit **`229f127`**.

tool: Opus, 2026-11-09

prompts: `prompts/25-task5-AC-5.md`, which quotes the failing test from entry 26

review: AI: the exact error before the change was `assert 1 not in [1]` (R3 saw R1's request id 1 in the Mountain Ridge list). The diff adds `AND submitted_by = ?` to the list query, keeping the D11 order. Human review of the diff: PENDING (assign a team member before submitting).

checks: `-k "ac5_ or d11_ or d20_ or r4_"` → 5 passed.

evidence: S-1 AC-5; R4; D2, D11, D20

risk: D11's tie-break by id is checked only for requests made within the same second in one test run; there is no test with equal `created_at` values set on purpose.

## Entry 28

artifact: S-1 task 6 (AC-6) and the manual check of the built story. No code changed: the AC-6 test already passed after task 4. Prompt commit **`ac93726`** (also the result).

tool: Opus, 2026-11-09

prompts: `prompts/26-task6-AC-6.md`

review: AI walked through the story on a running server (`uvicorn app.main:app`, a seeded resident): submitted a request with padded spaces (stored trimmed, status Open, `created_at` in the D5 format); listed it; opened it by id; tried a lower-case category (`422 "Unknown category"`), an unknown user on a non-numeric id (`401 "Unknown user"`, D6), a missing id (`404 "Not found"`) and a trailing slash (`404 "Not found"`, D21). The server log showed no errors or tracebacks. Human review: PENDING (assign a team member before submitting).

checks: `-k "ac6_"` → 1 passed. `python -m pytest` → 90 passed, 5 skipped (AC-18 to AC-22), 1 warning (StarletteDeprecationWarning about `httpx`).

evidence: S-1 AC-6; AC-1 to AC-6

risk: Only the API was checked; there is no web client yet. The manual walk-through used one resident and did not repeat the cross-community cases by hand.

## Entry 29

artifact: `docs/requirements/traceability.md` (29 rows, AC-1 to AC-29), entries 16 to 29 of this ledger, and the updated report. Commit: the one that adds this entry (its SHA is in the report's table of contents).

tool: Opus, 2026-11-09

prompts: `prompts/14-session-request-2026-11-09.md`; no separate prompt

review: AI checked that every AC has one row, that the eleven S-1 and S-6 test names in the matrix exist, and that every commit since entry 15 is named in an entry. Human review: PENDING (assign a team member before submitting).

checks: `python -m pytest --collect-only -q` lists all eleven matrix test names. Fresh clone, new venv, `pip install -r requirements.txt`, `python -m pytest` → result in the report's section 6e.

evidence: all ACs

risk: The report's evidence and backlog sections were copied from the team's document; if the team edits the report again, the repository copies must be updated by hand, because nothing checks that they match.

## Entry 30

artifact: design-first change for PostgreSQL and the team change: S-1 D12, D16 and D18 and S-6 D32 rewritten; a note added at the top of both gap checks; `AGENTS.md` (storage, test command note), `README.md` (PostgreSQL install, Docker option, test database, team roles), `requirements.txt` (adds `psycopg[binary]>=3.1`), new `docker-compose.yml` and `db/init/01-test-database.sql`, a "Change after the build" section in `docs/plans/S-1-plan.md`, and a "Changes since the proposal" section in `docs/requirements/proposal-followup.md`. Commit `85aa60f`.

tool: Opus, 2026-11-09

prompts: `prompts/27-postgresql-and-team-change.md` (Kundan Singh's request, quoted)

review: AI: following handout 6d, the design doc was changed before any test or code. Only storage decisions changed; no rule (R1 to R5), message, check order or criterion changed, so no acceptance criterion or expected test value needed to change. The gap-check replies were kept word for word, with a note that their SQLite questions refer to the earlier wording. Team change: Matthew Belanger (proposal role: quality and test lead) has left; Kundan Singh holds that role. Human review: PENDING (assign a team member before submitting).

checks: `grep -rn -i sqlite` over `docs/design/S-1.md`, `docs/design/S-6.md`, `AGENTS.md`, `README.md` and `docs/plans/S-1-plan.md`: only the plan's history section mentions SQLite.

evidence: S-1 D12, D16, D18; S-6 D32

risk: The revised D12, D16 and D18 were not gap-checked again; an engineer reading them fresh may still have to guess (for example, how many connections the API may open under load). `docker compose up -d db` was not run in this session (no Docker available); only a locally started PostgreSQL 16 server was used.

## Entry 31

artifact: `tests/conftest.py` (fixture `db_schema` replaces `db_path`: each test gets a new schema in the test database, dropped afterwards, and fails with "PostgreSQL test database not reachable at <URL>" if the server is down) and `tests/helpers.py` (`set_status`, `count_requests` now use `psycopg`). Commit `77a0f32`.

tool: Opus, 2026-11-09

prompts: `prompts/27-postgresql-and-team-change.md`, step 2

review: AI read the diff: no test function and no expected value changed; only the two fixture files did. Human review: PENDING (assign a team member before submitting).

checks: `python -m pytest -x` before the code change: `AttributeError: <module 'app.settings'> has no attribute 'DATABASE_URL'` (expected; the code still used SQLite).

evidence: S-1 D18

risk: The test suite now needs a running PostgreSQL server; on a machine without one every test fails (by design, with the message above), so the 6e result depends on the grader starting the database as the README says.

## Entry 32

artifact: S-1 task 7 (PostgreSQL): `app/settings.py` (`DATABASE_URL`, `DATABASE_SCHEMA` replace `DATABASE_PATH`), `app/db.py` (`psycopg` connection with `search_path`, schema and table creation, `BIGINT GENERATED ALWAYS AS IDENTITY` ids), `app/seed.py`, `app/auth.py`, `app/access.py`, `app/main.py` (`%s` placeholders, `RETURNING`, connections used as context managers; `app.main:app` is now built on first use so importing the module needs no database). Undo point `5a39089`, result commit **`c2540d5`**.

tool: Opus, 2026-11-09

prompts: `prompts/28-task7-postgresql.md`

review: AI read the diff: only the six named files changed; every endpoint keeps its messages and check order. The first full run gave 90 errors with `psycopg.ProgrammingError: the last operation didn't produce records (command status: INSERT 0 1)` from `add_membership`, whose INSERT has no `RETURNING`; `_insert` now fetches a row only when the statement returns one. Manual check: seeded a resident, ran `uvicorn app.main:app` against PostgreSQL, submitted a request with padded spaces (stored trimmed, status Open), listed it, tried an unknown user (`401 "Unknown user"`) and a missing id (`404 "Not found"`); the server log showed no errors, and `psql` showed the stored row. Human review of the diff: PENDING (assign a team member before submitting).

checks: `python -m pytest` → 90 passed, 5 skipped (AC-18 to AC-22). After the run, `information_schema.schemata` held 0 leftover `test_` schemas. With `COMMUNITYCONNECT_TEST_DATABASE_URL` pointing at a closed port, the test fails with "PostgreSQL test database not reachable at …".

evidence: S-1 AC-1 to AC-6; D12, D16, D18

risk: Each request opens a new PostgreSQL connection (D16) and there is no connection pool; behaviour under many simultaneous users is untested. Tested only on PostgreSQL 16; versions 14 and 15, which D12 allows, are unverified.

## Entry 33

artifact: this ledger's entries 30 to 33 and the updated report (team note in section 1, revised D12, D16, D18 and D32 in section 5, new 6e output, submitted commit). Commit: the one that adds this entry (its SHA is in the report's table of contents).

tool: Opus, 2026-11-09

prompts: `prompts/27-postgresql-and-team-change.md`

review: AI checked that every commit since entry 29 is named in an entry and that the traceability matrix needs no change (no test was renamed). Human review: PENDING (assign a team member before submitting).

checks: Fresh clone, new venv, `pip install -r requirements.txt`, PostgreSQL 16 running with an empty `communityconnect_test` database, `python -m pytest` → result in the report's section 6e.

evidence: all ACs

risk: The report's design-doc text in section 5 is now a copy of the repository docs that was edited by hand; nothing checks that the two stay the same.


## Entry 34

artifact: commits not yet named by SHA in this ledger: `c3a1b25` (entry 29: traceability matrix and ledger entries 16 to 29), `760d0ae` (entry 33: ledger entries 30 to 33), and `c28860f` (2026-11-09, Kundan Singh, "Updated the DB to postgresql": pushed with GitHub Desktop after unzipping the repository; it changes no content, only the file mode of 28 files from 100755 to 100644, undoing the executable bits set in `42ef893`, entry 16). This entry's own commit is the submitted commit; its SHA is in the report's table of contents and section 6e.

tool: Opus, 2026-11-09 (this entry); `c28860f` was made by hand in GitHub Desktop

prompts: Kundan Singh's request to check the pushed repository before submission (no separate prompt file)

review: AI cloned the repository from GitHub, confirmed that `c28860f` is a child of `760d0ae` with the same file contents (`diff -r` against the local tree: no differences; `git show --summary`: 28 mode changes, 0 lines changed), and checked that every commit in the history is named in some entry. Human review: PENDING (assign a team member before submitting).

checks: Fresh clone of the commit that adds this entry, new venv, `pip install -r requirements.txt`, PostgreSQL 16 with an empty `communityconnect_test` database, `python -m pytest` → result in the report's section 6e. `python -m pytest --collect-only -q`: all eleven test names in the traceability matrix exist. Every `prompts/` path referenced in this ledger exists.

evidence: none (provenance housekeeping)

risk: Sixteen review fields in entries 19 to 34 still say "Human review: PENDING". Handout 6d and 8 require a person to read each change, so the team must do those reviews and record what they found before submitting; until then the ledger shows AI-only review for that work.
