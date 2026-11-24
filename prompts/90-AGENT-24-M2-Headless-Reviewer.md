# Prompt 90 — AGENT-24: Milestone 2 Headless Reviewer

## Objective

Complete Deliverable 6 of the Milestone 2 handout.

## Execution

The human executed scripts/review_story.sh using Claude Code
2.1.331 under the existing repository permission rules.

## Prompt template passed to Claude Code

Use the reviewer subagent to review these files against
docs/design/S-6.md and its acceptance criteria in
docs/requirements/backlog.md.

Read AGENTS.md first.
Review AC-18 through AC-22 and the section 6 rules.
Do not edit any files.
Report only what the reviewer finds.
Return the verdict and findings using the supplied JSON schema.

Files:
app/payments.py
