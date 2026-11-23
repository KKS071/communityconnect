# Prompt 76A — AGENT-10 Patch Verification

Read-only verification. Do not edit, overwrite, apply, or recreate the existing patch.

Review `agent-patches/AGENT-10-S6-acceptance-organization.patch` against the complete current source files.

Verify:

1. `app/processor.py` defines the `get_processor()` and `set_processor()` functions used by the proposed fixture cleanup.
2. All references to moved constants, fixtures, classes, and helpers throughout `tests/test_s6_payments.py` remain valid.
3. All five acceptance tests are preserved exactly except the approved AC-18 comment.
4. No regression test or helper is accidentally removed.
5. Pytest fixture discovery and import paths will work.
6. The patch is valid unified Git diff format and has no unexpected file changes.
7. The fixture cleanup cannot introduce processor-state problems.

Report each check as PASS, FAIL, or NOT VERIFIED, with file and line evidence.

If anything fails, explain the minimal correction needed, but do not modify the patch.

Stop and wait for human approval.