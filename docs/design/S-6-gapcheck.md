# S-6 gap check

**Model:** Claude Sonnet, run as a separate agent from the Claude Opus 5.5 session on 2026-11-09. It was given `docs/design/S-6.md` at commit `36926c7` (the version copied from the Milestone 1 report), plus `docs/design/S-1.md` only for the S-1 decisions that S-6 refers to.

**Prompt** (`prompts/17-gapcheck-S-6.md`): "You are the engineer who must build this. List every question you would have to guess the answer to. Do not answer them."

## Full reply

1. What exact value do `RETRY_DELAY_DAYS` and `MAX_PAYMENT_ATTEMPTS` take in tests, and where do tests read them from, given the doc says tests read the settings but gives only provisional defaults?
2. What value (and what rounding or format) does `day_of_month` validation accept: does a bool, a float such as 5.0, or a numeric string count as a wrong type (`Invalid request body`) or as an out-of-range value (`Day must be 1 to 28`)?
3. Does "Unknown method" apply to a wrong-case value like "ACH" (S-1 D4 gave exact case-sensitive matching for categories, but this doc does not say so for methods)?
4. Is `manual` rejected as a method by the POST endpoint with `422 "Unknown method"`?
5. What counts as an empty token for `422 "Token is required"`: the empty string only, or whitespace-only too, and is the token trimmed?
6. What is the check order among the 401, 404, 409 and 422 errors on POST (D6 of S-1 applies, but where does 409 fit relative to the 422 body checks)?
7. If the caller is a resident in the community but their membership has a null unit_id (or the unit is missing), what is returned?
8. For `GET .../payment-schedules/mine`, what is returned when the resident has no schedule: `404 "Not found"`, or something else?
9. What is the exact status and message when a non-resident (manager, admin, board member, non-member) calls POST or GET `payment-schedules/mine`, given D7 only says who can create or read?
10. For `GET .../payments`, what do the list endpoint and its `month` parameter return for a manager managing no units, and how is "every unit they manage" defined (the S-1 data model has no manager-to-unit link; is it every unit in the community)?
11. When `month` is missing, what exact error is returned (D9 says required and otherwise `Invalid month`; is missing 422 "Invalid month")? Also, what happens with a non-numeric `community_id` in the path?
12. What is the order of checks for the payments list: caller, membership, then month, or month before membership?
13. Does the payments list include `Pending` Payments, and are they shown with the same fields (e.g. `processor_id` is absent from PaymentOut)?
14. What is the sort order exactly: unit_id ascending then attempt ascending, and where does a manual payment fall?
15. What is the `created_at` format in PaymentOut and ScheduleOut (S-1 D5 format assumed?), and is `now()` in `app/clock.py` returning a datetime or a string, and with what signature?
16. What is the "month's end" boundary for D18 and "the first month whose chosen day is after its created_at date" when created_at is exactly on the chosen day: is the day itself excluded (strictly after)? Also how is the created_at date compared to `today` (UTC date vs. test-clock)?
17. Is a schedule due in a month when the unit has any Payment that month (D18 says "no Payment that month") while R4 and R5 require retries and Pending resumption; how do these interact for a `Pending` or `Failed` attempt-1 payment, and which wins?
18. Which billing_month does a run on `today` charge: the month of `today`, always? And what is billing_month for a catch-up run after the month rolls over?
19. For R5, "the first run at least RETRY_DELAY_DAYS after that attempt": does a retry across a month boundary still use the old billing_month (D17 says same billing_month) even though the next month's charge becomes due, and can both happen in one run?
20. What is the retry time measured from: the `today` of the run (D17) or `created_at`? What happens when a retry would be due after the month ends?
21. How does a run decide whether the last attempt failed when a `Pending` retry exists with a processor outage: does a `Pending` attempt N≥2 keep its attempt number, and does it count as "latest attempt"?
22. In `Pending` restart (D4), is every `Pending` Payment charged again regardless of due date or retry delay, and regardless of whether the schedule is still due or the month is now Paid (R3)?
23. What happens to an existing `Pending` Payment when a manual payment is recorded for the same month (OQ5 says stop and ask): should `record_manual_payment` raise, ignore the pending, or leave it, and what does the next run do with that Pending? Is anything in this case buildable?
24. How does `AlreadyPaid` apply when the month has a `Failed` or `Pending` scheduled payment: manual payment still allowed? What are the manual Payment's `attempt` (1) conflict with an existing attempt-1 scheduled Payment key and the unique idempotency key, and what are amount_cents and the unit's dues amount at record time?
25. What does `record_manual_payment` do with an unknown unit_id or invalid billing_month (no errors are listed)? Where is `AlreadyPaid` defined (module and class)?
26. Where do `run_due_payments`, `RunResult`, `Processor`, `ChargeResult`, `ProcessorUnavailable`, `AlreadyPaid`, `StripeTestProcessor` and `FakeProcessor` live (module paths), and how does `run_due_payments` receive the processor (parameter, global, or setting) since its signature has only `today`?
27. How does `FakeProcessor` behave: how are declines, unavailability and idempotent replays scripted, and does it live in `tests/` or `app/`? How do tests make `StripeTestProcessor` vs `FakeProcessor` selectable at the API/CLI level (`python -m app.run_payments`)?
28. What does the processor do on an idempotent replay with a changed amount or token, and what happens if the stored token differs?
29. What `amount_cents` does a scheduled Payment use: the dues_amount_cents at charge time or at attempt creation, and what if the community's dues change between attempts or a restart?
30. What does the run do when the community's `dues_amount_cents` is missing or the data violates the > 0 rule (and are existing S-1 communities migrated with a default)?
31. How are `dues_amount_cents` values set by `app/seed.py` (new function signature, parameter name on community creation, default values), and do the S-1 seed functions change signature?
32. What exactly do `charged`, `failed` and `skipped` count when one unit has multiple outcomes in a run, and is a due schedule whose retry is not yet due counted as skipped, or not counted at all? Does a `Pending` left by `ProcessorUnavailable` count as skipped, and what about a unit whose attempts are exhausted?
33. When the processor is unavailable for one unit, does the run continue with other units or stop immediately? Is there a limit on retries within one run?
34. Does a processor exception other than `ProcessorUnavailable` abort the run, and what is the transaction/commit boundary (per Payment save, per unit)?
35. What happens when a decline is returned on an attempt below MAX_PAYMENT_ATTEMPTS during the same run it was created: no immediate second attempt that day, presumably; confirm. And what status transitions for `Failed` when retries are exhausted?
36. Given D16 says an unavailable processor "leaves the Payment `Pending` without using an attempt", does a retry attempt N≥2 that is `Pending` also keep its number, and does `attempt` value in an attempt-1 `Pending` Payment get reused next run?
37. How does R1's "at most one Paid" get enforced under concurrent runs or two processes (database unique constraint, locking), or is only sequential use assumed?
38. Does `day_of_month` apply to the UTC date, and what about a schedule whose `unit_id` has a pre-existing `Paid` manual payment on creation: first-due logic?
39. What is the schema/migration approach for existing S-1 databases given new tables and the added Community column (D12 of S-1: SQLite at DATABASE_PATH)? Are Schedule and Payment table names and column names prescribed?
40. Does the `ScheduleOut` for a POST return `active: true`, and does a 409 apply per unit across two residents of the same unit (different users, same unit), and across different communities (unit is community-specific)?
41. What is the `Stripe` mapping of amounts, currency, `payment_method` use of the "test token" (e.g. `pm_card_visa` vs `tok_visa`), `confirm`, off-session flags, and the exact currency code for PaymentIntents? How is `declined` distinguished from other Stripe errors (authentication required, invalid request)? What is stored in `processor_id` on a declined charge?
42. How do the AC tests set up scenarios: which helper functions (like S-1's `set_status`) exist in `tests/helpers.py` for creating schedules, setting the clock, and injecting a processor, and does AC-20's "restart mid-run" mean simulating a crash by a raising processor/fake or by killing the process?
43. What does AC-18 ("schedule shown on payments page") assert exactly, given D10 equates it with `GET .../payment-schedules/mine`; and what do AC-19 to AC-22 assert in terms of counts and statuses (the doc gives only test names)?
44. What does "the unit's payment history" for a resident in the payments list contain regarding the `month` filter versus all months, given `month` is required (is there no way to list all months)?
45. Is `skipped` returned/counted for inactive schedules (all schedules are `active` and cannot be changed, but should the run filter on `active`)?
46. What does `python -m app.run_payments` print or return, which exit code on failures, and which processor does it use and where is `STRIPE_TEST_KEY` read from (environment variable, settings)? What happens if the key is missing?
47. What are the HTTP response details for a request whose `X-User-Id` is missing or malformed on these endpoints (S-1 D1 assumed), and does a non-numeric `community_id` return `404 "Not found"` (S-1 D7 assumed)?
48. For OQ1 to OQ5, which parts of the design are considered "depending on" them: e.g. is the ACH `Paid` status (D4 "for ACH, see OQ2") to be built as immediate `Paid` or left unbuilt, and is the `ach` method acceptable to create and charge at all?

## Triage

"Answered" names the section of `docs/design/S-6.md` (or the S-1 decision it adopts) that already answers the question. Every "Real gap" is now decided in §8 (D21 to D34) or §9.

| # | Verdict | Where |
|---|---|---|
| 1 | Answered | §8 D15 (tests read `app.settings`, never the numbers) |
| 2 | Real gap | §8 D21 |
| 3 | Real gap | §8 D21 |
| 4 | Real gap | §8 D21 |
| 5 | Real gap | §8 D21 |
| 6 | Real gap | §8 D22 |
| 7 | Answered | §8 D6 adopts S-1's data rules; S-1 D17 makes a resident without a unit impossible |
| 8 | Real gap | §8 D22 |
| 9 | Answered | §8 D7 with D6 (S-1 D3: hidden is `404 "Not found"`) |
| 10 | Real gap | §8 D23 |
| 11 | Answered | §8 D9 (missing is "Invalid month"); D6 (S-1 D7, D14 for path ids) |
| 12 | Answered | §8 D6 (S-1 D6 order: caller, path and membership, then input) |
| 13 | Real gap | §8 D23 |
| 14 | Real gap (tie with manual) | §8 D23 |
| 15 | Real gap | §8 D24 |
| 16 | Real gap | §8 D25 |
| 17 | Real gap (D18 vs R4/R5) | §8 D25 |
| 18 | Real gap | §8 D25 |
| 19 | Real gap | §8 D25 (only `today`'s month is processed) |
| 20 | Real gap (after month end) | §8 D25; "measured from" is answered by D17 |
| 21 | Real gap | §8 D26 |
| 22 | Real gap | §8 D26 |
| 23 | Real gap | §8 D27 (fails closed; the choice itself stays OQ5) |
| 24 | Real gap | §8 D27; the manual key is answered by §5 |
| 25 | Real gap | §8 D27, D28 |
| 26 | Real gap | §8 D28 |
| 27 | Real gap | §8 D29, D28 |
| 28 | Real gap | §8 D29 |
| 29 | Real gap | §8 D30 |
| 30 | Real gap | §8 D30 |
| 31 | Real gap | §8 D30 (`set_dues`; S-1 seed signatures unchanged) |
| 32 | Answered | §8 D16 (what each count includes); a schedule not yet due is not counted |
| 33 | Real gap | §8 D31 |
| 34 | Real gap | §8 D31 |
| 35 | Answered | §8 D17 (retry no sooner than RETRY_DELAY_DAYS; nothing after the last attempt) |
| 36 | Real gap | §8 D26 |
| 37 | Real gap | §8 D32 |
| 38 | Answered | §8 D5 (UTC dates); §6 R3 (an existing Paid month is skipped) |
| 39 | Real gap | §8 D32 |
| 40 | Real gap (per unit) | §8 D22; `active: true` is answered by §5 |
| 41 | Real gap | §8 D33 |
| 42 | Real gap | §8 D28, D29, D31 (crash simulated by an exception) |
| 43 | Real gap (where the AC wording is) | §9 now points to the backlog |
| 44 | Answered | §8 D9 (`month` is required; there is no all-months list) |
| 45 | Real gap | §8 D25 (only active schedules) |
| 46 | Real gap | §8 D33 |
| 47 | Answered | §8 D6 (S-1 D1, D7, D14) |
| 48 | Real gap | §8 D34 |

**Totals:** 48 questions: 10 already answered, 38 real gaps, all resolved in §8 or §9.

**Found by this check:** AC-19 asks for a Paid payment after an ACH schedule (AC-18). That quietly settles OQ2 (whether a successful ACH charge shows as Paid before the return window has passed), which handout 4d does not allow. D34 keeps OQ2 open by using debit schedules in the tests for AC-19 to AC-22.
