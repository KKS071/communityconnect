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

risk: The interview notes were not yet in the repository at this commit: deliverables 2b–2e and the "most useful thing we learned" paragraph are empty templates, so the evidence trace for every story still has to be added.

## Entry 3

artifact: `docs/requirements/evidence-log.md` (A-1…A-12, Q-1…Q-8) and `docs/requirements/backlog.md` (S-1…S-11, AC-1…AC-28, ranking, cut line). Commit `8b3e8f0`.

tool: Opus, 2026-11-03

prompts: requirements drafting (`prompts/02-requirements.md`)

review: Kundan Singh: every story is traced to an A entry and a clarifying question (handout 4b allows this when no E entry exists). Checked that no AC uses a number the interviews did not settle: the reopen window, categories, photo size, retry delay and grace period are all named settings.

checks: Manual: 11 stories (≥ 8); 12 A entries (≥ 3); 8 Q entries (≥ 3); 0 E entries (≥ 12 required; the interview notes had not been added to the repository yet).

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

artifact: the two commits not named above: `f5fe0c4` and `4b0a2bc` (entry 15's traceability matrix, ledger and recount, 2026-11-03), and commit `42ef893` (2026-11-09, Kundan Singh): `.gitignore` gains `venv/`, `env/`, `.env`; file modes changed to executable; a README line and three lines of `docs/requirements/interviews.md` removed; in this ledger, the 3 Nov review lines of entries 1 to 9, which had marked the human review as still to do, were rewritten to name the team member who reviewed each change, and the note about unreviewed lines was removed.

tool: none (manual edit by Kundan Singh, 2026-11-09)

prompts: none

review: Opus read the diff on 2026-11-09 while checking the repository against the handout and reported it to Kundan Singh. Nothing in this commit was reverted.

checks: `git show --stat 42ef893`; `python -m pytest` on that commit → 70 passed, 7 skipped.

evidence: none (housekeeping)

risk: The team confirmed on 2026-11-09 that each member named in the review fields of entries 1 to 9 did that review. Those names were written into the ledger on 2026-11-09, not when each change was made in early November, so the dates of the reviews are not recorded.

## Entry 17

artifact: Deliverables 1 to 4 copied from the team's Milestone 1 report into the repository: `docs/requirements/proposal-followup.md`, `docs/interviews/interviews.md` (questions, participation table, raw notes INT-01 to INT-04, compliments and predictions, AI summaries "None", what we learned), `docs/requirements/evidence-log.md` (E-1 to E-21, A-1 to A-5, Q-1 to Q-6) and `docs/requirements/backlog.md` (S-1 to S-11, AC-1 to AC-29, INVEST, ranking, cut line). The pre-interview kit, empty note templates and old drafts were deleted. Commit `e9ff9d7`.

tool: Opus, 2026-11-09

prompts: session request (`prompts/14-session-request-2026-11-09.md`); copy instruction (`prompts/15-docs-from-report.md`)

review: Kundan Singh decided in the session that the report is the final version and the repository must match it. The AI copied the text without changing any interview note, quote, evidence entry or criterion; it did not write interview content. AI check of the copied content against the handout: 8 past-event questions (2 to 9; ≥ 5 required); 4 interviews; every note paragraph has an INT:P ID; 21 E entries (≥ 12), 5 A (≥ 3), 6 Q (≥ 3), each Q written as a question; 11 stories (≥ 8), each with an E trace or, for S-11, "Assumption, rests on A-5" plus a clarifying question; every INVEST fail names a problem; every value not settled by an interview is a named setting.

checks: A script compared every line of the four files (after the heading the AI added) with the report's text converted by `pandoc`: 0 lines differ. One reference was changed afterwards: `interviews.md` now points to "LEDGER.md Entry 17" (this entry) instead of "Entry 1", because entry 1 is the 3 Nov scaffold. Counts above made with `grep -c`.

evidence: INT-01 to INT-04; E-1 to E-21

risk: The interviews were held on 2026-10-31 and 2026-11-01, but their notes entered the repository only on 2026-11-09, so the repository cannot show when the notes were written up.

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

review: AI (Opus) marked each of the 42 questions as answered (17, naming the section) or real gap (25), and decided every real gap in §8 without answering OQ1 or OQ2. D19 sets the default while OQ2 is open: a board member who is not a resident gets 404, the narrowest rule. Human review of the triage verdicts: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) checked them on 2026-11-09 and agreed with every verdict.

checks: Every "Real gap" row names a D-number or §9, and each one exists in `S-1.md` (checked with `grep -n "D1[4-9]\|D2[01]" docs/design/S-1.md`).

evidence: S-1

risk: The checking model is from the same vendor as the drafting model, so they may share blind spots; no other vendor's model was used. With D14 to D21, S-1.md is about 1,340 words; it has not been measured on the PDF page, and the handout limit is two pages.

## Entry 20

artifact: gap check of S-6: `docs/design/S-6-gapcheck.md` (full reply and triage) and decisions D21 to D34 plus a §9 pointer added to `docs/design/S-6.md`. Commit `2a2f114`.

tool: Sonnet (gap check) and Opus (triage), 2026-11-09

prompts: lecture gap-finding prompt, given `S-6.md` and, only for its cross-references, `S-1.md` (`prompts/17-gapcheck-S-6.md`); triage instruction (`prompts/18-gap-triage.md`)

review: AI (Opus) marked 48 questions: 10 answered, 38 real gaps, all decided in §8. Question 48 showed that AC-19 expects a Paid payment for R1, whose schedule in AC-18 is ACH, which quietly settles OQ2 (handout 4d). D34 keeps OQ2 open: the tests for AC-19 to AC-22 use debit schedules. D27 makes `record_manual_payment` refuse while a charge is Pending instead of choosing an answer to OQ5. Human review of the triage verdicts: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) checked them on 2026-11-09 and agreed with every verdict.

checks: Every "Real gap" row names a D-number or §9 that exists in `S-6.md`.

evidence: S-6; AC-18 to AC-22; OQ2, OQ5

risk: S-6.md is now about 1,940 words, very likely over the handout's two-page limit; it has not been shortened. No S-6 code exists, so none of D21 to D34 has been tried in code, and `StripeTestProcessor` (D33) has never called Stripe.

## Entry 21

artifact: tests written before the code: `tests/conftest.py`, `tests/helpers.py`, `tests/__init__.py`, `tests/test_s1_requests.py` (AC-1 to AC-6 plus tests for R1 to R5 and decisions D1, D4 to D6, D9 to D12, D14, D15, D17, D19 to D21), `tests/test_s6_payments.py` (AC-18 to AC-22, each skipped with a reason starting with its AC ID). The pre-interview `app/` and tests were deleted. `AGENTS.md` and `README.md` were updated for the new design. Commit `e7f9eaa`.

tool: Opus, 2026-11-09

prompts: `prompts/19-tests-first.md`

review: AI: every expected value comes from the criterion text in `backlog.md` or an exact message in the design doc; values the interviews did not settle are read from `app.settings` (REQUEST_CATEGORIES, MAX_DESCRIPTION_CHARS, RETRY_DELAY_DAYS, MAX_PAYMENT_ATTEMPTS). Sample data follows the backlog (R1 unit 12 and R3 unit 20 in Mountain Ridge, R2 Pine Hollow, M1, M2). Before writing the D1 header tests, the AI checked with a throwaway FastAPI app that `TestClient` passes header whitespace and repeated headers through unchanged, so those tests can fail for the right reason. Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

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

review: AI read the diff: only the seven named files plus the plan's selectors changed; `GET /requests/{id}` always answers 404 (fail closed); `memberships` is read only in `app/access.py`. The first check run reported `5 failed, 47 passed` because `pytest -k "d1"` also selects `d10`, `d12` and `d15` (substring match): the failures were later tasks' tests, not task 1 code. The plan's selectors were changed to end in `_`, and the check was rerun. Human review of the diff: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) read it on 2026-11-09 and requested no changes.

checks: `python -m pytest tests/test_s1_requests.py -k "ac1_ or d1_ or d14_ or d17_"` → 38 passed. Full run → 16 failed (later tasks), 74 passed, 5 skipped.

evidence: S-1 AC-1; D1, D5, D8, D12 to D17

risk: Importing `app.main` builds the module-level `app`, which creates `communityconnect.db` in the current folder on every test run (git-ignored).

## Entry 24

artifact: S-1 task 2 (AC-2): `app/main.py`. Undo point `d003bad`, result commit **`7c5bf42`**.

tool: Opus, 2026-11-09

prompts: `prompts/22-task2-AC-2.md`

review: AI read the diff: the checks run in the D6 order (body shape, then description required and too long, then category), and the description is stored trimmed (D9). Human review of the diff: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) read it on 2026-11-09 and requested no changes.

checks: `-k "ac2_ or r5_ or d15_ or d4_ or d9_ or d6_"` → 27 passed.

evidence: S-1 AC-2; R5; D4, D6, D7, D9, D15

risk: Descriptions are checked with Python's `str.strip()` and `len()` (D9); no test uses non-ASCII whitespace or combining characters.

## Entry 25

artifact: S-1 task 3 (AC-3): `app/main.py` (the list now calls `require_resident`). Undo point `20dc028`, result commit **`5fdd3a0`**.

tool: Opus, 2026-11-09

prompts: `prompts/23-task3-AC-3.md`

review: AI read the diff: one line changed, plus the import. The AC-3 test already passed after task 1, because the list query filters by `community_id`; this task made managers, board members and admins get 404 on the list (D10, D19). Human review of the diff: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) read it on 2026-11-09 and requested no changes.

checks: `-k "ac3_ or d10_ or r3_ or r1_"` → 13 passed.

evidence: S-1 AC-3; R1, R3; D10, D19

risk: The board-member result (404) is only the default chosen while OQ2 is open; it will change if the team answers OQ2.

## Entry 26

artifact: S-1 task 4 (AC-4): `app/main.py` (`GET /requests/{id}` built; handler for framework HTTP errors). Undo point `f67f6e8`, result commit **`0bbd3fc`**.

tool: Opus, 2026-11-09

prompts: `prompts/24-task4-AC-4.md`

review: AI read the diff: a missing id, another community's id and a neighbour's id all raise the same `NotFound` (R2, D3); unknown paths get `{"detail": "Not found"}` and wrong methods keep Starlette's `{"detail": "Method Not Allowed"}` (D21). The full run after this task showed exactly one failure, AC-5, which is task 5. Human review of the diff: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) read it on 2026-11-09 and requested no changes.

checks: `-k "ac4_ or r2_ or d21_ or d5_ or d12_"` → 12 passed. Full run → 1 failed (`test_ac5_neighbor_in_same_community_does_not_see_request`), 89 passed, 5 skipped.

evidence: S-1 AC-4; R1, R2; D3, D5, D12, D21

risk: R2 is checked on status and body only; response headers and timing for hidden and missing records are not compared.

## Entry 27

artifact: S-1 task 5 (AC-5): `app/main.py` (the list filters by `submitted_by`). Undo point `cf58209`, result commit **`229f127`**.

tool: Opus, 2026-11-09

prompts: `prompts/25-task5-AC-5.md`, which quotes the failing test from entry 26

review: AI: the exact error before the change was `assert 1 not in [1]` (R3 saw R1's request id 1 in the Mountain Ridge list). The diff adds `AND submitted_by = ?` to the list query, keeping the D11 order. Human review of the diff: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) read it on 2026-11-09 and requested no changes.

checks: `-k "ac5_ or d11_ or d20_ or r4_"` → 5 passed.

evidence: S-1 AC-5; R4; D2, D11, D20

risk: D11's tie-break by id is checked only for requests made within the same second in one test run; there is no test with equal `created_at` values set on purpose.

## Entry 28

artifact: S-1 task 6 (AC-6) and the manual check of the built story. No code changed: the AC-6 test already passed after task 4. Prompt commit **`ac93726`** (also the result).

tool: Opus, 2026-11-09

prompts: `prompts/26-task6-AC-6.md`

review: AI walked through the story on a running server (`uvicorn app.main:app`, a seeded resident): submitted a request with padded spaces (stored trimmed, status Open, `created_at` in the D5 format); listed it; opened it by id; tried a lower-case category (`422 "Unknown category"`), an unknown user on a non-numeric id (`401 "Unknown user"`, D6), a missing id (`404 "Not found"`) and a trailing slash (`404 "Not found"`, D21). The server log showed no errors or tracebacks. Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

checks: `-k "ac6_"` → 1 passed. `python -m pytest` → 90 passed, 5 skipped (AC-18 to AC-22), 1 warning (StarletteDeprecationWarning about `httpx`).

evidence: S-1 AC-6; AC-1 to AC-6

risk: Only the API was checked; there is no web client yet. The manual walk-through used one resident and did not repeat the cross-community cases by hand.

## Entry 29

artifact: `docs/requirements/traceability.md` (29 rows, AC-1 to AC-29), entries 16 to 29 of this ledger, and the updated report. Commit: the one that adds this entry (its SHA is in the report's table of contents).

tool: Opus, 2026-11-09

prompts: `prompts/14-session-request-2026-11-09.md`; no separate prompt

review: AI checked that every AC has one row, that the eleven S-1 and S-6 test names in the matrix exist, and that every commit since entry 15 is named in an entry. Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

checks: `python -m pytest --collect-only -q` lists all eleven matrix test names. Fresh clone, new venv, `pip install -r requirements.txt`, `python -m pytest` → result in the report's section 6e.

evidence: all ACs

risk: The report's evidence and backlog sections were copied from the team's document; if the team edits the report again, the repository copies must be updated by hand, because nothing checks that they match.

## Entry 30

artifact: design-first change for PostgreSQL and the team change: S-1 D12, D16 and D18 and S-6 D32 rewritten; a note added at the top of both gap checks; `AGENTS.md` (storage, test command note), `README.md` (PostgreSQL install, Docker option, test database, team roles), `requirements.txt` (adds `psycopg[binary]>=3.1`), new `docker-compose.yml` and `db/init/01-test-database.sql`, a "Change after the build" section in `docs/plans/S-1-plan.md`, and a "Changes since the proposal" section in `docs/requirements/proposal-followup.md`. Commit `85aa60f`.

tool: Opus, 2026-11-09

prompts: `prompts/27-postgresql-and-team-change.md` (Kundan Singh's request, quoted)

review: AI: following handout 6d, the design doc was changed before any test or code. Only storage decisions changed; no rule (R1 to R5), message, check order or criterion changed, so no acceptance criterion or expected test value needed to change. The gap-check replies were kept word for word, with a note that their SQLite questions refer to the earlier wording. Team change: Matthew Belanger (proposal role: quality and test lead) has left; Kundan Singh holds that role. Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

checks: `grep -rn -i sqlite` over `docs/design/S-1.md`, `docs/design/S-6.md`, `AGENTS.md`, `README.md` and `docs/plans/S-1-plan.md`: only the plan's history section mentions SQLite.

evidence: S-1 D12, D16, D18; S-6 D32

risk: The revised D12, D16 and D18 were not gap-checked again; an engineer reading them fresh may still have to guess (for example, how many connections the API may open under load). `docker compose up -d db` was not run in this session (no Docker available); only a locally started PostgreSQL 16 server was used.

## Entry 31

artifact: `tests/conftest.py` (fixture `db_schema` replaces `db_path`: each test gets a new schema in the test database, dropped afterwards, and fails with "PostgreSQL test database not reachable at <URL>" if the server is down) and `tests/helpers.py` (`set_status`, `count_requests` now use `psycopg`). Commit `77a0f32`.

tool: Opus, 2026-11-09

prompts: `prompts/27-postgresql-and-team-change.md`, step 2

review: AI read the diff: no test function and no expected value changed; only the two fixture files did. Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

checks: `python -m pytest -x` before the code change: `AttributeError: <module 'app.settings'> has no attribute 'DATABASE_URL'` (expected; the code still used SQLite).

evidence: S-1 D18

risk: The test suite now needs a running PostgreSQL server; on a machine without one every test fails (by design, with the message above), so the 6e result depends on the grader starting the database as the README says.

## Entry 32

artifact: S-1 task 7 (PostgreSQL): `app/settings.py` (`DATABASE_URL`, `DATABASE_SCHEMA` replace `DATABASE_PATH`), `app/db.py` (`psycopg` connection with `search_path`, schema and table creation, `BIGINT GENERATED ALWAYS AS IDENTITY` ids), `app/seed.py`, `app/auth.py`, `app/access.py`, `app/main.py` (`%s` placeholders, `RETURNING`, connections used as context managers; `app.main:app` is now built on first use so importing the module needs no database). Undo point `5a39089`, result commit **`c2540d5`**.

tool: Opus, 2026-11-09

prompts: `prompts/28-task7-postgresql.md`

review: AI read the diff: only the six named files changed; every endpoint keeps its messages and check order. The first full run gave 90 errors with `psycopg.ProgrammingError: the last operation didn't produce records (command status: INSERT 0 1)` from `add_membership`, whose INSERT has no `RETURNING`; `_insert` now fetches a row only when the statement returns one. Manual check: seeded a resident, ran `uvicorn app.main:app` against PostgreSQL, submitted a request with padded spaces (stored trimmed, status Open), listed it, tried an unknown user (`401 "Unknown user"`) and a missing id (`404 "Not found"`); the server log showed no errors, and `psql` showed the stored row. Human review of the diff: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) read it on 2026-11-09 and requested no changes.

checks: `python -m pytest` → 90 passed, 5 skipped (AC-18 to AC-22). After the run, `information_schema.schemata` held 0 leftover `test_` schemas. With `COMMUNITYCONNECT_TEST_DATABASE_URL` pointing at a closed port, the test fails with "PostgreSQL test database not reachable at …".

evidence: S-1 AC-1 to AC-6; D12, D16, D18

risk: Each request opens a new PostgreSQL connection (D16) and there is no connection pool; behaviour under many simultaneous users is untested. Tested only on PostgreSQL 16; versions 14 and 15, which D12 allows, are unverified.

## Entry 33

artifact: this ledger's entries 30 to 33 and the updated report (team note in section 1, revised D12, D16, D18 and D32 in section 5, new 6e output, submitted commit). Commit: the one that adds this entry (its SHA is in the report's table of contents).

tool: Opus, 2026-11-09

prompts: `prompts/27-postgresql-and-team-change.md`

review: AI checked that every commit since entry 29 is named in an entry and that the traceability matrix needs no change (no test was renamed). Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

checks: Fresh clone, new venv, `pip install -r requirements.txt`, PostgreSQL 16 running with an empty `communityconnect_test` database, `python -m pytest` → result in the report's section 6e.

evidence: all ACs

risk: The report's design-doc text in section 5 is now a copy of the repository docs that was edited by hand; nothing checks that the two stay the same.


## Entry 34

artifact: commits not yet named by SHA in this ledger: `c3a1b25` (entry 29: traceability matrix and ledger entries 16 to 29), `760d0ae` (entry 33: ledger entries 30 to 33), and `c28860f` (2026-11-09, Kundan Singh, "Updated the DB to postgresql": pushed with GitHub Desktop after unzipping the repository; it changes no content, only the file mode of 28 files from 100755 to 100644, undoing the executable bits set in `42ef893`, entry 16). This entry's own commit is the submitted commit; its SHA is in the report's table of contents and section 6e.

tool: Opus, 2026-11-09 (this entry); `c28860f` was made by hand in GitHub Desktop

prompts: Kundan Singh's request to check the pushed repository before submission (no separate prompt file)

review: AI cloned the repository from GitHub, confirmed that `c28860f` is a child of `760d0ae` with the same file contents (`diff -r` against the local tree: no differences; `git show --summary`: 28 mode changes, 0 lines changed), and checked that every commit in the history is named in some entry. Human review: the team (Kundan Singh, Sandeep Garg, Gustavo Abreu) reviewed this change on 2026-11-09 and requested no changes.

checks: Fresh clone of the commit that adds this entry, new venv, `pip install -r requirements.txt`, PostgreSQL 16 with an empty `communityconnect_test` database, `python -m pytest` → result in the report's section 6e. `python -m pytest --collect-only -q`: all eleven test names in the traceability matrix exist. Every `prompts/` path referenced in this ledger exists.

evidence: none (provenance housekeeping)

risk: The human reviews of entries 19 to 34 are recorded as one review by the whole team, so the ledger does not show which member checked which change.

## Entry 35

artifact: this ledger only: the review fields of entries 19 to 34 now record the team's review instead of a placeholder; entry 2's risk and check fields, and the risk fields of entries 16, 17 and 34, are corrected. Commit `e3b6d14` (entry 34) is named here. The commit that adds this entry is the submitted commit; its SHA is in the report's table of contents and section 6e.

tool: Opus, 2026-11-09

prompts: Kundan Singh's message in the session: the team has reviewed every pending item; the "not yet held" wording in entry 2 was a typo, and the interviews were held on 2026-10-31 and 2026-11-01

review: Kundan Singh reported that Kundan Singh, Sandeep Garg and Gustavo Abreu reviewed every change whose human review was still open (entries 19 to 34) and requested no changes, and confirmed the reviewers named in entries 1 to 9. Entry 2's risk said that no interview had taken place; it now says that the interview notes were not yet in the repository at that commit, which matches the files of 2026-11-03 and the interview dates. Human review: Kundan Singh read the edited entries in this session.

checks: A search of this file finds no placeholder review line and no statement that the interviews had not been held. Fresh clone of the commit that adds this entry, new venv, PostgreSQL 16 with an empty `communityconnect_test` database, `python -m pytest` → result in the report's section 6e.

evidence: none (provenance housekeeping)

risk: Entries 1 to 15 still describe the superseded pre-interview code (bearer tokens, S-2), which no longer exists at the submitted commit; a reader must use the SHAs in those entries to see it.


## Entry 36

artifact: `docs/plans/S-6-plan.md` (implementation plan for AC-18 to AC-22), and updated `AGENTS.md` instructions permitting staged S-6 implementation. Plan commit `bd558d4`.

tool: ChatGPT (GPT-6), 2026-11-19

prompts: User request to prepare the S-6 implementation plan and proceed one acceptance criterion at a time. No separate prompt file verified.

review: The plan records team approval reported by the requester, including Gustavo's approval. It limits implementation to one AC at a time, requires separate file-scope approval, and keeps unresolved policy questions OQ1–OQ5 outside implementation.

checks: Reviewed the plan against `docs/design/S-6.md`, `AGENTS.md`, and the existing acceptance tests. AC-18 was separated from payment processing and settlement. AC-19 through AC-22 were assigned separate implementation stages.

evidence: S-6; AC-18 to AC-22; D1–D34; `docs/plans/S-6-plan.md`.

risk: The plan records reported team approval, but the individual AC approvals and review evidence must be retained separately. Future ACs may require additional files or separate dependency approval.

## Entry 37

artifact: S-6 task 1 (AC-18): `app/db.py`, `app/main.py`, new `app/clock.py`, and `tests/test_s6_payments.py`. Implementation commit **`6b1317f`**.

tool: ChatGPT (GPT-6), 2026-11-19; implementation patch applied and tested locally by Sandeep Garg.

prompts: User request to implement AC-18 using the approved S-6 plan. No separate repository prompt file verified.

review: The implementation adds the `schedules` table, POST and GET payment-schedule endpoints, and a UTC clock. Resident authorization uses `require_resident`; only one schedule is allowed per unit. Input validation follows D12 and D21. The response excludes the stored payment token. The AC-18 test uses a separate fixture without requiring the unimplemented payment processor. 

checks: `python3 -m pytest tests/test_s6_payments.py -k ac18_ -v` → 1 passed, 4 deselected. `python3 -m pytest tests/test_s1_requests.py -v` → 90 passed.

evidence: S-6 AC-18; D7, D10–D12, D21–D24; `tests/test_s6_payments.py::test_ac18_schedule_shown_on_payments_page`.

risk: AC-18 verifies schedule creation and retrieval only. It does not process payments, validate tokens with Stripe, or establish ACH settlement behavior. Duplicate-schedule and invalid-input edge cases are implemented but are not independently covered by the AC-18 acceptance test.

## Entry 38

artifact: AC-18 test activation and regression verification: `tests/test_s6_payments.py` (new `s6_schedule` fixture and removal of only the AC-18 skip marker). Included in commit **`6b1317f`**.

tool: ChatGPT (GPT-6) for test-fixture guidance; Sandeep Garg executed the tests locally, 2026-11-19.

prompts: User request to resolve the AC-18 test fixture dependency on unimplemented AC-19 modules and verify the implementation. No separate prompt file verified.

review: The fixture change isolates AC-18 from `app.processor` and `app.seed.set_dues`. The existing AC-18 assertions were preserved. AC-19 through AC-22 remained skipped. The test changes were reviewed against the requirement not to weaken acceptance criteria.

checks: `python3 -m pytest` → **91 passed, 4 skipped, 1 warning** in 100.09 seconds. `git diff --check` produced no errors. The warning was `StarletteDeprecationWarning` concerning `httpx` and `starlette.testclient`.

evidence: S-6 AC-18; `tests/test_s6_payments.py`; `AGENTS.md` test requirements.

risk: The successful test run covers the implemented AC-18 behavior and S-1 regression tests. AC-19 through AC-22 are skipped and must not be counted as passing. The dependency deprecation warning remains unresolved.

## Entry 39

artifact: AC-18 GitHub integration: feature branch `feature/s6-ac18-payment-schedule`, implementation commit **`6b1317f`**, and merge commit **`e7787de`** (pull request #2).

tool: Git and GitHub, with ChatGPT (GPT-6) verification, 2026-11-19.

prompts: User request to verify that all AC-18 changes were committed and present in `main`. No separate prompt file verified.

review: Verified that the merged `main` branch contains the schedule table, POST and GET endpoints, UTC clock, AC-18 fixture, and enabled AC-18 test. Confirmed that AC-19 through AC-22 remain skipped. The feature branch and merged `main` have identical AC-18 file contents.

checks: GitHub commit and branch comparison confirmed that PR #2 merged AC-18 into `main`. The verified local full test suite reported 91 passed, 4 skipped and 1 warning.

evidence: S-6 AC-18; commit `6b1317f`; merge commit `e7787de`; GitHub PR #2.

risk: GitHub source verification confirms the committed implementation but does not independently execute the test suite. AC-18 does not establish correctness of monthly charging, retry processing, crash recovery, or real payment-provider integration.

## Entry 40

artifact: S-6 AC-19 monthly scheduled payment implementation, including payment persistence, the monthly payment runner, FakeProcessor integration, payment history, and AC-19 test activation. Implementation commit `ce8671e7613b842cbec8b1775a4a725a26afa4a8`. Merged through GitHub PR #3, merge commit `7886408581cb325abb620678b87844c627c6c177`.

tool: ChatGPT (GPT-6), with implementation applied locally by Sandeep Garg, 2026-11-19 to 2026-11-20.

prompts: User request to implement AC-19 using `docs/plans/S-6-plan.md`, one acceptance criterion at a time. No separate repository prompt file verified.

review: The implementation adds monthly scheduled debit processing using FakeProcessor. It persists a Pending payment with an idempotency key before invoking the processor, then records the payment result. It follows the single-runner restriction and does not make real payment transactions. AC-19 was implemented separately from later acceptance criteria.

checks: AC-19 was implemented and merged. Its original AC-specific test output should be taken from the corresponding terminal record. Subsequent regression testing after AC-21 confirmed that AC-19 passed. The full suite at that later checkpoint reported 94 passed, 1 skipped, and 1 warning.

evidence: S-6 AC-19; R1–R3; D25, D28–D32; `docs/plans/S-6-plan.md`; implementation commit `ce8671e`; GitHub PR #3.

risk: FakeProcessor validates the local payment workflow, not Stripe integration or production charging. Concurrent runners are unsupported. The later regression result does not replace the original AC-19 test record.

## Entry 41

artifact: S-6 AC-20 crash-recovery and idempotent replay implementation. Implementation commit `caa65a8b1f098028e33d75b60595dfb516668c77`. Merged through GitHub PR #4, merge commit `b00603295139a9d7535ce83b53de2a5efde66c66`.

tool: ChatGPT (GPT-6), with implementation applied and tested locally by Sandeep Garg, 2026-11-20.

prompts: User request to implement AC-20 following the approved S-6 implementation plan. No separate repository prompt file verified.

review: The implementation supports replaying a Pending payment using the original idempotency key and stored amount. ProcessorUnavailable leaves the payment Pending so a later run can resume it. The implementation avoids creating another payment attempt during replay and remains within the approved FakeProcessor architecture.

checks: AC-20 was implemented and merged. Its original AC-specific test output should be verified from the corresponding terminal record. Subsequent regression testing after AC-21 confirmed that AC-20 passed alongside AC-18 and AC-19.

evidence: S-6 AC-20; D4, D26, D29–D31; `tests/test_s6_payments.py`; implementation commit `caa65a8`; GitHub PR #4.

risk: The test simulates processor interruption using a retained FakeProcessor instance. It does not demonstrate a complete process restart or independently durable external processor state. Concurrent replay remains unverified.

## Entry 42

artifact: S-6 AC-21 manual payment recording and scheduled-charge prevention. Implementation commit `456802fa4a0314333fde7e9807353b5ed44ad3a3`. Merged through GitHub PR #5, merge commit `6b86b5963016a85411426c6cc251323eb5d4bd64`.

tool: ChatGPT (GPT-6), with implementation applied and verified locally by Sandeep Garg, 2026-11-20.

prompts: User request to implement AC-21 following the approved S-6 implementation plan. No separate repository prompt file verified.

review: The implementation records manual Paid payments for valid units and billing months. A previously recorded manual payment prevents a subsequent scheduled charge for that month. Existing AlreadyPaid and PaymentPending behavior was preserved. AC-21 was completed independently of AC-22.

checks: `python3 -m pytest tests/test_s6_payments.py -k "ac21_" -v` → 1 passed, 4 deselected. `python3 -m pytest tests/test_s6_payments.py -k "ac18_ or ac19_ or ac20_" -v` → 3 passed, 2 deselected. `python3 -m pytest` → 94 passed, 1 skipped, 1 warning in 172.84 seconds. AC-22 remained skipped.

evidence: S-6 AC-21; R1, R3, D13, D27; `tests/test_s6_payments.py`; implementation commit `456802f`; GitHub PR #5.

risk: Manual payment before scheduled processing is covered by the acceptance test. Concurrent manual payment and scheduled retry operations have not been demonstrated safe. AC-22 remains unimplemented.

## Entry 43

artifact: Project 2 Claude Code configuration: `CLAUDE.md`, `.claude/settings.json`, `.claude/agents/test-analyst.md`, `.claude/agents/security-reviewer.md`, and `.claude/agents/code-reviewer.md`. Configuration commit `a60f745cf2dcf61a71a5b5942d826b32311d2661`. Merged through GitHub PR #6, merge commit `2d94009ce0d5cea7fae03160ec3635c7d7ea43c9`.

tool: ChatGPT (GPT-6) for configuration guidance; Claude Code 2.1.329 for configuration verification; Sandeep Garg created, committed, and merged the files, 2026-11-20.

prompts: User-approved request to create exactly five Claude Code configuration files without implementing AC-22. Follow-up interactive Claude Code prompt requested verification of the available subagents and active tool restrictions. No separate repository prompt file verified.

review: The configuration establishes project instructions, human-approval gates, a read-only default permission profile, and three specialized subagents. Claude Code recognized test-analyst, security-reviewer, and code-reviewer, each configured with Read, Grep, and Glob tools. GitHub PR #6 contains exactly the five approved configuration files and no application or test changes.

checks: Claude Code reported that all three project subagents were available. The main agent observed that Bash, Edit, Write, and NotebookEdit were unavailable under the project settings. GitHub confirms PR #6 merged into main on 2026-11-20. The merge commit is `2d94009`. No application tests were executed as part of this configuration verification.

evidence: `CLAUDE.md`; `.claude/settings.json`; `.claude/agents/`; GitHub PR #6; configuration commit `a60f745`; merge commit `2d94009`.

risk: The read-only settings also restrict teammates using Claude Code in this repository. Permission configuration was observed but not tested by deliberately attempting a forbidden operation. The current settings do not authorize AC-22 implementation.

## Entry 44

artifact: Project 2 AGENT-01 and AGENT-02 evidence for AC-22 preimplementation analysis. AGENT-01 used three actual Claude Code subagents. AGENT-02 executed Claude Code headlessly and produced structured JSON. Evidence includes the AGENT-01 transcript and `AGENT-02-headless.json`. No application changes were made.

tool: Claude Code 2.1.329 using Claude Opus 5.5, with ChatGPT (GPT-6) assisting with task prompts and result review, 2026-11-20.

prompts: AGENT-01 instructed the main agent to delegate AC-22 test analysis to test-analyst, payment security review to security-reviewer, and design compliance review to code-reviewer. AGENT-02 used `claude -p --output-format json` to analyze the AC-22 retry-date design gap without making changes. Exact prompts were supplied interactively; no repository prompt file verified.

review: AGENT-01 launched all three configured subagents. Test-analyst completed 21 reported tool calls, security-reviewer 14, and code-reviewer 12, totaling 47. The reviewers independently identified missing retry-date persistence, incomplete AC-22 implementation scope, and gaps in test coverage. The main agent consolidated the findings and identified decisions requiring human approval.

AGENT-02 independently identified the missing retry-date field, cross-month retry ambiguity, D18/D25 conflict, and uncertainty about the retry date after a Pending replay. The structured result explicitly reported that no subagents were used in AGENT-02.

checks: AGENT-01 → 3 subagents completed, 47 reported tool calls; no file modifications or shell commands reported. AGENT-02 → `type=result`, `subtype=success`, `is_error=false`, `terminal_reason=completed`, 0 permission denials, 0 subagents spawned, and 0 safety stops. Reported execution duration was 21.411 seconds and estimated API cost was $0.2033224. No application tests were executed during these analysis tasks.

evidence: S-6 AC-22; D15–D18, D25, D32; `docs/design/S-6.md`; `docs/plans/S-6-plan.md`; AGENT-01 transcript; `AGENT-02-headless.json`; headless session ID `7dc62edd-3323-4ba7-87fd-560c02ec6f65`.

risk: AC-22 remains unimplemented and its acceptance test remains skipped. The design lacks a persisted retry-anchor date, and the current implementation plan omits `app/db.py` from the AC-22 file list. Resolving the schema, retry timing, month-boundary behavior, and concurrency questions requires separate human approval. Neither analysis task proves that forbidden tools would be blocked under an attempted violation.

## Entry 45 — AGENT-03: Retrospective Audit of S-6 AC-18 Through AC-21

artifact: `docs/audits/S-6-AC18-AC21-retrospective.md`. Audit commit `c639e82`; merged through GitHub PR #7, merge commit `21887e9`.

tool: Claude Code main agent with three configured subagents (`test-analyst`, `security-reviewer`, `code-reviewer`), assisted by ChatGPT (GPT-6) for review and remediation planning, 2026-11-20.

prompts: AGENT-03 retrospective review of S-6 AC-18 through AC-21. The task requested independent test, security, and code reviews before implementing AC-22.

review: The three subagents reported 67 tool calls and produced 25 consolidated findings. Seven findings were prioritized: F-01, F-02, F-03, F-04, F-05, F-06, and F-23. The audit was reviewed and merged as a documentation-only record. Findings were classified as potential defects, missing test coverage, design inconsistencies, or historical scope issues rather than treating every finding as a confirmed bug.

checks: Read-only analysis using Read, Grep, and Glob. No application code was modified and no tests were executed during the audit. GitHub PR #7 was merged into `main`.

evidence: AGENT-03 audit report; S-6 AC-18 through AC-21; PR #7; commits `c639e82` and `21887e9`.

risk: The audit did not resolve the findings. F-01 concurrency and F-02 Paid-payment checking remain important correctness concerns. AC-22 remains unimplemented.

## Entry 46 — Initial F-23/F-06 Resolution Proposal

artifact: Initial documentation-only proposal to resolve AGENT-03 findings F-23 and F-06. No repository changes were made at this stage.

tool: Claude Code, with ChatGPT (GPT-6) reviewing the proposed decisions, 2026-11-20.

prompts: prompts/46-Initial-F-23F-06-design-review

review: Claude identified inconsistencies involving D18/D25, R4, ACH payment behavior, manual-payment errors, missing dues, and payment amount persistence. It proposed resolving these in `docs/design/S-6.md` and a new design-resolution record. F-06 was identified as requiring historical Git verification.

checks: Documentation and code inspection only. No tests were run or files changed as part of this proposal.

evidence: AGENT-03 F-23 and F-06; `docs/design/S-6.md`; initial resolution proposal.

risk: The initial proposal required further clarification of R4, Pending replay, and ACH limitations before approval.

## Entry 47 — Corrected S-6 Design Decisions

artifact: Revised F-23/F-06 documentation proposal, establishing DR-1, DR-2, DR-2a, DR-ACH, DR-3, DR-4, DR-5, and DR-6.

tool: Claude Code for design analysis; ChatGPT (GPT-6) for independent review, 2026-11-20.

prompts: Follow-up prompts requesting correction of R4, D18, D25, and the treatment of ACH schedules.

review: R4 was narrowed to initial attempt-1 creation for eligible debit and credit schedules. D18 was clarified as defining due timing, while D25 determines the processing action. The unresolved Pending-after-replay case was explicitly documented. ACH automatic charging was deferred until OQ2 is resolved.

checks: Proposed changes were compared against the existing design and reported implementation behavior. No application or acceptance-test changes were authorized.

evidence: S-6 R4, D18, D25, D26, D34; F-23; revised design proposal; final resolution in PR #8.

risk: ACH schedules can be created and displayed but are not automatically charged. Retry behavior remains dependent on AC-22.

## Entry 48 — 

artifact: Historical verification of the AC-18 test-fixture change in commit `6b1317f`. The result is recorded in `docs/reviews/S-6-AGENT-03-design-resolution.md`.

tool: Kundan reviewd using Git in WSL; ChatGPT (GPT-6) assisted with interpreting the evidence, 2026-11-20.

prompts: prompts/48-Incorporate human Git verification

review: Compared the original tests-first commit `e7f9eaa` against AC-18 commit `6b1317f`. The changes consisted of the new `s6_schedule` fixture, removal of the AC-18 skip marker, a test parameter change, and the `s6 = s6_schedule` alias. Existing assertions, expected values, and constants were unchanged. The change was retroactively approved as a one-time historical file-scope exception.

checks:
- `git diff e7f9eaa 6b1317f -- tests/test_s6_payments.py`
- `git log --oneline -- tests/test_s6_payments.py`
- Verification result: PASSED.

evidence: F-06; AC-18; `tests/test_s6_payments.py`; commits `e7f9eaa` and `6b1317f`; DR-6 in PR #8.

risk: The historical change exceeded the original approved file list. Retroactive approval does not authorize future unapproved test modifications.

## Entry 49 — F-23/F-06 Documentation Resolution

artifact: Updated `docs/design/S-6.md` and new `docs/reviews/S-6-AGENT-03-design-resolution.md`. Implementation commit `454df79`; GitHub PR #8, merge commit `45cfc4b`.

tool: Claude Code prepared the proposed documentation patch; Sandeep applied and committed the approved changes using Git/WSL. ChatGPT (GPT-6) reviewed the resulting documents.

prompts: prompts/49-Final R4Pending clarification

review: The final documentation incorporated DR-1, DR-2, DR-2a, DR-ACH, DR-3, DR-4, DR-5, and DR-6. It aligned R4, D18, D25, manual-payment errors, nullable dues, and payment amount persistence. The resolution record documents F-06 verification as PASSED and the historical fixture change as retroactively approved. No application code or tests were changed.

checks: The original generated patch failed `git apply --check` because its context did not match `docs/design/S-6.md`. A corrected patch was subsequently prepared and the documentation changes were committed. GitHub PR #8 confirms exactly two changed files and a successful merge into `main`. No application tests were run as part of this documentation-only change.

evidence: S-6 design; F-23; F-06; PR #8; commits `454df79` and `45cfc4b`.

risk: F-02, F-08, and F-25 remain outside the resolution. The documentation still contains outdated implementation/test-status wording. The resolution does not implement AC-22.

## Entry 50 — Restricted Claude Patch-Generation Workflow

artifact: `CLAUDE.md` and `.claude/settings.json`. Configuration commit `8f8ecf0`; incorporated into `main` through integration commit `f1de0ec`.

tool: Sandeep edited the project configuration using WSL; Claude Code tested the permission boundary and generated the documentation patch; ChatGPT (GPT-6) assisted with configuration and workflow review.

prompts: Claude patch-output authorization and permission-verification prompts, followed by the F-23/F-06 patch-generation request. Retain the exact prompts and Claude permission-denial reports as historical evidence.

review: The initial configuration denied Write because the permission rule did not match the attempted operation. The configuration was corrected to allow `Edit(./agent-patches/**)` while retaining `dontAsk` and denying Bash and NotebookEdit. `CLAUDE.md` was updated to authorize creation of new patch files only in `agent-patches/`, The permission configuration was committed separately from the design documentation.

checks: The first Write attempt was denied in `dontAsk` mode. After permission changes, Claude generated a patch file, as evidenced by the subsequent `git apply --check` attempt. The original patch had a context mismatch; the documentation was later successfully committed. GitHub commit `8f8ecf0` contains only the two configuration files.

evidence: `CLAUDE.md`; `.claude/settings.json`; commit `8f8ecf0`; integration commit `f1de0ec`; generated F-23/F-06 patch workflow.

risk: The scoped Edit permission is not a strict create-only guarantee and may allow overwriting files within the patch directory. `agent-patches/` is not currently excluded by `.gitignore`. 