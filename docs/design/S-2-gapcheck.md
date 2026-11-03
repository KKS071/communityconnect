# Gap check: S-2 design doc

- Doc checked: `docs/design/S-2.md` at commit `8b3e8f0` (draft before gap check)
- Model: Claude Sonnet (subagent launched from a Claude Opus 5.5 session), 2026-11-03. The subagent was told to read only `docs/design/S-2.md`.
- Prompt: see `prompts/06-gapcheck-S-2.md`

## Full reply

1. What value should `REOPEN_WINDOW_DAYS` have (Q-1), and what placeholder value should go in `app/settings.py` in the meantime?
2. Is the window measured in 24-hour periods or calendar days, and does DST or timezone handling matter for "days"?
3. Can a manager move a ticket backwards (Q-6), and what should happen in the code path where a manager requests `open` or any backward status?
4. What does the 422 for an unknown status value cover when the body sends `"open"` or `"resolved"` for the wrong source state, or `"open"` at all? Is `"open"` a "known but not allowed" value (409) or an "unknown" value (422)?
5. What exactly does the `POST /tickets/{ticket_id}/status` body accept for a missing `status` field, a null value, or extra fields?
6. What are the exact 401 and 404 bodies and the `require_member` behavior from S-1, given S-1 is not available to me?
7. What is the exact S-1 `Ticket` shape (field names, types, ID type, `created_by` representation), and how are the fields in `TicketWithHistory` combined with it?
8. What do `changed_by` and `changed_at` look like in the response (integer ID or user object; ISO-8601 format, "Z" suffix or offset, precision)?
9. What does the `kind` field contain for each entry, and is `kind` determined solely by the transition (`resolved→open` is `reopen`, all others `advance`)?
10. Which user is "a manager of the ticket's community": how is the manager role stored and determined, and can a user have multiple roles in one community?
11. What status code applies when the caller is a member of the community but is neither the manager nor the creator, and when a caller is a manager of a different community (404 per AC-12 vs 403 per the table)?
12. For `/reopen`, what is the 403 vs 409 vs 404 ordering when the caller is not the creator and the ticket is also not `resolved`? Does D2 (role then state) apply there?
13. For `/reopen`, which 409 applies first when the ticket is `resolved` but the window has passed versus the ticket not being `resolved`? And does the role check precede both?
14. Does the 409 for a disallowed transition apply when the status field is valid but the ticket is `resolved` and a manager sends `in_progress` or `resolved`? Is there any manager action on a `resolved` ticket?
15. What does "the ticket stays as it was" require for the refused request when the check order means some errors (e.g. 422) happen before DB access?
16. Who can call `GET /tickets/{ticket_id}`? Is it any community member, only the creator, or managers too, and what does "as S-1" mean for access control and errors there?
17. R5 says "by the creator", so must non-creator members (other residents, board members) also see the status and history, or only the creator?
18. How should `clock()` be used: called once per request, and is the same value used for `changed_at`, `resolved_at`, and the window check?
19. What does a naive or non-UTC datetime from `clock` do: is it rejected, converted, or assumed to be UTC?
20. How is `resolved_at` stored when a ticket is resolved, and how is it compared in R4 (parse the stored text, and what if parsing fails)?
21. How does `app.settings.REOPEN_WINDOW_DAYS` get read: at request time (so tests can change it) or at app creation, and is `app.settings` an object, module or `SimpleNamespace`? What validation enforces the "int ≥ 1" constraint?
22. What is the default system clock: `datetime.now(timezone.utc)`?
23. What is the migration path for the existing database: how do `resolved_at` and `ticket_history` get added to an existing S-1 DB, and what happens to existing tickets already in `resolved` or other states?
24. Does S-1 already define a `status` column and its allowed values (`open`, `in_progress`, `resolved`), and what are its defaults?
25. Does a ticket that has never changed status return an empty `history` list and `resolved_at` of null?
26. Are history `id` and `ticket_id` exposed in the response? The `history` entry lists only `from_status`, `to_status`, `changed_by`, `changed_at`, `kind`.
27. Does a reopen record the creator's user ID as `changed_by`, and does a manager who is also the creator reopening count as the creator?
28. For edge case 4, when a manager who is also the creator advances their own ticket, is `changed_by` the same ID and is `kind` still `advance`?
29. How should concurrency (D4) be implemented in SQLite: `BEGIN IMMEDIATE`, a conditional `UPDATE ... WHERE status = ?` with rowcount check, or something else? And what do the losing concurrent requests return (409)?
30. For edge case 5, is the second of two simultaneous manager requests that targets the same transition returned as a 409 "Transition not allowed"?
31. What is the transaction behavior if the history insert fails after the status update (atomic rollback)?
32. What 404 body is used for a missing ticket versus a non-member, and are they the same body as S-1 (no leaking of whether the ticket exists)?
33. What about a ticket ID that is not an integer in the path (422 from FastAPI or 404)?
34. What happens when a resolved ticket's creator account has been removed or is no longer a member of the community when they try to reopen?
35. Do the tests in section 9 exist already (skipped), and what fixtures, helpers and clock-injection approach do they expect? AC-6 to AC-12 are named, but their exact content is not defined here.
36. How do I unskip them, and what AC does each edge case in section 7 map to, given only AC-6 to AC-12 are listed?
37. Is there an AC for the "exactly at window boundary", "same status again", "board member reopen" or "concurrency" cases, or do I write new tests for them?
38. What does the backlog.md reference mean for the evidence IDs A-6 and A-7 — do I need to do anything with the unlogged interview evidence?
39. Are there any rate limits, audit logging, or schema-version requirements for the new endpoints?
40. Should `POST /tickets/{id}/status` with `"status": "open"` be accepted by the schema at all, given the body type allows only `in_progress | resolved`?
41. Should the response for the status endpoint be 200 with the full updated ticket, and does it need to be identical to what the `GET` returns right afterwards?
42. Do non-goals (no notifications, no assignment, no editing) imply that any other fields in the request body should be rejected or ignored?
43. What is the expected sort order of `history` when two entries share the same `changed_at` timestamp (tie-break by `id`)?

## Triage

| # | Verdict | Where |
|---|---|---|
| 1 | Answered (value) / Real gap (placeholder) | §8 Q-1 stays open; D5 says how the placeholder is marked |
| 2 | Real gap | D6 (window = N × 24 h of UTC time) |
| 3 | Answered | §8 Q-6 (open); D7 covers what the endpoint does with `"open"` |
| 4 | Real gap | D7 (`"open"` and any other value → 422) |
| 5 | Real gap | D7 (missing/null → 422; extra fields ignored) |
| 6 | Answered | S-1.md §4 (doc says "Builds on S-1") |
| 7 | Answered | S-1.md §4 |
| 8 | Answered | S-1.md D16 (timestamp format); §5 (`changed_by` is a user ID) |
| 9 | Real gap | D8 (`kind` = `reopen` exactly for `resolved→open`) |
| 10 | Answered | S-1.md §5 (`memberships.role`, one role per pair) |
| 11 | Answered | D2 (404 membership → 403 role → 409 state) |
| 12 | Answered | D2 |
| 13 | Real gap | D9 (state check before window check) |
| 14 | Answered | R1 (no manager transition out of `resolved`) |
| 15 | Answered | R1 (refused requests change nothing; a 422 never writes) |
| 16 | Answered | S-1.md R5 |
| 17 | Answered | S-1.md R5 (other residents cannot read the ticket) |
| 18 | Real gap | D10 (one `clock()` call per request) |
| 19 | Real gap | D10 (naive datetime is a programming error → raise) |
| 20 | Answered | §5 + S-1.md D16 (fixed format, parsed with the same format) |
| 21 | Real gap | D11 (module attribute read at request time) |
| 22 | Real gap | D10 (`datetime.now(timezone.utc)`) |
| 23 | Real gap | D12 (no migration in M1) |
| 24 | Answered | S-1.md §5 |
| 25 | Answered | R2, R3 |
| 26 | Answered | §4 (only the listed fields) |
| 27 | Answered | R5, edge case 4 |
| 28 | Answered | edge case 4, D8 |
| 29 | Real gap | D4 extended (conditional UPDATE; loser gets 409) |
| 30 | Real gap | D4 extended |
| 31 | Answered | D4 (one transaction) |
| 32 | Answered | S-1.md §4, R3 |
| 33 | Answered | S-1.md edge case 5 |
| 34 | Answered | D2 (membership check first → 404) |
| 35 | Answered | §9 (skipped tests exist) |
| 36 | Answered | `AGENTS.md` (unskip only when building the story) |
| 37 | Real gap | D13 (edge cases get their own non-AC tests during the build) |
| 38 | Answered | §1 note |
| 39 | Real gap | D14 (no rate limits or audit log in M1) |
| 40 | Real gap | D7 |
| 41 | Answered | §4 (`TicketWithHistory`, same as GET) |
| 42 | Real gap | D7 |
| 43 | Real gap | D8 (history ordered by `id`) |
