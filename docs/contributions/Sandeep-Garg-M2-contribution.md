# Contribution statement: Milestone 2

Name / UCID: Sandeep Garg / sg2938

## Personal authorship

As architecture lead, I primarily coordinated AI-agent prompts, conducted mutation-testing comparisons, maintained Git documentation and traceability, and contributed to the review of implementation patches and testing evidence.

I organized the baseline and final mutation runs, evaluated survivor dispositions, documented regression results, and maintained supporting evidence and commit references.

Specific artifacts associated with my contributions include:

- `LEDGER.md` — AI-assisted development activities, review decisions, and commit traceability.
- `MILESTONE2.md` — consolidated implementation, testing, mutation analysis, and verification documentation.
- `docs/audits/mutation-summary.md` — mutation-testing results and survivor dispositions.
- `evidence/mutation-baseline.txt` — baseline mutation results.
- `evidence/mutation-properties.txt` — mutation comparison with property-based tests.
- `evidence/mutation-after.txt` — final mutation-testing results.
- `evidence/coverage.txt` — final regression and coverage evidence.
- `docs/requirements/traceability.md` — requirements and implementation commit mapping.

The mutation-testing workflow is documented in LEDGER Entries 69–75, with subsequent verification and demonstration activities recorded in Entries 76–79.

## AI-assisted authorship

I used Claude Code and ChatGPT to assist with bounded implementation planning, mutation-testing configuration, survivor analysis, regression-test proposals, agent safety verification, and project documentation.

Specific prompt artifacts include:

- `prompts/83-Milestone-2-Mutation-Testing-Plan.md`
- `prompts/84-Milestone-2-Mutation-Configuration.md`
- `prompts/85-Milestone-2-Controlled-Mutation-Comparison.md`
- `prompts/87-AGENT-21-Prepare-Three-Mutation-Killing-Regression-Tests.md`
- `prompts/88-AGENT-22-M2-Mutation-Evidence-Ledger-Final-Audit.md`
- `prompts/90-AGENT-24-M2-Headless-Reviewer.md`

The baseline mutation experiments killed 25 of 30 selected mutants. Following the addition of three deterministic regression tests, the final mutation run killed 28 of 30 selected mutants, increasing the mutation score from 83.33% to 93.33%.

These results apply only to the 30 selected mutants, not the entire population of 603 generated mutants.

## Review

I reviewed AI-generated patch proposals and documentation against the approved S-6 design, locked acceptance tests, and mutation-testing evidence.

The mutation survivor analysis distinguished three genuine testing gaps from an unresolved concurrency-policy question and a mutant equivalent through the reviewed public API.

Specific regression tests reviewed in `tests/test_s6_payments.py` include:

- `test_d16_two_units_charged_in_one_run_are_both_counted`
- `test_d16_two_unavailable_charges_are_both_counted_as_skipped`
- `test_r4_paid_unit_does_not_stop_the_run_for_a_later_unit`

Additional supporting review artifacts include:

- `agent-patches/AGENT-21-M2-mutation-killing-tests.patch`
- `docs/audits/mutation-summary.md`
- `evidence/headless-review.json`
- Mutation regression commit `0f000db`
- Headless review correction commit `7063e9e`
- Final coverage evidence commit `7f613c4`

The final recorded regression execution reported 202 passing tests and 94.34% combined statement and branch coverage.

Signed: [Sandeep Garg]

Date: [23 Nov 2026]