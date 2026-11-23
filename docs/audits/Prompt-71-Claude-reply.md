I've confirmed the AGENT-06 changes are in the working tree, and checked the behaviour I'm documenting against the code. Writing the AGENT-07 patch now.

  Searched for 1 pattern

● Write(agent-patches/AGENT-07-S6-final-decisions.patch)
Wrote 75 lines to agent-patches/AGENT-07-S6-final-decisions.patch
diff --git a/docs/design/S-6.md b/docs/design/S-6.md
--- a/docs/design/S-6.md
+++ b/docs/design/S-6.md
@@ -59,10 +59,10 @@
 - **D4:** Each attempt is saved as `Pending` with its key before the processor call, then set to `Paid` or `Failed` (for ACH, see OQ2). On r
estart a `Pending` Payment is charged again with the same key, so the processor returns its earlier result. **D5:** `today` is a UTC date pas
sed to `run_due_payments`; every `created_at` comes from `app/clock.py::now()`, which tests replace.
-- **D6:** S-1’s D1, D3, D6, D7 and D12 apply (identity, hidden records, check order, error format, storage). **D7:** Only a caller with the
`resident` role in the community can create or read a schedule, and it is for their unit there.
+- **D6:** S-1’s D1, D3, D6, D7 and D12 apply (identity, hidden records, check order, error format, storage). **D7:** Only a caller with the
… +69 lines (~24 KB)

  Searched for 2 patterns

I've written the patch to agent-patches/AGENT-07-S6-final-decisions.patch. It's documentation only and built against the current working tree, so it includes the AGENT-06 changes. Nothing was applied, run or committed.

One possible snag in the patch

In the third hunk (@@ -99,5 +99,18 @@), I left a blank line after ## 9. Acceptance tests, just before the backlog.md section. That line isn't counted in the hunk header, but it matches the blank line 104 in S-6.md. I expect git apply to treat it as filler between the two files and skip it. If git apply --check complains instead, the file needs that header changed to @@ -99,6 +99,19 @@. I won't edit an existing patch, so I'd write a corrected v2 if needed.

Every other header matches its content:

┌───────────────┬───────────────────────────┐
│     Hunk      │ Context / removed / added │
├───────────────┼───────────────────────────┤
│ -59,10        │ 5 / 5 / 5                 │
├───────────────┼───────────────────────────┤
│ -70,15        │ 8 / 7 / 7                 │
├───────────────┼───────────────────────────┤
│ -99,5 +99,18  │ 5 / 0 / 13                │
├───────────────┼───────────────────────────┤
│ backlog -65,7 │ 5 / 2 / 2                 │
└───────────────┴───────────────────────────┘

All context lines match the current files.

Proposed changes

docs/design/S-6.md (§8 only):

┌───────────────────────────┬────────────────────────────────────────────────────────────────────────────────────┬───────────────────────────────────┐
│           Item            │                                       Change                                       │               Basis               │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D7                        │ Any caller who isn't a resident of the community gets 404 at the S-1 404 step,     │ G-06; code: require_resident runs │
│                           │ before the body checks                                                             │  before the body is read          │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│                           │ "A month with no Payment records visible to the caller returns an empty list". It  │                                   │
│ D9                        │ also notes that record_manual_payment accepts future months, and that this         │ Decision 4; C-03, G-09, G-10      │
│                           │ behaviour is unchanged.                                                            │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D10                       │ AC-18 is checked against the JSON from GET …/mine. Records the amendment as a      │ Decision 1; G-01, U-05            │
│                           │ human decision of 2026-11-23, quoting the original wording.                        │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│                           │ Documents the actual validation order: all type checks first, then values in field │                                   │
│ D12                       │  order. Tokens are opaque. pm_card_visa isn't a bank account, and there's no real  │ Decision 2; G-07 (F-10), G-02     │
│                           │ ACH support.                                                                       │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│                           │ Documents how replays are counted, and that a unit can be counted as both charged  │                                   │
│ D16                       │ and skipped in one run. Marked as a known limitation (F-08), not fixed and not     │ Decision 5; G-11                  │
│                           │ covered by a test.                                                                 │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D20                       │ processor_id is null while a payment is Pending and stored once it's Paid or       │ G-18; code: finish_payment        │
│                           │ Failed                                                                             │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D23                       │ "Every unit they manage" means only the units in the community named in the URL    │ G-05; code: main.py query;        │
│                           │                                                                                    │ existing cross-community test     │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D26                       │ A replay uses the stored amount and the unit's current schedule token, and takes   │ G-13, G-14; code:                 │
│                           │ no lock. It relies on the single-runner rule (D32) and the F-11 guard (D35).       │ db.pending_payments               │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D27                       │ If a month has both a Paid and a Pending payment, the function raises AlreadyPaid  │ G-15; code: the Paid check runs   │
│                           │                                                                                    │ first                             │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│                           │ Documents how FakeProcessor already behaves: it records the call first, a stored   │                                   │
│ D29                       │ result wins over "unavailable", the flags can be changed, and IDs look like        │ G-17; app/processor.py            │
│                           │ fake_<n>                                                                           │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D31                       │ A run that stops returns no RunResult. It lists the exceptions: RuntimeError for a │ G-19                              │
│                           │  conflicting result, ValueError for an unexpected status.                          │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D34                       │ Records your 2026-11-23 scope decision: ACH schedules can be created and viewed,   │ Decision 3; C-04                  │
│                           │ while ACH charging and settlement are deferred                                     │                                   │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ D35                       │ Defines "latest attempt" as ordered by attempt, then id                            │ G-16                              │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ New "Known limitations    │ Ten explicit limitations, each tagged with its Gap Check 2 IDs                     │ Decision 7                        │
│ and deferred items" block │                                                                                    │                                   │
└───────────────────────────┴────────────────────────────────────────────────────────────────────────────────────┴───────────────────────────────────┘

The ten limitations in that block:
- Stripe
- command line
- concurrency and the D35 duplicate-charge risk
- token storage and the lack of real ACH bank accounts
- manual-payment authorization and audit trail
- notifications
- refunds
- F-08 counting
- AC-20 restart simulation
- storage details

docs/requirements/backlog.md:
- AC-18: the Then clause now reads "the JSON response of R1's GET …/payment-schedules/mine shows method "ach", day_of_month 5 and active true". A note records it as a human amendment of 2026-11-23 and quotes the original text. The Given clause is unchanged.
- Step 1 scope note: adds that "test bank account" is satisfied by an opaque test token, that pm_card_visa isn't a real bank account, and that real ACH bank-account support isn't built.

The existing AC-18 test already checks method, day_of_month, active and unit_id, and that no token is returned, so the amendment needs no test change. That follows the handout's order of design doc, then criterion, then test. §9 test paths, code and tests are unchanged.

Gap Check 2 summary for MILESTONE2.md (draft)

Gap Check 2 (Deliverable 1d). The second S-6 gap check (docs/design/S-6-gap-check-2.md, prompt in prompts/) produced 54 findings: 25 ambiguities (G), 10 contradictions (C), 11 missing policies (P) and 8 untestable items (U). We triaged every finding:
- Real gaps (22), resolved by human-approved documentation changes in AGENT-06 and AGENT-07:
  - R5 now states the retry conditions and failed_on timing (C-01, C-02, G-23).
  - "Payment history" and AC-18 are defined (G-24, G-01/U-05).
  - The backlog notes and D8/D23 ordering and scope are corrected (C-09, C-10, G-05).
  - The existing behaviour is documented in D7, D9, D12, D16, D20, D26, D27, D29, D31 and D35 (G-06, C-03, G-07, G-11, G-18, G-13, G-14, G-15, G-17, G-19, G-16).
- Acceptance-criterion change (1): AC-18 was amended by human decision on 2026-11-23, from literal display text to the JSON fields method, day_of_month and active. It is recorded as an amendment, not as a pass against the original wording.
- Already answered (12): G-03, G-04, G-06, G-12, G-22, G-25, P-08, P-09, P-11, U-01, U-06, and the null-token part of G-08. Each cites the section that answers it.
- Deferred limitations (20), confirmed by human decision and listed in S-6 §8 "Known limitations": Stripe behaviour and key policy, the command-line runner, enforcing a single runner, token storage, manual-payment authorization, notifications, refunds, real-processor and concurrency verification.
- Code defects: none fixed in this step. The F-08 counting limitation (G-11) and future-month manual payments (C-03) are documented as existing behaviour, without claiming they are fixed.

Gap Check 2 has no ID for the G-08 whitespace, token-length and large-integer edge cases, so they aren't in the summary. Mention them if you want them recorded.

Unresolved issues

1. Patch structure: the possible issue at the top of this message.
2. docs/requirements/traceability.md may still quote AC-18's original wording. It wasn't in scope; please check it.
3. No ledger entries yet for the human decisions of 2026-11-23 (AC-18 amendment, ACH scope, deferrals), for Gap Check 2 (Prompt 69) or for Prompts 60–71. The handout requires one entry per agent task, and S-6 D35 and the OQ intro refer to LEDGER.md.
4. prompts/65-S6-gap-check-2.md and the actual Prompt 69 need to be saved under prompts/ if they aren't already.
5. Stale comment in code: the app/access.py:33 docstring still says "until OQ4 is answered". It's source code, so I didn't change it.
6. Known behaviours deliberately left in place:
   - F-08 counting (G-11).
   - Future-month manual payments are accepted (C-03).
   - The F-10 validation order is now documented, not changed. Tests still deliberately avoid mixed cases.
7. Next steps in the handout order:
   - Commit these documentation changes and the gap check.
   - Move the AC tests to tests/acceptance/.
   - Run the test-writer audit (needs the new subagent files and settings).
   - Decide how to produce red.txt honestly.
   - Lock the tests and tag m2-tests-locked.

Commands to check and apply the patch:
! git apply --check agent-patches/AGENT-07-S6-final-decisions.patch
! git apply agent-patches/AGENT-07-S6-final-decisions.patch
! git diff --stat

No tracked files were modified. I created one file, in agent-patches/, and ran no commands.
