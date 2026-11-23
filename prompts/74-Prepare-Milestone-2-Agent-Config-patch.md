**Prompt 74 — Prepare Milestone 2 Agent Configuration Patch**

The human has reviewed Prompt 73 and approves preparing the configuration changes below.

**Authorization: PATCH PREPARATION ONLY.**

Do not directly modify tracked files, apply patches, execute commands or tests, commit, or push.

Create one patch under:

`agent-patches/AGENT-09-m2-agent-config.patch`

Include only these six paths:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `.claude/settings.json`
4. `.claude/agents/test-writer.md` (new)
5. `.claude/agents/reviewer.md` (new)
6. `requirements.txt`

Requirements:

**AGENTS.md**
- Keep under 100 lines.
- Document installation, database setup, application run, test, and coverage commands.
- Include repository layout, including `tests/acceptance/`.
- State that expected test results come from acceptance criteria, not implementation behavior.
- Require running tests before claiming completion.
- Document one-task-per-commit and ledger requirements.
- Update S-6 status and settled OQ1–OQ5 decisions.
- Preserve human approval requirements.

**CLAUDE.md**
- First line must be exactly `@AGENTS.md`.
- Remove outdated statements describing S-6 as unimplemented.
- Document the five available subagents.
- Preserve the patch-only workflow unless the human explicitly authorizes another workflow.

**Subagents**
- Create `test-writer` with test-only responsibilities. It must derive expected results from the ACs, include AC IDs, never edit application code, and never weaken tests.
- Create `reviewer` as read-only. Findings must include file, line, AC ID, severity (blocking/minor), and problem.
- Preserve the three existing agents unchanged.

**Settings**
- Preserve `dontAsk` and the current human-approval boundary.
- Explicitly deny reading `.env`, `git push`, and destructive recursive deletion commands.
- Permit the exact approved pytest command without opening broad shell access.
- Do not add the `tests/acceptance/` edit-denial rule yet; it belongs at the test-lock milestone.
- Identify any restrictions that cannot be reliably enforced through Claude Code permissions.

**Dependencies**
- Add `pytest-cov` to `requirements.txt`.
- Do not add Hypothesis or mutmut yet.

**Output**
- Produce a valid unified patch.
- List every changed path.
- Explain the permission implications.
- Identify commands requiring human verification.
- Do not claim fresh-clone verification or successful tests without actual evidence.

Stop after creating the patch. Wait for human review and approval.