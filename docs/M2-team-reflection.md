# Milestone 2 — Team Reflection and Individual Contributions

**Project:** CommunityConnect  
**Course:** CS 690 — AI-Assisted Software Engineering  
**Team:** Gustavo Abreu, Kundan Singh, Sandeep Garg  
**Status:** Team review draft — confirm the reflection and individual statements before signing and submission.

## Team Reflection

During Milestone 2, our team worked on the S-6 scheduled monthly HOA dues feature using an AI-assisted development workflow. We learned that a successful implementation is not simply code that runs: it must also follow the design decisions, satisfy the acceptance criteria, and preserve existing behavior. Our workflow emphasized human review of proposed changes rather than automatically applying AI-generated patches.

One practical example was our treatment of acceptance tests for AC-18 through AC-22. The team used these tests as a stable reference while implementing and refining the scheduled-payment behavior. This helped us distinguish changing the implementation to satisfy a requirement from changing a test merely to obtain a passing result. Patch reviews and documentation checks were important safeguards in that process.

Mutation testing provided the clearest lesson about test quality. In a controlled comparison of 30 selected mutants, the original regression and acceptance tests killed 25 (83.33%). Adding the Hypothesis properties did not change that result. Analysis of the five surviving mutants identified three test gaps involving multiple units in a payment run. After three targeted deterministic regression tests were added, 28 of 30 selected mutants were killed (93.33%). These results showed that high coverage alone does not guarantee that tests detect meaningful defects. The project also recorded 202 passing tests and 94.34% branch-aware coverage.

We learned to document what the evidence actually establishes. The mutation score applies to 30 selected mutants, not all 603 generated mutants. Of the two survivors, one raised an unresolved concurrency-policy question and the other was considered equivalent through the public API. Similarly, the payment implementation does not provide automatic ACH settlement or live Stripe processing. Recording such limitations is more useful than overstating completion.

Finally, the team saw the value of traceability. AI prompts, proposed patches, test evidence, Git commits, and decisions were preserved so that the development process could be inspected later. Sandeep primarily coordinated the AI-agent prompts, mutation-testing runs, and Git documentation, while Gustavo and Kundan contributed primarily through documentation and patch reviews. The precise individual activities should be confirmed in the signed statements below. Overall, Milestone 2 reinforced that AI can accelerate engineering work, but responsibility for requirements, review, and evidence remains with the team.

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
