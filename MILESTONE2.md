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

The original acceptance-test audit was performed through Prompt 75 using the configured `test-writer` subagent. The audit was conducted before the acceptance-test relocation and lock, but after the original S-6 implementation.

The historical audit report and delegation records were subsequently recovered from the original Claude Code session.

The audit identified corresponding tests for all 11 acceptance criteria across S-1 and S-6. No acceptance tests were skipped or marked xfail. The reviewer confirmed that expected values were derived from approved acceptance criteria, design decisions, settings, and fixture data.

#### Audit Finding Dispositions

| Finding | Issue | Disposition | Evidence / Commit |
|---|---|---|---|
| F1 | AC-1 uses a configured category instead of literal Plumbing | Retained because S-1 D8 specifies settings-driven categories. | S-1 D8 |
| F2 | AC-2 setup assertion could be strengthened | Deferred; no correction established by the available evidence. | S-1 acceptance tests |
| F3 | AC-3 setup assertion could be strengthened | Deferred; no correction established by the available evidence. | S-1 acceptance tests |
| F4 | AC-5 setup assertion could be strengthened | Deferred; no correction established by the available evidence. | S-1 acceptance tests |
| F5 | Outdated AC-18 comment | Fixed. Comment now references amended AC-18 and D10. | `7104eed` |
| F6 | AC-19 does not explicitly assert empty initial payment history | Deferred. Existing test verifies the resulting payment; explicit initial-state verification remains an improvement opportunity. | Locked AC-19 test |
| F7 | AC-19 second-run assertion checks only history length | Deferred in the acceptance test. Stronger regression coverage should be evaluated separately. | Locked AC-19 test |
| F8 | Processor state leaks between tests | Fixed through fixture teardown that restores the previous processor, including after AC-20. | `7104eed` |
| F9 | AC-20 checks unique-key count rather than exact key and call sequence | Deferred in the acceptance test. Existing test verifies a single Paid payment and consistent observed idempotency keys. | Locked AC-20 test |
| F10 | Manual-payment test cannot verify manager authorization or check-payment type | Retained as a known scope limitation. The test verifies manual payment recording and prevention of a subsequent scheduled charge. | AC-21, P-05 |
| F11 | AC-22 does not explicitly verify retry date remains in December | Deferred. The existing test uses the configured retry delay; explicit month-boundary verification remains an improvement opportunity. | Locked AC-22 test |
| F12 | Before-delay assertion checks only payment count | Deferred. The test verifies the initial Failed payment and subsequent retry attempt, but the intermediate assertion could be strengthened. | Locked AC-22 test |
| F13 | Regression tests could be incorrectly relocated with acceptance tests | Fixed. Only the five designated S-6 acceptance tests were relocated. | `7104eed` |
| F14 | Shared fixtures and helpers could weaken locked acceptance tests | Addressed through relocation of S-6 support files, protection of the acceptance directory and conftest, and subsequent explicit protection of `tests/helpers.py`. | `7104eed`, `b46269f`, `0ee2a1ee6bd4ee1f2c77d4edb59884d7274428c1` |
| F15 | Acceptance-test package organization | Fixed through creation of `tests/acceptance/__init__.py` and distinct test modules. | `7104eed` |
| F16 | AC-18 amendment date discrepancy | The repository records November 23, 2026. Human confirmation of the historical date is required. | `docs/requirements/backlog.md` |

The team preserved the original acceptance-test assertions during relocation. Optional strengthening recommendations that were not implemented before the lock are documented rather than silently applied afterward.

The following command confirms that the acceptance directory remains unchanged:

```bash
git diff --stat m2-tests-locked HEAD -- tests/acceptance/
```

The command returned no differences.

The original audit also identified a reviewer-agent naming conflict. The subsequent headless review successfully delegated to the configured reviewer subagent, as documented in Section 6.

The red-to-green evidence is a historical reconstruction because the original S-6 implementation preceded the formal Milestone 2 acceptance-test lock. This limitation is disclosed rather than presented as an original chronological red-to-green development sequence.

### 4.3 Test Lock and Red-to-Green Development

The initial failing-test evidence is preserved in `evidence/red.txt`.

The acceptance tests were locked using the `m2-tests-locked` Git tag before the implementation reached its green milestone.

The passing-test evidence is preserved in `evidence/green.txt`, and the corresponding milestone is identified by the `m2-green` tag.

The acceptance-test comparison between these tags returned an empty diff, confirming that the protected acceptance tests remained unchanged during that interval.

### 4.4 Implementation Plan and Human Corrections

The original team-approved implementation plan is maintained in `docs/plans/S-6-plan.md`, committed as `bd558d4`.

During AC-22 development, AGENT-01 delegated independent analysis to the test-analyst, security-reviewer, and code-reviewer subagents. AGENT-02 subsequently investigated the retry-date design gap.

These reviews identified two significant corrections to the original implementation approach.

| Correction | Original Problem | Revised Implementation Approach | Evidence |
|---|---|---|---|
| P-01 — Retry-date persistence | The original design lacked a persisted date from which the required retry delay could be calculated. | Introduce persisted failure-date information so retry eligibility can be evaluated against the configured delay. | AGENT-01, AGENT-02, `719aecc` |
| P-02 — Implementation file scope | The original AC-22 task omitted `app/db.py`, although retry-date persistence required database changes. | Expand the task scope to include database schema and payment-state operations. | Prompts 54–59, `719aecc` |

The corrected AC-22 implementation includes changes to `app/settings.py`, `app/db.py`, `app/payments.py`, and the associated regression tests.

The original plan document was not amended. The corrections were instead incorporated into the subsequent task-specific implementation and review workflow.

The supporting AC-22 prompts and implementation evidence were recorded in commit `1f820df`, with post-merge documentation finalized in `17f5efc`.

These corrections demonstrate the value of reviewing design completeness and implementation scope before authorizing a bounded agent task.

### 4.5 Delegation Evidence

The team used specialized subagents to separate acceptance-test auditing, implementation analysis, and code review.

The historical test-writer delegation performed a read-only acceptance-test audit covering the implemented S-1 and S-6 acceptance criteria. The historical code-reviewer delegation reviewed the AC-22 v2 implementation.

Both subagent metadata records confirm completed execution using claude-opus-5-5.

| Delegation | Evidence |
|---|---|
| Acceptance-test audit | `evidence/test-audit.md` |
| Test-writer invocation | `evidence/delegation/test-writer-call.json` |
| Test-writer execution metadata | `evidence/delegation/test-writer-metadata.json` |
| AC-22 v2 code review | `evidence/delegation/ac22-code-review-v2.txt` |
| Code-reviewer execution metadata | `evidence/delegation/ac22-code-review-v2-metadata.json` |
| Final headless reviewer | `evidence/headless-review.json` |

The historical delegation evidence was recovered from the original Claude Code session and committed in `6f79ce31e58b2a78a485571c503f105fa42dc1c3`.

These recovered records are not native Claude Code `/export` transcripts. The historical build-phase code-reviewer is also distinct from the configured reviewer used during the final headless review. These limitations are explicitly disclosed.

The final headless review independently confirmed successful delegation to the configured reviewer subagent, as documented in Section 6.

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

### 5.4 Test Coverage and Quality Gate

The final test suite was executed on November 23, 2026, using Python 3.12.3, pytest 9.2.0, pytest-cov 7.1.0, and Hypothesis 6.170.15.

The following command was used to measure statement and branch coverage and enforce the minimum coverage threshold:

```bash
python -m pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

The original execution output is preserved in `evidence/coverage.txt`.

#### Final Test Results

| Metric | Result |
|---|---|
| Total tests collected | 202 |
| Tests passed | 202 |
| Tests failed | 0 |
| Tests skipped | 0 |
| Warnings | 1 |
| Execution time | 539.40 seconds |
| Statement coverage | 95.76% |
| Combined statement and branch coverage | 94.34% |
| Minimum required coverage | 80% |
| Coverage quality gate | PASS |

#### Module-Level Coverage

| Module | Statements | Missing | Branches | Partial Branches | Coverage |
|---|---:|---:|---:|---:|---:|
| `app/__init__.py` | 0 | 0 | 0 | 0 | 100% |
| `app/access.py` | 19 | 0 | 8 | 0 | 100% |
| `app/auth.py` | 14 | 0 | 4 | 0 | 100% |
| `app/clock.py` | 3 | 1 | 0 | 0 | 67% |
| `app/db.py` | 91 | 4 | 30 | 4 | 93% |
| `app/main.py` | 134 | 3 | 36 | 1 | 96% |
| `app/payments.py` | 83 | 2 | 42 | 2 | 97% |
| `app/processor.py` | 32 | 1 | 4 | 0 | 97% |
| `app/seed.py` | 42 | 7 | 16 | 5 | 79% |
| `app/settings.py` | 7 | 0 | 0 | 0 | 100% |
| Total | 425 | 18 | 140 | 12 | 94.34% |

The overall coverage exceeds the required threshold by 14.34 percentage points. All five S-6 acceptance tests, S-1 regression tests, S-6 regression tests, and both property-based tests passed.

#### Uncovered Code Analysis

One uncovered statement is `app/clock.py:7`, which returns the current UTC timestamp using `datetime.now(timezone.utc)`.

The S-6 acceptance tests replace this clock function with a deterministic timestamp using pytest's monkeypatch fixture. This allows payment scheduling, billing-month selection, and retry timing to be tested reproducibly without depending on the actual system date.

The uncovered statement is acceptable for the current milestone because the application clock is intentionally controlled during these tests. Direct verification of the production clock wrapper could be added as a separate unit test in a future iteration.

Another uncovered statement is `app/processor.py:46`, which raises `ProcessorUnavailable` in the placeholder Stripe processor. Real Stripe integration is explicitly deferred under the approved S-6 scope. Payment behavior is instead tested using FakeProcessor.

#### Test Execution Warning

The test suite reported one StarletteDeprecationWarning concerning the use of httpx with Starlette's TestClient. The warning did not affect test execution or the coverage quality gate. Dependency compatibility should be reviewed in a future maintenance task.

#### Coverage Conclusion

The final execution demonstrates that the complete test suite passes and exceeds the required coverage threshold. Coverage alone does not establish assertion strength or complete business-rule correctness. Mutation testing and property-based testing provide additional evidence of test effectiveness, as discussed in the following sections.

Evidence: `evidence/coverage.txt`.

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

During Milestone 2, our team implemented the S-6 scheduled monthly HOA dues feature using an AI-assisted development workflow. We learned that successful implementation involves more than producing working code. It requires alignment with approved requirements, reliable acceptance tests, controlled agent permissions, human review, and traceable development decisions.

One important lesson involved protecting acceptance tests from unauthorized agent modifications. During AGENT-13, Prompt 79, Claude Code attempted a harmless Edit operation on `tests/acceptance/test_s6_acceptance.py`. The configured permission restrictions rejected the operation, and subsequent SHA-256 and Git diff checks confirmed that the file remained unchanged. This incident is documented in `evidence/permission-denied.md`. Without these restrictions, an agent could potentially weaken an assertion instead of correcting the implementation, creating misleading passing results. The formal acceptance-test lock at commit `b46269f` provided an additional integrity checkpoint. Although the original implementation preceded the formal lock, preserving this limitation in our documentation helped maintain transparency.

Mutation testing provided another valuable lesson. Our initial regression and acceptance tests killed 25 of 30 selected mutants, achieving an 83.33% mutation score. Adding Hypothesis property-based tests did not improve this result. Analysis of the surviving mutants revealed weaknesses in outcome counting and processing multiple units. Three additional deterministic regression tests increased the score to 93.33%, as documented in `evidence/mutation-baseline.txt`, `evidence/mutation-after.txt`, and commit `0f000db`. Conventional coverage remained at 94.34%, demonstrating that high coverage does not necessarily establish strong assertions or complete business-rule verification.

We also recognized opportunities to improve subagent configuration and delegation. In future projects, we would configure specialized test-writer and read-only reviewer agents before implementation begins, verify their permissions, and resolve agent naming conflicts during setup. We would require independent reviews after each bounded implementation task and immediately preserve native delegation transcripts. Recovering historical delegation evidence later, as documented in Ledger Entry 77, required additional effort that could have been avoided through better evidence management.

The final headless review further demonstrated the value of independent verification. It returned a passing verdict with two minor findings concerning outdated ACH comments. Both findings were corrected in commit `7063e9e` without changing payment-processing behavior or acceptance tests.

Finally, the complete test suite passed all 202 tests with 94.34% combined statement and branch coverage, as recorded in `evidence/coverage.txt`. We also learned to communicate limitations honestly, including deferred ACH settlement, unresolved concurrency-policy questions, and the restricted mutation-testing sample.

Overall, Milestone 2 reinforced that AI can accelerate software engineering, but accountability remains with the development team. In future projects, we would establish safety controls earlier, strengthen independent reviews, preserve evidence continuously, and evaluate test effectiveness beyond conventional coverage metrics.

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