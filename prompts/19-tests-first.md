# Prompt 19: tests first for S-1 and S-6

Write a test for every acceptance criterion of S-1 (AC-1 to AC-6) and S-6 (AC-18 to AC-22) before any
code exists, using the test names in section 9 of each design doc. Take each expected result from the
criterion in docs/requirements/backlog.md and the exact messages in the design doc, never from code.
Read every value the interviews did not settle from app.settings. Use the sample data from the backlog
(Mountain Ridge, Pine Hollow, Elm Court; R1 unit 12, R3 unit 20, R2 Pine Hollow, M1, M2). Add tests for
the rules (R1 to R5) and decisions that can be checked from outside. Mark every S-6 test skipped with a
reason that starts with its AC ID. Change only tests/. Also update AGENTS.md and README.md for the new
design (X-User-Id caller, S-1 built, S-6 skipped).
