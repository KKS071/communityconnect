# Prompt 88 — AGENT-22: Milestone 2 Mutation Evidence, Ledger Update, and Final Submission Audit

## Role and objective

You are **AGENT-22**, a documentation and evidence-review agent for the CS690 Milestone 2 CommunityConnect HOA Payment System project.

Your task is to prepare the final mutation-testing evidence, update the project ledger, and audit the Milestone 2 submission requirements.

**This is a documentation-only, patch-first task. You are not authorized to modify application behavior, execute tests, commit changes, push, or create tags.**

Do not apply any proposed documentation changes without explicit human approval.

## 1. Verified project status

The human operator has completed the following checks.

### Full regression testing

Command:

```bash
python -m pytest \
  --cov=app \
  --cov-branch \
  --cov-report=term-missing \
  --cov-fail-under=80
```

Verified results:

- 202 tests collected.
- 202 tests passed.
- Total branch-aware coverage: 94.34%.
- Required coverage threshold: 80%.
- One non-failing Starlette/httpx deprecation warning.
- Evidence: `evidence/mutation-regression-tests.txt`.

### Mutation testing

Mutation testing used `mutmut 3.8.1` against `app/payments.py` and `app/db.py`.

A controlled set of 30 mutants was selected from 603 generated mutants.

| Experiment | Killed | Survived | Score |
|---|---:|---:|---:|
| Baseline A | 25 | 5 | 83.33% |
| Baseline B with Hypothesis | 25 | 5 | 83.33% |
| After deterministic regression tests | 28 | 2 | 93.33% |

Evidence files:

- `evidence/mutation-baseline.txt`
- `evidence/mutation-properties.txt`
- `evidence/mutation-after.txt`
- `evidence/mutation-selected-diffs.txt`
- `evidence/mutation-regression-tests.txt`

The mutation score improved by **10 percentage points**.

The final mutation run reported:

- 30 selected mutants processed.
- 28 killed.
- 2 survived.
- No timeout or error classifications.
- `MUTMUT_RUN_EXIT_STATUS=0`.

The mutation tool warned that non-Python evidence files had changed and retained cached dependency results. Document this limitation accurately. Do not claim that all 603 mutants were executed or freshly regenerated.

### Regression tests added

Three deterministic tests were added to `tests/test_s6_payments.py`.

1. `test_d16_two_units_charged_in_one_run_are_both_counted`
   - Confirms two successful charges produce `RunResult(charged=2, failed=0, skipped=0)`.
   - Killed `app.payments.x__count_outcome__mutmut_5`.

2. `test_d16_two_unavailable_charges_are_both_counted_as_skipped`
   - Confirms two unavailable charges produce `RunResult(charged=0, failed=0, skipped=2)`.
   - Killed `app.payments.x__count_outcome__mutmut_20`.

3. `test_r4_paid_unit_does_not_stop_the_run_for_a_later_unit`
   - Confirms a manually Paid unit does not prevent processing a later due unit.
   - Killed `app.payments.x_run_due_payments__mutmut_89`.

The human operator ran the three focused tests:

**3 passed, 102 deselected.**

The complete suite subsequently passed all 202 tests.

### Protected files

The human operator verified:

```bash
git diff --exit-code m2-tests-locked -- \
  tests/acceptance \
  tests/conftest.py \
  tests/__init__.py \
  conftest.py \
  pytest.ini
```

Result:

`PROTECTED-UNCHANGED`

### Database cleanup

The human operator ran:

```bash
psql "$COMMUNITYCONNECT_TEST_DATABASE_URL" \
  -Atc "SELECT current_database(), (SELECT count(*) FROM pg_namespace WHERE nspname LIKE 'test_%')"
```

Result:

`communityconnect_test|0`

No temporary test schemas remain.

## 2. Analyze the two remaining mutants

Document both survivors carefully.

### Survivor A — `app.payments.x_run_due_payments__mutmut_109`

Mutation:

```python
prior["attempt"] < MAX_PAYMENT_ATTEMPTS
```

becomes:

```python
prior["attempt"] <= MAX_PAYMENT_ATTEMPTS
```

AGENT-20's analysis found:

- The database retry guard normally prevents an additional attempt beyond the maximum.
- In ordinary sequential execution, the mutation may not change externally visible results.
- A manual payment committed between the Paid pre-check and the payment claim may expose a difference in `RunResult.skipped`.
- D35 supports excluding exhausted schedules from the count.
- D16/D25 may support counting a schedule whose month becomes Paid during the race.

**Classification:** Survived; potentially observable under concurrency; unresolved specification/design question.

Do not classify this mutant as universally equivalent.

Do not invent a new requirement or choose the expected counter value without human approval.

Record the design question:

> If a schedule has exhausted its automatic payment attempts and a manual payment arrives between the Paid pre-check and the claim, should `RunResult.skipped` increase by one or remain unchanged?

### Survivor B — `app.payments.x__charge_pending__mutmut_38`

Mutation:

```python
return "Unchanged"
```

becomes:

```python
return "XXUnchangedXX"
```

AGENT-20 found:

- The public payment workflow ignores both return markers in `_count_outcome`.
- The observable `RunResult` and payment history remain unchanged.
- Calling the private helper directly would reveal the difference.

**Classification:** Equivalent through the reviewed public API, but not identical at the private function level.

Do not add tests solely to pin the internal marker.

Do not misrepresent this survivor as killed.

## 3. Inspect the repository and submission requirements

Read the relevant files before drafting documentation.

Inspect, where present:

- `MILESTONE2.md`
- `LEDGER.md` or the project's actual ledger file
- `S-6.md`
- `docs/audits/Milestone2-Completion-Audit.md`
- Existing milestone instructions and reports
- Existing evidence files
- Relevant prompt and agent-output records
- `git status --short`
- `git diff --stat`
- `git log -5 --oneline`

Identify the authoritative requirements and distinguish them from locally prepared checklists or summaries.

Do not assume that the local completion audit is the original assignment handout.

If a required document is missing, report it as missing. Do not invent its contents.

Verify the actual ledger filename, structure, and latest entry before proposing an update.

Preserve the existing ledger format, chronology, and terminology.

## 4. Prepare the mutation evidence summary

Prepare a proposed Markdown document:

`evidence/mutation-summary.md`

Include:

1. Experiment objective and scope.
2. Source files under mutation testing.
3. Tool version and selected mutant count.
4. Test selections used for Baselines A and B and the after-regression run.
5. Baseline A results.
6. Baseline B Hypothesis results.
7. Three new deterministic regression tests.
8. After-regression results.
9. Before-and-after comparison table.
10. Analysis of the two remaining survivors.
11. Coverage and regression-testing results.
12. Protected-file verification.
13. Database cleanup verification.
14. Reproducibility notes, including cached dependency warning.
15. Limitations and unresolved questions.

Clearly distinguish:

- Verified observations.
- Inferences from source-code inspection.
- Open design questions.

Use exact evidence filenames and commands where appropriate.

Do not claim the 93.33% score applies to all 603 generated mutants.

## 5. Prepare a ledger entry

Draft the next chronological ledger entry using the repository's established format.

The entry should capture:

- Mutation testing of the S-6 payment workflow.
- Initial 25/30 result.
- Hypothesis comparison with no score improvement.
- Analysis of the five original survivors.
- Three deterministic regression tests.
- Improved 28/30 mutation result.
- Full suite of 202 passing tests.
- Coverage of 94.34%.
- Protected acceptance tests unchanged.
- Zero leftover test schemas.
- Remaining mutants `_109` and `_38`.
- Evidence file references.
- Human review and approval boundaries.

Do not overwrite or rewrite previous ledger entries.

Do not invent commit SHAs or claim that a commit was created.

## 6. Prepare the Milestone 2 reflection

Inspect `MILESTONE2.md` and the actual assignment requirements.

If the project requires a 300–500 word reflection, prepare a draft within that word range.

Discuss the following, where supported by evidence:

- The RED/GREEN/REFACTOR workflow.
- The role of locked acceptance tests.
- AI-generated implementation and human approval.
- How Hypothesis expanded testing but did not improve the selected mutation score.
- Why deterministic tests killed three surviving mutants.
- The distinction between code coverage and mutation score.
- The importance of concurrency and explicit requirements.
- The remaining design question involving exhausted retries.
- Lessons about verification, reproducibility, and human oversight.

Do not falsely claim that the historical RED phase demonstrated a failing business-rule assertion if the recorded RED evidence only shows collection/import errors.

Do not invent team participation, agent runs, timings, or decisions.

Preserve any existing reflection text unless a revision is explicitly necessary and explain the proposed changes.

## 7. Final submission audit

Produce a concise audit table containing:

| Deliverable | Required? | Current status | Evidence | Action needed |
|---|---|---|---|---|

Check:

- Acceptance tests.
- Production implementation.
- RED/GREEN/REFACTOR evidence.
- Hypothesis/property tests.
- Mutation testing evidence.
- Mutation survivor analysis.
- Project ledger.
- Milestone reflection.
- Agent prompt and response records.
- Individual reports, if required.
- Git history and required tags.
- Submission packaging requirements.

Use these status values:

- Verified complete
- Present but needs review
- Missing
- Not yet verified
- Not applicable

Do not declare Milestone 2 ready for submission merely because the test suite passes.

Identify any remaining requirements that need human verification.

## 8. File and execution restrictions

**You may read files and run read-only inspection commands.**

You may create a proposed patch under `agent-patches/`.

Do not:

- Modify `app/**`.
- Modify `tests/**`.
- Modify locked acceptance files.
- Modify `pyproject.toml` or `pytest.ini`.
- Modify existing evidence logs.
- Apply a patch.
- Run pytest.
- Run mutmut.
- Create or delete database schemas.
- Modify database records.
- Delete or regenerate `mutants/`.
- Commit or push.
- Create or move Git tags.
- Stage files.
- Modify existing documentation directly without approval.

If a necessary action exceeds these permissions, stop and request human approval.

## 9. Required patch output

Create a unified diff patch:

`agent-patches/AGENT-22-M2-final-documentation.patch`

It should propose changes only to the appropriate documentation files, such as:

- `evidence/mutation-summary.md`
- The actual ledger file
- `MILESTONE2.md`, if a reflection update is required

For new files, use valid unified diff syntax.

Do not include unrelated formatting or cleanup changes.

Do not apply the patch.

If you cannot safely create a complete patch, provide the proposed document contents and explain the blocker instead.

## 10. Required final response

Return the following:

**A. Evidence verification**

List each evidence file inspected and the results it supports.

**B. Mutation results**

Show the three-experiment comparison and the two surviving mutants.

**C. Documentation patch**

Provide the patch filename, proposed files affected, and a summary of changes.

**D. Reflection**

Report the proposed reflection word count and its key themes.

**E. Submission audit**

Show completed, missing, and unverified deliverables.

**F. Risks and open questions**

Include the `_109` concurrency counting decision, the `_38` public-API equivalence assessment, and any submission requirements that could not be verified.

**G. Safety report**

Confirm which commands were run, which files were created, whether tests were executed, whether the patch was applied, and whether any commits or tags were created.

**H. Approval request**

Stop and request explicit human approval before applying any documentation changes.

**Do not commit, push, tag, or declare final submission complete.**