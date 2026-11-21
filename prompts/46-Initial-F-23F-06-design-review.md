# Prompt 46 - Initial F-23/F-06 design review

Task: AGENT-03 retrospective design resolution for F-23 and F-06 only.

Read AGENTS.md, CLAUDE.md, docs/design/S-6.md, docs/plans/S-6-plan.md, docs/requirements/backlog.md, tests/test_s6_payments.py, and the AGENT-03 retrospective audit.

**F-23:** Identify the exact contradictions between D18/D25, R4/ACH scope, §4/D27 manual-payment errors, and §5/D30 missing dues. For each, quote the existing rule, explain the current code behavior, and propose the smallest consistent design amendment.

**F-06:** Review the historical AC-18 fixture change. Determine whether existing assertions were preserved and whether the fixture change was within the approved file scope. Do not claim prior authorization without evidence.

Output a proposed decision record, exact documentation-only diff, remaining human decisions, and suggested commit message.

PLAN ONLY. No edits, tests, commits, pushes, or AC-22 implementation. Stop for human approval.
