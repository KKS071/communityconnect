# Gap check: S-1 design doc

- Doc checked: `docs/design/S-1.md` at commit `8b3e8f0` (draft before gap check)
- Model: Claude Sonnet (subagent launched from a Claude Opus 5.5 session), 2026-11-03. The subagent was told to read only `docs/design/S-1.md`.
- Prompt (from lecture, verbatim plus output-format line): see `prompts/05-gapcheck-S-1.md`

## Full reply

1. What hashing or storage format applies to tokens? The doc says `users.token` is stored as plain text, unique and at least 32 chars, but it doesn't say how tokens are compared.
2. Which web framework features apply? Specifically, how should the 401 body be forced to exactly `{"detail": "Not authenticated"}`, given that FastAPI's default security helpers return different wording and status codes?
3. How should the 404 body be made byte-for-byte identical (R3) across the "no membership" and "does not exist" cases? That covers whitespace, key order, content-type header and any other headers.
4. Does a 401 for a malformed header (edge case 4) need the same body as a missing header? Is the scheme match `Bearer` case-sensitive?
5. What exactly counts as "extra spaces" in a token? Should leading or trailing whitespace be trimmed, or rejected outright?
6. What is the order of checks when a request has both a bad token and a non-integer or nonexistent ID? Does the 422 for a non-integer path ID come before or after the 401? R2 says 401 comes before any community data is read, but edge case 5 doesn't say whether 422 can leak to unauthenticated callers.
7. Do integer IDs that are zero, negative or larger than SQLite's integer range return 404 or 422? The data section says IDs are ≥ 1.
8. What should the 404 be for `GET /tickets/{id}` when the ticket exists in the caller's community but belongs to someone else? It is described only as 404 in R5, so is its body the same as the standard one?
9. How should the sqlite3 connection be created and managed? Per request, pooled, or on a dependency? Are foreign keys enabled with `PRAGMA foreign_keys`? Thread-safety settings (`check_same_thread`) are not specified for FastAPI's threadpool.
10. What does `create_app` do when the schema exists but differs from §5? "Creates the schema if missing" doesn't say whether it checks, migrates or ignores the difference.
11. Are the §5 constraints (length limits, enums, the ≥ 1 and ≥ 32 checks, `is_admin` 0 or 1) enforced as SQLite `CHECK` constraints, in application code, or only documented?
12. What are the full column types, NOT NULL constraints, indexes and ON DELETE behaviour for each foreign key?
13. Where does the `COMMUNITYCONNECT_DB` environment variable get read? Does `create_app(db_path)` ignore it, and who reads it for the production entry point? What is the ASGI entry module for running the app?
14. What are the seed script's name, location, data and invocation? D2 and the non-goals mention a "seed script" that creates tokens, but the doc never defines it, and nothing says whether it is in scope.
15. How are tokens generated in the seed script and tests (length, alphabet, source of randomness)?
16. What is `NotFound`? Where is it defined (module, base class)? How is it mapped to the 404 response? Is it raised by `require_member` only, or also for missing items?
17. What does `require_member` do for a non-existent community, or a non-existent `user_id`? It should presumably raise `NotFound`, but this is unstated.
18. How do item endpoints (`/tickets/{id}`, `/documents/{id}`, `/announcements/{id}`) find the community? D4 says endpoints never query `memberships`, so does the endpoint look up the item first and then call `require_member`? The doc doesn't say whether the lookup and the membership check are sequenced to avoid timing differences, and whether timing parity matters for D1.
19. For the item endpoints, what happens with a document whose `folder` is `board_only` (R4)? Is it 404 for everyone, including members of that community? Does `GET /documents/{id}` on a board_only document return the same 404 as non-existent?
20. Does the documents list filter `board_only` out in SQL, or in the application? What if the list ends up with zero items: 200 with `[]`?
21. Does a member of a community with no tickets, documents or announcements get 200 with `[]`? The doc implies it but doesn't state it.
22. What is the tie-break ordering for announcements with equal `posted_at`? What is the ordering of the documents list, since no order is given? Is `posted_at` compared as text, given that formats like "Z" vs "+00:00" could break sorting?
23. What exactly is the ISO-8601 UTC format for `created_at`, `uploaded_at` and `posted_at` (suffix `Z` or `+00:00`, fractional seconds, precision)? Does the API emit the stored string unchanged?
24. Are response models strict, meaning extra fields such as `token` or `is_admin` can never appear? Is `Community` expected to carry the caller's role? The shape says only `{id, name}`.
25. What are the field types in the JSON shapes: are `created_by` and `posted_by` just user integer IDs, and may display names be exposed? Does that leak other members' identity, for example a manager seeing resident names?
26. What does `GET /me/communities` return for users whose membership rows reference deleted communities? Is there any referential cleanup?
27. Does a user with multiple roles in one community exist? The primary key forbids it, but how is the DB error handled in tests and seed data?
28. What is the status code for unsupported methods such as POST or DELETE on these paths (405, or 404 to avoid leaking)? What about HEAD and OPTIONS, and does CORS matter given there is no web client?
29. What happens on trailing slashes (`/me/communities/`)? FastAPI's default redirect is 307, which may bypass the 401/404 rules.
30. What does the 401 do when the token is valid but belongs to a user whose row is later deleted mid-request? Is there a requirement on transactional consistency?
31. R1 says "every item's `community_id`" is one the caller is a member of. For a manager token, does R1 hold across all communities, or only the requested one? How is R1 checked in tests: per item or per response?
32. Is the AC-3 requirement for `resident sees own ticket` also meant to cover a `board` member? The AC list has a single test for "resident", though R5 treats board the same way.
33. What are the AC-1 and AC-2 definitions of "outsider" in the parametrisation? Is the outsider a member of another community, a member of none, or an admin with no memberships (edge case 3)? Does "3 roles" mean the caller's role in their own community or in the target one?
34. For AC-5, "every endpoint × missing/unknown token": which token variants from edge case 4 are included? Do the tests also need to assert that no DB read happened (R2's "before any community data is read")? How would that be observed?
35. Are the tests expected to use `fastapi.testclient.TestClient` or `httpx`? What are the fixtures for seeding data, and who owns the test helpers? Are the minimum Python, FastAPI and SQLite versions specified, and how are dependencies declared (pyproject, requirements.txt)?
36. What is the repository layout beyond `app/main.py`, `app/access.py`, `app/auth.py` and `tests/test_s1_community_isolation.py`? Where do models, DB helpers and routers go?
37. What do Q-3 and Q-5/Q-7 imply for admin users and for board/resident ticket visibility? Currently both are "stop and ask", so is it acceptable that admin gets 404 everywhere (edge case 3), or does that count as depending on Q-3? Likewise, is R5's narrow rule itself "building something that depends on Q-5/Q-7"?
38. The doc says "Evidence IDs (A-2, A-5, A-12) are assumptions until the interviews are logged; see backlog.md". Are these assumptions safe to build on, and is backlog.md required reading? Who resolves them?
39. Are there performance, pagination or limit requirements for list endpoints? There are none stated, so are all rows always returned?
40. Is there any logging or audit requirement for denied requests? Should logs avoid recording tokens?
41. Does the manager "work in every community they are assigned to with one token" imply anything beyond multiple membership rows, such as a default or "current" community, or a switching endpoint? AC-4's test name says "switches", but the interface has no switch operation.

## Triage

"Answered" names the section that already answered it. "Real gap" names where it was resolved in
the updated doc (§8 decision D-number, or a rule rewrite).

| # | Verdict | Where |
|---|---|---|
| 1 | Real gap | D7 (plain-text token, exact match) |
| 2 | Answered | §4 error bodies |
| 3 | Answered | §4 error bodies, R3 |
| 4 | Real gap | D8 (header format) |
| 5 | Real gap | D8 |
| 6 | Real gap | D9 (401 before 422/404); R2 reworded so it can be checked from outside |
| 7 | Real gap | D10 (out-of-range IDs → 404) |
| 8 | Answered | §4 error bodies (one 404 body for all 404s) |
| 9 | Real gap | D11 (connection per request, foreign keys on) |
| 10 | Real gap | D12 (CREATE IF NOT EXISTS; no migrations in M1) |
| 11 | Real gap | D12 (CHECK constraints for enums and ranges) |
| 12 | Real gap | D12 (all columns NOT NULL; no deletes in S-1) |
| 13 | Real gap | D6 extended (`app.main:app` reads the variable) |
| 14 | Real gap | D13 (no seed script in M1) |
| 15 | Real gap | D13 (tests use `secrets.token_hex(16)`) |
| 16 | Real gap | D4 extended (`NotFound` and its handler) |
| 17 | Answered | §4 (`require_member` raises `NotFound` when there is no membership row) |
| 18 | Real gap | D14 (item endpoints: look up item, then `require_member`; timing parity is not a goal) |
| 19 | Answered | R4, R3 |
| 20 | Real gap | D15 (empty list → 200 `[]`; filtering in SQL) |
| 21 | Real gap | D15 |
| 22 | Real gap | D15 (ties by `id`; documents by `id`), D16 |
| 23 | Real gap | D16 (timestamp format) |
| 24 | Answered | §4 JSON shapes are the exact field lists |
| 25 | Answered | §4 (`created_by`/`posted_by` are integer IDs; no names) |
| 26 | Answered | §3 (no delete endpoints in S-1) |
| 27 | Answered | §5 primary key |
| 28 | Real gap | D17 (405 for wrong method) |
| 29 | Real gap | D17 (no slash redirects; trailing slash → 404) |
| 30 | Answered | §3 (no deletes) |
| 31 | Answered | R1 (every item in every 200 response) |
| 32 | Answered | R5 covers board members; AC-3 is about residents |
| 33 | Real gap | D18 (who counts as an outsider in AC-1/AC-2) |
| 34 | Real gap | D8 lists the variants; R2 reworded |
| 35 | Answered | `AGENTS.md` (pytest + TestClient, `requirements.txt`) |
| 36 | Real gap | D19 (module layout) |
| 37 | Real gap | Q-3 reworded: admin's 404 follows from D3, and the open question is whether to *add* admin read access. Q-5/Q-7 likewise ask whether to *widen* D5. |
| 38 | Answered | §1 note |
| 39 | Real gap | D20 (no pagination in M1) |
| 40 | Real gap | D20 (no audit log; never log tokens) |
| 41 | Real gap | D21 ("switching" means choosing the community ID in the path) |
