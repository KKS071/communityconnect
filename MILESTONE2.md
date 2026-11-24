# CommunityConnect — Milestone 2

CS 690 — AI-Assisted Software Engineering, Fall 2026

Status: Draft

## 1. Project Overview

CommunityConnect is a FastAPI and PostgreSQL-based community management application for homeowner associations. The system supports role-based access to community information and workflows.

Milestone 1 implemented S-1, maintenance request submission and tracking. Milestone 2 focuses on S-6, scheduled monthly HOA dues payments.

## 2. Milestone 2 Implementation

The S-6 implementation covers acceptance criteria AC-18 through AC-22:

| Criterion | Functionality |
|---|---|
| AC-18 | Create and display a monthly ACH payment schedule through the API |
| AC-19 | Process a scheduled debit payment and record its payment history |
| AC-20 | Prevent duplicate monthly charges after an interrupted or restarted run |
| AC-21 | Avoid charging a unit already paid manually |
| AC-22 | Record a failed charge and support the defined retry behavior |

ACH schedule creation is supported, but automatic ACH settlement is outside the implemented scope. Real bank-account integration is not included.

The implementation follows `docs/design/S-6.md` and the acceptance criteria in `docs/requirements/backlog.md`.

## 3. Architecture and Implementation

The application uses Python, FastAPI, PostgreSQL and pytest.

Key implementation files include:

- `app/payments.py` — scheduled payment processing
- `app/processor.py` — payment processor interface and test implementation
- `app/db.py` — database operations
- `app/settings.py` — named policy settings
- `app/main.py` — API routes

Access restrictions and payment-processing behavior are governed by the design documentation.

## 4. Testing and Quality Assurance

The recorded final regression run reported:

| Measure | Result |
|---|---|
| Tests | 202 passed |
| Branch coverage | 94.34% |
| Required coverage threshold | 80% |
| Selected mutants | 30 of 603 generated |
| Initial mutation score | 25/30 killed (83.33%) |
| Final mutation score | 28/30 killed (93.33%) |

Three additional deterministic regression tests detected mutations that survived the initial runs.

Two mutants remained: one involves an unresolved concurrency-policy question, and the other is equivalent through the reviewed public API.

These results are documented in `docs/audits/mutation-summary.md` and the corresponding `evidence/` files. They describe recorded runs, not a new verification performed for this document.

## 5. AI-Assisted Development and Traceability

AI-assisted work was documented through prompts, proposed patches, human review, tests, and Git commits.

Relevant artifacts:

- `AGENTS.md` — development and safety instructions
- `LEDGER.md` — chronological AI-assisted development record
- `prompts/` — recorded prompts
- `agent-patches/` — preserved agent proposals
- `docs/audits/mutation-summary.md` — mutation-testing analysis

The mutation-testing documentation and traceability updates are recorded in LEDGER Entries 69–75.

## 6. Known Limitations

- Automatic ACH settlement is not implemented.
- Real payment-provider integration is not demonstrated by the recorded acceptance tests.
- Mutation scores cover 30 selected mutants, not all 603 generated.
- One payment-run concurrency behavior remains an unresolved design question.
- The final mutation run reused a cached mutmut workspace; its evidence does not print the test-selection configuration.

## 7. Reproduction

Set up the application according to `README.md`, with Python and PostgreSQL available.

Run the test suite:

```bash
python -m pytest
```

Run branch-aware coverage:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

The tests require a running PostgreSQL test database.

## 8. Team Reflection and Contributions

Done.

## 9. Submission Verification

Before final submission, confirm:

- [ ] The README describes the implemented Milestone 2 functionality.
- [ ] Required demonstration instructions and screenshots are present.
- [ ] The required team reflection and contribution statements are complete.
- [ ] Tests and coverage have been checked against the final commit.
- [ ] The submission commit and any required tag are recorded.
