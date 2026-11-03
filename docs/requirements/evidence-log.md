# Deliverable 3: Evidence log

Scheme from Assignment 3. **E** = something a real interviewee said or described (cites INT-xx:Pyy).
**A** = an assumption the team is making that the interviews did not establish (source "Team").
**Q** = an open question that must be answered before a related decision is settled.

Status: Observed (a specific past event someone described), Stated (a rule or fact someone
asserted), Assumption (A entries), Open (Q entries).

## E entries: from real interviews (minimum 12)

> **Not yet filled (2026-11-03).** Add E entries only from the numbered notes in
> `interview-notes/`. An AI model, including a synthetic user, can never be the source of an E entry.
> When an E entry confirms an A entry below, note "confirms A-n" in the Claim and update the
> story's trace in `backlog.md` from the A entry to the E entry.

| ID | Claim | Source | Status | Owner |
|---|---|---|---|---|
| E-1 | | INT-__:P__ | | |
| … | | | | |
| E-12 | | INT-__:P__ | | |

**What to listen for.** These are the A entries each interview could confirm or contradict.
Writing them here is not evidence; it is a reminder of what to ask follow-ups about.
INT-01/04 (manager): A-1, A-2, A-3, A-4, A-6, A-8, A-9. INT-02 (board): A-2, A-5, A-11.
INT-03 (resident): A-6, A-7, A-4. INT-05 (tenant): A-10.

## A entries: team assumptions

| ID | Claim | Source | Status | Owner |
|---|---|---|---|---|
| A-1 | We assume a community manager looks after several HOAs at once and tracks resident requests in an email inbox or a spreadsheet. | Team | Assumption | Kundan Singh |
| A-2 | We assume board-only files are shared as shared-drive links, and stay private only if nobody forwards the link. | Team | Assumption | Kundan Singh |
| A-3 | We assume announcements go out as group emails and the manager cannot tell who has seen them. | Team | Assumption | Gustavo Abreu |
| A-4 | We assume dues arrive as paper checks or through a separate bank website, and the manager matches each payment to a home by hand. | Team | Assumption | Matthew Belanger |
| A-5 | We assume that one community's tickets, documents or announcements reaching another community's residents would be treated as a serious breach by a board. | Team | Assumption | Sandeep Garg |
| A-6 | We assume residents want to see where their request stands without having to call or email the manager. | Team | Assumption | Gustavo Abreu |
| A-7 | We assume a resident needs a limited window after a request is resolved to say it was not really fixed. (The proposal's "7 days" was our number, not a user's.) | Team | Assumption | Matthew Belanger |
| A-8 | We assume a manager sometimes needs to send the same announcement to more than one of their communities. | Team | Assumption | Gustavo Abreu |
| A-9 | We assume an automatic reminder after a grace period would replace some of the manager's manual follow-up on late dues. | Team | Assumption | Matthew Belanger |
| A-10 | We assume tenants (renters) are often the first to notice maintenance problems but do not hold the owner's account. | Team | Assumption | Kundan Singh |
| A-11 | We assume communities accept that a manager or admin invites each resident (no self sign-up). | Team | Assumption | Sandeep Garg |
| A-12 | We assume managers need to work in more than one community in the same sitting, so separate logins per community would get in their way. | Team | Assumption | Sandeep Garg |

## Q entries: open questions

| ID | Claim | Source | Status | Owner |
|---|---|---|---|---|
| Q-1 | How many days after a request is marked Resolved should a resident still be able to reopen it? (Setting: `REOPEN_WINDOW_DAYS`.) | Team | Open | Matthew Belanger |
| Q-2 | Can a tenant who lives in a unit but does not own it submit and track a request without seeing the owner's payments? | Team | Open | Kundan Singh |
| Q-3 | Should a management-company admin be able to read a community's tickets, documents and announcements, or only manage accounts and memberships? | Team | Open | Sandeep Garg |
| Q-4 | How many days after a failed payment should the system retry, and how many days after the due date is a unit Overdue? (Settings: `PAYMENT_RETRY_DAYS`, `OVERDUE_GRACE_DAYS`.) | Team | Open | Matthew Belanger |
| Q-5 | Should a board member see every ticket in their community, or only the tickets they submitted as a resident? | Team | Open | Kundan Singh |
| Q-6 | Can a manager move a ticket backwards (In progress → Open), for example when it was started by mistake? | Team | Open | Gustavo Abreu |
| Q-7 | Should a resident be able to see other residents' tickets in the same community (for example, to avoid duplicate reports of a broken gate)? | Team | Open | Kundan Singh |
| Q-8 | Which ticket categories do managers actually use? | Team | Open | Gustavo Abreu |

If two interviewees disagree, log the disagreement as a new A or Q entry; do not choose a side.
