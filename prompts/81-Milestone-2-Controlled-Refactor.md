# Prompt 81 — Milestone 2 Controlled REFACTOR

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-15

Mode: PATCH PREPARATION ONLY

## Objective

Prepare one small, behavior-preserving refactor of the existing S-6 payment implementation after the verified GREEN milestone.

Current baseline:
- GREEN commit: `74bb7fc`
- GREEN tag: `m2-green`
- Acceptance-test lock: `m2-tests-locked`
- GREEN evidence: `evidence/green.txt`
- Verified results: 197 tests passed; 93.55% branch-aware coverage.

The refactor must improve internal code structure without changing externally observable behavior.

## Step 1 — Inspect the relevant files

Read:
- `AGENTS.md`
- `CLAUDE.md`
- `app/payments.py`
- `app/processor.py`
- `docs/design/S-6.md`
- `docs/plans/S-6-plan.md`
- `LEDGER.md`
- `evidence/green.txt`

Review the existing counting logic in `app/payments.py`, particularly repeated handling of successful, declined and unchanged payment outcomes.

Identify one narrowly scoped duplication that can be safely removed.

Do not assume a refactor is safe without inspecting the code.

## Step 2 — Select the smallest refactor

Prefer extracting a small internal helper or consolidating duplicated outcome-counting logic.

Requirements:
- Preserve all public function signatures.
- Preserve return values and dictionary keys.
- Preserve transaction boundaries.
- Preserve exception handling.
- Preserve payment ordering and idempotency.
- Preserve retry timing.
- Preserve scheduled and manual payment behavior.
- Do not introduce new dependencies.
- Do not change the database schema.
- Do not add new features.

If the proposed extraction risks changing behavior, stop and recommend a safer alternative.

## Step 3 — Protect locked acceptance tests

Do not modify:
- `tests/acceptance/**`
- `tests/conftest.py`
- `tests/__init__.py`
- Root `conftest.py`
- `pytest.ini`

Do not weaken assertions, remove tests, alter fixtures or change acceptance criteria.

## Step 4 — Prepare a patch

Create only:

`agent-patches/AGENT-15-M2-refactor.patch`

The patch should modify only `app/payments.py`, unless a different production file is demonstrably necessary and explicitly approved by the human.

Do not apply the patch.

Do not directly edit production files.

Do not modify the ledger or evidence files.

Do not commit, push or create tags.

## Step 5 — Explain the change

Provide:
1. Exact duplicated logic identified.
2. Why the refactor is behavior-preserving.
3. Functions affected.
4. Expected changes to production code.
5. Potential regression risks.
6. Complete patch filename.
7. Exact human commands for checking and applying the patch.
8. Recommended tests to run after applying it.

## Step 6 — Verification plan

Recommend these checks for the human:

- `git apply --check`
- `git diff --check`
- Focused S-6 tests
- All five acceptance tests
- Full test suite with branch-aware coverage
- Comparison against `m2-tests-locked` for protected files

The human will capture raw test output in `evidence/refactor.txt`.

Do not execute the tests yourself.

## Required output

Use these headings:

1. Refactor Candidate
2. Current Duplication
3. Proposed Change
4. Behavior Preservation Analysis
5. Risks
6. Patch Details
7. Human Verification Commands
8. Final Recommendation

Stop after creating the patch and reporting your findings.

Wait for explicit human approval before any production code is changed.