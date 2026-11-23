# Prompt 84 — Milestone 2 Mutation Testing Configuration

Project: CommunityConnect — CS690 Milestone 2

Task ID: AGENT-18

Mode: PATCH PREPARATION ONLY

Baseline: 1573ae3, or the current documentation-only successor commit.

## Objective

Prepare the configuration required for controlled mutmut 3.8.1 mutation testing.

Human approvals:
1. Create pyproject.toml.
2. Add mutants/ to .gitignore.
3. Add mutmut>=3.8,<4 to requirements.txt.
4. Preserve separate A/B comparison evidence and handout-oriented before/after evidence.

## Required configuration

Create pyproject.toml containing:

```toml
[tool.mutmut]
source_paths = ["app"]
only_mutate = ["app/payments.py", "app/db.py"]
also_copy = ["pytest.ini"]
pytest_add_cli_args_test_selection = [
    "tests/test_s6_payments.py",
    "tests/acceptance",
]
```

Add one line to .gitignore:

```text
mutants/
```

Add one dependency to requirements.txt:

```text
mutmut>=3.8,<4
```

Preserve all existing contents.

## Required patches

Prepare exactly three separate patches:

- agent-patches/AGENT-18-M2-mutmut-config.patch
- agent-patches/AGENT-18-M2-mutmut-gitignore.patch
- agent-patches/AGENT-18-M2-mutmut-dependency.patch

Do not apply the patches.

## Pilot design

Recommend a pilot containing approximately 5–10 mutants from the following functions:

- app.payments._count_outcome
- app.payments.run_due_payments
- app.db._retry_allowed

Verify the exact mutant identifiers and supported CLI syntax before proposing execution commands.

Use only the isolated PostgreSQL test database.

Use one mutation worker.

Do not assume that mutation runs are safe merely because the application tests use separate schemas.

## Evidence naming

Plan these files:

- evidence/mutation-baseline.txt — existing regression and acceptance tests
- evidence/mutation-properties.txt — same tests plus Hypothesis properties
- evidence/mutation-before.txt — handout-oriented initial mutation evidence
- evidence/mutation-after.txt — handout-oriented evidence after any approved test improvements

Do not claim that the two comparisons are equivalent.

## Restrictions

Do not:
- Apply patches.
- Install dependencies.
- Execute mutation tests.
- Run the full pytest suite.
- Modify application code or tests.
- Modify locked acceptance files.
- Modify LEDGER.md.
- Commit or push.
- Create milestone tags.
- Delete existing directories.

## Required report

1. Exact contents of each patch.
2. Files changed.
3. mutmut configuration compatibility.
4. Pilot mutant-selection method.
5. Database safety and isolation checks.
6. Estimated pilot runtime.
7. Proposed human verification commands.
8. Open risks and approval request.

Stop after preparing the patches and report.