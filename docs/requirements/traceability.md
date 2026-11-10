# Deliverable 7: Traceability matrix

The test names for S-1 and S-6 are the names in each design doc’s section 9. All eleven exist in the repository at the submitted commit (checked with `python -m pytest --collect-only -q`).

| Evidence ID      | Story ID | AC ID | Test name                                                                           |
|------------------|----------|-------|-------------------------------------------------------------------------------------|
| E-1, E-2, E-12   | S-1      | AC-1  | tests/test_s1_requests.py::test_ac1_resident_submits_request_shown_as_open          |
| E-1, E-12        | S-1      | AC-2  | tests/test_s1_requests.py::test_ac2_blank_description_rejected_and_list_unchanged   |
| E-1, E-12        | S-1      | AC-3  | tests/test_s1_requests.py::test_ac3_other_community_resident_does_not_see_request   |
| E-1, E-12        | S-1      | AC-4  | tests/test_s1_requests.py::test_ac4_other_community_direct_id_returns_not_found     |
| E-1, E-12        | S-1      | AC-5  | tests/test_s1_requests.py::test_ac5_neighbor_in_same_community_does_not_see_request |
| E-2, E-12        | S-1      | AC-6  | tests/test_s1_requests.py::test_ac6_resident_sees_in_progress_status                |
| E-1, E-12        | S-2      | AC-7  | Not yet written                                                                     |
| E-2              | S-2      | AC-8  | Not yet written                                                                     |
| E-1              | S-2      | AC-9  | Not yet written                                                                     |
| E-3              | S-2      | AC-10 | Not yet written                                                                     |
| E-3              | S-3      | AC-11 | Not yet written                                                                     |
| E-3              | S-3      | AC-12 | Not yet written                                                                     |
| E-5, E-20        | S-4      | AC-13 | Not yet written                                                                     |
| E-5              | S-4      | AC-14 | Not yet written                                                                     |
| E-6              | S-4      | AC-15 | Not yet written                                                                     |
| E-4, E-13        | S-5      | AC-16 | Not yet written                                                                     |
| E-4              | S-5      | AC-17 | Not yet written                                                                     |
| E-21             | S-6      | AC-18 | tests/test_s6_payments.py::test_ac18_schedule_shown_on_payments_page                |
| E-21             | S-6      | AC-19 | tests/test_s6_payments.py::test_ac19_due_day_charges_exactly_once                   |
| E-9              | S-6      | AC-20 | tests/test_s6_payments.py::test_ac20_restart_mid_run_keeps_one_payment              |
| E-9              | S-6      | AC-21 | tests/test_s6_payments.py::test_ac21_manual_payment_prevents_scheduled_charge       |
| E-21             | S-6      | AC-22 | tests/test_s6_payments.py::test_ac22_declined_charge_retried_after_delay            |
| E-7, E-17        | S-7      | AC-23 | Not yet written                                                                     |
| E-16             | S-7      | AC-24 | Not yet written                                                                     |
| E-7              | S-7      | AC-25 | Not yet written                                                                     |
| E-14, E-15       | S-8      | AC-26 | Not yet written                                                                     |
| E-11             | S-9      | AC-27 | Not yet written                                                                     |
| E-19             | S-10     | AC-28 | Not yet written                                                                     |
| A-5 (Assumption) | S-11     | AC-29 | Not yet written                                                                     |
