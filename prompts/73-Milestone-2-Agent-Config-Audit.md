**Prompt 73 — Milestone 2 Agent Configuration Audit**

We are completing CS690 Milestone 2 for CommunityConnect.

The S-6 implementation is already merged. We need to complete the required agent configuration before auditing and locking acceptance tests.

**Task: READ-ONLY AUDIT. Do not modify any tracked file.**

Inspect:
- `AGENTS.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/agents/`
- `README.md`
- The Milestone 2 assignment requirements, if available locally.

Report:

1. Which Milestone 2 agent-configuration requirements are already satisfied?
2. Which requirements are missing or outdated?
3. Does `AGENTS.md` accurately describe the current S-6 implementation and settled OQ1–OQ5 decisions?
4. Does `CLAUDE.md` begin with `@AGENTS.md`?
5. Are `test-writer` and `reviewer` subagents present with the required responsibilities and restrictions?
6. Do the settings enforce the required restrictions, including acceptance-test protection, `.env` access, destructive commands, and `git push`?
7. Are the installation, test, and coverage commands documented and verified from a fresh clone?
8. What is the smallest safe set of files to change?

**Output requirements:**
- A PASS / PARTIAL / FAIL checklist.
- Exact file paths and line numbers for findings.
- A proposed minimal patch plan.
- Identify any permission changes that could conflict with the existing human-approval workflow.

Do not apply patches, run commands, execute tests, change permissions, or commit anything.

Stop after reporting. Wait for human approval.