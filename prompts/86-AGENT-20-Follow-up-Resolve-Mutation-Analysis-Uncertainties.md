**Prompt 86 — AGENT-20 Follow-up: Resolve Mutation Analysis Uncertainties**

Continue AGENT-20 in READ-ONLY mode.

Before preparing any patch:

1. Investigate why `app.payments.x__count_outcome__mutmut_5` survived despite Hypothesis Property 1 supporting multiple units.
2. Inspect the exact Hypothesis strategy, assertions, and mutmut test selection. Do not assume which examples were generated.
3. Verify the actual `due_schedules` ordering and the proposed manually-paid-first test setup for mutant `_89`.
4. Reassess mutant `_109`, especially whether a concurrent manual payment could make its behavior observable. Do not label it equivalent without adequate justification.
5. Reassess mutant `_charge_pending_38`, distinguishing public API behavior from direct internal function behavior.
6. Propose three minimal deterministic regression tests for mutants `_5`, `_20`, and `_89`, with exact setup and assertions.
7. Identify the precise files each test would change.

Constraints:
- No file modifications.
- No tests or mutation runs.
- No commits or pushes.
- No changes to locked acceptance tests.
- Do not modify production code.
- If shell access is denied, use available read-only file inspection and explicitly state what remains unverified.

Return your findings and stop for human approval.