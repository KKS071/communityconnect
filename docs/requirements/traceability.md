# Deliverable 7: Traceability matrix

One row per acceptance criterion. **Evidence IDs are A entries until the interviews are logged.**
After the interviews, replace each A ID with the E ID that supports the story (see `backlog.md`).
Test names for S-1 and S-2 exist in the repository at the submitted commit. S-2 tests are skipped
until S-2 is built.

| Evidence ID | Story | AC | Test name |
|---|---|---|---|
| A-5, A-12 | S-1 | AC-1 | `tests/test_s1_community_isolation.py::test_ac1_outsider_item_read_blocked`, `::test_ac1_blocked_item_is_indistinguishable_from_missing` |
| A-5, A-12 | S-1 | AC-2 | `tests/test_s1_community_isolation.py::test_ac2_outsider_list_read_blocked` |
| A-5, A-12 | S-1 | AC-3 | `tests/test_s1_community_isolation.py::test_ac3_member_lists_announcements_and_documents`, `::test_ac3_resident_sees_own_ticket`, `::test_ac3_manager_sees_all_community_tickets` |
| A-5, A-12 | S-1 | AC-4 | `tests/test_s1_community_isolation.py::test_ac4_manager_switches_communities_with_one_token` |
| A-5, A-12 | S-1 | AC-5 | `tests/test_s1_community_isolation.py::test_ac5_unauthenticated_request_blocked` |
| A-6, A-7 | S-2 | AC-6 | `tests/test_s2_ticket_status.py::test_ac6_manager_starts_ticket_resident_sees_in_progress` (skipped) |
| A-6, A-7 | S-2 | AC-7 | `tests/test_s2_ticket_status.py::test_ac7_manager_resolves_ticket_resident_sees_resolved` (skipped) |
| A-6, A-7 | S-2 | AC-8 | `tests/test_s2_ticket_status.py::test_ac8_skipping_in_progress_is_refused` (skipped) |
| A-6, A-7 | S-2 | AC-9 | `tests/test_s2_ticket_status.py::test_ac9_resident_cannot_advance_ticket` (skipped) |
| A-6, A-7 | S-2 | AC-10 | `tests/test_s2_ticket_status.py::test_ac10_reopen_within_window` (skipped) |
| A-6, A-7 | S-2 | AC-11 | `tests/test_s2_ticket_status.py::test_ac11_reopen_after_window_refused` (skipped) |
| A-6, A-7 | S-2 | AC-12 | `tests/test_s2_ticket_status.py::test_ac12_manager_of_other_community_gets_404` (skipped) |
| A-12, A-11 | S-3 | AC-13 | Not yet written |
| A-12, A-11 | S-3 | AC-14 | Not yet written |
| A-2 | S-4 | AC-15 | Not yet written |
| A-2 | S-4 | AC-16 | Not yet written |
| A-1 | S-5 | AC-17 | Not yet written |
| A-1 | S-5 | AC-18 | Not yet written |
| A-3, A-8 | S-6 | AC-19 | Not yet written |
| A-3 | S-7 | AC-20 | Not yet written |
| A-3 | S-7 | AC-21 | Not yet written |
| A-4 | S-8 | AC-22 | Not yet written |
| A-4 | S-8 | AC-23 | Not yet written |
| A-4 | S-8 | AC-24 | Not yet written |
| A-9, A-4 | S-9 | AC-25 | Not yet written |
| A-9, A-4 | S-9 | AC-26 | Not yet written |
| A-9 | S-11 | AC-27 | Not yet written |
| A-10 | S-10 | AC-28 | Not yet written |

Tests from the design docs that are not AC tests (rules and edge cases): `test_r4_board_only_document_never_returned`,
`test_r5_resident_cannot_read_neighbours_ticket`, `test_edge3_admin_without_membership`,
`test_d10_out_of_range_ids_are_404`, `test_d9_auth_checked_before_path_validation`, `test_d17_trailing_slash_is_404`.
