# Deliverable 4: Backlog

Roles come from the stakeholder grid in the proposal (Appendix B). Evidence IDs refer to
`evidence-log.md`.

> **Trace status on 2026-11-03.** No interviews have been held yet, so every story below is
> marked **Assumption**, with the A entry it rests on and the clarifying question we will ask a
> real user. After the interviews, replace "Assumption: A-n" with the E entry that supports the
> story, or move the story below the cut line if the interviews contradict it.

Settings used by acceptance criteria (values not settled by interviews; defined in `app/settings.py`):
`REOPEN_WINDOW_DAYS` (Q-1), `TICKET_CATEGORIES` (Q-8), `MAX_PHOTO_MB`, `PAYMENT_RETRY_DAYS` and
`OVERDUE_GRACE_DAYS` (Q-4).

---

## S-1 Community isolation

**As a** resident or board member of a community, **I want** the portal to show me only my own
community's tickets, documents and announcements, **so that** our community's information never
reaches people in another community.

- **Trace:** Assumption: A-5, A-12. Clarifying question: "Has one community's information ever reached someone in another community? What happened the last time?" (interview-kit manager Q8, board Q3)
- **INVEST:** I pass · N pass · V pass · E pass · S pass (read endpoints only; writes come with later stories) · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-1 | A resident, a board member and a manager who have no membership in community B, and B has a ticket, a Community-folder document and an announcement | each of them requests one of those items by its ID | the API answers 404 Not Found and the response contains none of B's titles or text |
| AC-2 | The same three users and community B | each of them requests B's list of tickets, documents or announcements | the API answers 404 Not Found and the response contains none of B's titles or text |
| AC-3 | A resident, a board member and a manager of community A; A has an announcement, a Community-folder document and a ticket the resident submitted; community B has its own items | each of them lists A's announcements and documents, and the resident and manager list A's tickets | each list contains A's items and no item from B; the resident's ticket list includes the ticket they submitted; the manager's ticket list includes every ticket in A |
| AC-4 | A manager assigned to communities A and C (not B), using one sign-in token | they list their communities, then list A's tickets, then C's tickets | the community list shows exactly A and C; each ticket list shows only that community's tickets |
| AC-5 | A request with no token, or with a token that belongs to nobody | it calls any community endpoint | the API answers 401 and the response contains no community data |

## S-2 Ticket status lifecycle

**As a** resident, **I want** to see my request move from Open to In progress to Resolved, and
to reopen it if it was not really fixed, **so that** I know where it stands without calling the manager.

- **Trace:** Assumption: A-6, A-7. Clarifying question: "Tell me about the last time you asked for an update on a request. How did you find out?" (resident Q2, Q3; manager Q3, Q4)
- **INVEST:** I pass (tests seed tickets directly, so it does not need S-5 built first) · N pass · V pass · E pass (reopen window is a named setting) · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-6 | An Open ticket in community A, submitted by a resident of A | A's manager moves it to In progress | the resident's view of the ticket shows In progress, and its history lists Open → In progress with the time of the change |
| AC-7 | An In progress ticket in A | A's manager moves it to Resolved | the resident's view shows Resolved and its history lists In progress → Resolved |
| AC-8 | An Open ticket in A | A's manager tries to move it straight to Resolved | the API answers 409 Conflict and the resident still sees Open |
| AC-9 | An Open ticket in A | the resident who submitted it tries to move it to In progress | the API answers 403 Forbidden and the ticket still shows Open |
| AC-10 | A ticket resolved less than `REOPEN_WINDOW_DAYS` days ago | the resident who submitted it reopens it | the ticket shows Open, and its history lists Resolved → Open as a reopen by the resident |
| AC-11 | A ticket resolved `REOPEN_WINDOW_DAYS` days ago or more | the resident who submitted it tries to reopen it | the API answers 409 Conflict and the ticket still shows Resolved |
| AC-12 | An Open ticket in A and a manager assigned only to community C | that manager tries to move it to In progress | the API answers 404 Not Found and the ticket still shows Open to A's manager |

## S-3 Admin assigns a manager to communities

**As a** management-company admin, **I want** to give a manager access to another community,
**so that** the manager can take over a community without a second account.

- **Trace:** Assumption: A-12, A-11. Clarifying question: "Tell me about the last time a community was handed from one manager to another. What had to be set up?"
- **INVEST:** I pass · N pass · V pass · E pass · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-13 | An admin, and a manager assigned only to community A | the admin assigns the manager to community C | the manager's community list shows A and C |
| AC-14 | A manager assigned only to A | a non-admin user tries to assign that manager to C | the API answers 403 and the manager's community list still shows only A |

## S-4 Board Only folder

**As a** board member, **I want** to put files in a Board Only folder that residents cannot open,
even with a direct link, **so that** board files stay private without relying on nobody forwarding a link.

- **Trace:** Assumption: A-2. Clarifying question: "When did a board member last ask you for a document? Where was it kept, and who else could open it?"
- **INVEST:** I fail: depends on S-1's membership check being built first · N pass · V pass · E pass · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-15 | A file in community A's Board Only folder | a resident of A opens its direct link | the API answers 404 and no file content is returned |
| AC-16 | A board member of A has uploaded a file to the Board Only folder | the server is restarted | the board member can still open the file, and it does not appear in a resident's document list |

## S-5 Submit a request with a category and a photo

**As a** resident, **I want** to send a maintenance request with a category and a photo, **so that**
the manager knows what is wrong and where without a back-and-forth.

- **Trace:** Assumption: A-1. Clarifying question: "Tell me about the last maintenance request a resident sent you. How did it reach you?"
- **INVEST:** I pass · N pass · V pass · E fail: the category list is not known yet (Q-8) · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-17 | A resident of A | they submit a request with a category from `TICKET_CATEGORIES` and a photo under `MAX_PHOTO_MB` | A's manager sees the request in A's ticket list as Open, with its category and photo |
| AC-18 | A resident of A | they submit a request with a category not in `TICKET_CATEGORIES` | the API answers 422, says the category is not allowed, and no new ticket appears in the manager's list |

## S-6 Manager posts one announcement to several communities

**As a** community manager, **I want** to post one announcement to several of my communities at
once, **so that** I do not send the same group email several times.

- **Trace:** Assumption: A-3, A-8. Clarifying question: "Have you ever sent the same notice to more than one of your communities? Tell me about the last time."
- **INVEST:** I fail: needs the email sender that S-9 also uses · N pass · V pass · E pass · S fail: feed fan-out plus email may need to be split into two stories · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-19 | A manager of A and C; residents in A, B and C | the manager posts one announcement to A and C | every resident of A and C sees it at the top of their feed and receives exactly one email; no resident of B sees it or receives an email |

## S-7 Board member posts to their own community

**As a** board member, **I want** to post an announcement to my own community, **so that** board
news reaches residents without waiting for the manager.

- **Trace:** Assumption: A-3. Clarifying question: "Tell me about the last announcement the board wanted sent. Who wrote it and who sent it?"
- **INVEST:** I pass · N pass · V pass · E pass · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-20 | A board member of A | they post an announcement to A | every resident of A sees it at the top of their feed |
| AC-21 | A board member of A only | they try to post an announcement to B | the API answers 404 and no resident of B sees it |

## S-8 Scheduled monthly dues payment

**As a** resident, **I want** my monthly HOA fee charged on a day of the month I choose, by ACH,
debit or credit card, **so that** I do not have to mail a check or use a separate bank website.

- **Trace:** Assumption: A-4. Clarifying question: "Think of how you paid your last HOA dues. Walk me through what you did."
- **INVEST:** I pass · N pass · V pass · E fail: Stripe test-mode ACH timing is new to us · S fail: scheduling, charging, retry and restart safety are a lot for one story; may split into charge (S-8a) and retry (S-8b) · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-22 | A resident has scheduled their monthly fee for day *d*, and the simulated clock reaches day *d* | the payment worker runs | the unit's payment history shows exactly one Paid payment for that month, to both the resident and the manager |
| AC-23 | 50 units scheduled for the same day | the payment worker is restarted part-way through the batch and then finishes | every unit has exactly one payment for that month |
| AC-24 | A resident whose test card is declined | the payment worker runs on the due day, and again `PAYMENT_RETRY_DAYS` days later | the first attempt shows as Failed, exactly one retry is made, and its result appears in the payment history |

## S-9 Automatic overdue status and reminder

**As a** community manager, **I want** a unit that is still unpaid `OVERDUE_GRACE_DAYS` after the
due date to be marked Overdue and reminded once, automatically, **so that** I do not chase late dues by hand.

- **Trace:** Assumption: A-9, A-4. Clarifying question: "Tell me about the last late payment you followed up on. How many days after the due date was that, and what did you send?"
- **INVEST:** I fail: depends on S-8, or on the manual balance from the cut line · N pass · V pass · E fail: grace period unknown (Q-4) · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-25 | A unit unpaid `OVERDUE_GRACE_DAYS` days after its due date | the daily job runs twice | the unit shows Overdue to the manager, and the resident has exactly one automatic reminder in the portal and one email |
| AC-26 | A unit that paid on time | the daily job runs | the unit is not Overdue and the resident has no reminder |

---- **CUT LINE** ----

## S-11 Manager sends another reminder with one click

**As a** community manager, **I want** to send an overdue unit another reminder with one click,
**so that** I can follow up without writing an email.

- **Trace:** Assumption: A-9. Clarifying question: "After the first late notice, what did you do the last time a resident still had not paid?"
- **INVEST:** I fail: depends on S-9 being built first · N pass · V pass · E pass · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-27 | An Overdue unit | the manager clicks Send reminder | the resident gets one more reminder in the portal and by email, and the manager sees the time of the latest reminder |

## S-10 Tenant submits and tracks a request

**As a** tenant renting a unit, **I want** to submit and track a maintenance request, **so that**
problems I notice first get reported without going through the owner. This story exists only if
Q-2 is answered "yes".

- **Trace:** Assumption: A-10. Clarifying question: "The last time a tenant reported a problem, how did it reach you and what happened?" Related open question: Q-2.
- **INVEST:** I fail: depends on S-5 · N pass · V fail: value unproven until A-10 is checked · E fail: depends on Q-2 · S pass · T pass

| AC | Given | When | Then |
|---|---|---|---|
| AC-28 | A tenant account linked to a unit in A | the tenant submits a request and then opens the unit's payment history | the request appears in the tenant's ticket list, and the payment history answers 404 |

---

## 4e Ranking and cut line

| Rank | Story | Why it is above the line |
|---|---|---|
| 1 | S-1 | Every other story relies on the community boundary, and the approval told us to run these access tests from week one. |
| 2 | S-2 | Tickets are the manager's highest-volume job, and the status rules are the clearest invariant we can test early. |
| 3 | S-5 | Without a way to submit a request, the ticket lifecycle has nothing to act on in real use. |
| 4 | S-4 | The Board Only folder is the boards' main privacy need, and it reuses S-1's membership check. |
| 5 | S-3 | Managers cover several communities, so access must be grantable without a second account. |
| 6 | S-6 | One post to several communities replaces repeated group emails, and the delivery test also checks the boundary. |
| 7 | S-7 | Lets boards post without the manager, at small cost once S-6's posting path exists. |
| 8 | S-8 | Scheduled dues are in the proposal's scope, but they carry the most risk, so they come after the access work. |
| 9 | S-9 | Overdue status and one automatic reminder complete the dues capability. |
| — | **Cut line** | |
| 10 | S-11 | Below: a nice-to-have once S-9 works. |
| 11 | S-10 | Below: depends on Q-2 and an unproven assumption (A-10). |

**Conditional cut (from the approved proposal):** if S-1's access tests are not all passing by
Milestone 2, S-8 and S-9 move below the line. Residents would then see a dues balance the manager
types in, and S-9's reminders would be based on that balance.
