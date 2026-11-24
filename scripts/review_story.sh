#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

FILES=$(git diff --name-only m2-tests-locked HEAD -- app/)

if [[ -z "$FILES" ]]; then
    echo "No changed application files found."
    exit 1
fi

PROMPT="Use the reviewer subagent to review these files against
docs/design/S-6.md and its acceptance criteria in
docs/requirements/backlog.md.

Read AGENTS.md first.
Review AC-18 through AC-22 and the section 6 rules.
Do not edit any files.
Report only what the reviewer finds.
Return the verdict and findings using the supplied JSON schema.

Files:
$FILES"

claude -p "$PROMPT" \
    --output-format json \
    --json-schema "$(cat agent/review-schema.json)" \
    > evidence/headless-review.json
