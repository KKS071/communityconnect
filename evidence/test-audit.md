# Milestone 2 acceptance-test audit (read-only)

All 11 acceptance criteria (S-1 AC-1–6, S-6 AC-18–22) have a test. None is skipped or marked xfail, and each matches its approved AC, including the amended AC-18. Nothing blocks the move today, but two things must be settled before the lock:
- **Fixture scope (F14):** the tests would be locked while their shared fixtures and helpers sit in files outside `tests/acceptance/`, which could still change and weaken them.
- **`reviewer` subagent:** the one this session exposes isn't the project's.

A genuine red run looks reproducible from a historical commit in a separate worktree, but I couldn't verify that commit's contents.

**How this audit was done:**
- I handed the test review to `test-writer`, with a read-only instruction; it used only Read.
- I didn't delegate to `reviewer`, because the `reviewer` this session offers is a different agent ("Reviews a changed Python file against spec.md"), not `.claude/agents/reviewer.md`. See G1.
- The Grep tool was unavailable here, so the subagent read each file in full.
- I worked out the commit history by reading `.git/logs/HEAD`, without running git.
- I modified nothing and ran nothing.

## A. Acceptance-test inventory

**Collection:** I checked statically. None has a skip or xfail marker. The `NOT_BUILT` constant at `tests/test_s6_payments.py:21` is now unused. `pytest.ini` sets `testpaths = tests`, and all names start with `test_`. Your 197-passed run is consistent with these being collected, but I didn't run pytest.

| Story | AC | Test | File:line | Reference | Matches approved AC? |
|---|---|---|---|---|---|
| S-1 | AC-1 | `test_ac1_resident_submits_request_shown_as_open` | `tests/test_s1_requests.py:30` | backlog AC-1; S-1 D5, D8 | Yes; uses `REQUEST_CATEGORIES[0]` rather than the literal "Plumbing" (F1) |
| S-1 | AC-2 | `test_ac2_blank_description_rejected_and_list_unchanged` | `:50` | AC-2; D9, D15 | Yes |
| S-1 | AC-3 | `test_ac3_other_community_resident_does_not_see_request` | `:63` | AC-3; R1, R2 | Yes (F3) |
| S-1 | AC-4 | `test_ac4_other_community_direct_id_returns_not_found` | `:74` | AC-4; R2, D3 | Yes |
| S-1 | AC-5 | `test_ac5_neighbor_in_same_community_does_not_see_request` | `:84` | AC-5; D2, D20 | Yes (F4) |
| S-1 | AC-6 | `test_ac6_resident_sees_in_progress_status` | `:93` | AC-6; D13 | Yes |
| S-6 | AC-18 | `test_ac18_schedule_shown_on_payments_page` | `tests/test_s6_payments.py:67` | amended AC-18; D10, §5 | Yes: `method` "ach", `day_of_month` 5, `active` True, no token. The comment is stale (F5). |
| S-6 | AC-19 | `test_ac19_due_day_charges_exactly_once` | `:83` | AC-19; R1, R3, D30, OQ1 | Yes |
| S-6 | AC-20 | `test_ac20_restart_mid_run_keeps_one_payment` | `:100` | AC-20; R2, D4, D29, D31 | Yes |
| S-6 | AC-21 | `test_ac21_manual_payment_prevents_scheduled_charge` | `:129` | AC-21; R3, D13, D25 | Yes |
| S-6 | AC-22 | `test_ac22_declined_charge_retried_after_delay` | `:144` | AC-22; R5, D15, D17, D35 | Yes |

The names match S-1 §9, S-6 §9 and `traceability.md`. About 20 other tests are also named `test_ac22_*`, but they are regression tests, not acceptance tests (F13).

## B. Findings
The findings are the test-writer's. I checked them against the sources and agree with all of them; the reviewer comparison wasn't possible. Every expected value is derived from the ACs, settings or fixture data, not from implementation behaviour.

| # | File:line | AC | Severity | Problem | Recommended correction |
|---|---|---|---|---|---|
| **F14** | `tests/conftest.py:20-111`, `tests/helpers.py:15`, `tests/test_s6_payments.py:21-64` | all | **blocking (for the lock)** | The locked tests would depend on fixtures, helpers and constants outside `tests/acceptance/`: `world`, `set_status`, `s6`, `s6_schedule`, `schedule`, `history`, `SimulatedCrash`, `DUES_CENTS` and others. Editing those could weaken a locked test without touching it. The handout's `git diff … -- tests/acceptance` check wouldn't show such a change. | Move the S-6 shared items into `tests/acceptance/`, and also deny edits to `tests/conftest.py` and `tests/helpers.py` at lock time (section C). |
| F8 | `tests/test_s6_payments.py:42`, `:116` | AC-19–22 | minor; fix before the lock | The `s6` fixture and the AC-20 test call `set_processor` and never restore it (F-16). Processor state leaks between tests, though no current order fails. | Restore it with `monkeypatch`, like `install_processor`. This doesn't change any expected value. |
| F5 | `:68-69` | AC-18 | minor; fix before the lock | The comment still quotes the old display text | Cite amended AC-18 and D10 instead |
| F6 | `:88-89` | AC-19 | minor | The Given ("no payment for the month") isn't asserted | Add `assert history(s6) == []` before the run |
| F7 | `:96-97` | AC-19 | minor | After the second run only the length is checked, and the processor call count isn't checked | Add `history(s6) == rows` and `len(s6.fake.calls) == 1` |
| F9 | `:125-126` | AC-20 | minor | `len(keys) == 1` doesn't check the key value or that the restart called the processor again | Check the call keys equal `["{unit}:2026-12:1"] * 2` (§5, D4) |
| F11 | `:149-159` | AC-22 | minor | No check that the retry date stays in December | Add `assert DUE_DAY + settings.RETRY_DELAY_DAYS <= 31` |
| F12 | `:157` | AC-22 | minor | The before-delay check only counts rows, and it's skipped when the delay is 1 | Assert `[(1, "Failed")]` |
| F10 | `:135` | AC-21 | minor | "The manager recorded a check" can't be fully tested: there's no caller, authorization or payment-type field (P-05) | Record it as a known limitation; no test change |
| F13 | `:870-1232` | AC-22 | minor | The `test_ac22_*` regression tests could be moved or locked by mistake | Move tests by exact test ID |
| F15 | (new folder) | all | minor | `tests/` is a package, so new files there need care | Add `tests/acceptance/__init__.py` and use distinct file names |
| F1 | `tests/test_s1_requests.py:33` | AC-1 | minor | AC-1 names "Plumbing", but S-1 D8 says tests read categories from settings | Your decision (G4) |
| F2–F4 | `test_s1_requests.py:54`, `:67-71`, `:88-90` | AC-2, 3, 5 | minor | The setup isn't asserted, so a check against an empty list could pass without testing anything | Assert the setup step returns 201, or that the result is `[]` (D20) |
| F16 | `docs/requirements/backlog.md:69` | AC-18 | minor | The amendment is dated 2026-11-23. Your message gives that date; the session's environment date was 2026-11-22. | Confirm the date for the ledger |

**Strengthening before the lock:** F2–F9, F11 and F12 only add assertions and don't change any expected value. The handout allows human fixes before the lock if they're committed separately from agent changes.

## C. Test organization plan

The handout's 3a moves the tests of the story being built, S-6. I recommend moving **only the five S-6 acceptance tests** and leaving S-1 in `tests/test_s1_requests.py`. That's the smallest change, and S-1 stays protected by the rule against weakening tests. If you want S-1 locked too, that's G2.

Proposed layout. The file has to be split, and the moved tests stay word for word:

| Path | Contents |
|---|---|
| `tests/acceptance/__init__.py` | empty |
| `tests/acceptance/s6_support.py` | Moved word for word from `test_s6_payments.py:15-64`: imports, the constants `NOT_BUILT`, `MONTH`, `DUE_DAY`, `DUES_CENTS`, `GOOD_TOKEN`, `DECLINED_TOKEN`, plus `SimulatedCrash`, the fixtures `s6` and `s6_schedule`, and the helpers `schedule` and `history`. Plus the F8 restore fix, if approved. |
| `tests/acceptance/test_s6_acceptance.py` | The five AC tests (`:67-163`) moved word for word, importing fixtures and helpers from `s6_support`. Plus the F5 comment fix and any approved strengthening. |
| `tests/test_s6_payments.py` | Remove the moved blocks; import the shared items from `tests.acceptance.s6_support`. The regression tests stay as they are. |

Points about the layout:
- **How the fixtures are found:** pytest picks up fixtures that are imported into a test module. `tests/conftest.py` still supplies `world` to both locations.
- **Lock scope (F14):** at lock time, deny edits to `tests/acceptance/**`, `tests/conftest.py` and `tests/helpers.py`.
- **Name clashes:** no two test files share a base name.
- **The rest of `pytest.ini`:** works as it is.
- **Module docstring:** the docstring in `test_s6_payments.py` would need a small wording change.
- **Paths elsewhere:** S-6 §9 and the S-6 rows of `traceability.md` must then point to the new paths (handout 5f).

## D. Red-evidence feasibility

**Candidate commit:** `bd558d4` ("docs: add S-6 implementation plan after team review"). It's the last commit before `6b1317f` ("Implement S-6 AC-18…"); see reflog lines 8–11. At that point, according to LEDGER entries 35–38:
- the S-6 tests existed and were all skipped;
- `app/payments.py`, `processor.py`, `clock.py`, the schedule routes and the S-6 tables did not exist;
- S-1 was already complete on PostgreSQL.

I couldn't check the files in that commit without git. Confirm with `git ls-tree -r --name-only bd558d4 app tests`.

**Expected outcome if the current acceptance files run against that code:**

| Test | Expected result | Reason |
|---|---|---|
| AC-18 | FAIL | The POST route is missing, so it returns 404 instead of 201 |
| AC-19–21 | ERROR at setup | The `s6` fixture imports `app.processor` and `app.clock`, which don't exist yet |
| AC-22 | ERROR at setup | Same fixture import, before its own check of `settings.MAX_PAYMENT_ATTEMPTS` can run |
| S-1 tests | PASS | S-1 was complete at that commit |

Setup errors count as not passing, but the honest description is "4 errors at fixture setup, 1 failure", not "5 failures".

**Compatibility risks:**
- `tests/conftest.py` and `tests/helpers.py` must match between `bd558d4` and `main`. Check with `git diff bd558d4 main -- tests/conftest.py tests/helpers.py`.
- The working tree at that commit has no `tests/acceptance/`. You'd copy the moved files in.
- No migrations are involved: each test creates a fresh schema.

**Honest capture plan (for you to run):**
1. Create a worktree at `bd558d4` outside the main checkout.
2. Copy `tests/acceptance/` from the post-move commit into it.
3. Run the README test command there and save its raw output as `evidence/red.txt`.
4. In `MILESTONE2.md` and the ledger, state plainly that this is a **historical reconstruction**: the code was built before the lock, so the red run was produced afterwards against the pre-implementation commit. Give the commit, the copy step and the reason.

The handout's red → lock → green order can't be replayed exactly. This is the limitation to record in the reflection.

## E. Test-lock checklist (in order; nothing done yet)
1. You approve this audit and the decisions in section G.
2. Prompt 76: I prepare the organization patch (section F).
3. You apply it, review the diff, and run `python -m pytest` and the coverage command. Record the real results.
4. Save the audit report as `evidence/test-audit.md` and export the delegation transcript (`/export evidence/delegation/test-writer-audit.txt`). Answer each finding in `MILESTONE2.md` as fixed (with SHA) or rejected (with reason). Commit your own fixes separately from the agent's changes.
5. Capture `evidence/red.txt` as in section D.
6. Add deny rules to `.claude/settings.json`: `Edit(./tests/acceptance/**)`, `Edit(./tests/conftest.py)`, `Edit(./tests/helpers.py)`. Commit, then restart Claude Code and check with `/permissions`.
7. Ask the agent to change an expected value in one acceptance test, and save the tool's refusal as `evidence/permission-denied.md`.
8. Tag the lock commit `m2-tests-locked` and push the tag.

## F. Prompt 76 patch, files that would change
- `tests/acceptance/__init__.py` (new)
- `tests/acceptance/s6_support.py` (new)
- `tests/acceptance/test_s6_acceptance.py` (new)
- `tests/test_s6_payments.py` (moved blocks removed, imports added)
- `docs/design/S-6.md` §9: test paths
- `docs/requirements/traceability.md`: the S-6 rows' paths

The settings deny rules are a separate patch at lock time (step E6).

## G. Decisions needed from you
1. **The `reviewer` subagent isn't the project's.** The agent exposed here is a different "reviewer", probably a user-level `~/.claude/agents/reviewer.md` with the same name. Check for and rename or remove it. Otherwise 4c (delegation) and 6 (headless review) would use the wrong agent.
2. **S-1 lock scope:** move only S-6 (recommended), or also lock S-1?
3. **F14:** approve the `s6_support.py` approach and extending the lock to `tests/conftest.py` and `tests/helpers.py`.
4. **Pre-lock fixes:** include F5 and F8, and optionally F2–F4, F6, F7, F9, F11, F12. Decide F1 ("Plumbing" vs S-1 D8).
5. **Red evidence:** approve the `bd558d4` historical-reconstruction method and the disclosure wording.
6. **F16:** confirm the amendment date.

## Report details
- **Task:** Prompt 75 acceptance-test audit.
- **Agents:** main agent plus `test-writer` (read-only).
- **Not examined this session:** the handout (read earlier) and LEDGER.md beyond the commit references (from earlier reads).
- **Changes, commands and tests:** none.
- **Approval status:** waiting for you.