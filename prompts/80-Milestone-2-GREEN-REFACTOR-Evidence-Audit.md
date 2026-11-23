# Prompt 80 — Milestone 2 GREEN/REFACTOR Evidence Audit

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-14

Mode: READ-ONLY AUDIT

## Objective

Audit the existing Git history, test results and documentation to determine what evidence supports the GREEN and REFACTOR phases of the S-6 implementation.

Do not reconstruct or invent a test-first development history.

The acceptance tests have been locked at:

- Tag: `m2-tests-locked`
- Commit: `b46269f52f397f0eae7f1d2b0833833eed65f222`

## Mandatory restrictions

Do not:

- Edit application code, tests or documentation.
- Modify `tests/acceptance/**` or any protected shared fixtures.
- Create or apply patches.
- Run the full pytest suite or coverage suite.
- Commit, push, tag, reset, checkout or modify Git history.
- Create evidence files.
- Claim historical tests ran unless recorded evidence supports that claim.

This task is strictly an evidence audit.

## Step 1 — Inspect the Milestone 2 requirements

Read:

- `handout/CS690_Milestone2_Handout.pdf`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/design/S-6.md`
- `docs/plans/S-6-plan.md`
- `docs/requirements/traceability.md`
- `LEDGER.md`, especially Entries 54 and 62–65
- `evidence/red.txt`
- `evidence/m2-acceptance-relocation-tests.md`
- `evidence/permission-denied.md`

Identify the exact GREEN and REFACTOR evidence requirements from the handout.

If the PDF cannot be read, report that limitation rather than guessing.

## Step 2 — Audit historical Git commits

Use read-only Git commands to examine the implementation sequence for AC-18 through AC-22.

Relevant known references:

- Historical pre-implementation baseline: `bd558d4`
- First S-6 implementation commit: `6b1317f`
- Acceptance-test source commit: `7104eed`
- Acceptance-test lock commit: `b46269f`

Inspect the commits that introduced:

- Payment schedules
- Scheduled charging
- Idempotency and restart handling
- Manual payment safeguards
- Declined-payment retry behavior
- Acceptance-test organization
- Refactoring and cleanup

For each meaningful commit, identify:

- Commit SHA
- Date
- Files changed
- Acceptance criterion
- Whether the change represents implementation, test addition, bug fix or refactoring
- Available evidence that tests passed at that point

Do not classify a commit as REFACTOR merely because its message uses that word. Examine whether behavior was preserved.

## Step 3 — Evaluate GREEN evidence

Review the recorded test results:

- Five S-6 acceptance tests passed.
- Full suite: 197 passed, one warning.
- Branch-aware coverage: 93.55%.
- Historical RED reconstruction: five fixture setup errors.

Determine whether these results establish a verified GREEN state.

Clearly distinguish:

1. A passing implementation.
2. Historical test-first development.
3. Retrospective reconstruction.

Do not present the reconstructed RED run as five failing assertions.

Identify the most appropriate existing evidence for `m2-green`.

## Step 4 — Evaluate REFACTOR evidence

Identify any historical refactoring that can be substantiated by Git diffs and test evidence.

For each candidate, explain:

- What changed structurally.
- Why it qualifies or does not qualify as refactoring.
- Whether acceptance behavior remained unchanged.
- What supporting test evidence exists.
- Whether additional verification is necessary.

Do not propose unnecessary code changes solely to manufacture a REFACTOR phase.

## Step 5 — Protect the acceptance-test lock

Verify the current tag and its target.

Provide exact read-only commands to compare the protected files between `m2-tests-locked` and any proposed future `m2-green` commit.

Protected scope:

- `tests/acceptance/**`
- `tests/conftest.py`
- `tests/__init__.py`
- Root `conftest.py`, if present
- `pytest.ini`

No locked acceptance-test files may be weakened or changed.

## Step 6 — Recommend the next actions

Provide:

1. A GREEN evidence assessment.
2. A REFACTOR evidence assessment.
3. A chronological table of relevant commits.
4. Missing evidence and limitations.
5. Exact human commands for any necessary lightweight verification.
6. A proposed `m2-green` tag strategy.
7. Suggested content for the next ledger entry.
8. Whether the project is ready to proceed to property-based and mutation testing.

Do not create the `m2-green` tag.

## Required final report

Use these headings:

1. Handout Requirements
2. Historical Commit Timeline
3. GREEN Evidence
4. REFACTOR Evidence
5. RED Reconstruction Limitations
6. Acceptance-Test Integrity
7. Missing Evidence
8. Recommended Human Verification
9. Proposed Tag Strategy
10. Final Verdict

Stop after reporting your findings.

Wait for human approval before any implementation or documentation changes.