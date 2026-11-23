Prompt 69: S-6 Gap Check 2 findings

Sources read: docs/design/S-6.md, the S-6 section of docs/requirements/backlog.md (lines 61–75), and docs/design/S-1.md R2, D1, D3, D5, D6, D7, D12 and D14 (the ones S-6 cites). I also read AGENTS.md because CLAUDE.md requires it before every task. I did not use it as a source for any finding.

Each item below is a question I would have to guess the answer to. I have not answered any of them.

---

1. Ambiguities that could lead to different implementations

┌──────┬─────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ID  │            Reference            │                                                  Question                                                  │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ AC-18 expects the text "Scheduled: day 5 of each month, ACH". D10 says the "Payments page" is the JSON     │
│ G-01 │ AC-18, D10, §4 ScheduleOut      │ from GET .../mine, which returns method: "ach" and day_of_month: 5. Does anything have to produce that     │
│      │                                 │ exact text, uppercase "ACH" included? Or does the JSON alone satisfy AC-18?                                │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ AC-18 "Given R1 has saved a     │ No endpoint or entity saves a bank account. Is "saved a test bank account" just the token in the POST?     │
│ G-02 │ test bank account", D12, §5     │ What format must an ACH test token have, and is it different from a card token?                            │
│      │ Schedule.token                  │                                                                                                            │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-03 │ D7 "it is for their unit there" │ How is "their unit" found? What happens when a resident has two or more units in the community, or no      │
│      │                                 │ unit? Which unit gets the schedule, and what error applies?                                                │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-04 │ D7, D8, D23                     │ What applies when a caller holds more than one role in a community, such as manager and resident, or admin │
│      │                                 │  and resident? Which visibility rule wins in the payments list and the schedule endpoints?                 │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ D23 "every unit in a community  │                                                                                                            │
│ G-05 │ where the caller has the        │ Does a manager calling /communities/A/payments see only A's units, or every unit in every community they   │
│      │ manager role" vs. the path      │ manage? Read literally, D23 says every community.                                                          │
│      │ community_id                    │                                                                                                            │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ Is "caller is not a resident" (a manager or board member calling POST or GET .../mine) part of the 404     │
│ G-06 │ D22, D7, S-1 D6                 │ step before the body checks? Or is it checked later? For example, does a manager sending an invalid body   │
│      │                                 │ get 404 or 422? D7 also never states the status code for a member who is not a resident.                   │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ Are the body-shape checks for all fields done before the value checks? Or is each field checked fully in   │
│ G-07 │ D12, D21, S-1 D6                │ order (method, then day, then token)? For example, {"method":"xyz","day_of_month":"5","token":"t"} could   │
│      │                                 │ return "Unknown method" or "Invalid request body".                                                         │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ Is "token": null a wrong type ("Invalid request body") or empty ("Token is required")? What counts as      │
│ G-08 │ D21                             │ "whitespace": ASCII only or Unicode? Is there a maximum token length? Is a day_of_month integer larger     │
│      │                                 │ than 64 bits "Day must be 1 to 28" or "Invalid request body"?                                              │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-09 │ D9                              │ "A future month returns an empty list": future compared to what, clock.now() or something else? What year  │
│      │                                 │ range is valid (is 0000-01 allowed)? What about a repeated month parameter, or surrounding whitespace?     │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-10 │ D9 vs. D27                      │ Does record_manual_payment check billing_month with exactly the D9 rule? Can it record future months?      │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ Are D26 replays (of this month or earlier months, for any schedule) counted in charged/failed? When a      │
│ G-11 │ D16 counting                    │ replay hits ProcessorUnavailable during the D26 phase, is the due schedule counted as skipped? D16 counts  │
│      │                                 │ only "due schedules", so an unavailable replay from an earlier month seems to be counted nowhere. Is that  │
│      │                                 │ intended?                                                                                                  │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-12 │ D16 "skipped … because the      │ Should a due schedule in a month already Paid be counted as skipped on every daily run until the month     │
│      │ month was Paid"                 │ ends?                                                                                                      │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-13 │ D26, §5 Payment (no token       │ Which token does a replay of a Pending Payment use? The Payment stores no token. Should it be the unit's   │
│      │ field)                          │ schedule token? What if the Payment is a retry, or the unit has no schedule?                               │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-14 │ D26, D32, Step 1 clarification  │ Does the D26 replay take the same unit-row lock and READ COMMITTED transaction as attempts and             │
│      │                                 │ record_manual_payment? Only attempt creation is said to be locked.                                         │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-15 │ D13/D27 precedence              │ When a month has both a Paid and a Pending Payment (possible under D26), which does record_manual_payment  │
│      │                                 │ raise, AlreadyPaid or PaymentPending?                                                                      │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-16 │ D35 "its latest attempt is N −  │ How is "latest" ordered: by attempt, id or created_at? A month can hold two attempt-1 rows (a Failed       │
│      │ 1"                              │ scheduled one and a manual one).                                                                           │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ With unavailable=True, does a repeated key return its stored result or raise? Is a call that raised        │
│ G-17 │ D29 FakeProcessor               │ recorded in calls? Does it store anything? Can unavailable or declined_tokens be changed after             │
│      │                                 │ construction? What is the processor_id format?                                                             │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-18 │ §5 processor_id, §4             │ Is processor_id stored for a declined result? What is it while the Payment is Pending?                     │
│      │ ChargeResult                    │                                                                                                            │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-19 │ D31, D35 "the run stops with an │ What exception type does run_due_payments raise when it stops (a conflicting result, a non-card Stripe     │
│      │  error" vs. §4 "Errors: none"   │ error, any other exception)? Does any partial RunResult reach the caller?                                  │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ Where does python -m app.run_payments get "today's UTC date": clock.now().date() or the system clock? What │
│ G-20 │ D19, D5                         │  should be done when the today passed in and clock.now() disagree (for example, today is before a          │
│      │                                 │ schedule's created_at)?                                                                                    │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-21 │ D32, §5                         │ What SQL column types do created_at, billing_month and failed_on use (text, timestamptz, date)? Which      │
│      │                                 │ table and row is "the unit row" that gets locked?                                                          │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-22 │ D25, D11, §5 active             │ Nothing can ever set active to false. Should active be enforced as a real filter or treated as always      │
│      │                                 │ true?                                                                                                      │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                 │ R5 says "at least RETRY_DELAY_DAYS after that attempt". D17 says "after the today of the run that made the │
│ G-23 │ R5, D17, D35                    │  failed attempt". Only D35 settles this as failed_on. If attempt 1 was created on day 5 (processor         │
│      │                                 │ unavailable) and declined on replay on day 6, the retry could be on day 8 or day 9 depending on which rule │
│      │                                 │  an engineer reads.                                                                                        │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-24 │ AC-19/21/22 "payment history"   │ Is "payment history" the response of GET .../payments?month=? Which caller's view does it mean (R1's or    │
│      │                                 │ the manager's)? Which month does "this month" mean?                                                        │
├──────┼─────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ G-25 │ §8 Named settings, D14          │ Does app/seed.py call set_dues(Mountain Ridge, 18500) by default, or only in tests and demos? AC-19 calls  │
│      │                                 │ DUES_AMOUNT_CENTS a named setting, but it is a per-community column and not in app/settings.py.            │
└──────┴─────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

2. Contradictions

┌──────┬───────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│  ID  │                   Reference                   │                                           Conflict                                           │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                                               │ R5 is unqualified: a unit whose latest attempt is Failed gets a retry on the first run at    │
│ C-01 │ R5 vs. D35 / OQ3                              │ least RETRY_DELAY_DAYS later. D35 says a retry whose date falls in the next month never      │
│      │                                               │ happens, and the next month starts again at attempt 1. R5 also leaves out D35's exceptions   │
│      │                                               │ (the month is Paid, failed_on is null, the attempt is not N − 1).                            │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ C-02 │ R5 vs. R3 / D27                               │ When a manual payment is recorded after a decline, R5 still requires "exactly one new        │
│      │                                               │ attempt". R3 and D35 forbid it.                                                              │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ C-03 │ D9 vs. D27                                    │ D9 says a future month returns an empty list, but nothing in D27 prevents a manual Paid      │
│      │                                               │ Payment for a future month.                                                                  │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ §2 Scope ("charges each scheduled unit") and  │ ACH schedules are accepted and shown as scheduled, but they are never charged and give no    │
│ C-04 │ the backlog user story ("paid automatically   │ signal. The scope and story promise automatic ACH payment.                                   │
│      │ by ACH") vs. D34 / OQ2                        │                                                                                              │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ C-05 │ §1 Problem ("can never be charged twice") vs. │ The design accepts a possible duplicate external charge when D32 is violated. §1 states an   │
│      │  D35's residual risk and D32                  │ absolute guarantee.                                                                          │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ D12 ("a bad [token] is declined at charge     │ In Stripe, a nonexistent or invalid PaymentMethod id usually raises InvalidRequestError, not │
│ C-06 │ time") vs. D33 ("a CardError is declined; any │  CardError. Under D33 that would stop the whole run instead of declining.                    │
│      │  other Stripe error stops the run")           │                                                                                              │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ D20 ("a connection error or 5xx raises        │ Which rule wins for Stripe connection errors, 5xx errors, and errors that neither covers     │
│ C-07 │ ProcessorUnavailable") vs. D33 ("any other    │ (rate limiting, authentication)?                                                             │
│      │ Stripe error stops the run")                  │                                                                                              │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ §2 status (StripeTestProcessor is a           │ Should StripeTestProcessor be built to D20/D33 or stay a placeholder? With the placeholder   │
│ C-08 │ placeholder that raises ProcessorUnavailable) │ as the default processor (D28), every real run leaves Payments Pending forever.              │
│      │  vs. D20 / D33 (its full behavior)            │                                                                                              │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ backlog Step 1 scope clarification and        │ The backlog still says "design/test-only in Milestone 1; all five tests are skipped", "leave │
│ C-09 │ Verification boundaries vs. S-6 §2, §8, §9    │  ACH settlement OQ2 open" and "concurrent manual overlap remains OQ5". The design doc says   │
│      │                                               │ OQ2 and OQ5 are settled and the tests are not skipped.                                       │
├──────┼───────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ C-10 │ D8 ("by unit_id, then attempt") vs. D23       │ These are compatible, but D8 as written leaves ties between attempt-1 rows unordered. Which  │
│      │ ("unit_id, then attempt, then id")            │ rule is authoritative?                                                                       │
└──────┴───────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

3. Missing policy decisions or settings without a documented source

┌──────┬──────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ID  │        Reference         │                                                        Gap                                                        │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │                          │ Stripe idempotency keys expire after about 24 hours. D4 assumes a replay "returns its earlier result", but a      │
│ P-01 │ D4, D26, D29             │ Pending Payment replayed days later (for example after a long processor outage) could be charged again. There is  │
│      │                          │ no policy on key lifetime.                                                                                        │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│      │ §5 idempotency_key       │ "{unit_id}:{billing_month}:{attempt}" is unique only within one database. Different schemas or environments       │
│ P-02 │ format                   │ sharing one Stripe test account would collide, and Stripe would return another Payment's result. There is no      │
│      │                          │ namespacing policy.                                                                                               │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-03 │ D32 "Only one run at a   │ No mechanism enforces a single runner (an advisory lock, a lock file, operations guidance). D35's residual risk   │
│      │ time is supported"       │ depends on it.                                                                                                    │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-04 │ D33, §4 ChargeResult     │ Off-session PaymentIntents can return requires_action or processing. Only succeeded and declined are defined.     │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-05 │ D13, D27, AC-21          │ record_manual_payment has no caller, authorization, payment-type field (AC-21 says "check") or audit trail. Who   │
│      │                          │ may record a manual payment, and how is that recorded and enforced?                                               │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-06 │ §5 Schedule.token, D33   │ The token is stored but never returned. How should it be stored (plaintext or protected) and kept? There is no    │
│      │                          │ sensitive-data rule.                                                                                              │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-07 │ D17 after the last       │ Nothing tells the resident or manager when retries are exhausted or when an ACH schedule will never charge.       │
│      │ attempt, D34 ACH         │ Reminders are non-goals (S-7), but no interim behavior is set.                                                    │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-08 │ D30, D35                 │ A retry's amount is the dues at the time the retry is created, so it can differ from attempt 1 if dues change     │
│      │                          │ mid-month. Is that the intended policy? It is stated but not justified.                                           │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-09 │ OQ5, §1                  │ If a check arrives while a charge is Pending and the charge then succeeds, the money is received twice outside    │
│      │                          │ the system. OQ5 sets no refund policy, even though §1 names this exact problem (E-9).                             │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-10 │ D33 exit codes           │ What exit code and output should python -m app.run_payments give when the run stops with an exception?            │
├──────┼──────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ P-11 │ D9, D25 billing_month    │ Which timezone defines "this month" for the payments list? Is it UTC like today, or the community's local         │
│      │                          │ timezone?                                                                                                         │
└──────┴──────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

4. Untestable or unverified acceptance criteria and design rules

┌──────┬─────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  ID  │              Reference              │                                                 Issue                                                  │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-01 │ AC-20                               │ "Interrupted and restarted" cannot be tested as written. The design says the test keeps the same       │
│      │                                     │ FakeProcessor and does not restart a process or use a durable external processor result.               │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-02 │ §1 "never be charged twice", R1/R2  │ These can be verified only against FakeProcessor. Real-processor deduplication (P-01, P-02) cannot be  │
│      │ across real processors              │ tested.                                                                                                │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-03 │ D20, D33                            │ StripeTestProcessor behavior and the CLI contract cannot be tested: tests use only FakeProcessor, and  │
│      │                                     │ neither piece is built.                                                                                │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-04 │ D32 / Step 1 clarification          │ The concurrency guarantees (unit-row lock, READ COMMITTED) are tested only within one process, not     │
│      │                                     │ with concurrent connections.                                                                           │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-05 │ AC-18                               │ The exact display text has no surface where it can be asserted (G-01).                                 │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-06 │ AC-22                               │ The AC does not say a run happens after RETRY_DELAY_DAYS, what the retry's outcome is, or whether      │
│      │                                     │ "after" means exactly the delay or later. Several implementations would pass.                          │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-07 │ OQ2 "a cleared ACH payment is       │ This depends on a step outside the system. No acceptance criterion or test can verify it.              │
│      │ recorded manually"                  │                                                                                                        │
├──────┼─────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ U-08 │ D35 residual risk                   │ A duplicate external charge after a conflicting completion is accepted but has no detection criterion, │
│      │                                     │  so it cannot be observed or tested.                                                                   │
└──────┴─────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

Task report

- Task: Prompt 69, S-6 Gap Check 2 (read-only analysis)
- Agent: Main agent only. I delegated nothing to subagents, because the prompt limited the allowed context to the files listed above.
- Files read: AGENTS.md (required by CLAUDE.md, not used as a source), docs/design/S-6.md, docs/requirements/backlog.md lines 58–77, and the cited rules in docs/design/S-1.md
- Changes: None. I modified no files and ran no shell commands, tests, commits or pushes. File access used only the Read and Grep tools.
- Unresolved issues: All 54 findings above (G-01–G-25, C-01–C-10, P-01–P-11, U-01–U-08), left unanswered as instructed.
- Human approval status: Read-only analysis; there is nothing to approve.
- Commit SHA: None. HEAD when the task started was 7d24517.
