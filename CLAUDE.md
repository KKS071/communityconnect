@AGENTS.md

# CommunityConnect — Claude Code Instructions

## Source of truth

Follow:
- docs/design/S-1.md for S-1 requirements.
- docs/design/S-6.md for S-6 requirements, including the settled OQ1–OQ5 decisions in §8.
- docs/plans/S-6-plan.md for S-6 implementation planning.
- docs/requirements/backlog.md for acceptance criteria, and tests/ for the tests that carry their AC IDs.
- handout/CS690_Milestone2_Handout.pdf for the Milestone 2 deliverables.

If instructions conflict, stop and ask the human reviewer.

## Agent workflow

1. Analyze the requested task and its acceptance criterion.
2. Delegate independent analysis to the appropriate subagent.
3. Report findings, risks, and unresolved design questions.
4. Propose an exact list of files and intended changes.
5. Wait for explicit human approval before any change.
6. Prepare approved changes only through the patch workflow below,
   under the tool-enforced permissions in .claude/settings.json.
7. Run only the test commands those permissions allow, and report real results.
8. Review the diff and report any unexpected changes.
9. Stop after completing the approved task.
10. Provide evidence for the human-maintained provenance ledger.

## Current status

AC-18 through AC-22 are implemented, tested and merged into `main` (merge commit `5c87562`). AC-22 was implemented under Prompts 54–59; see LEDGER.md Entry 54 (implementation commit `719aecc`, documentation commit `1f820df`).

The five S-6 acceptance tests (AC-18 to AC-22) are in `tests/acceptance/test_s6_acceptance.py`, and the S-6 regression tests are in `tests/test_s6_payments.py`. The acceptance tests have not yet been locked.

Do not modify application code, tests, requirements,
design documents, plans, prompts, or LEDGER.md.

### Agent Patch Authorization

Claude Code is authorized to create new `.patch` files only within `agent-patches/`.

This authorization is limited to preparing proposed changes for human review.

Rules:

1. Use a unique patch filename for each task.
2. Never overwrite or modify an existing patch file.
3. Never directly modify existing project files, including `app/`, `tests/`, `docs/`, or `LEDGER.md`.
4. Never modify `AGENTS.md`, `CLAUDE.md`, or `.claude/settings.json`.
5. Generate patches in standard unified Git diff format.
6. Include only files explicitly approved for the task.
7. Never apply patches, run tests, commit, or push without separate authorization.
8. If patch creation fails, report the exact restriction and stop.

Creating a patch file does not authorize applying its contents.

## Delegation

Use these project subagents:

- test-writer: checks and writes tests from the acceptance criteria and the design doc,
  with AC IDs; never edits application code or weakens a test. Under the patch-only
  workflow it proposes test changes as new patches in `agent-patches/`.
- reviewer: read-only review of code against the design doc and the acceptance criteria;
  each finding gives file, line, AC ID, severity (blocking or minor) and problem.
- test-analyst: acceptance tests, coverage, mutations,
  property-based testing, and test gaps.
- security-reviewer: authorization, payment integrity,
  idempotency, database safety, and security risks.
- code-reviewer: architecture, design compliance,
  implementation diffs, and scope verification.

The main agent must review subagent findings and identify
disagreements instead of silently resolving them.

Subagents never edit application code. Only test-writer may prepare test changes,
and only as patches while the patch-only workflow applies.

## Safety

Never use permission-bypass options, `--dangerously-skip-permissions`, or `--bare`.

Never execute destructive commands, install dependencies,
alter Git history, or access production payment systems
without separate explicit authorization.

Never weaken acceptance tests to make an implementation pass.

No real payment processing is authorized.

## Reporting

For every agent task, report:
- Acceptance criterion or task ID
- Agent and delegated subagents
- Files examined
- Proposed or actual changes
- Commands and test results, if any
- Design references
- Unresolved issues
- Human approval status
- Git commit SHA, if applicable

Do not claim that tests or tools ran unless they actually ran.
