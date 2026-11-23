# Prompt 76 — Prepare S-6 Acceptance-Test Organization Patch

Project: CommunityConnect, CS690 Milestone 2.

The human has reviewed Prompt 75.

Authorization: PATCH PREPARATION ONLY. Do not directly modify tracked files, apply patches, execute tests, commit, push, or create tags.

Prepare a minimal unified patch under:

`agent-patches/AGENT-10-S6-acceptance-organization.patch`

## Approved scope

Move only the five S-6 acceptance tests, AC-18 through AC-22, into `tests/acceptance/`.

Keep all other S-6 regression tests in `tests/test_s6_payments.py`.

Preserve existing assertions and expected values. Do not weaken, skip, delete, or silently rewrite tests.

## Files

Proposed:
- `tests/acceptance/__init__.py`
- `tests/acceptance/s6_support.py`
- `tests/acceptance/test_s6_acceptance.py`
- `tests/test_s6_payments.py`

If necessary, propose updates to `docs/design/S-6.md` and `docs/requirements/traceability.md`, but do not include documentation changes without explicit human approval.

## Requirements

1. Preserve the exact five AC test names.
2. Preserve all existing regression tests.
3. Ensure pytest discovers the moved tests exactly once.
4. Preserve fixtures, helpers, and database isolation.
5. Do not introduce import cycles or duplicate fixtures.
6. Identify shared dependencies that must be protected at lock time.
7. Correct the stale AC-18 comment without changing its assertions.
8. Address processor-state leakage using appropriate fixture cleanup, without changing payment behavior.
9. Do not add optional assertion-strengthening changes in this patch.
10. Do not add acceptance-test edit-denial rules yet.

Before creating the patch, inspect all imports and references to the shared helpers and fixtures.

If the proposed layout would break regression tests or require broader changes, stop and report the issue instead of guessing.

## Output

Report:
- Exact changed paths
- Acceptance tests moved
- Regression tests preserved
- Fixture/import strategy
- Any unresolved dependency protection issues
- Commands the human should run to validate the patch
- Any required documentation updates

Create only the patch file and stop for human approval.

Do not claim tests passed unless they were actually run.