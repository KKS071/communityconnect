# Prompt 68 — Correct AGENT-05 Patch

I choose Option A.

Create a new patch:

agent-patches/AGENT-05-S6-policy-finalization-v2.patch

Requirements:

1. Correct the fifth hunk header to @@ -87,17 +87,18 @@, adjusting counts again if the additional R4 change requires it.
2. Include the R4 wording correction in section 6 so it accurately reflects the settled OQ2 decision.
3. Preserve all other intended changes from AGENT-05.
4. Change only docs/design/S-6.md.
5. Do not modify application code, tests, acceptance criteria, or section 9 test paths.
6. Do not invent approvals or evidence. If the three named settings have not been explicitly approved, mark their approval as pending rather than settled.
7. Verify every hunk's line counts and context against the current design document.

Do not overwrite or edit the original patch. Create the v2 patch as a separate file.

Do not apply patches, modify tracked files, run shell commands, commit, or push.

After writing v2, report its exact path, any remaining unresolved decisions, and stop for human approval.