# Prompt 77 — Milestone 2 Acceptance-Test Documentation Synchronization

Project: CommunityConnect — CS690 Milestone 2

Task: Prepare a documentation-only patch reflecting the successful relocation of the five S-6 acceptance tests.

Authorization: PATCH PREPARATION ONLY.

Do not directly edit tracked files, apply patches, run tests, commit, push, or create Git tags.

## Verified human test results

- Acceptance-test collection: 5 tests.
- Acceptance tests: 5 passed in 13.02 seconds.
- Full suite: 197 passed in 415.98 seconds.
- Branch-aware coverage: 93.55%.
- Coverage requirement: 80%.
- One nonblocking StarletteDeprecationWarning.

These results were obtained after applying AGENT-10.

## Files to inspect

- `docs/design/S-6.md`
- `docs/requirements/traceability.md`
- `AGENTS.md`
- `CLAUDE.md`
- `tests/acceptance/test_s6_acceptance.py`
- `tests/test_s6_payments.py`

## Required changes

Prepare a unified Git patch named:

`agent-patches/AGENT-11-S6-acceptance-docs.patch`

The patch must update only these four documentation files:

1. `docs/design/S-6.md`
2. `docs/requirements/traceability.md`
3. `AGENTS.md`
4. `CLAUDE.md`

Update the AC-18 through AC-22 test paths to:

`tests/acceptance/test_s6_acceptance.py`

Clarify that the remaining regression tests are in:

`tests/test_s6_payments.py`

Preserve all AC IDs, design decisions, expected outcomes, and requirements.

Do not claim that the acceptance tests are locked.

Do not claim that `m2-tests-locked` exists.

Do not change any business rules or implementation requirements.

## Output

Report:

1. Exact documentation changes.
2. Whether any outdated test paths remain.
3. Whether any statements incorrectly claim tests are already locked.
4. Any conflicting documentation.
5. Patch filename.
6. Commands for human verification.

Create only the patch file.

Stop for human approval.