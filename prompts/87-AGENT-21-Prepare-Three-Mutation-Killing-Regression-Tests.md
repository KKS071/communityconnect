**Prompt 87 — AGENT-21: Prepare Three Mutation-Killing Regression Tests**

Prepare a unified diff patch for three deterministic regression tests addressing confirmed gaps in Milestone 2 mutation testing.

**Evidence**

- Baseline A: 25/30 mutants killed (83.33%).
- Baseline B with Hypothesis: 25/30 mutants killed (83.33%).
- The same five mutants survived both runs.
- `mutmut tests-for-mutant` confirmed that Hypothesis Property 1 was selected for `_count_outcome_5`.
- The human-run verbose Hypothesis output confirmed all 10 examples used only one resident.
- AGENT-20 Prompt 86 confirmed that `due_schedules()` orders by `unit_id`, with MR-12 created before MR-20.

**Target file**

`tests/test_s6_payments.py` only.

**Required tests**

T1 — Multiple successful charges (D16)

- Schedule R1 and R3 with valid payment methods.
- Execute one due-date payment run.
- Assert `RunResult(charged=2, failed=0, skipped=0)`.
- Verify both units have Paid payment records.
- Verify exactly two processor calls.
- Target: `app.payments.x__count_outcome__mutmut_5`.

T2 — Multiple unavailable charges (D16/R4)

- Make the fake processor unavailable.
- Schedule R1 and R3.
- Execute one due-date payment run.
- Assert `RunResult(charged=0, failed=0, skipped=2)`.
- Verify both units remain Pending.
- Target: `app.payments.x__count_outcome__mutmut_20`.

T3 — Paid unit must not stop later due units (R4/D25)

- Schedule both R1 and R3.
- Record a manual Paid payment for MR-12.
- Confirm MR-12 precedes MR-20 in due-schedule ordering.
- Execute the due-date payment run.
- Assert `RunResult(charged=1, failed=0, skipped=1)`.
- Verify MR-12 remains manually Paid.
- Verify MR-20 receives an attempt-1 Paid debit payment.
- Verify only MR-20 is charged by the processor.
- Target: `app.payments.x_run_due_payments__mutmut_89`.

**Implementation constraints**

1. Reuse existing fixtures, helpers, and conventions.
2. Add only the three tests to `tests/test_s6_payments.py`.
3. Do not modify production code.
4. Do not modify locked acceptance tests, fixtures, or configuration.
5. Do not modify Hypothesis properties.
6. Do not change the behavior of existing tests.
7. Do not run pytest or mutation testing.
8. Do not commit or push.
9. Create a unified diff patch under `agent-patches/`.
10. Do not apply the patch.

**Reporting**

Return:
- Patch filename.
- Exact files affected.
- Complete proposed test code.
- Mapping of each test to its mutant and requirements.
- Any assumptions or potential issues requiring human review.

**Deferred survivors**

Do not attempt to kill `_109` or `_38` in this patch.

Classify `_109` as an unresolved race-sensitive design question involving D16/D35. Classify `_38` as equivalent through the public API, not universally equivalent.

Stop after preparing the patch and wait for human approval.