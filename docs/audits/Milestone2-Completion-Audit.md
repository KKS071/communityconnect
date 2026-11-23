# Milestone 2 Completion Audit — Claude Code Read-Only Report

> Source: Claude Code response to Prompt 62, supplied by the project owner. This is a preserved audit report, not independently verified test output. The audited reference was `main (5c87562)`; check against current `main` before acting. No commands or tests were run during this audit.

---

Milestone 2 completion audit: handout vs. main (5c87562)

The S-6 code is the strongest part of the repository: all five ACs are built and your last run showed 197 passed, 0 skipped. But Milestone 2 is graded on the handout's deliverables, and nearly all of those are still missing. I estimate about 30–45 team-hours of remaining work.

Before most of it can start, four decisions are yours:
1. Answer OQ1–OQ5.
2. Choose an honest way to produce the "red → lock → green" evidence, because S-6 was built before the tests were locked.
3. Rework the Claude Code setup to match the handout.
4. Approve the new test dependencies.

I modified no files. Bash is denied in .claude/settings.json, so I couldn't run git, tests, coverage or mutation, and every "unverified" below needs you to run a command. I also read the git refs directly: no tags exist locally.

Deliverable-by-deliverable status

Status: ✅ done · 🟡 partial · ❌ missing. Blocks: Yes = required for submission.

1. Follow-up, story and open questions

§: 1a
Requirement: Milestone 1 follow-up ("No items" or a response to each
  feedback item)
Status: ❌
Evidence: Not in the repository
Remaining: Get the instructor's Milestone 1 feedback; answer each item
  in MILESTONE2.md
Blocks: Yes
Hours: 0.5–1
────────────────────────────────────────
§: 1b
Requirement: Story ID, Connextra story, E-IDs, AC IDs, file list
Status: 🟡
Evidence: docs/requirements/backlog.md (S-6), docs/design/S-6.md
Remaining: Write it up in MILESTONE2.md. Files: app/payments.py,
  app/db.py, app/processor.py, app/clock.py, app/settings.py,
  app/main.py, app/access.py
Blocks: Yes
Hours: 0.5
────────────────────────────────────────
§: 1c
Requirement: Settle every open question and every named setting in §8,
  with sources
Status: ❌
Evidence: S-6.md §8 still says "Stop and ask" for OQ1–OQ5.
  RETRY_DELAY_DAYS and MAX_PAYMENT_ATTEMPTS are provisional (D15). The
  DUES_AMOUNT_CENTS value has no source.
Remaining: Team decides OQ1–OQ5 (each with an E entry, interviewee
  follow-up, or team reason). If an answer changes an AC, update the
  doc, then the AC, then the test. Record each setting's value and
  source.
Blocks: Yes
Hours: 3–6
────────────────────────────────────────
§: 1d
Requirement: Gap check 2: prompt in prompts/, reply in
  docs/design/S-6-gap-check-2.md, triage marks, gaps settled in §8,
  committed before the lock
Status: ❌
Evidence: Only the Milestone 1 S-6-gapcheck.md exists
Remaining: Run the gap-check prompt with the agent on the updated doc,
  triage each question, then commit
Blocks: Yes
Hours: 2–3

2. Agent setup

§: 2a
Requirement: AGENTS.md under 100 lines, with install, run, test and
  coverage commands tried on a fresh clone; folder layout including
  tests/acceptance/; testing rules; git and ledger rules. CLAUDE.md
  first line @AGENTS.md
Status: 🟡
Evidence: AGENTS.md is 63 lines but out of date: it says S-1 is "the
  story being built". It has no coverage command, no tests/acceptance/
  rules, and no commit-message or ledger rule. CLAUDE.md doesn't start
  with @AGENTS.md.
Remaining: Rewrite both files and do a fresh-clone run of the commands
Blocks: Yes
Hours: 1.5–2
────────────────────────────────────────
§: 2b
Requirement: .claude/settings.json: deny Edit(./tests/acceptance/**)
  (added at lock time), Read(./.env), Bash(git push *) and Bash(rm -rf
  *); allow the test command
Status: ❌
Evidence: Current file denies all Bash and allows edits only under
  agent-patches/. No .env or push rules.
Remaining: Replace the blanket Bash deny with the handout's rules, plus
  allows for python -m pytest and the coverage command.
Blocks: Yes
Hours: 0.5–1
────────────────────────────────────────
§: 2b
Requirement: evidence/permission-denied.md: prompt, the tool's refusal
  message, and the rule that blocked it
Status: ❌
Evidence: No evidence/ directory
Remaining: After the lock, ask the agent to change an expected value in
  one acceptance test and save the tool's own refusal
Blocks: Yes
Hours: 0.5
────────────────────────────────────────
§: 2c
Requirement: Subagents named test-writer (Read, Grep, Glob, Edit, Write,
  Bash; never edits source; AC ID on every test) and reviewer
  (read-only; each finding gives file, line, AC ID, severity "blocking"
  or "minor", problem)
Status: ❌
Evidence: Only test-analyst, security-reviewer and code-reviewer exist
Remaining: Write the two new agent files yourselves, as the handout
  requires. Keep or retire the existing three.
Blocks: Yes
Hours: 1–1.5

3. Acceptance tests and the lock

§: 3a
Requirement: Move S-6 tests to tests/acceptance/, remove skip marks,
  keep AC IDs
Status: ❌
Evidence: All tests are in tests/test_s6_payments.py, which mixes
  AC-18–22 with the F-0x and AC-22 regression tests
Remaining: Move AC-18–22 (and their fixtures and helpers) to
  tests/acceptance/. Move the regression tests to tests/unit/ or
  tests/integration/.
Blocks: Yes
Hours: 1–2
────────────────────────────────────────
§: 3b
Requirement: test-writer audit of the tests: evidence/test-audit.md,
  each finding answered in MILESTONE2.md with a SHA or reason, human
  fixes committed separately
Status: ❌
Evidence: The AGENT-03 audit used test-analyst, and the handout names
  test-writer
Remaining: Run it with test-writer, review it, answer each finding
Blocks: Yes
Hours: 2–3
────────────────────────────────────────
§: 3c
Requirement: evidence/red.txt: S-6 acceptance tests fail, S-1 tests pass
Status: ❌ conflict
Evidence: S-6 is already built, so its tests now pass
Remaining: Decision needed (D-2 below)
Blocks: Yes
Hours: 1–2
────────────────────────────────────────
§: 3d
Requirement: Add the lock rule, commit, tag and push m2-tests-locked
Status: ❌
Evidence: No tags
Remaining: Depends on D-2
Blocks: Yes
Hours: 0.25

4. Plan and build

§: 4a
Requirement: docs/plans/S-6-plan.md, with at least 2 team changes
  recorded in MILESTONE2.md
Status: 🟡
Evidence: The plan exists (Milestone 1 / 2026-11-19), but it's out of
  date: it lists D1–D34 and doesn't include db.py for AC-22
Remaining: Record at least 2 plan changes and why. Optionally refresh
  the plan.
Blocks: Yes
Hours: 0.5–1
────────────────────────────────────────
§: 4b
Requirement: Bounded tasks: prompts in prompts/, commits naming the task
  and AC ID, ledger entry per task
Status: 🟡
Evidence: AC-18–21 were built through ChatGPT. Ledger entries 37–44 say
  "no separate prompt file verified". AC-22 was built through Claude
  (Prompts 54–59, commit 719aecc).
Remaining: Honestly record which tool built AC-18–21 (the handout says
  to name another tool in the ledger). Back-fill prompt files only if
  the real prompts exist; never reconstruct them. Commit-message format
  is unverified.
Blocks: Partly
Hours: 1–2
────────────────────────────────────────
§: 4c
Requirement: Delegation: reviewer report and test-writer audit in
  evidence/delegation/, plus /export transcripts
Status: ❌
Evidence: Earlier delegations used other agent names and weren't
  exported
Remaining: Delegate a finished task to reviewer and run /export
  evidence/delegation/<name>.txt
Blocks: Yes
Hours: 1
────────────────────────────────────────
§: 4d
Requirement: evidence/green.txt, tag m2-green, empty git diff --stat
  m2-tests-locked m2-green -- tests/acceptance
Status: ❌
Evidence: The 197-passed run is recorded in the ledger only, not as a
  tool-output file
Remaining: Run after the lock; depends on D-2
Blocks: Yes
Hours: 0.5
────────────────────────────────────────
§: 4e
Requirement: One agent refactor with all tests passing,
  evidence/refactor.txt
Status: ❌
Evidence: —
Remaining: Small refactor, for example dedupe the counting blocks in
  payments.py. This needs an edit permission or the patch workflow.
Blocks: Yes
Hours: 1–2
────────────────────────────────────────
§: 4f
Requirement: README "Try the story": one start command, steps showing
  each AC, screenshots in evidence/screens/ including the empty and
  error states
Status: ❌
Evidence: README still describes Milestone 1 ("S-6 … tests skipped").
  S-6 has no UI (D10). run_due_payments has no command (D19 not built),
  and the default processor always raises "unavailable".
Remaining: Decision needed (D-5)
Blocks: Yes
Hours: 3–5

5. Test strength

§: 5a
Requirement: Unit test for every §7 edge case, and at least one invalid
  input per §4 function
Status: 🟡
Evidence: Many already exist as F-04 and AC-22 regression tests
Remaining: Move them out of the acceptance file and map them to §7 and
  §4. Fill gaps, for example a day_of_month of 29–31, which §7 lists.
Blocks: Yes
Hours: 1–2
────────────────────────────────────────
§: 5b
Requirement: At least 1 integration test with no mocks, naming the two
  parts joined
Status: 🟡
Evidence: Most tests already exercise payments against real PostgreSQL
  through db
Remaining: Pick and label one, then name the two parts in MILESTONE2.md
Blocks: Yes
Hours: 0.5
────────────────────────────────────────
§: 5c
Requirement: At least 2 Hypothesis property tests, each built from an §6
  rule
Status: ❌
Evidence: hypothesis isn't installed
Remaining: Write them, for example R1 (at most one Paid per unit and
  month) and R2 (unique keys) over random run sequences
Blocks: Yes
Hours: 2–3
────────────────────────────────────────
§: 5d
Requirement: Test command fails below 80% line coverage (--cov-branch);
  evidence/coverage.txt; one uncovered line or branch explained
Status: ❌
Evidence: pytest-cov isn't installed; pytest.ini has no threshold
Remaining: Add the threshold to pytest.ini and the README command, then
  run
Blocks: Yes
Hours: 1
────────────────────────────────────────
§: 5e
Requirement: mutmut configured for the story's logic files only
  (pyproject.toml); mutation-before.txt and mutation-after.txt; survivor
  table with SHAs or reasons; one sentence on mutation vs. coverage
Status: ❌
Evidence: No pyproject.toml; mutmut isn't installed
Remaining: Scope it to app/payments.py, and maybe app/db.py. The full
  suite takes about 350 s on PostgreSQL, so mutation runs will be slow:
  restrict which tests run. Triage up to 20 survivors.
Blocks: Yes
Hours: 4–8
────────────────────────────────────────
§: 5f
Requirement: Traceability rows in MILESTONE2.md (evidence ID, story, AC,
  test, commit that made it pass); §9 lists the same tests
Status: 🟡
Evidence: docs/requirements/traceability.md (Milestone 1); S-6.md §9
Remaining: Add the passing-commit column; update §9 after the test move.
  Implementation SHAs exist in the ledger: AC-19 ce8671e, AC-20 caa65a8,
  AC-22 719aecc.
Blocks: Yes
Hours: 1

6–9. Headless run, ledger, report, contribution statements

§: 6a
Requirement: agent/review-schema.json
Status: ❌
Evidence: —
Remaining: Write the schema
Blocks: Yes
Hours: 0.5
────────────────────────────────────────
§: 6b
Requirement: scripts/review_story.sh
Status: ❌
Evidence: Entry 44's claude -p run is only partial precedent
Remaining: Use the handout's template with src changed to app. No --bare
  or bypass.
Blocks: Yes
Hours: 0.5
────────────────────────────────────────
§: 6c
Requirement: evidence/headless-review.json as written by the tool; every
  finding answered
Status: ❌
Evidence: —
Remaining: Run at or after m2-green, answer each finding
Blocks: Yes
Hours: 1–2
────────────────────────────────────────
§: 7
Requirement: Ledger: an entry for every agent task, subagent named in
  the tool field, SHAs, prompt files, at least 5 specific review fields,
  at least 3 specific risks
Status: 🟡
Evidence: 54 entries in LEDGER.md. The specific review and risk counts
  are met.
Remaining: Problems to fix:<br>• Entries 37–45 have no prompt
  files.<br>• Entries 51–54 use non-standard field names (Date, Status,
  Tests).<br>• Some tool fields lack a model version.<br>• Prompts 60–62
  have no entries yet.<br>• Every new Milestone 2 task needs an entry.
Blocks: Yes
Hours: 2–3 (plus ongoing)
────────────────────────────────────────
§: 8
Requirement: MILESTONE2.md in the handout's 7 sections, including a
  300–500-word reflection written by the team
Status: ❌
Evidence: —
Remaining: Write it last. The reflection must be your own writing.
Blocks: Yes
Hours: 3–4
────────────────────────────────────────
§: 9
Requirement: Signed contribution statement from each member
Status: ❌
Evidence: Only docs/contribution-statement-TEMPLATE.md
Remaining: Each member writes their own
Blocks: Yes (per person)
Hours: 0.5 each
────────────────────────────────────────
§: Turn-in
Requirement: Tags m2-tests-locked, m2-green, m2-submit pushed; public
  URL; final SHA
Status: ❌
Evidence: No tags
Remaining: Tag and push at the end
Blocks: Yes
Hours: 0.25
────────────────────────────────────────
§: Other
Requirement: README follows on a fresh clone; no .env committed
Status: 🟡
Evidence: README install steps exist but the status is stale; .gitignore
  exists
Remaining: Update the status and add the coverage command. Check .env is
  git-ignored (unverified).
Blocks: Yes
Hours: 0.5

Decisions you need to make first

- D-1. OQ1–OQ5 (deliverable 1c). The handout requires answers. Until now the project deliberately left them open, so the answers must come from the team, not the agent. Some answers may change ACs and tests:
  - OQ2 (ACH shown as Paid) affects D34 and the ACH tests.
  - OQ4 (board members) affects payment-list access.
  - OQ5 (manual payment vs. Pending) affects D26, D27 and F-01.
  - OQ3 (earlier months) affects the cross-month retry limitation.
- D-2. Red → lock → green when the code already exists. The handout counts evidence not produced by the tools as fabrication. Honest options:
  - (a) Lock the acceptance tests now on main and record red.txt as it really is (passing), with an explanation. Then tag m2-green after a later commit.
  - (b) In a separate worktree at a pre-S-6 commit, run the moved, unskipped acceptance tests to get a genuine failing run. Disclose clearly that it's a historical reconstruction.
  - Either way, explain it in MILESTONE2.md and the ledger. Asking the instructor first would be wise.
- D-3. Claude Code setup. This means three changes:
  - Rewrite .claude/settings.json to the handout's rules. That removes the blanket Bash deny and the patch-only mode, or narrows them.
  - Add test-writer and reviewer.
  - Make CLAUDE.md start with @AGENTS.md.

  These change how I work in this repository, so they're your call.
- D-4. Dependencies. Approve pytest-cov, hypothesis and mutmut, as AGENTS.md requires.
- D-5. How to demonstrate the story (4f). Options:
  - FastAPI's built-in /docs page covers AC-18, the payment list and the error states.
  - AC-19 to AC-22 need either a demo command that runs run_due_payments with FakeProcessor, or the D19 python -m app.run_payments command. Both are new code to approve.

F-08 and the other open AGENT-03 findings

None of these is required by the handout. The reviewer runs in 3b and 6c may raise them, and you'd then answer them as fixed or rejected.

Finding: F-08: double-counted skipped in RunResult
Status: Open. Tests deliberately don't pin skipped after a replay.
Milestone 2 relevance: Likely to surface in a mutation survivor or a
  reviewer finding
Recommendation: Make a D16 ruling, then a small fix (about 1–2 h).
  Otherwise reject it in MILESTONE2.md with a reason. Optional.
────────────────────────────────────────
Finding: F-07 placeholder processor leaves payments Pending forever
Status: Open
Milestone 2 relevance: Affects 4f: a real run never charges
Recommendation: Covered by the D-5 demo approach
────────────────────────────────────────
Finding: F-09 ACH
Status: Settled by DR-ACH / D34
Milestone 2 relevance: Becomes D-1 (OQ2)
Recommendation: —
────────────────────────────────────────
Finding: F-10 validation order
Status: Open; needs a D12 ruling
Milestone 2 relevance: Could appear in the test audit
Recommendation: Decide with the 1c work
────────────────────────────────────────
Finding: F-12 concurrent POSTs give a 500
Status: Open
Milestone 2 relevance: Optional
Recommendation: Fix only if the reviewer raises it
────────────────────────────────────────
Finding: F-13 manual-payment ValueError for no dues
Status: Settled by DR-4
Milestone 2 relevance: —
Recommendation: —
────────────────────────────────────────
Finding: F-14 UTC conversion
Status: Open
Milestone 2 relevance: Optional
Recommendation: Small fix if wanted
────────────────────────────────────────
Finding: F-15 missing DB constraints
Status: Open
Milestone 2 relevance: Optional
Recommendation: Defer
────────────────────────────────────────
Finding: F-16 s6 fixture doesn't restore the processor
Status: Partly mitigated by install_processor
Milestone 2 relevance: Becomes relevant when fixtures move to
  tests/acceptance/ (3a)
Recommendation: Fix during the move, before the lock
────────────────────────────────────────
Finding: F-17, F-18, F-19, F-20, F-21
Status: Known limitations
Milestone 2 relevance: Future work (Stripe, CLI)
Recommendation: Document as risks
────────────────────────────────────────
Finding: F-22 board members
Status: Becomes D-1 (OQ4)
Milestone 2 relevance: —
Recommendation: —
────────────────────────────────────────
Finding: F-24 AGENTS.md SQL-file list
Status: Open
Milestone 2 relevance: AGENTS.md is being rewritten for 2a anyway
Recommendation: Fix in 2a
────────────────────────────────────────
Finding: D32/D35 conflict risk
Status: Accepted residual risk
Milestone 2 relevance: Reflection material
Recommendation: Keep as a ledger risk

Effort and suggested order

┌──────────────┬────────────────────────────────────┬─────────────────┐
│    Phase     │                Work                │      Hours      │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ A. Decisions │ D-1 to D-5, Milestone 1 feedback   │ 3–6             │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ B. Docs      │ 1b–1d, gap check 2                 │ 3–4             │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ C. Agent     │ 2a–2c                              │ 3–4             │
│ setup        │                                    │                 │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ D. Tests     │ Move, audit, red, lock, permission │ 5–8             │
│              │  proof (3a–3d, 2b proof)           │                 │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ E. Build     │ Plan notes, delegation, green,     │                 │
│ evidence     │ refactor, demo and screenshots     │ 6–10            │
│              │ (4a, 4c–4f)                        │                 │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ F. Test      │ Unit, integration, properties,     │                 │
│ strength     │ coverage, mutation, traceability   │ 9–15            │
│              │ (5a–5f)                            │                 │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ G. Headless  │ 6a–6c                              │ 2–3             │
│ review       │                                    │                 │
├──────────────┼────────────────────────────────────┼─────────────────┤
│ H. Paperwork │ Ledger cleanup, MILESTONE2.md,     │ 6–8             │
│              │ reflection, statements, tags (7–9) │                 │
├──────────────┼────────────────────────────────────┼─────────────────┤
│              │                                    │ about 37–58     │
│ Total        │                                    │ hours across    │
│              │                                    │ the team        │
└──────────────┴────────────────────────────────────┴─────────────────┘

The total is above the handout's 30–40-hour estimate, mainly because of D-2, mutation runs against PostgreSQL, and the S-6 demo.

Critical path: D-1 → 1c/1d committed → 2a–2c → 3a–3d (lock) → 4c–4f → 5 → 6 → MILESTONE2.md → tags.

Commands for you to run (things I couldn't check)

! git tag -l
! git ls-files | grep -E '^(evidence|tests/acceptance|scripts|agent)/|MILESTONE2|pyproject'
! git ls-files agent-patches | head
! git check-ignore .env && echo ignored
! git log --oneline -n 40
! python -m pytest

The git log --oneline -n 40 command checks the commit-message format ("task N … (AC-x)").

agent-patches/ is local work. Decide whether it belongs in the submission, and if not, add it to .gitignore.

Report details

Field: Task
Value: Milestone 2 completion audit
────────────────────────────────────────
Field: Agent
Value: Main agent only, no subagents
────────────────────────────────────────
Field: Files examined
Value: Handout PDF (all 11 pages); AGENTS.md; CLAUDE.md; README.md;
  LEDGER.md (prompt and tool fields); .claude/settings.json;
  .claude/agents/; requirements.txt; file listings of docs/, prompts/,
  tests/; S-6.md §8; the AGENT-03 audit; git refs
────────────────────────────────────────
Field: Changes
Value: None
────────────────────────────────────────
Field: Commands and tests
Value: None run
────────────────────────────────────────
Field: Approval status
Value: Waiting for your decisions D-1 to D-5
