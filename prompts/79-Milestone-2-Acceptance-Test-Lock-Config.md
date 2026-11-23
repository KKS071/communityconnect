# Prompt 79 — Milestone 2 Acceptance-Test Lock Configuration

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-13

Authorization: READ-ONLY AUDIT AND PATCH PREPARATION ONLY.

Do not directly edit tracked files, apply patches, run tests, create commits, push, create tags, or modify Git history.

## Objective

Prepare a safe, enforceable acceptance-test lock for Milestone 2.

The five S-6 acceptance tests have already passed, the full regression suite passed, and the historical reconstruction evidence has been recorded.

The next requirement is to protect the accepted tests from unauthorized agent modification before creating the `m2-tests-locked` tag.

## Verified project status

- S-6 acceptance tests: 5 passed.
- Full regression suite: 197 passed.
- Branch-aware coverage: 93.55%.
- Historical reconstruction: 5 setup errors caused by missing `app.clock`.
- Historical baseline: `bd558d4`.
- Acceptance-test source commit: `7104eed`.
- Raw reconstruction evidence: `evidence/red.txt`.
- Acceptance-test lock: not yet created.

The historical reconstruction is not proof of assertion-level RED or original test-first development.

## Step 1 — Inspect the existing configuration

Read:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/agents/reviewer.md`
- `.claude/agents/test-writer.md`
- `tests/conftest.py`
- `tests/acceptance/__init__.py`
- `tests/acceptance/s6_support.py`
- `tests/acceptance/test_s6_acceptance.py`
- `docs/requirements/traceability.md`
- `LEDGER.md` Entries 62–64

Identify the complete set of files whose modification could change the behavior or expected outcomes of the locked S-6 acceptance tests.

Distinguish acceptance-test source files, shared fixtures, test configuration, and application code.

## Step 2 — Prepare permission restrictions

Prepare a minimal patch to `.claude/settings.json`.

The proposed configuration must explicitly deny agent modifications to:

- `tests/acceptance/**`
- `tests/conftest.py`

Consider whether `tests/__init__.py`, `pytest.ini`, or other shared test infrastructure also needs protection. Explain the recommendation before including additional files.

Preserve:

- Existing patch-only workflow.
- `dontAsk` permission mode.
- Disabled permission bypass.
- Existing sensitive-file restrictions.
- Existing Git push restrictions.
- Existing allowed patch-file creation under `agent-patches/`.

Use valid Claude Code permission-rule syntax.

Account for Write, Edit, NotebookEdit, and indirect modification through Bash or other tools.

Do not assume a textual deny rule provides complete filesystem protection. Identify any remaining bypass paths and propose an independent Git-based integrity check.

## Step 3 — Reviewer-subagent conflict

Investigate the previously reported conflict between:

- Project reviewer: `.claude/agents/reviewer.md`
- User-level agent also named `reviewer`

Determine how Claude Code resolves this name collision in the installed environment.

Do not rename, overwrite, or delete either agent without human approval.

Recommend a safe resolution that preserves the project review requirements and enables later headless review.

If a rename is necessary, propose the smallest consistent set of changes.

## Step 4 — Prepare a minimal patch

Create a new unified Git patch:

`agent-patches/AGENT-13-M2-acceptance-lock-config.patch`

Allowed patch targets:

- `.claude/settings.json`
- `AGENTS.md`
- `CLAUDE.md`

Include `.claude/agents/reviewer.md` only if a specific, justified correction is required.

Do not modify application code, acceptance tests, fixtures, requirements, or historical evidence.

Keep `AGENTS.md` within 100 lines.

Do not state that the tests are already locked.

## Step 5 — Prepare human verification commands

Provide exact commands for:

1. `git apply --check` of the proposed patch.
2. Applying the patch after human approval.
3. Validating `.claude/settings.json` syntax.
4. Restarting Claude Code so the new permissions load.
5. Performing a harmless attempted edit to a locked acceptance-test file.
6. Confirming that the attempted edit was denied.
7. Verifying that the file hash and Git diff remain unchanged.
8. Testing that creation of a new patch file in `agent-patches/` remains permitted.
9. Checking that the project reviewer resolves to the intended agent.

A denied edit attempt must not weaken or alter any acceptance-test assertion.

Do not execute these checks yourself.

## Step 6 — Lock readiness

Provide a checklist for the human to verify before creating the tag:

- All five acceptance tests are present.
- All five tests passed.
- Full suite passed.
- Coverage exceeds 80%.
- Historical reconstruction evidence is committed.
- Lock configuration is applied and committed.
- Permission-denial evidence is captured.
- No acceptance-test files were modified during verification.
- Reviewer-subagent conflict is resolved or explicitly documented.
- Working tree is clean.

Provide the exact commands for creating and pushing an annotated `m2-tests-locked` tag, but do not execute them.

The tag must reference the approved commit containing the acceptance tests and verified lock configuration.

## Required output

Report:

1. Current permission risks.
2. Proposed lock rules.
3. Shared-fixture protection decisions.
4. Reviewer-subagent conflict resolution.
5. Exact patch contents and filename.
6. Human verification commands.
7. Remaining risks.
8. Whether the project is ready for lock verification.

Create only the approved patch file and stop for human review.

Do not create the `m2-tests-locked` tag.