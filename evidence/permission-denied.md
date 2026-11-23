# Milestone 2 — Acceptance-Test Permission-Denial Evidence

Task: AGENT-13 / Prompt 79

Protected target: `tests/acceptance/test_s6_acceptance.py`

## Configuration verification

All five required Edit deny rules were confirmed in `.claude/settings.json` and visible in Claude Code's permission configuration.

## Enforcement attempt

Claude Code was instructed to attempt a harmless Edit-tool operation on the protected acceptance-test file, without using alternative tools or workarounds.

Actual tool response:

```text
<tool_use_error>File is in a directory that is denied by your permission settings.</tool_use_error>
```

Claude reported that it made one Edit attempt, did not retry, and did not use Bash, patches, or other tools.

Result: Permission denied.

## Integrity verification

Post-denial SHA-256 checks: Passed.

Post-denial Git diff: Passed.

## Conclusion

The Edit-tool permission restriction was enforced for the tested acceptance-test path.

This verification does not establish protection against every possible editing mechanism, human modifications, or manually applied patches.