# CommunityConnect — Milestone 2

CS 690 — AI-Assisted Software Engineering, Fall 2026

**Status:** Draft — Pending Final Verification

**Repository:** https://github.com/KKS071/communityconnect

## 1. Deliverable Mapping

CommunityConnect is a FastAPI and PostgreSQL-based community management application for homeowner associations. The system supports role-based access to community information and workflows.

Milestone 1 implemented S-1, maintenance request submission and tracking. Milestone 2 focuses on S-6, scheduled monthly HOA dues payments.

### Deliverable Status

| Deliverable | Repository Artifact / Evidence | Status |
|---|---|---|
| D1 — Requirements and Design | `docs/design/S-6.md`, `docs/requirements/backlog.md`, `docs/design/S-6-gap-check-2.md` | Artifacts available; final verification pending |
| D2 — Agent Configuration and Safety | `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.claude/agents/`, `evidence/permission-denied.md` | Artifacts available |
| D3 — Acceptance Tests and Test Lock | `tests/acceptance/test_s6_acceptance.py`, `evidence/red.txt`, `m2-tests-locked` | Test lock verified; audit evidence pending |
| D4 — Implementation and Demonstration | `docs/plans/S-6-plan.md`, `app/`, `evidence/green.txt`, `evidence/refactor.txt`, `m2-green` | Implementation complete; demonstration and delegation evidence pending |
| D5 — Test Strength and Traceability | `tests/`, `evidence/properties.txt`, `docs/audits/mutation-summary.md`, mutation evidence files | Recorded tests complete; final evidence verification pending |
| D6 — Headless Reviewer | `scripts/review_story.sh`, `agent/review-schema.json`, `evidence/headless-review.json` | Execution successful; disposition commits to be recorded |
| D7 — AI-Assisted Development Ledger | `LEDGER.md`, `prompts/`, `agent-patches/` | Final verification pending |
| D8 — Consolidated Report | `MILESTONE2.md` | Draft |
| D9 — Individual Contributions | `docs/contributions/` | Committed; signature and content verification required |

### Git Milestone Tags

| Tag | Commit SHA | Status |
|---|---|---|
| `m2-tests-locked` | `b46269f52f397f0eae7f1d2b0833833eed65f222` | Pushed and verified |
| `m2-green` | `74bb7fcaec2b17b72738f31308fbd8de25b5d547` | Pushed and verified |
| `m2-submit` | Pending | To be created after final verification |

The following command returned no differences, confirming that the acceptance tests remained unchanged between the test-lock and green milestones:

```bash
git diff --stat m2-tests-locked m2-green -- tests/acceptance
```

## 2. Team Roles and Responsibilities

The CommunityConnect team consists of three members who contributed to requirements, architecture, implementation, AI-assisted development, documentation, and quality assurance.

| Team Member | Project Role |
|---|---|
| Gustavo Abreu | Project Lead |
| Kundan Singh | Requirements and Quality Assurance Lead |
| Sandeep Garg | Architecture Lead |

The detailed individual responsibilities, personal contributions, AI-assisted contributions, and review activities are documented in:

- `docs/contributions/Gustavo-Abreu-M2-contribution.md`
- `docs/contributions/Kundan-Singh-M2-contribution.md`
- `docs/contributions/Sandeep-Garg-M2-contribution.md`

The reflection and contribution documents were committed in `54db6d3`.

### Milestone 2 Responsibility Mapping

| Activity | Responsible Team Member(s) |
|---|---|
| Agent configuration and safety setup | Pending team confirmation |
| Acceptance-test preparation and review | Pending team confirmation |
| Implementation and agent task management | Pending team confirmation |
| Test strengthening and mutation testing | Pending team confirmation |
| Documentation and final submission review | Pending team confirmation |

## 3. Milestone 1 Follow-up and Selected Story

### 3.1 Milestone 1 Feedback

Pending confirmation of professor feedback and the corresponding team responses.

Each feedback item will be documented together with the action taken to address it.

### 3.2 Selected Story — S-6

**Story:** Scheduled Monthly HOA Dues Payments

**User Story:** As a homeowner, I want to schedule monthly HOA dues payments so that I can pay my community dues conveniently and avoid duplicate or missed payments.

The authoritative story, evidence IDs, and acceptance criteria are maintained in `docs/requirements/backlog.md` and `docs/design/S-6.md`.

### 3.3 Acceptance Criteria

| Criterion | Functionality |
|---|---|
| AC-18 | Create and display a monthly ACH payment schedule through the API |
| AC-19 | Process a scheduled debit payment and record its payment history |
| AC-20 | Prevent duplicate monthly charges after an interrupted or restarted run |
| AC-21 | Avoid charging a unit already paid manually |
| AC-22 | Record a failed charge and support the defined retry behavior |

ACH schedule creation is supported, but automatic ACH settlement is outside the implemented scope. Real bank-account integration is not included.

### 3.4 Design Decisions and Open Questions

The S-6 design is maintained in `docs/design/S-6.md`. The second design gap-check is documented in `docs/design/S-6-gap-check-2.md`.

The settled design decisions include:

| Open Question | Decision |
|---|---|
| OQ1 | No additional card-processing fee is applied. |
| OQ2 | ACH schedules may be created and displayed, but ACH payments are not automatically charged or replayed. |
| OQ3 | New scheduled payment attempts are processed for the current billing month. |
| OQ4 | Board-member access to the resident payment-list operation returns HTTP 404. |
| OQ5 | Manual payment is refused while a scheduled payment attempt is Pending. |

The exact policy values and their sources are documented in the design specification and named application settings.

### 3.5 Architecture and Implementation

The application uses Python, FastAPI, PostgreSQL, pytest, and a payment processor abstraction.

| File | Responsibility |
|---|---|
| `app/payments.py` | Scheduled payment processing, replay, retry, and payment outcomes |
| `app/processor.py` | Payment processor interface and test implementation |
| `app/db.py` | Database operations and payment persistence |
| `app/settings.py` | Named payment policy settings |
| `app/main.py` | API routes and request handling |

Access restrictions and payment-processing behavior are governed by the S-6 design documentation.

## 4. Test Audit, Agent Safety, and Implementation Plan

### 4.1 Agent Configuration and Safety

The team established repository-level instructions and tool permission boundaries to control AI-assisted development.

| Artifact | Purpose |
|---|---|
| `AGENTS.md` | Development instructions, repository rules, testing requirements, and human approval boundaries |
| `CLAUDE.md` | Claude Code entry point for repository instructions |
| `.claude/settings.json` | Tool permissions and prohibited operations |
| `.claude/agents/test-writer.md` | Specialized acceptance-test audit agent |
| `.claude/agents/reviewer.md` | Read-only code and design review agent |
| `evidence/permission-denied.md` | Recorded permission-enforcement evidence |

The configuration restricts sensitive operations, including protected acceptance-test modifications, access to environment secrets, unauthorized Git pushes, and destructive filesystem commands.

### 4.2 Acceptance-Test Audit

The acceptance tests for S-6 are located in:

`tests/acceptance/test_s6_acceptance.py`

The tests cover AC-18 through AC-22.

The test-writer audit report, individual findings, and corresponding resolutions will be included after verification of the required audit evidence.

| Finding | Acceptance Criterion | Disposition | Commit SHA |
|---|---|---|---|
| Pending audit evidence | Pending | Pending | Pending |

### 4.3 Test Lock and Red-to-Green Development

The initial failing-test evidence is preserved in `evidence/red.txt`.

The acceptance tests were locked using the `m2-tests-locked` Git tag before the implementation reached its green milestone.

The passing-test evidence is preserved in `evidence/green.txt`, and the corresponding milestone is identified by the `m2-green` tag.

The acceptance-test comparison between these tags returned an empty diff, confirming that the protected acceptance tests remained unchanged during that interval.

### 4.4 Implementation Plan and Human Corrections

The implementation plan is maintained in:

`docs/plans/S-6-plan.md`

The plan provides a structured approach to implementing the S-6 acceptance criteria and associated business rules.

| Plan Correction | Reason for Human Intervention | Evidence |
|---|---|---|
| Pending verification of first actual plan correction | Pending | Pending |
| Pending verification of second actual plan correction | Pending | Pending |

### 4.5 Delegation Evidence

The team configured specialized test-writer and reviewer subagents to separate implementation, test auditing, and review responsibilities.

The headless reviewer execution independently confirmed successful delegation to the reviewer subagent.

Additional evidence demonstrating delegation during the implementation phase must be verified and included separately. The headless review does not, by itself, establish that delegation occurred during the original build phase.

### 4.6 Refactoring and Demonstration

Post-green refactoring evidence is preserved in:

`evidence/refactor.txt`

Application setup and demonstration instructions are maintained in `README.md`.

The demonstration screenshots and their mapping to the acceptance criteria are pending final verification.

## 5. Testing, Quality Assurance, and Traceability

### 5.1 Regression and Coverage Results

The recorded final regression run reported:

| Measure | Result |
|---|---|
| Tests passed | 202 |
| Branch-aware combined coverage | 94.34% |
| Required coverage threshold | 80% |
| Generated mutants | 603 |
| Selected mutants evaluated | 30 |
| Initial mutation score | 25/30 killed (83.33%) |
| Final mutation score | 28/30 killed (93.33%) |
| Remaining selected survivors | 2 |

These results describe recorded runs and do not represent a new verification performed for this report.

### 5.2 Test Categories

| Test Category | Purpose | Evidence |
|---|---|---|
| Acceptance tests | Verify AC-18 through AC-22 | `tests/acceptance/test_s6_acceptance.py` |
| Unit and regression tests | Verify payment behavior and edge cases | `tests/test_s6_payments.py` |
| Integration tests | Verify interactions between application components | Exact test names pending verification |
| Property-based tests | Verify payment invariants across generated inputs | `evidence/properties.txt` |
| Mutation tests | Evaluate the ability of tests to detect introduced defects | `evidence/mutation-baseline.txt`, `evidence/mutation-after.txt` |
| Refactoring verification | Verify behavior after post-green refactoring | `evidence/refactor.txt` |

### 5.3 Integration Testing

The application integrates scheduled payment-processing logic with PostgreSQL-backed persistence.

The integration-test names, two participating components, and confirmation that no mock replaces the boundary between those components will be recorded after final test inspection.

### 5.4 Coverage Verification

The application test suite can be executed using:

```bash
python -m pytest
```

Branch-aware coverage can be checked using:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

The tests require a running PostgreSQL test database.

The recorded combined coverage result of 94.34% exceeds the configured 80% threshold used in the recorded command.

The final coverage evidence will be preserved in `evidence/coverage.txt`.

**Uncovered line or branch analysis:** Pending inspection of the final coverage report.

### 5.5 Mutation Testing

Mutation testing was conducted to evaluate the effectiveness of the S-6 test suite beyond conventional code coverage.

A total of 603 mutants were generated. A selected group of 30 mutants was evaluated through the recorded mutation-testing experiments.

| Experiment | Killed | Survived | Mutation Score |
|---|---:|---:|---:|
| Initial regression and acceptance tests | 25 | 5 | 83.33% |
| Regression, acceptance, and property-based tests | 25 | 5 | 83.33% |
| Final run after additional deterministic regression tests | 28 | 2 | 93.33% |

The three additional regression tests increased the selected mutation score by 10 percentage points.

### 5.6 Mutation Survivor Dispositions

| Mutant | Disposition | Test or Reason |
|---|---|---|
| `_count_outcome__mutmut_5` | Killed | `test_d16_two_units_charged_in_one_run_are_both_counted` |
| `_count_outcome__mutmut_20` | Killed | `test_d16_two_unavailable_charges_are_both_counted_as_skipped` |
| `run_due_payments__mutmut_89` | Killed | `test_r4_paid_unit_does_not_stop_the_run_for_a_later_unit` |
| `run_due_payments__mutmut_109` | Survived | Unresolved concurrency-policy question involving payment-processing behavior |
| `_charge_pending__mutmut_38` | Survived | Considered equivalent through the reviewed public API |

The regression tests and associated mutation evidence were recorded in commit `0f000db`. The exact individual mutant-to-test mappings should be checked against `docs/audits/mutation-summary.md` before submission.

Mutation testing revealed weaknesses that were not apparent from the high conventional coverage percentage, demonstrating that executing code does not necessarily mean that the tests detect incorrect behavior.

### 5.7 Mutation Evidence

The supporting evidence includes:

- `docs/audits/mutation-summary.md`
- `evidence/mutation-baseline.txt`
- `evidence/mutation-properties.txt`
- `evidence/mutation-regression-tests.txt`
- `evidence/mutation-selected-diffs.txt`
- `evidence/mutation-after.txt`

The mutation-testing activities are documented in LEDGER Entries 69–75.

### 5.8 Requirements Traceability

| Evidence ID | Story ID | AC ID | Verified Behavior | Acceptance Test Name | Passing Commit |
|---|---|---|---|---|---|
| Pending | S-6 | AC-18 | ACH schedule creation and display | Pending exact name | Pending |
| Pending | S-6 | AC-19 | Scheduled debit payment processing | Pending exact name | Pending |
| Pending | S-6 | AC-20 | Restart-safe duplicate prevention | Pending exact name | Pending |
| Pending | S-6 | AC-21 | Manual payment prevents scheduled charge | Pending exact name | Pending |
| Pending | S-6 | AC-22 | Failed charge and retry behavior | Pending exact name | Pending |

The final traceability matrix will use the exact evidence IDs, test names, and commits that made each acceptance test pass. These entries will be reconciled with Section 9 of `docs/design/S-6.md`.

### 5.9 Known Limitations

- Automatic ACH settlement is not implemented.
- Real payment-provider integration is not demonstrated by the recorded acceptance tests.
- Mutation scores cover 30 selected mutants, not all 603 generated mutants.
- One payment-run concurrency behavior remains an unresolved design question.
- The final mutation run reused a cached mutmut workspace; its evidence does not print the test-selection configuration.
- Final regression and coverage verification against the submission commit remains pending.

## 6. Headless Reviewer Findings

### 6.1 Headless Reviewer Configuration

The team implemented a repeatable headless review process using Claude Code and the existing read-only reviewer subagent.

The following artifacts support the headless review:

| Artifact | Purpose |
|---|---|
| `scripts/review_story.sh` | Identifies changed application files and executes the headless reviewer |
| `agent/review-schema.json` | Defines the required structured JSON response |
| `.claude/agents/reviewer.md` | Defines the specialized reviewer role and review restrictions |
| `evidence/headless-review.json` | Preserves the original machine-generated review output |
| `prompts/90-AGENT-24-M2-Headless-Reviewer.md` | Records the review prompt and file scope |

The review script identifies application files changed since `m2-tests-locked` and instructs the reviewer to evaluate them against `docs/design/S-6.md`, the requirements backlog, AC-18 through AC-22, and the Section 6 business rules.

### 6.2 Execution

The reviewer was executed using:

```bash
bash scripts/review_story.sh
```

The initial execution encountered a JSON Schema compatibility error:

```text
Error: --json-schema is not a valid JSON Schema:
no schema with key or ref
"https://json-schema.org/draft/2020-12/schema"
```

The issue was resolved by removing the explicit Draft 2020-12 schema declaration while retaining the required properties, field types, and validation constraints.

The script was then executed successfully without changing the application code, acceptance tests, or permission settings.

### 6.3 Headless Review Results

| Metric | Result |
|---|---|
| Execution date | November 23, 2026 |
| Tool | Claude Code 2.1.331 |
| Model | claude-opus-5-5 |
| Execution subtype | success |
| Execution error | false |
| Structured verdict | PASS |
| Reviewer subagents spawned | 1 |
| Reviewer subagents completed | 1 |
| Reviewer subagents failed | 0 |
| Permission denials | 0 |
| Safety stops | 0 |
| Blocking findings | 0 |
| Minor findings | 2 |
| Shell execution time | 50.146 seconds |
| API execution time | 39.247 seconds |
| Reported API-equivalent cost | $0.4735198 |

The structured output explicitly confirmed that the reviewer subagent was spawned and completed. Therefore, a separate fallback execution using `--agent reviewer` was not necessary.

### 6.4 Review Findings and Dispositions

| Finding | File and Line | AC ID | Severity | Disposition | Resolution Commit |
|---|---|---|---|---|---|
| F-01 | `app/payments.py:81` | None | Minor | Accepted. Update the outdated ACH replay comment to reference settled OQ2 and D34. | `7063e9ee80dc70579c70762459b69159db5a51b1` |
| F-02 | `app/payments.py:92` | None | Minor | Accepted. Update the outdated ACH schedule-processing comment to reference settled OQ2 and D34. | `7063e9ee80dc70579c70762459b69159db5a51b1` |

#### Finding F-01 — ACH Replay Comment

The reviewer identified an outdated comment in the pending-payment replay section:

```python
# ACH settlement remains OQ2.
```

The comment incorrectly suggested that ACH settlement was still an open design question.

The reviewer confirmed that the implementation correctly skips ACH payments during the D26 replay process. The finding concerns documentation rather than functional behavior.

#### Finding F-02 — ACH Schedule-Processing Comment

The reviewer identified the same outdated comment in the scheduled-payment processing section.

The implementation correctly skips ACH schedules before updating payment outcome counts, consistent with D34.

The proposed correction for both comments is:

```python
# D34 (settled OQ2): ACH is not charged automatically.
```

Both findings require comment-only corrections. No payment-processing logic or acceptance-test changes are necessary.

### 6.5 Review Evidence and Traceability

| Item | Reference |
|---|---|
| Reviewed repository commit | `54db6d3` |
| Headless review artifact commit | `4f1e47c195288f2f9c91f63fc9df349488933f59` |
| Finding-resolution commit | `7063e9ee80dc70579c70762459b69159db5a51b1` |
| Prompt reference | Prompt 90 — AGENT-24 |
| Ledger reference | Entry 76 |
| Original review output | `evidence/headless-review.json` |

The original headless review output is retained as machine-generated evidence. The finding dispositions and corresponding commits are documented separately.

The successful review provides additional confidence in the consistency of the S-6 implementation with its design specification. However, an AI-assisted static review does not replace acceptance, regression, integration, property-based, or mutation testing.

## 7. Team Reflection and Contributions

### 7.1 Team Reflection

**Insert the complete team-authored 300–500-word reflection from `docs/M2-team-reflection.md` here before final submission.**

The reflection must address:

- Where permission restrictions or the acceptance-test lock prevented unauthorized agent actions, and what could have happened without those controls.
- What mutation testing revealed about weaknesses in the existing test suite.
- What the team would change about subagent configuration and delegation in future development.
- At least two specific references to repository evidence files or Git commits.

The reflection was committed in `54db6d3`.

### 7.2 Individual Contribution Statements

Individual contribution statements are maintained in the following files:

| Team Member | Contribution Statement |
|---|---|
| Gustavo Abreu | `docs/contributions/Gustavo-Abreu-M2-contribution.md` |
| Kundan Singh | `docs/contributions/Kundan-Singh-M2-contribution.md` |
| Sandeep Garg | `docs/contributions/Sandeep-Garg-M2-contribution.md` |

Each team member must verify that their statement accurately identifies personal authorship, AI-assisted authorship, and review activities, with supporting evidence and the required signature and date.

### 7.3 Final Submission Verification

- [x] Milestone 2 implementation documented.
- [x] `m2-tests-locked` tag pushed and verified.
- [x] `m2-green` tag pushed and verified.
- [x] Acceptance-test lock verified between milestone tags.
- [x] Headless reviewer successfully executed.
- [x] Structured review returned a pass verdict.
- [x] Reviewer subagent delegation confirmed.
- [x] Team reflection and contribution files committed.
- [x] Headless review findings resolved and commit SHAs recorded.
- [x] Ledger Entry 76 committed and verified.
- [ ] Milestone 1 feedback responses completed.
- [ ] Team responsibility mapping confirmed.
- [ ] Test-writer audit findings and resolutions documented.
- [ ] Two actual implementation-plan corrections documented.
- [ ] Build-phase delegation evidence verified.
- [ ] Demonstration instructions and screenshots completed.
- [ ] Final coverage evidence generated.
- [ ] Integration-test names and uncovered coverage analysis documented.
- [ ] Mutation survivor dispositions verified.
- [ ] Requirements traceability matrix completed.
- [ ] Complete team-authored reflection inserted into this report.
- [ ] Individual contribution signatures verified.
- [ ] Fresh-clone reproduction and final regression verification completed.
- [ ] Final submission commit recorded.
- [ ] `m2-submit` tag created and pushed.
- [ ] Repository URL and final submission SHA submitted through Canvas.

**Final submission SHA:** Pending

**Submission tag:** `m2-submit` — Pending

**End of Milestone 2 Report**