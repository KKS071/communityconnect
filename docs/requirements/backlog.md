# Deliverable 4: Backlog

Evidence IDs refer to `evidence-log.md`. Named settings in capitals are defined in `app/settings.py` once a story that uses them is built.

## 4a, 4b, 4d. Stories, evidence trace and acceptance criteria

Values the interviews did not settle are written as named settings in capitals, such as GRACE_PERIOD_DAYS. The sample data uses three communities: Mountain Ridge, Pine Hollow and Elm Court. Manager M1 manages Mountain Ridge and Pine Hollow; manager M2 manages only Elm Court.

### S-1: Submit and track a maintenance request

As a resident, I want to submit a maintenance request and see its current status in the portal, so that I do not have to email or visit the office to ask for updates.

**Evidence:** E-1, E-2, E-12

- **AC-1** Given resident R1 of unit 12 in Mountain Ridge is signed in, When R1 submits a request with category “Plumbing” and description “Kitchen sink leaks”, Then R1’s request list shows that request with status Open and today’s date.
- **AC-2** Given R1 is signed in, When R1 submits a request whose description is empty or only spaces, Then the portal shows “Description is required” and R1’s request list is unchanged.
- **AC-3** Given R1 has an Open request in Mountain Ridge and resident R2 of Pine Hollow is signed in, When R2 opens the Pine Hollow request list, Then R1’s request is not listed.
- **AC-4** Given R2 of Pine Hollow is signed in, When R2 opens R1’s request directly by its ID, Then the portal shows “Not found” and none of the request’s details.
- **AC-5** Given R1 has an Open request and resident R3 of unit 20 in Mountain Ridge is signed in, When R3 opens the Mountain Ridge request list, Then R1’s request is not listed.
- **AC-6** Given R1’s request has status In progress, When R1 opens the request, Then the portal shows status In progress.

### S-2: Manager updates a request’s status

As a community manager, I want to move a request from Open to In progress to Resolved, so that the resident can see progress without contacting me.

**Evidence:** E-1, E-2, E-12

- **AC-7** Given R1’s request in Mountain Ridge is Open and M1 manages Mountain Ridge, When M1 sets it to In progress, Then R1’s request list shows In progress.
- **AC-8** Given R1’s request is Open, When M1 sets it straight to Resolved, Then the portal shows “Status must move to In progress first” and the request stays Open.
- **AC-9** Given R1’s request was Resolved less than REOPEN_WINDOW_DAYS ago, When R1 reopens it, Then the request shows status Open.
- **AC-10** Given M2 manages only Elm Court, When M2 tries to change the status of R1’s Mountain Ridge request, Then the portal shows “Not found” and the status is unchanged.

### S-3: Manager switches between communities

As a community manager, I want to switch between my communities from one login and see only the selected community’s requests, so that I never answer a resident with another community’s information.

**Evidence:** E-3

- **AC-11** Given M1 manages Mountain Ridge and Pine Hollow and each has one Open request, When M1 selects Pine Hollow, Then the request list shows only the Pine Hollow request.
- **AC-12** Given M2 manages only Elm Court, When M2 opens the community selector, Then only Elm Court is offered.

### S-4: Board Only folder

As a board member, I want to upload files to a Board Only folder that residents cannot open, even with a direct link, so that draft budgets stay private until the board votes.

**Evidence:** E-5, E-6, E-20

- **AC-13** Given board member B1 of Mountain Ridge uploaded “Draft budget 2027.pdf” to the Board Only folder, When resident R1 opens the Documents page, Then that file is not listed.
- **AC-14** Given R1 has the direct link to that file, When R1 opens the link, Then the portal shows “Not found” and no file is downloaded.
- **AC-15** Given an admin has removed B1’s board member role, When B1 opens the Board Only folder, Then the portal shows “Not found”.

### S-5: Announcement to several communities

As a community manager, I want to post one announcement to several of my communities at once, so that I do not send the same email once per community and miss one.

**Evidence:** E-4, E-13

- **AC-16** Given M1 manages Mountain Ridge and Pine Hollow, When M1 posts “Office closed November 26” to both, Then every resident of both communities sees it at the top of their feed and receives one email about it.
- **AC-17** Given resident R4 lives in Elm Court, which M1 does not manage, When M1 posts that announcement, Then R4 does not see it and receives no email.

### S-6: Scheduled monthly dues payment

As a resident, I want my monthly HOA fee paid automatically by ACH, debit card or credit card on a day I choose, so that I do not miss a due date.

**Evidence:** E-9, E-21

- **AC-18** Given R1 has saved a test bank account, When R1 schedules payment on day 5 of each month by ACH, Then R1’s Payments page shows “Scheduled: day 5 of each month, ACH”.
- **AC-19** Given R1’s payment is scheduled for day 5 and unit 12 has no payment for the month, When the daily payment run happens on day 5, Then R1’s payment history shows exactly one payment for that month, marked Paid, for Mountain Ridge’s DUES_AMOUNT_CENTS.
- **AC-20** Given the payment run on day 5 is interrupted and restarted after R1 was charged, When the restarted run finishes, Then R1’s payment history still shows exactly one payment for that month.
- **AC-21** Given the manager recorded a check payment for unit 12 for this month, When the payment run happens on day 5, Then no scheduled charge is made and the history shows one payment for the month.
- **AC-22** Given the test processor declines R1’s charge on day 5, When RETRY_DELAY_DAYS have passed, Then R1’s payment history shows the first attempt as Failed and one retry attempt.

### S-7: Overdue flag and automatic reminder

As a community manager, I want overdue units flagged and a reminder sent automatically after each community’s grace period, so that I do not chase late payers by hand.

**Evidence:** E-7, E-16, E-17; rests on A-4

- **AC-23** Given unit 12 in Mountain Ridge has no payment for the month, When GRACE_PERIOD_DAYS for Mountain Ridge have passed after the due date, Then the manager’s dues page shows unit 12 as Overdue and R1 receives one reminder in the portal and one by email.
- **AC-24** Given unit 14’s payment for the month was recorded before the reminder run, When the reminder run happens, Then unit 14 is not shown as Overdue and its resident receives no reminder.
- **AC-25** Given R1 already received the automatic reminder for this month, When the reminder run happens again in the same month, Then R1 receives no second automatic reminder.

### S-8: Treasurer’s dues report

As a board treasurer, I want to see each unit’s dues status for the month, so that I can report at board meetings without waiting for a spreadsheet.

**Evidence:** E-14, E-15

- **AC-26** Given Mountain Ridge has units with Paid, Failed and Overdue payments for October, When board member B2 opens the October dues report, Then each unit appears exactly once with its status.

### S-9: Tenant submits a request

As a tenant, I want to submit a maintenance request for the unit I rent without seeing the owner’s payments, so that the person who notices a problem can report it.

**Evidence:** E-11

- **AC-27** Given tenant T1 rents unit 7 in Mountain Ridge, When T1 signs in, Then T1 sees the Requests page and no Payments page.

### S-10: Community documents

As a resident, I want to read my community’s rules and policies in the portal, so that I do not have to email the manager for them.

**Evidence:** E-19

- **AC-28** Given M1 uploaded “Pet policy.pdf” to the Mountain Ridge Community folder, When R1 opens the Documents page, Then R1 sees and can open “Pet policy.pdf”.

### S-11: Photo on a request

As a resident, I want to attach a photo to a maintenance request, so that the manager or vendor can see the problem without a site visit.

**Evidence:** Assumption, rests on A-5. Clarifying question for a user: “Tell me about the last request where you or a vendor had to visit just to see what the problem was.”

- **AC-29** Given R1 attaches a JPEG photo no larger than MAX_PHOTO_MB to a new request, When R1 submits it, Then the request’s detail page shows the photo.

## 4c. INVEST check

| Story | I    | N    | V    | E    | S    | T    | Problems for each fail                                                                                                                                                         |
|-------|------|------|------|------|------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S-1   | Pass | Pass | Pass | Pass | Pass | Pass | None                                                                                                                                                                           |
| S-2   | Fail | Pass | Pass | Fail | Pass | Pass | I: depends on S-1 being built first, because there are no requests to update. E: the reopen window is unknown until Q-6 is answered.                                           |
| S-3   | Fail | Pass | Pass | Pass | Pass | Pass | I: depends on S-1 being built first, because the selector filters S-1’s request list.                                                                                          |
| S-4   | Pass | Pass | Pass | Fail | Pass | Pass | E: how quickly board access must end is unknown until Q-4 is answered.                                                                                                         |
| S-5   | Pass | Pass | Pass | Fail | Pass | Pass | E: whether a board member must approve announcements first is unknown until Q-2 is answered.                                                                                   |
| S-6   | Pass | Pass | Pass | Fail | Fail | Pass | E: who pays the card fee is unknown until Q-1 is answered. S: covers scheduling, charging and retrying; the retry (AC-22) may need its own story.                              |
| S-7   | Fail | Pass | Pass | Fail | Pass | Pass | I: depends on S-6’s payment records being built first (or the manual balance from the proposal’s cut line). E: each community’s grace period is unknown until Q-3 is answered. |
| S-8   | Fail | Pass | Pass | Pass | Pass | Pass | I: depends on S-6 and S-7 producing the Paid, Failed and Overdue statuses.                                                                                                     |
| S-9   | Pass | Pass | Pass | Fail | Pass | Pass | E: how a tenant is linked to a unit, and when they lose access, is unknown until Q-5 is answered.                                                                              |
| S-10  | Pass | Pass | Pass | Pass | Pass | Pass | None                                                                                                                                                                           |
| S-11  | Fail | Pass | Fail | Pass | Pass | Pass | I: depends on S-1 being built first. V: the benefit rests on A-5, which no interviewee confirmed.                                                                              |

## 4e. Ranking and cut line

| Rank | Story        | Why it is above the cut line                                                                                                       |
|------|--------------|------------------------------------------------------------------------------------------------------------------------------------|
| 1    | S-1          | It is the core resident task, and it carries the cross-community access checks our approval asked us to run from the first week.   |
| 2    | S-3          | A manager answering with the wrong community’s information is an observed failure (E-3) that only one-login switching fixes.       |
| 3    | S-2          | Residents can only stop asking for updates (E-1, E-12) once managers can change a request’s status.                                |
| 4    | S-4          | Two board-only leaks were observed (E-5, E-20), and privacy failures are the hardest to undo.                                      |
| 5    | S-10         | It is small, and it removes repeated emails for the same documents (E-19).                                                         |
| 6    | S-5          | It fixes the observed missed-community notice (E-4) with little new logic.                                                         |
| 7    | S-6          | It is the proposal’s highest-risk capability, so it sits after the safer stories, where the proposal’s cut line can still drop it. |
| 8    | S-7          | It depends on S-6’s payment records and fixes the observed reminders sent to people who had paid (E-16).                           |
| 9    | S-11         | It completes the request capability promised in our proposal, and it is small once S-1 exists.                                     |
| —    | **Cut line** | Stories below this line will not be in our final release.                                                                          |
| 10   | S-8          |                                                                                                                                    |
| 11   | S-9          |                                                                                                                                    |
