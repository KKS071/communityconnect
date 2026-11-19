# S-6 Implementation Plan — Scheduled Monthly HOA Dues

**Status:** Team approval reported by requester on 2026-11-19. Gustavo approval reported by requester; Implementation proceeds one AC at a time after scope instructions are updated.  
**Repository:** `KKS071/communityconnect`  
**Source of truth:** `docs/design/S-6.md` (R1–R5, D1–D34, OQ1–OQ5), `docs/requirements/backlog.md` (AC-18–AC-22), `tests/test_s6_payments.py`, `AGENTS.md`, and `docs/reviews/S-6-requirements-finalization.md`.

## Authorization gate

`AGENTS.md` currently states that S-6 is not built, that S-6 tests remain skipped, and that AI tools must not implement S-6 code. The requester reports team approval of this plan and explicitly authorizes changes to `AGENTS.md` and S-6 test skip markers on 2026-11-19. Update the repository instructions before implementation. Remove only the current AC skip marker when its code is ready for verification; leave the remaining ACs skipped. The `docs/` directory is human-owned. Do not modify test assertions, requirements, ledger, prompts, or unrelated files.

## Design constraints

Use Python 3.11+, FastAPI, PostgreSQL 14+ via psycopg 3 and `%s` SQL parameters. Preserve S-1 authentication/authorization and 404 concealment. No new dependencies without approval. No real money: Stripe **test mode** only. The S-6 Payments page is represented by an API response, not a new frontend (D10). AC-18 permits ACH schedule creation/display, **not ACH settlement**. AC-19–AC-22 use debit schedules with `FakeProcessor` (D34). Only one payment runner at a time is supported (D32).

## Proposed files and responsibilities

| File | Planned changes | Stage |
| --- | --- | --- |
| `app/db.py` | Add schedules; later payments, dues column, unique idempotency key and partial unique paid-per-unit/month index (D32) | AC-18, AC-19 |
| `app/main.py` | POST schedule, GET own schedule; later GET payment history with role and month checks (D7–D10, D21–D23) | AC-18, AC-19 |
| `app/clock.py` (new) | UTC-aware `now()` for timestamps, replaceable in tests (D5, D24) | AC-18 |
| `app/seed.py` | `set_dues` with positive-cent validation (D30) | AC-19 |
| `app/processor.py` (new) | `Processor`, `ChargeResult`, `ProcessorUnavailable`, `FakeProcessor`, `get_processor`, `set_processor`; Stripe test adapter only after dependency approval (D20, D28–D29, D33) | AC-19 / separate task |
| `app/payments.py` (new) | `run_due_payments`, `record_manual_payment`, `RunResult`, `AlreadyPaid`, `PaymentPending` (D4, D16–D18, D25–D31) | AC-19–AC-22 |
| `app/settings.py` | Provisional `RETRY_DELAY_DAYS = 3`, `MAX_PAYMENT_ATTEMPTS = 2`; read from settings rather than hard-code (D15) | By AC-22 |
| `app/run_payments.py` (new) | Optional CLI from D19/D33; requires separate approval | Later |
| `app/access.py` | No planned edit; reuse `require_resident`/`require_member` | — |

**This inventory is a forecast, not blanket approval.** Each task below requires its own approved file list. Existing `tests/`, `docs/`, `AGENTS.md`, `README.md`, `requirements.txt`, `pytest.ini`, `LEDGER.md`, and `prompts/` are excluded from implementation edits unless separately authorized by humans.

## Bounded tasks — one acceptance criterion at a time

### 2.1 — AC-18: schedule creation and display

**Proposed files:** `app/db.py`, `app/main.py`, new `app/clock.py`. Implement `POST /communities/{community_id}/payment-schedules` and `GET /communities/{community_id}/payment-schedules/mine`. Resident-only access for own unit; one schedule per unit; `ScheduleOut` omits token. Validate method (`ach`, `debit`, `credit`, case-sensitive), integer day 1–28 (not bool), and nonblank token in D12/D21 order. Preserve 401/404/409/422 behavior and UTC timestamps. No ACH charge or settlement.

**Verification after separately approved unskip of AC-18:** `python -m pytest tests/test_s6_payments.py -k ac18_` and `python -m pytest tests/test_s1_requests.py`. A skipped result is not a pass. Stop after this AC.

### 2.2 — AC-19: monthly charge exactly once

**Proposed files:** `app/db.py`, `app/main.py`, `app/seed.py`, new `app/processor.py`, new `app/payments.py`; `app/settings.py` only if needed. Add payment storage and indexes, positive dues setting, debit fake processor, due-day run and payment-history endpoint. Persist `Pending` with stable unique key **before** charging; transition to `Paid`/`Failed`, with committed state. Rerunning the day must not duplicate the unit/month payment (R1–R3, D25, D28–D32). Single runner only.

**Verification after separately approved unskip:** `python -m pytest tests/test_s6_payments.py -k ac19_` plus S-1 regression tests. Do not claim ACH settlement, concurrent-run safety, or real processor validation.

### 2.3 — AC-20: simulated crash and replay

**Proposed files:** `app/payments.py`, `app/processor.py`; `app/db.py` only if necessary. Resume `Pending` using original key and stored amount; replay with same fake processor and produce one `Paid` row. Continue after `ProcessorUnavailable` and preserve `Pending`; other exceptions stop the run after prior commits (D4, D26, D29–D31).

**Verification after separately approved unskip:** `python -m pytest tests/test_s6_payments.py -k ac20_` plus S-1 tests. The existing fixture retains the same fake processor object: it does **not** demonstrate actual process restart or independently durable processor state. Stronger integration testing needs separate approval.

### 2.4 — AC-21: manual payment prevents scheduled charge

**Proposed files:** `app/payments.py`; `app/db.py` only if necessary. `record_manual_payment` records a `Paid` manual payment for valid unit/month at current dues, raises `AlreadyPaid` for a paid month, and prevents the scheduled charge when recorded first (R1, R3, D13, D27). For an existing `Pending` payment, preserve the specified `PaymentPending` behavior; do not invent an OQ5 refund/conflict policy.

**Verification after separately approved unskip:** `python -m pytest tests/test_s6_payments.py -k ac21_` plus S-1 tests.

### 2.5 — AC-22: declined-payment retry

**Proposed files:** `app/payments.py`, `app/settings.py`; `app/processor.py` only if necessary. Preserve failed attempt 1, retry no earlier than `RETRY_DELAY_DAYS`, use a new per-attempt key, and stop at `MAX_PAYMENT_ATTEMPTS` (D15–D17, R5). Provisional defaults are 3 and 2 respectively; tests read settings.

**Verification after separately approved unskip:** `python -m pytest tests/test_s6_payments.py -k ac22_`; then `python -m pytest` with PostgreSQL available. Confirm S-1 regressions and all enabled S-6 tests; do not count skips as passing.

### Separate integration task — not preapproved

D19/D20/D33 describe `python -m app.run_payments` and Stripe PaymentIntents in **test mode**. Check the approved dependencies and obtain separate approval for `StripeTestProcessor`, CLI, and integration tests. No scheduler, live credentials, production charges, or external calls are included in the five AC tasks.

## Review, testing, and rollback procedure

1. Obtain team approval for the specific AC and exact file list; record reviewer, date, and scope authorization. Keep one bounded commit or PR per AC.
2. Human-maintained changes to `AGENTS.md` and to `tests/test_s6_payments.py` skip markers require separate approval; never weaken assertions or expected values.
3. Start PostgreSQL test service per `README.md`. Tests must use isolated schemas and never target live payment systems.
4. Run the AC-specific test after authorized unskip, S-1 regression tests, `git diff --check`, `git diff --stat`, and `git status`. Report actual pass/fail/skip counts.
5. Stop after the agreed check. Revert the bounded commit if tests fail. Obtain independent human review before merging.

## Open policy questions — stop if a task depends on one

| Gate | Restriction |
| --- | --- |
| OQ1 — processing fees | Do not allocate or charge card fees |
| OQ2 — ACH settlement and returns | ACH schedule/display only; no ACH `Paid` semantics |
| OQ3 — arrears | Current billing month only (D25) |
| OQ4 — board payment visibility | No board payment-list access until decided |
| OQ5 — manual payment during `Pending` | Keep D27 `PaymentPending`; no invented refund/conflict policy |

## Team approval record

- Reported approver: **Gustavo** (reported by requester; not independently verified)
- Approval date: **2026-11-19** (reported)
- Decision: **Team-approved implementation plan** (reported by requester)
- First implementation task: **AC-18**, proposed code files `app/db.py`, `app/main.py`, `app/clock.py`
- Authorization to revise `AGENTS.md`: **Yes**, requester explicitly approved
- Authorization for test-marker changes: **Yes**, requester explicitly approved; unskip only current AC once implementation is ready
- PR or meeting reference: #11-19-2026

**Approval is not evidence of implemented functionality or passing tests.**
