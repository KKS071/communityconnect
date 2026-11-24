import subprocess
import sys

TEST_FILE = "tests/acceptance/test_s6_acceptance.py"

scenarios = [
    (
        "AC-18",
        "ACH schedule creation and retrieval",
        "test_ac18_schedule_shown_on_payments_page",
    ),
    (
        "AC-19",
        "Exactly-once scheduled payment",
        "test_ac19_due_day_charges_exactly_once",
    ),
    (
        "AC-20",
        "Interrupted payment recovery",
        "test_ac20_restart_mid_run_keeps_one_payment",
    ),
    (
        "AC-21",
        "Manual payment prevents duplicate charge",
        "test_ac21_manual_payment_prevents_scheduled_charge",
    ),
    (
        "AC-22",
        "Declined payment and delayed retry",
        "test_ac22_declined_charge_retried_after_delay",
    ),
]

for ac, description, test in scenarios:
    print("\n" + "=" * 70, flush=True)
    print(f"{ac}: {description}", flush=True)
    print("=" * 70, flush=True)

    result = subprocess.run([
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--tb=short",
        f"{TEST_FILE}::{test}",
    ])

    if result.returncode != 0:
        print(f"{ac}: FAILED")
        sys.exit(result.returncode)

    print(f"\n{ac}: PASS")
    input("Capture screenshot and press Enter to continue...")

print("\nAll five S-6 acceptance scenarios passed.")
