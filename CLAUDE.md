# CommunityConnect — Claude Code Instructions

## Source of truth

Read AGENTS.md before every task.

Follow:
- docs/design/S-1.md for S-1 requirements.
- docs/design/S-6.md for S-6 requirements.
- docs/plans/S-6-plan.md for S-6 implementation planning.
- tests/ for existing acceptance criteria.

If instructions conflict, stop and ask the human reviewer.

## Project 2 agent workflow

1. Analyze the requested acceptance criterion.
2. Delegate independent analysis to appropriate subagents.
3. Report findings, risks, and unresolved design questions.
4. Propose an exact list of files and intended changes.
5. Wait for explicit human approval before implementation.
6. Modify only approved files, under separately configured
   tool-enforced permissions.
7. Run the approved tests.
8. Review the diff and report any unexpected changes.
9. Stop after completing the approved acceptance criterion.
10. Provide evidence for the human-maintained provenance ledger.

## Current authorization

This configuration task authorizes only:
- CLAUDE.md
- .claude/settings.json
- .claude/agents/test-analyst.md
- .claude/agents/security-reviewer.md
- .claude/agents/code-reviewer.md

AC-18 through AC-22 are implemented, tested and merged into `main` (merge commit `5c87562`). AC-22 was implemented under Prompts 54–59; see LEDGER.md Entry 54 (implementation commit `719aecc`, documentation commit `1f820df`).

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

Use these project subagents for independent analysis:

- test-analyst: acceptance tests, coverage, mutations,
  property-based testing, and test gaps.
- security-reviewer: authorization, payment integrity,
  idempotency, database safety, and security risks.
- code-reviewer: architecture, design compliance,
  implementation diffs, and scope verification.

The main agent must review subagent findings and identify
disagreements instead of silently resolving them.

Subagents are reviewers, not implementation agents.

## Safety

Never use permission-bypass options.

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
