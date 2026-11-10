# S-1 gap check

**Model:** Claude Sonnet, run as a separate agent from the Claude Opus 5.5 session on 2026-11-09. It was given only `docs/design/S-1.md` at commit `36926c7` (the version copied from the Milestone 1 report).

**Prompt** (`prompts/16-gapcheck-S-1.md`): "You are the engineer who must build this. List every question you would have to guess the answer to. Do not answer them."

## Full reply

1. What is the exact JSON shape of the "Invalid request body" 422 versus the other 422s, and does a framework (FastAPI/Pydantic) validation error need to be intercepted globally to produce `{"detail": <message>}` as a string rather than the default list?
2. What is the exact `created_at` format when several requests are created within the same second, and does the `created_at` then `id` ordering (D11) make the "appears first" guarantee in R4 hold?
3. What does `X-User-Id` with leading or trailing whitespace, a plus sign, leading zeros, a very large integer, or duplicate header values do, beyond the regex in D1?
4. What is the status code and body when `X-User-Id` is missing entirely: does it follow `401 "Unknown user"` rather than the framework's default 422?
5. How is a non-numeric or out-of-range `community_id` or `request_id` handled (negative, zero, huge integers, floats, overflow beyond SQLite's int range), given D7 says non-numeric returns 404?
6. What is the precedence when the caller is unknown (401) and the path id is also non-numeric (404), given D6's order?
7. For POST, does the body-shape check (422 "Invalid request body") run before or after the membership check, and what happens when the body is invalid and the caller is not a resident (D6 says 404 first)?
8. Is an empty or non-JSON body, a JSON body that is not an object (array, string, null), or a wrong Content-Type treated as "Invalid request body"?
9. Does a `description` of only whitespace return "Description is required", and does an empty string do the same?
10. What counts as whitespace for `strip()` on unusual Unicode characters, and should length be counted in code points rather than grapheme clusters or bytes?
11. Is the order of the description checks fixed (required before too long), and what happens when the description is invalid and the category is also invalid: which error is returned first, given D6 lists description before category?
12. What happens with a boolean, number, null or object for `category` or `description`: is each "Invalid request body"?
13. What happens when `category` is an empty string or has surrounding whitespace: "Unknown category" and is it trimmed?
14. How are the settings in `app/settings.py` read by the app: at import time or per request, and how do tests override REQUEST_CATEGORIES and MAX_DESCRIPTION_CHARS?
15. Where is DATABASE_PATH defined, how is it configured per test (environment variable, setting, dependency override), and what is the default value?
16. What is the database schema, including constraints, indexes, foreign keys (is PRAGMA foreign_keys enabled), and who creates the tables and when (at app startup, in the seed, or in a test fixture)?
17. How are concurrent requests and SQLite connections handled (connection per request, check_same_thread, write locking), and what ensures id assignment is unique and R4's "grown by exactly 1" holds under concurrency?
18. What are the signatures, parameters and return values of the functions in `app/seed.py`, and does the seed create data on startup or only when tests call it?
19. What is the interface of `tests/helpers.py::set_status`: does it open the same database through DATABASE_PATH, and who writes it, given the API does not expose status changes?
20. Do I write the six acceptance tests myself, and what exact setup, fixtures and test client (TestClient vs real server) do they use?
21. What exactly should AC-2's test assert (which blank descriptions, and that the list is unchanged and not just the count)?
22. Should the test for R5 be checked for every rejection type (401, 404, 422), and how is "total number of requests" observed, since there is no endpoint for it?
23. What is the data of a resident whose Membership has `unit_id` null or pointing to a unit in another community; is this impossible (seed validation) or should the API respond with a specific error?
24. What happens when a user holds a `resident` membership and also another role in the same community: the Membership is one row per user and community, so can this occur, and is it ignored?
25. Which role-specific behavior is required for `board_member`, `manager` and `admin` in the same community, as the doc says D10 returns 404 for managers and admins but board members are OQ2: for a board member who is not a resident, do I return 404 for now, or stop and ask?
26. Does the instruction "Do not build anything that depends on this. Stop and ask" for OQ1 and OQ2 mean I must halt the whole task, or only leave those cases unbuilt, and what default behavior should apply to those users in the meantime?
27. What does R1 mean for a request whose submitter later loses the resident role or moves unit (memberships are fixed here, but can the seed change them), and should the list and detail still check the current role?
28. For GET `/requests/{request_id}`, if the caller is a resident of the request's community and submitted it, what is returned when the caller's unit has since changed; is `unit_id` the stored value?
29. Does the list endpoint return an empty list `[]` with 200 for a resident with no requests, and 404 only for non-residents?
30. Does `unit_id` in the response and storage come from the caller's Membership at the time of submission, and is it ever accepted from the client?
31. What are the maximum lengths and uniqueness constraints that must be enforced in the code versus only documented (Community name, Unit label, user id), and is validation of seed data expected?
32. Is `created_at` second precision truncated or rounded, and does the ordering use a higher-precision stored value or only the truncated string?
33. What is the status value serialization: are the strings exactly "Open", "In progress" and "Resolved", and what if the database holds any other value?
34. Is there an `OPTIONS`, `HEAD`, or unsupported-method behavior to define, for example 405 responses, and is their body also `{"detail": ...}`?
35. What should happen for paths not defined at all (404 body), or a trailing slash on routes?
36. Are CORS, logging, authentication-failure rate limiting or any other cross-cutting concerns expected?
37. What are the project's dependency versions, Python version, run command, how the app is started, and the project layout beyond `app/main.py`, `app/settings.py`, `app/seed.py`, and `tests/`?
38. Does "newest first" for the list apply across all of the caller's requests in that community only, and is there any limit on how many requests a resident can submit or any duplicate-submission handling?
39. Does `POST` response include a `Location` header, and is the `201` body identical to what GET returns?
40. Are error messages case-sensitive and punctuation-exact as quoted (for example, `"Unknown user"`), and should the 404 body for a hidden record be byte-identical, including headers, to a missing one (R2)?
41. Does R2 need the response time or other side channels to be indistinguishable between hidden and missing records?
42. How should the doc's references to other items (E-1, E-2, E-12, S-2, S-9, S-11, Q-5) be treated, and is any of that content required reading for the build?

## Triage

"Answered" names the section of `docs/design/S-1.md` that already answers the question. Every "Real gap" is now decided in §8 (D14 to D21) or §9.

| # | Verdict | Where |
|---|---|---|
| 1 | Answered | §8 D7 (every error body is `{"detail": <message>}`, framework errors included) |
| 2 | Answered | §8 D11 (ties broken by id descending), D5 |
| 3 | Real gap (repeated header) | §8 D14; the rest is answered by D1's regex |
| 4 | Answered | §8 D1 (a missing header does not match the regex, so 401) |
| 5 | Real gap (zero, negative, overflow) | §8 D14 |
| 6 | Answered | §8 D6 (caller check first) |
| 7 | Answered | §8 D6 (membership 404 before body checks) |
| 8 | Real gap | §8 D15 |
| 9 | Real gap (which message) | §8 D15 |
| 10 | Answered | §8 D9 (`str.strip()`, `len()` in code points) |
| 11 | Answered | §8 D6 (description before category); required and too long cannot both apply |
| 12 | Answered | §8 D7 (non-string is "Invalid request body") |
| 13 | Answered | §8 D4 (exact match, so no trimming) |
| 14 | Real gap | §8 D16 |
| 15 | Real gap | §8 D16 |
| 16 | Real gap | §8 D16 |
| 17 | Real gap | §8 D16 (connection per call, AUTOINCREMENT ids) |
| 18 | Real gap | §8 D17 |
| 19 | Answered | §8 D13 (signature); the database path is D16 and D18 |
| 20 | Real gap (test client) | §8 D18; the test names are in §9 |
| 21 | Real gap (where the AC wording is) | §9 now points to the backlog |
| 22 | Real gap | §8 D18 (`count_requests()`) |
| 23 | Real gap | §8 D17 (the seed rejects it) |
| 24 | Answered | §5 Membership (one row per user and community) |
| 25 | Real gap | §8 D19 |
| 26 | Real gap | §8 D19 |
| 27 | Answered | §6 R1 (current role is checked) |
| 28 | Real gap | §8 D20 |
| 29 | Real gap | §8 D20 |
| 30 | Real gap | §8 D20 |
| 31 | Real gap | §8 D17 |
| 32 | Answered | §8 D5 (seconds), D11 (id tie-break) |
| 33 | Answered | §4 `RequestOut`, §5 Request.status |
| 34 | Real gap | §8 D21 |
| 35 | Real gap | §8 D21 |
| 36 | Real gap | §8 D21 |
| 37 | Real gap | §8 D16 |
| 38 | Real gap (limits, duplicates) | §8 D20; the ordering scope is answered by §2 |
| 39 | Real gap | §8 D21 |
| 40 | Answered | §4 (exact messages), §6 R2 (status and body) |
| 41 | Answered | §6 R2 defines "exactly what it returns" as status and body |
| 42 | Answered | §1 (evidence IDs are for traceability only) |

**Totals:** 42 questions: 17 already answered, 25 real gaps, all resolved in §8 or §9.
