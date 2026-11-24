# Milestone 2 — Team Reflection and Individual Contributions

**Project:** CommunityConnect  
**Course:** CS 690 — AI-Assisted Software Engineering  
**Team:** Gustavo Abreu, Kundan Singh, Sandeep Garg  
**Status:** Team-approved reflection — November 23, 2026.

## Team Reflection

During Milestone 2, our team implemented the S-6 scheduled monthly HOA dues feature using an AI-assisted development workflow. We learned that successful implementation involves more than producing working code. It requires alignment with approved requirements, reliable acceptance tests, controlled agent permissions, human review, and traceable development decisions.

One important lesson involved protecting acceptance tests from unauthorized agent modifications. During AGENT-13, Prompt 79, Claude Code attempted a harmless Edit operation on `tests/acceptance/test_s6_acceptance.py`. The configured permission restrictions rejected the operation, and subsequent SHA-256 and Git diff checks confirmed that the file remained unchanged. This incident is documented in `evidence/permission-denied.md`. Without these restrictions, an agent could potentially weaken an assertion instead of correcting the implementation, creating misleading passing results. The formal acceptance-test lock at commit `b46269f` provided an additional integrity checkpoint. Although the original implementation preceded the formal lock, preserving this limitation in our documentation helped maintain transparency.

Mutation testing provided another valuable lesson. Our initial regression and acceptance tests killed 25 of 30 selected mutants, achieving an 83.33% mutation score. Adding Hypothesis property-based tests did not improve this result. Analysis of the surviving mutants revealed weaknesses in outcome counting and processing multiple units. Three additional deterministic regression tests increased the score to 93.33%, as documented in `evidence/mutation-baseline.txt`, `evidence/mutation-after.txt`, and commit `0f000db`. Conventional coverage remained at 94.34%, demonstrating that high coverage does not necessarily establish strong assertions or complete business-rule verification.

We also recognized opportunities to improve subagent configuration and delegation. In future projects, we would configure specialized test-writer and read-only reviewer agents before implementation begins, verify their permissions, and resolve agent naming conflicts during setup. We would require independent reviews after each bounded implementation task and immediately preserve native delegation transcripts. Recovering historical delegation evidence later, as documented in Ledger Entry 77, required additional effort that could have been avoided through better evidence management.

The final headless review further demonstrated the value of independent verification. It returned a passing verdict with two minor findings concerning outdated ACH comments. Both findings were corrected in commit `7063e9e` without changing payment-processing behavior or acceptance tests.

Finally, the complete test suite passed all 202 tests with 94.34% combined statement and branch coverage, as recorded in `evidence/coverage.txt`. We also learned to communicate limitations honestly, including deferred ACH settlement, unresolved concurrency-policy questions, and the restricted mutation-testing sample.

Overall, Milestone 2 reinforced that AI can accelerate software engineering, but accountability remains with the development team. In future projects, we would establish safety controls earlier, strengthen independent reviews, preserve evidence continuously, and evaluate test effectiveness beyond conventional coverage metrics.

## Individual Contribution Statements

Each member's statement follows the course template with **Personal authorship**, **AI-assisted authorship**, and **Review** sections, plus a signature and date. These are separate files so each member can review and sign their own account.

| Team member | Role | Individual statement |
|---|---|---|
| **Gustavo Abreu** | Project Lead | [Gustavo — Milestone 2 contribution](contributions/Gustavo-Abreu-M2-contribution.md) |
| **Kundan Singh** | Requirements and Quality/Test Lead | [Kundan — Milestone 2 contribution](contributions/Kundan-Singh-M2-contribution.md) |
| **Sandeep Garg** | Architecture Lead | [Sandeep — Milestone 2 contribution](contributions/Sandeep-Garg-M2-contribution.md) |

**Review note:** Gustavo's and Kundan's statements contain proposed examples that must be verified by those individuals. Each person should confirm the files they authored, AI assistance they personally used, specific reviews performed, and any `Human: PENDING` ledger entries they actually replaced. Do not attribute project-wide ledger entries to an individual without confirmation.

## Supporting Project Evidence

- [Milestone 2 overview](../MILESTONE2.md)
- [Development and AI provenance ledger](../LEDGER.md)
- [S-6 design](design/S-6.md)
- [Requirements backlog](requirements/backlog.md)
- [Mutation-testing summary](audits/mutation-summary.md)
- [Mutation baseline evidence](../evidence/mutation-baseline.txt)
- [Hypothesis comparison evidence](../evidence/mutation-properties.txt)
- [Final mutation evidence](../evidence/mutation-after.txt)
- [Regression-test evidence](../evidence/mutation-regression-tests.txt)

## Submission Check

Before submission, confirm the official Milestone 2 reflection length and format, obtain each member's approval and signature, and check that the three relative contribution links resolve in the committed repository.
