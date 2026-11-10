# Prompt 07: tests first

Before any code in app/ exists, write pytest tests for every acceptance criterion of S-1 (AC-1..AC-5)
and S-2 (AC-6..AC-12), from docs/design/S-1.md and S-2.md only. Put the AC ID in each test name. Take
expected values from the criteria and the doc's exact error bodies, not from code. Use the named setting
REOPEN_WINDOW_DAYS for the reopen window. Insert fixture rows with plain SQL using the §5 column names.
Mark every S-2 test skipped with a reason that names its AC ID. Do not write any app code.
