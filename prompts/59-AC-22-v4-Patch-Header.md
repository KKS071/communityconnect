# Prompt 59 — AC-22 v4 Patch Header Correction

I approve Option A.

Create a new complete patch:

`agent-patches/AGENT-03-AC22-retry-v4.patch`

Use `AGENT-03-AC22-retry-v3.patch` as the source.

## Authorized correction

Correct the final test hunk header from:

`@@ -774,3 +773,527 @@`

to:

`@@ -774,3 +773,528 @@`

Do not make any other content changes.

Preserve all five approved file changes, all AC-22 tests, and all SF-1 through SF-7 corrections exactly as written in v3.

## Verification

Perform a read-only comparison between v3 and v4 and verify:

1. The only difference is the corrected hunk header.
2. Every hunk's declared line counts match its actual content.
3. Only the five previously approved application, test and documentation files are represented.
4. The patch contains no unintended additional changes.

Do not apply either patch, run tests, modify application files, commit, push, or edit LEDGER.md or prompts/.

If any other malformed hunk is discovered, stop and report it rather than silently modifying the patch.

Return the exact verification findings and human application commands.